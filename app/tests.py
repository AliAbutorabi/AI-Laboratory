from django.test import TestCase

from .algorithms import astar_stream


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
