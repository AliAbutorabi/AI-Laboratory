from collections import deque


def _build_neighbors(size):
    neighbors = [[] for _ in range(size * size)]

    directions = [
        (-1, 0, "up"),
        (1, 0, "down"),
        (0, -1, "left"),
        (0, 1, "right"),
    ]

    for index in range(size * size):

        x, y = divmod(index, size)

        for dx, dy, direction in directions:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < size and 0 <= ny < size:

                neighbor_index = nx * size + ny

                neighbors[index].append(
                    (neighbor_index, direction)
                )

    return neighbors


def _state_to_grid(state, size):
    return [
        list(state[i:i + size])
        for i in range(0, len(state), size)
    ]


def bfs_stream(puzzle):

    print("BFS STARTED", flush=True)

    size = len(puzzle)

    start = tuple(
        number
        for row in puzzle
        for number in row
    )

    goal = tuple(range(1, size * size)) + (None,)

    neighbors = _build_neighbors(size)

    queue = deque([
        (start, start.index(None))
    ])

    parent = {
        start: None
    }

    move = {}

    checked_nodes = 0

    while queue:

        state, blank = queue.popleft()

        checked_nodes += 1

        print(
            f"BFS CHECKING NODE: {checked_nodes}",
            flush=True
        )

        yield {
            "type": "checked",
            "state": _state_to_grid(state, size),
            "checked_nodes": checked_nodes,
        }

        if state == goal:

            print(
                f"BFS SOLVED - NODES CHECKED: {checked_nodes}",
                flush=True
            )

            solution = []

            current = goal

            while current != start:

                solution.append(
                    move[current]
                )

                current = parent[current]

            solution.reverse()

            yield {
                "type": "solved",
                "checked_nodes": checked_nodes,
                "solution": solution,
                "state": _state_to_grid(state, size),
            }

            return

        for new_blank, direction in neighbors[blank]:

            new_state = list(state)

            new_state[blank], new_state[new_blank] = (
                new_state[new_blank],
                new_state[blank],
            )

            new_state = tuple(new_state)

            if new_state in parent:
                continue

            parent[new_state] = state

            move[new_state] = direction

            queue.append(
                (new_state, new_blank)
            )

    print(
        f"BFS FINISHED - NO SOLUTION - NODES CHECKED: {checked_nodes}",
        flush=True
    )

    yield {
        "type": "finished",
        "checked_nodes": checked_nodes,
        "solution": None,
    }