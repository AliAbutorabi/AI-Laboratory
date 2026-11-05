"""Puzzle state and worker-thread search for the widget interface."""

from queue import Empty, Queue
from threading import Thread

import core
from solver_worker import SolverWorker


SETUP_MODES = ("standard", "random")
ALGORITHMS = core.ALGORITHMS
SHUFFLE_MIN, SHUFFLE_MAX = 1, 2000
NODE_MIN, NODE_MAX = 1000, 5000000


class PuzzleBackend:
    def __init__(self):
        self.puzzleSize = 4
        self.setupModeIndex = 0
        self.shuffleMoves = 100
        self.algorithmIndex = 2
        self.nodeLimit = 100000
        self.checkedNodes = 0
        self.statusText = "پازل جدید ساخته شد"
        self.busy = False

        self._puzzle = core.create_puzzle(self.puzzleSize)
        self._goal = core.copy_puzzle(self._puzzle)
        self.displayPuzzle = core.copy_puzzle(self._puzzle)
        self._events = Queue()
        self._thread = None

    @property
    def goalPuzzle(self):
        return self._goal

    def setPuzzleSize(self, value):
        self.puzzleSize = max(2, min(10, int(value)))

    def setSetupMode(self, value):
        self.setupModeIndex = max(
            0, min(len(SETUP_MODES) - 1, int(value))
        )

    def setShuffleMoves(self, value):
        self.shuffleMoves = max(
            SHUFFLE_MIN, min(SHUFFLE_MAX, int(value))
        )

    def setAlgorithmIndex(self, value):
        self.algorithmIndex = max(
            0, min(len(ALGORITHMS) - 1, int(value))
        )

    def setNodeLimit(self, value):
        self.nodeLimit = max(NODE_MIN, min(NODE_MAX, int(value)))

    def createPuzzle(self):
        if self.busy:
            return
        if SETUP_MODES[self.setupModeIndex] == "random":
            self._puzzle = core.random_puzzle(self.puzzleSize)
        else:
            self._puzzle = core.create_puzzle(self.puzzleSize)
        self._goal = core.copy_puzzle(self._puzzle)
        self.checkedNodes = 0
        self.displayPuzzle = core.copy_puzzle(self._puzzle)
        self.statusText = "پازل جدید ساخته شد"

    def shufflePuzzle(self):
        if self.busy:
            return
        self.checkedNodes = 0
        previous_blank = None
        for _ in range(self.shuffleMoves):
            current_blank = core.blank_position(self._puzzle)
            self._puzzle = core.shuffle_puzzle(
                self._puzzle, previous_blank
            )
            previous_blank = current_blank
        self.displayPuzzle = core.copy_puzzle(self._puzzle)
        self.statusText = "پازل به‌هم‌ریخته شد"

    def solve(self):
        if self.busy:
            return
        self.checkedNodes = 0
        self.statusText = ""
        self.busy = True
        worker = SolverWorker(
            ALGORITHMS[self.algorithmIndex],
            self._puzzle,
            self._goal,
            max_nodes=self.nodeLimit,
            events=self._events,
        )
        self._thread = Thread(target=worker.run, daemon=True)
        self._thread.start()

    def process_events(self):
        while True:
            try:
                kind, *data = self._events.get_nowait()
            except Empty:
                break

            if kind == "progress":
                self.displayPuzzle, self.checkedNodes = data
            elif kind == "solved":
                directions, self.checkedNodes = data
                self._puzzle = core.copy_puzzle(self._goal)
                self.displayPuzzle = core.copy_puzzle(self._goal)
                self.statusText = (
                    f"پازل حل شد! {self.checkedNodes:,} گره بررسی و "
                    f"{len(directions)} حرکت انجام شد."
                )
            elif kind == "finished":
                self.checkedNodes, = data
                self.displayPuzzle = core.copy_puzzle(self._puzzle)
                self.statusText = (
                    "جست‌وجو بدون یافتن راه‌حل پایان یافت "
                    f"({self.checkedNodes:,} گره بررسی شد)."
                )
            elif kind == "aborted":
                reason, self.checkedNodes = data
                self.displayPuzzle = core.copy_puzzle(self._puzzle)
                self.statusText = (
                    f"{reason} {self.checkedNodes:,} گره بررسی شد."
                )
            elif kind == "failed":
                self.statusText, = data
                self.displayPuzzle = core.copy_puzzle(self._puzzle)
            elif kind == "done":
                self.busy = False
                self._thread = None

    def shutdown(self):
        if self._thread is not None:
            self._thread.join(timeout=1)
