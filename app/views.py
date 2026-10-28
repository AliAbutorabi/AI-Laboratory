import json

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .models import Algorithm
from .puzzle import create_puzzle, random_puzzle, shuffle_puzzle
from .algorithms import astar_stream, bfs_stream, dfs_stream


def index(request):
    algorithms = Algorithm.objects.all()

    return render(
        request,
        "index.html",
        {
            "algorithms": algorithms,
        },
    )


def puzzle_state(request):
    if "puzzle" not in request.session:
        request.session["size"] = 3
        request.session["puzzle"] = create_puzzle(3)
        request.session["goal_puzzle"] = create_puzzle(3)
        request.session["move_count"] = 0

    if "goal_puzzle" not in request.session:
        request.session["goal_puzzle"] = create_puzzle(request.session["size"])

    return JsonResponse(
        {
            "puzzle": request.session["puzzle"],
            "goal_puzzle": request.session["goal_puzzle"],
            "size": request.session["size"],
            "move_count": request.session.get("move_count", 0),
        }
    )


def create(request):
    data = json.loads(request.body)

    try:
        size = int(data.get("size", 3))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Puzzle size must be a number."}, status=400)

    if not 2 <= size <= 10:
        return JsonResponse(
            {"error": "Puzzle size must be between 2 and 10."}, status=400
        )

    mode = data.get("mode", "standard")
    if mode == "standard":
        puzzle = create_puzzle(size)
    elif mode == "random":
        puzzle = random_puzzle(size)
    elif mode == "manual":
        puzzle = data.get("puzzle")
        expected_tiles = set(range(1, size * size)) | {None}
        if (
            not isinstance(puzzle, list)
            or len(puzzle) != size
            or any(not isinstance(row, list) or len(row) != size for row in puzzle)
            or any(
                type(tile) is not int and tile is not None
                for row in puzzle
                for tile in row
            )
            or {tile for row in puzzle for tile in row} != expected_tiles
        ):
            return JsonResponse(
                {
                    "error": (
                        f"Enter each number from 1 to {size * size - 1} once "
                        "and leave one cell blank."
                    )
                },
                status=400,
            )
    else:
        return JsonResponse({"error": "Choose a valid puzzle setup mode."}, status=400)

    request.session["size"] = size
    request.session["puzzle"] = puzzle
    request.session["goal_puzzle"] = [row.copy() for row in puzzle]
    request.session["move_count"] = 0

    return JsonResponse(
        {
            "puzzle": puzzle,
            "goal_puzzle": request.session["goal_puzzle"],
            "size": size,
            "move_count": 0,
        }
    )


def shuffle(request):

    puzzle = request.session["puzzle"]

    puzzle = shuffle_puzzle(puzzle)

    request.session["puzzle"] = puzzle

    return JsonResponse(
        {
            "puzzle": puzzle,
            "size": len(puzzle),
        }
    )


def solve_stream(request):

    algorithm = request.GET.get("algorithm")

    puzzle = request.session["puzzle"]
    goal_puzzle = request.session["goal_puzzle"]

    def event_stream():

        if algorithm == "Breadth First Search":
            solver = bfs_stream(puzzle, goal_puzzle)
        elif algorithm == "Depth First Search":
            solver = dfs_stream(puzzle, goal_puzzle)
        elif algorithm == "A* Search Algorithm":
            solver = astar_stream(puzzle, goal_puzzle)
        else:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Unsupported algorithm'})}\n\n"
            return

        for event in solver:
            yield f"data: {json.dumps(event)}\n\n"

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )

    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"

    return response
