"""Pure-Python puzzle engine for the desktop application.

This module is a faithful, Django-free port of ``app/algorithms.py`` and
``app/puzzle.py`` from the original web project:

* ``bfs_stream``   -> Breadth First Search (deque, parent map, shortest path)
* ``dfs_stream``   -> Depth First Search (stack, parent map, not optimal)
* ``astar_stream`` -> A* (binary heap, Manhattan distance heuristic)

The streaming generator contract is kept exactly as in the web version so the
migration does not change any solving behaviour.  Each yielded event is a dict::

    {"type": "checked",  "state": [[...]], "checked_nodes": int}
    {"type": "solved",   "state": [[...]], "checked_nodes": int,
                                  "solution": ["up", "left", ...]}
    {"type": "finished", "checked_nodes": int, "solution": None}

``solution`` contains the directions in which the BLANK tile moves.

Only the per-node debug ``print`` calls from the original BFS/DFS were removed
(they flooded stdout on every explored node).
"""

from collections import deque
from heapq import heappop, heappush
from itertools import count
import random


ALGORITHMS = (
    "Breadth First Search",
    "Depth First Search",
    "A* Search Algorithm",
)

DIRECTIONS = (
    (-1, 0, "up"),
    (1, 0, "down"),
    (0, -1, "left"),
    (0, 1, "right"),
)


# ---------------------------------------------------------------------------
# Ported from app/algorithms.py
# ---------------------------------------------------------------------------


def neighbors_list(puzzle_size):
    neighbor_positions = [[] for _ in range(puzzle_size * puzzle_size)]
    for i in range(puzzle_size * puzzle_size):
        x, y = divmod(i, puzzle_size)
        for direction_x, direction_y, direction in DIRECTIONS:
            neighbor_row_index = x + direction_x
            neighbor_column_index = y + direction_y
            if (
                0 <= neighbor_row_index < puzzle_size
                and 0 <= neighbor_column_index < puzzle_size
            ):
                neighbor_position_index = (
                    neighbor_row_index * puzzle_size + neighbor_column_index
                )
                neighbor_positions[i].append((neighbor_position_index, direction))
    return neighbor_positions


def _state_to_grid(current_state, puzzle_size):
    return [
        list(current_state[row_start_index: row_start_index + puzzle_size])
        for row_start_index in range(0, len(current_state), puzzle_size)
    ]


def _initial_and_goal(initial_puzzle, goal_puzzle):
    puzzle_size = len(initial_puzzle)
    starting_state = tuple(
        tile_value for puzzle_row in initial_puzzle for tile_value in puzzle_row
    )
    goal_state = (
        tuple(tile for row in goal_puzzle for tile in row)
        if goal_puzzle
        else tuple(range(1, puzzle_size * puzzle_size)) + (None,)
    )
    return puzzle_size, starting_state, goal_state


def bfs_stream(initial_puzzle, goal_puzzle=None):
    puzzle_size, starting_state, goal_state = _initial_and_goal(
        initial_puzzle, goal_puzzle
    )
    neighbor_positions = neighbors_list(puzzle_size)
    state_queue = deque([(starting_state, starting_state.index(None))])
    parent_state_by_state = {starting_state: None}
    movement_direction_by_state = {}
    checked_node_count = 0

    while state_queue:
        current_state, blank_position = state_queue.popleft()
        checked_node_count += 1
        yield {
            "type": "checked",
            "state": _state_to_grid(current_state, puzzle_size),
            "checked_nodes": checked_node_count,
        }

        if current_state == goal_state:
            solution_directions = []
            backtracking_state = goal_state
            while backtracking_state != starting_state:
                solution_directions.append(
                    movement_direction_by_state[backtracking_state]
                )
                backtracking_state = parent_state_by_state[backtracking_state]
            solution_directions.reverse()
            yield {
                "type": "solved",
                "checked_nodes": checked_node_count,
                "solution": solution_directions,
                "state": _state_to_grid(current_state, puzzle_size),
            }
            return

        for neighbor_blank_position, movement_direction in neighbor_positions[
            blank_position
        ]:
            neighboring_state = list(current_state)
            (
                neighboring_state[blank_position],
                neighboring_state[neighbor_blank_position],
            ) = (
                neighboring_state[neighbor_blank_position],
                neighboring_state[blank_position],
            )
            neighboring_state = tuple(neighboring_state)
            if neighboring_state in parent_state_by_state:
                continue
            parent_state_by_state[neighboring_state] = current_state
            movement_direction_by_state[neighboring_state] = movement_direction
            state_queue.append((neighboring_state, neighbor_blank_position))

    yield {
        "type": "finished",
        "checked_nodes": checked_node_count,
        "solution": None,
    }


def dfs_stream(initial_puzzle, goal_puzzle=None):
    puzzle_size, starting_state, goal_state = _initial_and_goal(
        initial_puzzle, goal_puzzle
    )
    neighbor_positions = neighbors_list(puzzle_size)
    state_stack = [(starting_state, starting_state.index(None))]
    parent_state_by_state = {starting_state: None}
    movement_direction_by_state = {}
    checked_node_count = 0

    while state_stack:
        current_state, blank_position = state_stack.pop()
        checked_node_count += 1
        current_grid = _state_to_grid(current_state, puzzle_size)
        yield {
            "type": "checked",
            "state": current_grid,
            "checked_nodes": checked_node_count,
        }

        if current_state == goal_state:
            solution_directions = []
            backtracking_state = current_state
            while parent_state_by_state[backtracking_state] is not None:
                solution_directions.append(
                    movement_direction_by_state[backtracking_state]
                )
                backtracking_state = parent_state_by_state[backtracking_state]
            solution_directions.reverse()
            yield {
                "type": "solved",
                "state": current_grid,
                "checked_nodes": checked_node_count,
                "solution": solution_directions,
            }
            return

        for neighbor_blank_position, movement_direction in neighbor_positions[
            blank_position
        ]:
            neighboring_state = list(current_state)
            (
                neighboring_state[blank_position],
                neighboring_state[neighbor_blank_position],
            ) = (
                neighboring_state[neighbor_blank_position],
                neighboring_state[blank_position],
            )
            neighboring_state = tuple(neighboring_state)
            if neighboring_state not in parent_state_by_state:
                parent_state_by_state[neighboring_state] = current_state
                movement_direction_by_state[neighboring_state] = movement_direction
                state_stack.append((neighboring_state, neighbor_blank_position))

    yield {
        "type": "finished",
        "checked_nodes": checked_node_count,
        "solution": None,
    }


def astar_stream(initial_puzzle, goal_puzzle=None):
    puzzle_size = len(initial_puzzle)
    starting_state = tuple(tile for row in initial_puzzle for tile in row)
    goal_state = (
        tuple(tile for row in goal_puzzle for tile in row)
        if goal_puzzle
        else tuple(range(1, puzzle_size * puzzle_size)) + (None,)
    )
    neighbor_positions = neighbors_list(puzzle_size)
    goal_positions = {tile: position for position, tile in enumerate(goal_state)}
    distances = {
        tile: tuple(
            abs(position // puzzle_size - goal_positions[tile] // puzzle_size)
            + abs(position % puzzle_size - goal_positions[tile] % puzzle_size)
            for position in range(puzzle_size * puzzle_size)
        )
        for tile in goal_state
        if tile is not None
    }

    def heuristic(state):
        return sum(
            distances[tile][position]
            for position, tile in enumerate(state)
            if tile is not None
        )

    sequence = count()
    starting_heuristic = heuristic(starting_state)
    frontier = [
        (
            starting_heuristic,
            next(sequence),
            0,
            starting_state,
            starting_state.index(None),
            starting_heuristic,
        )
    ]
    cost_by_state = {starting_state: 0}
    parent_state_by_state = {starting_state: None}
    movement_direction_by_state = {}
    checked_node_count = 0

    while frontier:
        (
            _,
            _,
            current_cost,
            current_state,
            blank_position,
            current_heuristic,
        ) = heappop(frontier)
        if current_cost != cost_by_state[current_state]:
            continue

        checked_node_count += 1
        yield {
            "type": "checked",
            "state": _state_to_grid(current_state, puzzle_size),
            "checked_nodes": checked_node_count,
        }
        if current_state == goal_state:
            solution_directions = []
            backtracking_state = current_state
            while backtracking_state != starting_state:
                solution_directions.append(
                    movement_direction_by_state[backtracking_state]
                )
                backtracking_state = parent_state_by_state[backtracking_state]
            solution_directions.reverse()
            yield {
                "type": "solved",
                "checked_nodes": checked_node_count,
                "solution": solution_directions,
                "state": _state_to_grid(current_state, puzzle_size),
            }
            return

        for neighbor_blank_position, movement_direction in neighbor_positions[
            blank_position
        ]:
            neighboring_state = list(current_state)
            tile = neighboring_state[neighbor_blank_position]
            neighboring_state[blank_position], neighboring_state[
                neighbor_blank_position
            ] = tile, None
            neighboring_state = tuple(neighboring_state)
            tentative_cost = current_cost + 1

            if tentative_cost >= cost_by_state.get(neighboring_state, float("inf")):
                continue

            cost_by_state[neighboring_state] = tentative_cost
            parent_state_by_state[neighboring_state] = current_state
            movement_direction_by_state[neighboring_state] = movement_direction
            neighboring_heuristic = (
                current_heuristic
                - distances[tile][neighbor_blank_position]
                + distances[tile][blank_position]
            )
            heappush(
                frontier,
                (
                    tentative_cost + neighboring_heuristic,
                    next(sequence),
                    tentative_cost,
                    neighboring_state,
                    neighbor_blank_position,
                    neighboring_heuristic,
                ),
            )

    yield {
        "type": "finished",
        "checked_nodes": checked_node_count,
        "solution": None,
    }


SOLVERS = {
    "Breadth First Search": bfs_stream,
    "Depth First Search": dfs_stream,
    "A* Search Algorithm": astar_stream,
}


# ---------------------------------------------------------------------------
# Ported from app/puzzle.py
# ---------------------------------------------------------------------------


def create_puzzle(size):
    puzzle = []
    for i in range(size):
        row = []
        for j in range(size):
            number = i * size + j + 1
            row.append(None if number == size * size else number)
        puzzle.append(row)
    return puzzle


def random_puzzle(size):
    tiles = list(range(1, size * size)) + [None]
    random.shuffle(tiles)
    return [
        tiles[row_start: row_start + size]
        for row_start in range(0, size * size, size)
    ]


def shuffle_puzzle(puzzle, previous_blank_position=None):
    """One random legal move of the blank (ported from the web version).

    ``previous_blank_position`` is an optional desktop improvement: when given,
    the blank avoids immediately undoing the previous move, so N shuffle steps
    actually produce a meaningfully scrambled board.
    """
    n = len(puzzle)
    x, y = next((i, j) for i in range(n) for j in range(n) if puzzle[i][j] is None)
    neighbors = [
        (x + dx, y + dy)
        for dx, dy, _ in DIRECTIONS
        if 0 <= x + dx < n and 0 <= y + dy < n
    ]
    if previous_blank_position is not None and len(neighbors) > 1:
        neighbors = [pos for pos in neighbors if pos != previous_blank_position]
    direction_x, direction_y = random.choice(neighbors)
    puzzle[x][y], puzzle[direction_x][direction_y] = (
        puzzle[direction_x][direction_y],
        puzzle[x][y],
    )
    return puzzle


def copy_puzzle(puzzle):
    return [row.copy() for row in puzzle]


def blank_position(puzzle):
    for row_index, row in enumerate(puzzle):
        for column_index, tile in enumerate(row):
            if tile is None:
                return row_index, column_index
    raise ValueError("Puzzle has no blank tile")
