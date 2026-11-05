"""Application logic for the Qt Quick desktop UI.

This module deliberately contains no QWidget / QML presentation code. It owns
the puzzle state and exposes it to QML as QObject properties, signals, slots
and two QAbstractListModel board models. The solving algorithms live in
``core.py`` and the threaded generator consumer in ``solver_worker.py``.

Goal-state rule (product requirement):
    The goal is a snapshot of the configuration the user *created*.  The user
    then shuffles the board; solving returns the board to that original
    arrangement.  The goal can never be edited afterwards, so there are no
    "use current as goal" / "canonical goal" / "restore goal" operations in
    this backend or in the UI.
"""

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    QThread,
    QTimer,
    Signal,
    Slot,
)

import core
from solver_worker import SolverWorker


ARROWS = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
SETUP_MODES = ("standard", "manual", "random")
SETUP_MODE_LABELS = ["Standard Mode", "Manual Mode", "Random Mode"]
ALGORITHMS = list(core.ALGORITHMS)

GOAL_DESCRIPTION = (
    "Green tiles already match the goal. The goal is a snapshot of the board "
    "taken when the puzzle was created."
)

# Validation ranges are kept here so the QML controls and the Python engine
# can never disagree about what a legal setting is.
SHUFFLE_MIN, SHUFFLE_MAX = 1, 2000
DELAY_MIN, DELAY_MAX = 10, 400
NODE_MIN, NODE_MAX = 1000, 5000000


class BoardModel(QAbstractListModel):
    """Flat list of N*N cells, used by the read-only goal board.

    Roles stay stable between updates so delegates are reused rather than
    destroyed and recreated whenever the board changes.
    """

    NUMBER = Qt.ItemDataRole.UserRole + 1
    BLANK = Qt.ItemDataRole.UserRole + 2
    CORRECT = Qt.ItemDataRole.UserRole + 3
    ROW = Qt.ItemDataRole.UserRole + 4
    COLUMN = Qt.ItemDataRole.UserRole + 5
    VERSION = Qt.ItemDataRole.UserRole + 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self._size = 0
        self._cells = []
        self._version = 0

    def roleNames(self):
        return {
            self.NUMBER: b"number",
            self.BLANK: b"blank",
            self.CORRECT: b"correct",
            self.ROW: b"cellRow",
            self.COLUMN: b"cellColumn",
            self.VERSION: b"version",
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self._cells)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        row = index.row()
        if not index.isValid() or not 0 <= row < len(self._cells):
            return None
        cell = self._cells[row]
        return {
            self.NUMBER: cell["number"],
            self.BLANK: cell["blank"],
            self.CORRECT: cell["correct"],
            self.ROW: cell["row"],
            self.COLUMN: cell["column"],
            self.VERSION: cell["version"],
        }.get(role)

    def setBoard(self, puzzle, goal=None, highlight=False):
        size = len(puzzle)
        whole_solved = goal is not None and puzzle == goal
        version = self._version + 1
        cells = []
        for row_index, row in enumerate(puzzle):
            for column_index, value in enumerate(row):
                correct = bool(
                    highlight
                    and goal is not None
                    and value is not None
                    and not whole_solved
                    and goal[row_index][column_index] == value
                )
                cells.append(
                    {
                        "number": "" if value is None else str(value),
                        "blank": value is None,
                        "correct": correct,
                        "row": row_index,
                        "column": column_index,
                        "version": version,
                    }
                )
        self._version = version
        if size != self._size:
            self.beginResetModel()
            self._size = size
            self._cells = cells
            self.endResetModel()
        else:
            self._cells = cells
            if cells:
                self.dataChanged.emit(
                    self.index(0),
                    self.index(len(cells) - 1),
                    [self.NUMBER, self.BLANK, self.CORRECT, self.VERSION],
                )


class TileModel(QAbstractListModel):
    """One row per *tile* (not per cell) for the interactive board.

    Each row keeps the tile's current ``tileRow`` / ``tileColumn``.  QML
    delegates bind their x/y to those roles, so a move becomes a real sliding
    animation instead of a text swap.  Row order is stable (1..n^2-1, blank),
    which means delegates are never recreated for ordinary moves.
    """

    NUMBER = Qt.ItemDataRole.UserRole + 1
    BLANK = Qt.ItemDataRole.UserRole + 2
    CORRECT = Qt.ItemDataRole.UserRole + 3
    ROW = Qt.ItemDataRole.UserRole + 4
    COLUMN = Qt.ItemDataRole.UserRole + 5
    VERSION = Qt.ItemDataRole.UserRole + 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self._size = 0
        self._tiles = []
        self._version = 0

    def roleNames(self):
        return {
            self.NUMBER: b"number",
            self.BLANK: b"blank",
            self.CORRECT: b"correct",
            self.ROW: b"tileRow",
            self.COLUMN: b"tileColumn",
            self.VERSION: b"version",
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self._tiles)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        row = index.row()
        if not index.isValid() or not 0 <= row < len(self._tiles):
            return None
        tile = self._tiles[row]
        return {
            self.NUMBER: tile["number"],
            self.BLANK: tile["blank"],
            self.CORRECT: tile["correct"],
            self.ROW: tile["row"],
            self.COLUMN: tile["column"],
            self.VERSION: tile["version"],
        }.get(role)

    def setBoard(self, puzzle, goal=None, highlight=False):
        size = len(puzzle)
        whole_solved = goal is not None and puzzle == goal
        version = self._version + 1
        order = list(range(1, size * size)) + [None]
        positions = {}
        for row_index, row in enumerate(puzzle):
            for column_index, value in enumerate(row):
                positions[value] = (row_index, column_index)
        tiles = []
        for value in order:
            row_index, column_index = positions[value]
            correct = bool(
                highlight
                and goal is not None
                and value is not None
                and not whole_solved
                and goal[row_index][column_index] == value
            )
            tiles.append(
                {
                    "number": "" if value is None else str(value),
                    "blank": value is None,
                    "correct": correct,
                    "row": row_index,
                    "column": column_index,
                    "version": version,
                }
            )
        self._version = version
        if size != self._size:
            self.beginResetModel()
            self._size = size
            self._tiles = tiles
            self.endResetModel()
        else:
            self._tiles = tiles
            if tiles:
                self.dataChanged.emit(
                    self.index(0),
                    self.index(len(tiles) - 1),
                    [self.ROW, self.COLUMN, self.CORRECT, self.VERSION],
                )


def state_property(type_hint, name, notify):
    """Build a read-only, QML-visible Property with a shared notify signal.

    PySide6 only registers properties that exist when the QObject class is
    created, so these must be declared in the class body. QML never writes to
    them directly: all writes go through explicit @Slot methods, which keeps a
    strict one-way data flow and avoids shiboken re-entrancy.
    """
    private = "_" + name

    def getter(self):
        return getattr(self, private)

    return Property(type_hint, getter, notify=notify)


# (property name, default). Callables are used for mutable defaults.
_DEFAULTS = (
    ("puzzleSize", 4),               # selected size for the next create
    ("boardSize", 4),                # actual board size
    ("setupModes", lambda: list(SETUP_MODE_LABELS)),
    ("setupModeIndex", 0),
    ("setupTabIndex", 0),
    ("manualCells", lambda: [""] * 16),
    ("shuffleMoves", 100),
    ("algorithms", lambda: list(ALGORITHMS)),
    ("algorithmIndex", 2),           # A* by default (reference design)
    ("liveVisualization", True),
    ("animationDelay", 28),
    ("nodeLimit", 100000),
    ("checkedNodes", 0),
    ("manualMoves", 0),
    ("solvable", True),
    ("statusText", "New puzzle created"),
    ("statusKind", "normal"),
    ("solutionText", ""),
    ("playbackStep", 0),
    ("playbackTotal", 0),
    ("playbackAvailable", False),
    ("playing", False),
    ("busy", False),
    ("stopEnabled", False),
    ("boardExpanded", False),
    ("goalDescription", GOAL_DESCRIPTION),
    ("alertText", ""),
    ("alertVisible", False),
    ("confirmVisible", False),
    ("confirmTitle", ""),
    ("confirmText", ""),
    ("windowMaximized", False),
)


class PuzzleBackend(QObject):
    """Bridge between QML and the pure-Python puzzle engine."""

    stateChanged = Signal()
    showAlert = Signal(str)                  # message
    showConfirm = Signal(str, str)           # title, message

    # ---- QML-visible, read-only state -------------------------------------
    puzzleSize = state_property(int, "puzzleSize", stateChanged)
    boardSize = state_property(int, "boardSize", stateChanged)
    setupModes = state_property(list, "setupModes", stateChanged)
    setupModeIndex = state_property(int, "setupModeIndex", stateChanged)
    setupTabIndex = state_property(int, "setupTabIndex", stateChanged)
    manualCells = state_property(list, "manualCells", stateChanged)
    shuffleMoves = state_property(int, "shuffleMoves", stateChanged)
    algorithms = state_property(list, "algorithms", stateChanged)
    algorithmIndex = state_property(int, "algorithmIndex", stateChanged)
    liveVisualization = state_property(bool, "liveVisualization", stateChanged)
    animationDelay = state_property(int, "animationDelay", stateChanged)
    nodeLimit = state_property(int, "nodeLimit", stateChanged)
    checkedNodes = state_property(int, "checkedNodes", stateChanged)
    manualMoves = state_property(int, "manualMoves", stateChanged)
    solvable = state_property(bool, "solvable", stateChanged)
    statusText = state_property(str, "statusText", stateChanged)
    statusKind = state_property(str, "statusKind", stateChanged)
    solutionText = state_property(str, "solutionText", stateChanged)
    playbackStep = state_property(int, "playbackStep", stateChanged)
    playbackTotal = state_property(int, "playbackTotal", stateChanged)
    playbackAvailable = state_property(bool, "playbackAvailable", stateChanged)
    playing = state_property(bool, "playing", stateChanged)
    busy = state_property(bool, "busy", stateChanged)
    stopEnabled = state_property(bool, "stopEnabled", stateChanged)
    boardExpanded = state_property(bool, "boardExpanded", stateChanged)
    goalDescription = state_property(str, "goalDescription", stateChanged)
    alertText = state_property(str, "alertText", stateChanged)
    alertVisible = state_property(bool, "alertVisible", stateChanged)
    confirmVisible = state_property(bool, "confirmVisible", stateChanged)
    confirmTitle = state_property(str, "confirmTitle", stateChanged)
    confirmText = state_property(str, "confirmText", stateChanged)
    windowMaximized = state_property(bool, "windowMaximized", stateChanged)

    def __init__(self, parent=None):
        super().__init__(parent)
        for name, default in _DEFAULTS:
            setattr(self, "_" + name, default() if callable(default) else default)

        # One row per tile for the interactive board, one row per cell for the
        # read-only goal board.
        self.board_model = TileModel(self)
        self.goal_model = BoardModel(self)

        self._puzzle = core.create_puzzle(self._puzzleSize)
        # The created configuration IS the goal. It is never mutated again.
        self._goal = core.copy_puzzle(self._puzzle)
        self._solve_start = core.copy_puzzle(self._puzzle)
        self._solution_directions = []
        self._solution_states = []
        self._solution_index = 0
        self._viewing_solution = False

        self._shuffling = False
        self._solving = False
        self._shuffle_remaining = 0
        self._shuffle_batch = 1
        self._shuffle_previous_blank = None
        self._thread = None
        self._worker = None
        self._window = None
        self._pending_solve = False

        self._shuffle_timer = QTimer(self)
        self._shuffle_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._shuffle_timer.timeout.connect(self._shuffle_step)
        self._play_timer = QTimer(self)
        self._play_timer.timeout.connect(self._on_play_tick)

        self._refresh_all()

    def setWindow(self, window):
        """Receive the QQuickWindow for custom title-bar controls."""
        self._window = window

    # ------------------------------------------------------------- helpers

    def _refresh_all(self):
        self._display_board()
        self._boardSize = len(self._puzzle)
        self._solvable = bool(core.is_solvable(self._puzzle, self._goal))
        self.stateChanged.emit()

    def _display_board(self):
        if self._viewing_solution and self._solution_states:
            shown = self._solution_states[self._solution_index]
        else:
            shown = self._puzzle
        self.board_model.setBoard(shown, self._goal, highlight=True)
        self.goal_model.setBoard(self._goal, highlight=False)

    def _current_displayed(self):
        if self._viewing_solution and self._solution_states:
            return core.copy_puzzle(self._solution_states[self._solution_index])
        return core.copy_puzzle(self._puzzle)

    def _set_status(self, text, kind="normal"):
        self._statusText = text
        self._statusKind = kind
        self.stateChanged.emit()

    def _set_busy(self, shuffling=None, solving=None):
        if shuffling is not None:
            self._shuffling = shuffling
        if solving is not None:
            self._solving = solving
        self._busy = self._shuffling or self._solving
        self._stopEnabled = self._solving
        self.stateChanged.emit()

    # ---------------------------------------------------------- setup

    @Slot()
    def createPuzzle(self):
        if self._busy:
            return
        size = max(2, min(10, int(self._puzzleSize)))
        mode = SETUP_MODES[int(self._setupModeIndex)]

        if mode == "manual":
            values = [str(value).strip() for value in self._manualCells]
            if len(values) != size * size:
                return
            board, valid = [], True
            for row_index in range(size):
                row = []
                for column_index in range(size):
                    raw = values[row_index * size + column_index]
                    if raw == "":
                        row.append(None)
                    elif raw.isdigit():
                        row.append(int(raw))
                    else:
                        valid = False
                        row.append(None)
                board.append(row)
            if not valid or not core.validate_puzzle(board, size):
                message = (
                    f"Enter each number from 1 to {size * size - 1} once "
                    "and leave exactly one cell blank."
                )
                self._set_status(message, "error")
                self._show_alert(message)
                return
            puzzle = board
        elif mode == "random":
            puzzle = core.random_puzzle(size)
        else:
            puzzle = core.create_puzzle(size)

        self._puzzle = puzzle
        # Product rule: the arrangement just created becomes the goal and is
        # immutable from here on. Only Create Puzzle can replace it.
        self._goal = core.copy_puzzle(puzzle)
        self._manualMoves = 0
        self._checkedNodes = 0
        self._reset_solution()
        self._refresh_all()
        self._set_status("New puzzle created")

    def _show_alert(self, message):
        self._alertText = message
        self._alertVisible = True
        self.stateChanged.emit()
        self.showAlert.emit(message)

    def _show_confirm(self, title, message):
        self._confirmTitle = title
        self._confirmText = message
        self._confirmVisible = True
        self.stateChanged.emit()
        self.showConfirm.emit(title, message)

    @Slot()
    def dismissAlert(self):
        self._alertVisible = False
        self._confirmVisible = False
        self.stateChanged.emit()

    @Slot(int)
    def setPuzzleSize(self, value):
        value = max(2, min(10, int(value)))
        if value == self._puzzleSize:
            return
        self._puzzleSize = value
        self._manualCells = [""] * (value * value)
        self.stateChanged.emit()

    @Slot(int)
    def setSetupMode(self, value):
        value = max(0, min(len(SETUP_MODES) - 1, int(value)))
        if value != self._setupModeIndex:
            self._setupModeIndex = value
            self.stateChanged.emit()

    @Slot(int)
    def setSetupTab(self, value):
        value = max(0, min(1, int(value)))
        if value != self._setupTabIndex:
            self._setupTabIndex = value
            self.stateChanged.emit()

    @Slot(int, str)
    def setManualCell(self, index, text):
        if 0 <= index < len(self._manualCells):
            # Assign into a fresh list so QML bindings on manualCells refresh.
            cells = list(self._manualCells)
            cells[index] = "" if text is None else str(text)
            self._manualCells = cells
            self.stateChanged.emit()

    @Slot()
    def clearManualCells(self):
        self._manualCells = [""] * (int(self._puzzleSize) ** 2)
        self.stateChanged.emit()

    @Slot(int)
    def setShuffleMoves(self, value):
        value = max(SHUFFLE_MIN, min(SHUFFLE_MAX, int(value)))
        if value != self._shuffleMoves:
            self._shuffleMoves = value
            self.stateChanged.emit()

    @Slot(int)
    def setAlgorithmIndex(self, value):
        value = max(0, min(len(ALGORITHMS) - 1, int(value)))
        if value != self._algorithmIndex:
            self._algorithmIndex = value
            self.stateChanged.emit()

    @Slot(bool)
    def setLiveVisualization(self, value):
        value = bool(value)
        if value != self._liveVisualization:
            self._liveVisualization = value
            self.stateChanged.emit()

    @Slot(int)
    def setAnimationDelay(self, value):
        value = max(DELAY_MIN, min(DELAY_MAX, int(value)))
        if value != self._animationDelay:
            self._animationDelay = value
            self.stateChanged.emit()

    @Slot(int)
    def setNodeLimit(self, value):
        value = max(NODE_MIN, min(NODE_MAX, int(value)))
        if value != self._nodeLimit:
            self._nodeLimit = value
            self.stateChanged.emit()

    @Slot()
    def resetSettings(self):
        """Restore the settings that the reference design ships with."""
        self._liveVisualization = True
        self._animationDelay = 28
        self._nodeLimit = 100000
        self._algorithmIndex = 2
        self._shuffleMoves = 100
        self._set_status("Settings restored to defaults")

    @Slot()
    def shufflePuzzle(self):
        if self._busy:
            return
        self._reset_solution()
        self._checkedNodes = 0
        self._shuffle_remaining = max(1, int(self._shuffleMoves))
        self._shuffle_batch = max(1, self._shuffle_remaining // 80)
        self._shuffle_previous_blank = None
        self._set_busy(shuffling=True)
        self._set_status("Shuffling puzzle...", "working")
        self._shuffle_timer.start(max(10, int(self._animationDelay)))

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
        self._manualMoves += applied
        self._refresh_all()
        if self._shuffle_remaining <= 0:
            self._shuffle_timer.stop()
            self._set_busy(shuffling=False)
            self._set_status("Puzzle is ready")

    # ------------------------------------------------------- manual moves

    @Slot(int, int)
    def moveTile(self, row, column):
        if self._busy:
            return
        current = self._current_displayed()
        direction = core.move_for_tile_click(current, int(row), int(column))
        if direction is None:
            return
        self._apply_manual_move(current, direction)

    @Slot(str)
    def moveBlank(self, direction):
        if self._busy:
            return
        current = self._current_displayed()
        if core.apply_move(current, str(direction)) is not None:
            self._apply_manual_move(current, str(direction))

    def _apply_manual_move(self, current, direction):
        moved = core.apply_move(current, direction)
        if moved is None:
            return
        self._puzzle = moved
        self._manualMoves += 1
        self._viewing_solution = False
        self._refresh_all()

    # ------------------------------------------------------------ solving

    @Slot()
    def solve(self):
        if self._busy:
            return
        if not core.is_solvable(self._puzzle, self._goal):
            self._pending_solve = True
            self._show_confirm(
                "Unsolvable configuration",
                "This board cannot be transformed into the goal state.\n"
                "The search would explore the entire state space "
                f"(up to the {self._nodeLimit:,} node limit). Run it anyway?",
            )
            return
        self._start_solve()

    @Slot()
    def confirmSolve(self):
        self._confirmVisible = False
        self.stateChanged.emit()
        if self._pending_solve:
            self._pending_solve = False
            self._start_solve()

    @Slot()
    def cancelSolve(self):
        self._pending_solve = False
        self._confirmVisible = False
        self.stateChanged.emit()

    def _start_solve(self):
        algorithm = ALGORITHMS[int(self._algorithmIndex)]
        if self._viewing_solution and self._solution_states:
            self._puzzle = core.copy_puzzle(
                self._solution_states[self._solution_index]
            )
        hint = ""
        if len(self._puzzle) >= 4 and algorithm != "A* Search Algorithm":
            hint = (
                f" (A* is recommended for {len(self._puzzle)}x"
                f"{len(self._puzzle)} boards)"
            )
        self._solve_start = core.copy_puzzle(self._puzzle)
        self._checkedNodes = 0
        self._reset_solution()
        self._set_busy(solving=True)
        self._set_status(f"Running {algorithm}...{hint}", "working")

        thread = QThread(self)
        worker = SolverWorker(
            algorithm,
            self._puzzle,
            self._goal,
            max_nodes=int(self._nodeLimit),
            visualize=bool(self._liveVisualization),
            frame_delay_ms=int(self._animationDelay),
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
        thread.finished.connect(lambda t=thread: self._on_thread_done(t))
        self._thread = thread
        self._worker = worker
        thread.start()

    @Slot()
    def stopSolve(self):
        if self._thread is not None and self._thread.isRunning():
            self._thread.requestInterruption()
            self._set_status("Stopping search...", "working")

    def _finish_solving(self):
        self._set_busy(solving=False)

    def _on_thread_done(self, thread=None):
        if thread is not None and thread is not self._thread:
            return
        self._thread = None
        self._worker = None
        if self._solving:
            self._finish_solving()

    def _on_progress(self, state, count):
        self._checkedNodes = int(count)
        if state is not None:
            self.board_model.setBoard(state, self._goal, highlight=True)
        self.stateChanged.emit()

    def _on_solved(self, directions, count):
        self._checkedNodes = int(count)
        self._solution_directions = list(directions)
        self._solution_states = core.solution_states(
            self._solve_start, self._solution_directions
        )
        self._solution_index = len(self._solution_states) - 1
        self._viewing_solution = True
        self._puzzle = core.copy_puzzle(self._goal)
        self._fill_solution_text()
        self._playbackTotal = self._solution_index
        self._playbackStep = self._solution_index
        self._playbackAvailable = True
        self._update_playback()
        self._refresh_all()
        self._set_status(
            f"Puzzle solved! {count:,} nodes checked, "
            f"{len(self._solution_directions)} moves.",
            "success",
        )
        self._finish_solving()

    def _on_finished(self, count):
        self._checkedNodes = int(count)
        self._viewing_solution = False
        self._refresh_all()
        self._set_status(
            f"Search finished without solution ({count:,} nodes checked).",
            "error",
        )
        self._finish_solving()

    def _on_aborted(self, reason, count):
        self._checkedNodes = int(count)
        self._viewing_solution = False
        self._refresh_all()
        self._set_status(f"{reason} {count:,} nodes checked.", "warning")
        self._finish_solving()

    def _on_failed(self, message):
        self._viewing_solution = False
        self._refresh_all()
        self._set_status(message, "error")
        self._show_alert(message)
        self._finish_solving()

    # ---------------------------------------------------------- playback

    def _reset_solution(self):
        self._play_timer.stop()
        self._solution_directions = []
        self._solution_states = []
        self._solution_index = 0
        self._viewing_solution = False
        self._solutionText = ""
        self._playbackStep = 0
        self._playbackTotal = 0
        self._playbackAvailable = False
        self._playing = False
        self.stateChanged.emit()

    def _fill_solution_text(self):
        if not self._solution_directions:
            text = "Puzzle was already in the goal state - 0 moves required."
        else:
            total = len(self._solution_directions)
            shown = min(total, 160)
            chunks = [
                f"{index:>2}.{ARROWS[direction]}  "
                for index, direction in enumerate(
                    self._solution_directions[:shown], 1
                )
            ]
            lines = [
                "  ".join(chunks[i: i + 8]) for i in range(0, len(chunks), 8)
            ]
            text = "\n".join(lines)
            if total > shown:
                text += (
                    f"\n... {total - shown:,} more moves - "
                    "use the slider to inspect the full path."
                )
            if total > 200 and ALGORITHMS[int(self._algorithmIndex)] == (
                "Depth First Search"
            ):
                text = (
                    "DFS is not optimal: it returned a very long path "
                    f"({total:,} moves). Use BFS or A* for the shortest one.\n"
                    + text
                )
        self._solutionText = text
        self.stateChanged.emit()

    def _update_playback(self):
        self._playbackStep = self._solution_index
        self._playbackTotal = max(0, len(self._solution_states) - 1)
        self._display_board()
        self.stateChanged.emit()

    @Slot()
    def playPause(self):
        if not self._solution_states:
            return
        if self._play_timer.isActive():
            self._play_timer.stop()
            self._playing = False
            self.stateChanged.emit()
            return
        if self._solution_index >= len(self._solution_states) - 1:
            self._solution_index = 0
        self._viewing_solution = True
        self._update_playback()
        self._playing = True
        self.stateChanged.emit()
        self._play_timer.start(max(30, int(self._animationDelay) * 2))

    def _on_play_tick(self):
        if self._solution_index >= len(self._solution_states) - 1:
            self._play_timer.stop()
            self._playing = False
            self.stateChanged.emit()
            return
        self._solution_index += 1
        self._update_playback()

    def _pause(self):
        self._play_timer.stop()
        self._playing = False

    @Slot()
    def firstStep(self):
        if not self._solution_states:
            return
        self._pause()
        self._solution_index = 0
        self._viewing_solution = True
        self._update_playback()

    @Slot()
    def lastStep(self):
        if not self._solution_states:
            return
        self._pause()
        self._solution_index = len(self._solution_states) - 1
        self._viewing_solution = True
        self._update_playback()

    @Slot(int)
    def stepBy(self, delta):
        if not self._solution_states:
            return
        self._pause()
        self._solution_index = max(
            0,
            min(len(self._solution_states) - 1, self._solution_index + int(delta)),
        )
        self._viewing_solution = True
        self._update_playback()

    @Slot(int)
    def seekStep(self, value):
        if not self._solution_states:
            return
        self._pause()
        self._solution_index = max(
            0, min(len(self._solution_states) - 1, int(value))
        )
        self._viewing_solution = True
        self._update_playback()

    # -------------------------------------------------- window + settings

    @Slot()
    def toggleBoardExpanded(self):
        self._boardExpanded = not self._boardExpanded
        self.stateChanged.emit()

    @Slot()
    def startWindowMove(self):
        if self._window is not None:
            self._window.startSystemMove()

    @Slot(int)
    def startWindowResize(self, edges):
        if self._window is not None:
            self._window.startSystemResize(Qt.Edge(int(edges)))

    @Slot()
    def toggleMaximize(self):
        if self._window is None:
            return
        if self._window.windowStates() & Qt.WindowState.WindowMaximized:
            self._window.showNormal()
            self._windowMaximized = False
        else:
            self._window.showMaximized()
            self._windowMaximized = True
        self.stateChanged.emit()

    @Slot()
    def minimizeWindow(self):
        if self._window is not None:
            self._window.showMinimized()

    @Slot()
    def closeWindow(self):
        self.shutdown()
        if self._window is not None:
            self._window.close()

    @Slot()
    def shutdown(self):
        self._shuffle_timer.stop()
        self._play_timer.stop()
        if self._thread is not None and self._thread.isRunning():
            self._thread.requestInterruption()
            self._thread.quit()
            self._thread.wait(3000)
