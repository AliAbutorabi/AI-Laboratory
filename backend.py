"""Puzzle state and solving logic for the widget interface."""

from PySide6.QtCore import (
    QObject,
    Qt,
    QThread,
    QTimer,
    Slot,
)

import core
from solver_worker import FRAME_DELAY_MS, SolverWorker


SETUP_MODES = ("standard", "random")
ALGORITHMS = core.ALGORITHMS
SHUFFLE_MIN, SHUFFLE_MAX = 1, 2000
NODE_MIN, NODE_MAX = 1000, 5000000


class PuzzleBackend(QObject):
    """Own puzzle state and run searches without blocking the widget UI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._puzzleSize = 4
        self._setupModeIndex = 0
        self._shuffleMoves = 100
        self._algorithmIndex = 2
        self._nodeLimit = 100000
        self._checkedNodes = 0
        self._statusText = "پازل جدید ساخته شد"
        self._busy = False
        self._shuffling = False
        self._solving = False
        self._shuffle_remaining = 0
        self._shuffle_batch = 1
        self._shuffle_previous_blank = None
        self._thread = None
        self._worker = None

        self._puzzle = core.create_puzzle(self._puzzleSize)
        self._goal = core.copy_puzzle(self._puzzle)
        self._displayPuzzle = core.copy_puzzle(self._puzzle)

        self._shuffle_timer = QTimer(self)
        self._shuffle_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._shuffle_timer.timeout.connect(self._shuffle_step)
        self._refresh_all()

    @property
    def puzzleSize(self):
        return self._puzzleSize

    @property
    def displayPuzzle(self):
        return self._displayPuzzle

    @property
    def goalPuzzle(self):
        return self._goal

    @property
    def setupModeIndex(self):
        return self._setupModeIndex

    @property
    def shuffleMoves(self):
        return self._shuffleMoves

    @property
    def algorithms(self):
        return ALGORITHMS

    @property
    def algorithmIndex(self):
        return self._algorithmIndex

    @property
    def nodeLimit(self):
        return self._nodeLimit

    @property
    def checkedNodes(self):
        return self._checkedNodes

    @property
    def statusText(self):
        return self._statusText

    # ------------------------------------------------------------- helpers

    def _refresh_all(self):
        self._displayPuzzle = core.copy_puzzle(self._puzzle)

    def _set_status(self, text):
        self._statusText = text

    def _set_busy(self, shuffling=None, solving=None):
        if shuffling is not None:
            self._shuffling = shuffling
        if solving is not None:
            self._solving = solving
        self._busy = self._shuffling or self._solving

    # ---------------------------------------------------------- setup

    @Slot()
    def createPuzzle(self):
        if self._busy:
            return
        size = max(2, min(10, int(self._puzzleSize)))
        mode = SETUP_MODES[int(self._setupModeIndex)]
        puzzle = (
            core.random_puzzle(size)
            if mode == "random"
            else core.create_puzzle(size)
        )

        self._puzzle = puzzle
        self._goal = core.copy_puzzle(puzzle)
        self._checkedNodes = 0
        self._refresh_all()
        self._set_status("پازل جدید ساخته شد")

    @Slot(int)
    def setPuzzleSize(self, value):
        value = max(2, min(10, int(value)))
        self._puzzleSize = value

    @Slot(int)
    def setSetupMode(self, value):
        value = max(0, min(len(SETUP_MODES) - 1, int(value)))
        self._setupModeIndex = value

    @Slot(int)
    def setShuffleMoves(self, value):
        value = max(SHUFFLE_MIN, min(SHUFFLE_MAX, int(value)))
        self._shuffleMoves = value

    @Slot(int)
    def setAlgorithmIndex(self, value):
        value = max(0, min(len(ALGORITHMS) - 1, int(value)))
        self._algorithmIndex = value

    @Slot(int)
    def setNodeLimit(self, value):
        value = max(NODE_MIN, min(NODE_MAX, int(value)))
        self._nodeLimit = value

    @Slot()
    def shufflePuzzle(self):
        if self._busy:
            return
        self._checkedNodes = 0
        self._set_status("")
        self._shuffle_remaining = max(1, int(self._shuffleMoves))
        self._shuffle_batch = max(1, self._shuffle_remaining // 80)
        self._shuffle_previous_blank = None
        self._set_busy(shuffling=True)
        self._shuffle_timer.start(FRAME_DELAY_MS)

    def _shuffle_step(self):
        applied = 0
        while applied < self._shuffle_batch and self._shuffle_remaining > 0:
            previous = core.blank_position(self._puzzle)
            self._puzzle = core.shuffle_puzzle(
                self._puzzle, self._shuffle_previous_blank
            )
            self._shuffle_previous_blank = previous
            self._shuffle_remaining -= 1
            applied += 1
        self._refresh_all()
        if self._shuffle_remaining <= 0:
            self._shuffle_timer.stop()
            self._set_busy(shuffling=False)

    # ------------------------------------------------------------ solving

    @Slot()
    def solve(self):
        if self._busy:
            return
        algorithm = ALGORITHMS[int(self._algorithmIndex)]
        self._checkedNodes = 0
        self._set_status("")
        self._set_busy(solving=True)

        thread = QThread(self)
        worker = SolverWorker(
            algorithm,
            self._puzzle,
            self._goal,
            max_nodes=int(self._nodeLimit),
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._on_progress)
        worker.solved.connect(self._on_solved)
        worker.finished.connect(self._on_finished)
        worker.aborted.connect(self._on_aborted)
        worker.failed.connect(self._on_failed)
        worker.done.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._on_thread_done)
        self._thread = thread
        self._worker = worker
        thread.start()

    def _finish_solving(self):
        self._set_busy(solving=False)

    def _on_thread_done(self):
        self._thread = None
        self._worker = None
        if self._solving:
            self._finish_solving()

    def _on_progress(self, state, count):
        self._checkedNodes = int(count)
        self._displayPuzzle = state

    def _on_solved(self, directions, count):
        self._checkedNodes = int(count)
        self._puzzle = core.copy_puzzle(self._goal)
        self._refresh_all()
        self._set_status(
            f"پازل حل شد! {count:,} گره بررسی و "
            f"{len(directions)} حرکت انجام شد."
        )
        self._finish_solving()

    def _on_finished(self, count):
        self._checkedNodes = int(count)
        self._refresh_all()
        self._set_status(
            f"جست‌وجو بدون یافتن راه‌حل پایان یافت ({count:,} گره بررسی شد)."
        )
        self._finish_solving()

    def _on_aborted(self, reason, count):
        self._checkedNodes = int(count)
        self._refresh_all()
        self._set_status(f"{reason} {count:,} گره بررسی شد.")
        self._finish_solving()

    def _on_failed(self, message):
        self._refresh_all()
        self._set_status(message)
        self._finish_solving()

    @Slot()
    def shutdown(self):
        self._shuffle_timer.stop()
        if self._thread is not None and self._thread.isRunning():
            self._thread.requestInterruption()
            self._thread.quit()
            self._thread.wait(3000)
