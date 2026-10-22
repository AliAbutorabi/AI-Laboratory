from collections import deque


def neighbors_list(puzzle_size):
    neighbor_positions = [[] for position_index in range(puzzle_size * puzzle_size)]

    directions = [
        (-1, 0, "up"),
        (1, 0, "down"),
        (0, -1, "left"),
        (0, 1, "right"),
    ]

    for i in range(puzzle_size * puzzle_size):

        x, y = divmod(i, puzzle_size)

        for direction_x, direction_y, direction in directions:

            neighbor_row_index = x + direction_x
            neighbor_column_index = y + direction_y

            if (
                0 <= neighbor_row_index < puzzle_size
                and 0 <= neighbor_column_index < puzzle_size
            ):

                neighbor_position_index = (
                    neighbor_row_index * puzzle_size + neighbor_column_index
                )

                neighbor_positions[i].append(
                    (neighbor_position_index, direction)
                )

    return neighbor_positions


def _state_to_grid(current_state, puzzle_size):
    return [
        list(current_state[row_start_index : row_start_index + puzzle_size])
        for row_start_index in range(0, len(current_state), puzzle_size)
    ]


def bfs_stream(initial_puzzle):

    print("BFS STARTED", flush=True)

    puzzle_size = len(initial_puzzle)

    starting_state = tuple(
        tile_value for puzzle_row in initial_puzzle for tile_value in puzzle_row
    )

    goal_state = tuple(range(1, puzzle_size * puzzle_size)) + (None,)

    neighbor_positions = neighbors_list(puzzle_size)

    state_queue = deque([(starting_state, starting_state.index(None))])

    parent_state_by_state = {starting_state: None}

    movement_direction_by_state = {}

    checked_node_count = 0

    while state_queue:

        current_state, blank_position = state_queue.popleft()

        checked_node_count += 1

        print(
            f"BFS CHECKING NODE: {checked_node_count}",
            flush=True,
        )

        yield {
            "type": "checked",
            "state": _state_to_grid(current_state, puzzle_size),
            "checked_nodes": checked_node_count,
        }

        if current_state == goal_state:

            print(
                f"BFS SOLVED - NODES CHECKED: {checked_node_count}",
                flush=True,
            )

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

    print(
        f"BFS FINISHED - NO SOLUTION - NODES CHECKED: {checked_node_count}",
        flush=True,
    )

    yield {
        "type": "finished",
        "checked_nodes": checked_node_count,
        "solution": None,
    }


def dfs_stream(initial_puzzle):
    puzzle_size = len(initial_puzzle)

    starting_state = tuple(
        tile_value for puzzle_row in initial_puzzle for tile_value in puzzle_row
    )

    goal_state = tuple(range(1, puzzle_size * puzzle_size)) + (None,)

    neighbor_positions = [[] for position_index in range(puzzle_size * puzzle_size)]

    for position_index in range(puzzle_size * puzzle_size):

        row_index, column_index = divmod(position_index, puzzle_size)

        for row_offset, column_offset, movement_direction in [
            (-1, 0, "up"),
            (1, 0, "down"),
            (0, -1, "left"),
            (0, 1, "right"),
        ]:

            neighbor_row_index = row_index + row_offset
            neighbor_column_index = column_index + column_offset

            if (
                0 <= neighbor_row_index < puzzle_size
                and 0 <= neighbor_column_index < puzzle_size
            ):

                neighbor_position_index = (
                    neighbor_row_index * puzzle_size + neighbor_column_index
                )

                neighbor_positions[position_index].append(
                    (neighbor_position_index, movement_direction)
                )

    state_stack = [(starting_state, starting_state.index(None))]

    parent_state_by_state = {starting_state: None}

    movement_direction_by_state = {}

    checked_node_count = 0

    while state_stack:

        current_state, blank_position = state_stack.pop()

        checked_node_count += 1

        print(
            f"DFS CHECKING NODE: {checked_node_count} | STATE: {current_state}",
            flush=True,
        )

        current_grid = _state_to_grid(current_state, puzzle_size)

        yield {
            "type": "checked",
            "state": current_grid,
            "checked_nodes": checked_node_count,
        }

        if current_state == goal_state:

            print(
                f"DFS SOLVED - FINAL NODE: {current_state}",
                flush=True,
            )

            print(
                f"DFS SOLVED - NODES CHECKED: {checked_node_count}",
                flush=True,
            )

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

    print(
        f"DFS FINISHED - NO SOLUTION - NODES CHECKED: {checked_node_count}",
        flush=True,
    )

    yield {
        "type": "finished",
        "checked_nodes": checked_node_count,
        "solution": None,
    }
