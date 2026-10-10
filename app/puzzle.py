import random


def create_puzzle(size):
    puzzle = []

    for i in range(size):
        row = []

        for j in range(size):
            number = i * size + j + 1

            if number == size * size:
                row.append(None)
            else:
                row.append(number)

        puzzle.append(row)

    return puzzle


def shuffle_puzzle(puzzle):
    n = len(puzzle)

    x, y = next(
        (i, j)
        for i in range(n)
        for j in range(n)
        if puzzle[i][j] is None
    )

    neighbors = [
        (x + dx, y + dy)
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]
        if 0 <= x + dx < n and 0 <= y + dy < n
    ]

    nx, ny = random.choice(neighbors)

    puzzle[x][y], puzzle[nx][ny] = (
        puzzle[nx][ny],
        puzzle[x][y],
    )

    return puzzle