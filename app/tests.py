import json

from django.test import TestCase
from django.urls import reverse

from .algorithms import astar_stream
from .puzzle import create_puzzle, random_puzzle, shuffle_puzzle


class AStarTests(TestCase):
    def test_finds_shortest_solution(self):
        events = list(astar_stream([[1, 2, 3], [4, 5, 6], [None, 7, 8]]))

        self.assertEqual(events[-1]["type"], "solved")
        self.assertEqual(events[-1]["solution"], ["right", "right"])

    def test_returns_empty_solution_for_solved_puzzle(self):
        events = list(astar_stream([[1, 2], [3, None]]))

        self.assertEqual(events[-1]["type"], "solved")
        self.assertEqual(events[-1]["solution"], [])

    def test_finishes_for_unsolvable_puzzle(self):
        events = list(astar_stream([[2, 1], [3, None]]))

        self.assertEqual(events[-1]["type"], "finished")
        self.assertIsNone(events[-1]["solution"])


class PuzzleSetupTests(TestCase):
    def create_setup(self, mode, size=2, puzzle=None):
        payload = {"mode": mode, "size": size}
        if puzzle is not None:
            payload["puzzle"] = puzzle
        return self.client.post(
            reverse("create"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_standard_mode_uses_canonical_initial_state(self):
        response = self.create_setup("standard")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["puzzle"], [[1, 2], [3, None]])
        self.assertEqual(response.json()["goal_puzzle"], [[1, 2], [3, None]])

    def test_manual_mode_validates_and_preserves_initial_state(self):
        puzzle = [[None, 2], [3, 1]]
        response = self.create_setup("manual", puzzle=puzzle)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["puzzle"], puzzle)
        self.assertEqual(response.json()["goal_puzzle"], puzzle)

        self.client.post(reverse("shuffle"))
        self.assertEqual(self.client.session["goal_puzzle"], puzzle)

    def test_manual_mode_rejects_duplicate_tiles(self):
        response = self.create_setup("manual", puzzle=[[1, 1], [3, None]])

        self.assertEqual(response.status_code, 400)

    def test_random_mode_generates_a_permutation(self):
        response = self.create_setup("random")
        puzzle = response.json()["puzzle"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            sorted(tile for row in puzzle for tile in row if tile is not None),
            [1, 2, 3],
        )
        self.assertEqual(sum(tile is None for row in puzzle for tile in row), 1)
        self.assertEqual(response.json()["goal_puzzle"], puzzle)

    def test_random_puzzle_contains_each_tile_once(self):
        puzzle = random_puzzle(3)

        self.assertEqual(
            sorted(tile for row in puzzle for tile in row if tile is not None),
            list(range(1, 9)),
        )
        self.assertEqual(sum(tile is None for row in puzzle for tile in row), 1)

    def test_shuffle_does_not_mutate_the_initial_puzzle(self):
        initial_puzzle = create_puzzle(3)
        puzzle = [row.copy() for row in initial_puzzle]

        shuffle_puzzle(puzzle)

        self.assertEqual(initial_puzzle, create_puzzle(3))
        self.assertNotEqual(puzzle, initial_puzzle)
