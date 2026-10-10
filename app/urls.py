from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),

    path(
        "api/puzzle/state/",
        views.puzzle_state,
        name="puzzle_state",
    ),

    path(
        "api/puzzle/create/",
        views.create,
        name="create",
    ),

    path(
        "api/puzzle/shuffle/",
        views.shuffle,
        name="shuffle",
    ),

    path(
        "api/puzzle/solve/",
        views.solve_stream,
        name="solve_stream",
    ),
]