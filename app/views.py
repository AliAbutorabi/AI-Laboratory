import json

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .models import Algorithm
from .puzzle import create_puzzle, shuffle_puzzle
from .algorithms import bfs_stream, dfs_stream


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
        request.session["move_count"] = 0

    return JsonResponse(
        {
            "puzzle": request.session["puzzle"],
            "size": request.session["size"],
            "move_count": request.session.get("move_count", 0),
        }
    )


def create(request):
    data = json.loads(request.body)

    size = int(data.get("size", 3))

    puzzle = create_puzzle(size)

    request.session["size"] = size
    request.session["puzzle"] = puzzle
    request.session["move_count"] = 0

    return JsonResponse(
        {
            "puzzle": puzzle,
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

    def event_stream():

        if algorithm == "Breadth First Search":
            solver = bfs_stream(puzzle)
        elif algorithm == "Depth First Search":
            solver = dfs_stream(puzzle)
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
