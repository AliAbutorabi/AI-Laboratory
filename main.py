"""Puzzle Solver - minimal, unstyled front end.

core.py, backend.py and solver_worker.py are used unchanged.  This file only
wires stock Qt widgets to the backend's slots and reads its properties.
"""
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QSpinBox,
    QCheckBox, QSlider, QPlainTextEdit, QMessageBox, QGroupBox,
    QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout,
)

from backend import PuzzleBackend


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.b = PuzzleBackend()
        self.setWindowTitle("Puzzle Solver")
        self.setMinimumSize(760, 620)
        self.resize(800, 650)
        self._dialog = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        # ------------------------------------------------------------ setup
        setup = QGroupBox("Puzzle")
        row = QHBoxLayout(setup)
        row.setContentsMargins(10, 12, 10, 10)
        row.setSpacing(8)
        self.size = QSpinBox()
        self.size.setRange(2, 10)
        self.size.setFixedWidth(100)
        self.size.setValue(self.b.puzzleSize)
        create = QPushButton("Create Puzzle")
        self.shuffles = QSpinBox()
        self.shuffles.setRange(1, 2000)
        self.shuffles.setFixedWidth(100)
        self.shuffles.setValue(self.b.shuffleMoves)
        shuffle = QPushButton("Shuffle")
        for widget in (QLabel("Size"), self.size, create,
                       QLabel("Shuffle moves"), self.shuffles, shuffle):
            row.addWidget(widget)
        row.addStretch(1)
        root.addWidget(setup)

        # ----------------------------------------------------------- search
        search = QGroupBox("Search")
        row = QHBoxLayout(search)
        row.setContentsMargins(10, 12, 10, 10)
        row.setSpacing(8)
        self.algorithm = QComboBox()
        self.algorithm.addItems(self.b.algorithms)
        self.algorithm.setCurrentIndex(self.b.algorithmIndex)
        self.algorithm.setMinimumWidth(180)
        self.live = QCheckBox("Live visualization")
        self.live.setChecked(self.b.liveVisualization)
        self.delay = QSpinBox()
        self.delay.setRange(10, 400)
        self.delay.setFixedWidth(100)
        self.delay.setValue(self.b.animationDelay)
        self.nodeLimit = QSpinBox()
        self.nodeLimit.setRange(1000, 5000000)
        self.nodeLimit.setSingleStep(50000)
        self.nodeLimit.setFixedWidth(120)
        self.nodeLimit.setValue(self.b.nodeLimit)
        for widget in (QLabel("Algorithm"), self.algorithm, self.live,
                       QLabel("Delay (ms)"), self.delay,
                       QLabel("Node limit"), self.nodeLimit):
            row.addWidget(widget)
        row.addStretch(1)
        root.addWidget(search)

        # -------------------------------------------------- board + readouts
        boardBox = QGroupBox("Board")
        body = QHBoxLayout(boardBox)
        body.setContentsMargins(10, 12, 10, 10)
        body.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(2)
        self.cells = []
        for r in range(10):
            line = []
            for c in range(10):
                button = QPushButton()
                button.setFixedSize(40, 34)
                button.clicked.connect(
                    lambda _checked=False, r=r, c=c: self.b.moveTile(r, c)
                )
                grid.addWidget(button, r, c)
                line.append(button)
            self.cells.append(line)

        boardSide = QHBoxLayout()
        boardSide.addStretch(1)
        boardSide.addLayout(grid)
        boardSide.addStretch(1)
        body.addLayout(boardSide, 3)

        self.status = QLabel()
        self.nodes = QLabel()
        self.moves = QLabel()
        self.solvable = QLabel()
        for label in (self.status, self.nodes, self.moves, self.solvable):
            label.setWordWrap(True)
        info = QFormLayout()
        info.setSpacing(8)
        info.addRow("Status:", self.status)
        info.addRow("Checked nodes:", self.nodes)
        info.addRow("Manual moves:", self.moves)
        info.addRow("Solvable:", self.solvable)
        body.addLayout(info, 2)
        root.addWidget(boardBox, 1)

        # ---------------------------------------------------------- actions
        actions = QGroupBox("Solve / Playback")
        column = QVBoxLayout(actions)
        column.setContentsMargins(10, 12, 10, 10)
        column.setSpacing(8)
        row = QHBoxLayout()
        row.setSpacing(6)
        self.solve = QPushButton("Solve Puzzle")
        self.stop = QPushButton("Stop")
        first = QPushButton("|<")
        previous = QPushButton("<")
        self.play = QPushButton("Play")
        following = QPushButton(">")
        last = QPushButton(">|")
        for button in (first, previous, self.play, following, last):
            button.setFixedWidth(48)
        self.play.setFixedWidth(64)
        for widget in (self.solve, self.stop, first, previous, self.play,
                       following, last):
            row.addWidget(widget)
        row.addStretch(1)
        column.addLayout(row)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        column.addWidget(self.slider)
        root.addWidget(actions)

        # ---------------------------------------------------------- solution
        solutionBox = QGroupBox("Solution")
        column = QVBoxLayout(solutionBox)
        column.setContentsMargins(10, 12, 10, 10)
        self.solution = QPlainTextEdit()
        self.solution.setReadOnly(True)
        self.solution.setFixedHeight(90)
        column.addWidget(self.solution)
        root.addWidget(solutionBox)

        # ----------------------------------------------------------- wiring
        create.clicked.connect(
            lambda: (self.b.setPuzzleSize(self.size.value()),
                     self.b.createPuzzle())
        )
        shuffle.clicked.connect(
            lambda: (self.b.setShuffleMoves(self.shuffles.value()),
                     self.b.shufflePuzzle())
        )
        self.algorithm.currentIndexChanged.connect(self.b.setAlgorithmIndex)
        self.live.toggled.connect(self.b.setLiveVisualization)
        self.delay.valueChanged.connect(self.b.setAnimationDelay)
        self.nodeLimit.valueChanged.connect(self.b.setNodeLimit)
        self.solve.clicked.connect(self.b.solve)
        self.stop.clicked.connect(self.b.stopSolve)
        first.clicked.connect(self.b.firstStep)
        previous.clicked.connect(lambda: self.b.stepBy(-1))
        self.play.clicked.connect(self.b.playPause)
        following.clicked.connect(lambda: self.b.stepBy(1))
        last.clicked.connect(self.b.lastStep)
        self.slider.valueChanged.connect(self.b.seekStep)

        # Poll instead of binding to stateChanged: solver progress arrives from
        # the worker thread, and widgets may only be touched on the UI thread.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(50)
        self.refresh()

    def keyPressEvent(self, event):
        keys = {
            Qt.Key.Key_Up: "up", Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left", Qt.Key.Key_Right: "right",
        }
        if event.key() in keys:
            self.b.moveBlank(keys[event.key()])
        else:
            super().keyPressEvent(event)

    def refresh(self):
        b = self.b
        model = b.board_model
        size = b.boardSize
        board = [[""] * size for _ in range(size)]
        for i in range(model.rowCount()):
            index = model.index(i, 0)
            if model.data(index, model.BLANK):
                continue
            r, c = model.data(index, model.ROW), model.data(index, model.COLUMN)
            if 0 <= r < size and 0 <= c < size:
                board[r][c] = str(model.data(index, model.NUMBER))
        for r in range(10):
            for c in range(10):
                cell = self.cells[r][c]
                cell.setVisible(r < size and c < size)
                if r < size and c < size:
                    cell.setText(board[r][c])

        self.status.setText(b.statusText)
        self.nodes.setText("{:,}".format(b.checkedNodes))
        self.moves.setText(str(b.manualMoves))
        self.solvable.setText("yes" if b.solvable else "no")
        text = b.solutionText
        if self.solution.toPlainText() != text:
            self.solution.setPlainText(text)

        self.slider.blockSignals(True)
        self.slider.setRange(0, max(0, b.playbackTotal))
        self.slider.setValue(b.playbackStep)
        self.slider.blockSignals(False)
        self.solve.setEnabled(not b.busy)
        self.stop.setEnabled(b.stopEnabled)
        self.slider.setEnabled(b.playbackAvailable)
        self.play.setEnabled(b.playbackAvailable)
        self.play.setText("Pause" if b.playing else "Play")
        self.checkDialogs()

    def checkDialogs(self):
        if self._dialog:
            return
        self._dialog = True
        if self.b.confirmVisible:
            answer = QMessageBox.question(
                self, self.b.confirmTitle, self.b.confirmText,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                self.b.confirmSolve()
            else:
                self.b.cancelSolve()
        elif self.b.alertVisible:
            QMessageBox.information(self, "Puzzle Solver", self.b.alertText)
            self.b.dismissAlert()
        self._dialog = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.aboutToQuit.connect(window.b.shutdown)
    sys.exit(app.exec())
