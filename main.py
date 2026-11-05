"""Puzzle Solver - minimal, unstyled front end.

core.py, backend.py and solver_worker.py are used unchanged.  This file only
wires stock Qt widgets to the backend's slots and reads its properties.
"""
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QSpinBox,
    QCheckBox, QSlider, QPlainTextEdit, QMessageBox, QGridLayout,
    QHBoxLayout, QVBoxLayout,
)

from backend import PuzzleBackend


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.b = PuzzleBackend()
        self.setWindowTitle("Puzzle Solver")
        self._dialog = False
        root = QVBoxLayout(self)

        row = QHBoxLayout()
        self.size = QSpinBox()
        self.size.setRange(2, 10)
        self.size.setValue(self.b.puzzleSize)
        create = QPushButton("Create Puzzle")
        self.shuffles = QSpinBox()
        self.shuffles.setRange(1, 2000)
        self.shuffles.setValue(self.b.shuffleMoves)
        shuffle = QPushButton("Shuffle")
        for w in (QLabel("Size"), self.size, create,
                  QLabel("Shuffle moves"), self.shuffles, shuffle):
            row.addWidget(w)
        root.addLayout(row)

        row = QHBoxLayout()
        self.algorithm = QComboBox()
        self.algorithm.addItems(self.b.algorithms)
        self.algorithm.setCurrentIndex(self.b.algorithmIndex)
        self.live = QCheckBox("Live visualization")
        self.live.setChecked(self.b.liveVisualization)
        self.delay = QSpinBox()
        self.delay.setRange(10, 400)
        self.delay.setValue(self.b.animationDelay)
        self.nodeLimit = QSpinBox()
        self.nodeLimit.setRange(1000, 5000000)
        self.nodeLimit.setSingleStep(50000)
        self.nodeLimit.setValue(self.b.nodeLimit)
        for w in (QLabel("Algorithm"), self.algorithm, self.live,
                  QLabel("Delay ms"), self.delay,
                  QLabel("Node limit"), self.nodeLimit):
            row.addWidget(w)
        root.addLayout(row)

        body = QHBoxLayout()
        grid = QGridLayout()
        self.cells = []
        for r in range(10):
            line = []
            for c in range(10):
                button = QPushButton()
                button.setFixedSize(46, 36)
                button.clicked.connect(
                    lambda _checked=False, r=r, c=c: self.b.moveTile(r, c)
                )
                grid.addWidget(button, r, c)
                line.append(button)
            self.cells.append(line)
        body.addLayout(grid)

        info = QVBoxLayout()
        self.status = QLabel()
        self.nodes = QLabel()
        self.moves = QLabel()
        self.solvable = QLabel()
        for label in (self.status, self.nodes, self.moves, self.solvable):
            label.setWordWrap(True)
            info.addWidget(label)
        info.addStretch(1)
        body.addLayout(info)
        root.addLayout(body)

        row = QHBoxLayout()
        self.solve = QPushButton("Solve Puzzle")
        self.stop = QPushButton("Stop")
        first = QPushButton("|<")
        previous = QPushButton("<")
        self.play = QPushButton("Play")
        following = QPushButton(">")
        last = QPushButton(">|")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        for w in (self.solve, self.stop, first, previous, self.play,
                  following, last, self.slider):
            row.addWidget(w)
        root.addLayout(row)

        self.solution = QPlainTextEdit()
        self.solution.setReadOnly(True)
        self.solution.setMaximumHeight(110)
        root.addWidget(self.solution)

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

        self.status.setText("Status: " + b.statusText)
        self.nodes.setText("Checked nodes: " + str(b.checkedNodes))
        self.moves.setText("Manual moves: " + str(b.manualMoves))
        self.solvable.setText("Solvable: " + ("yes" if b.solvable else "no"))
        text = b.solutionText
        if self.solution.toPlainText() != text:
            self.solution.setPlainText(text)

        self.slider.blockSignals(True)
        self.slider.setRange(0, max(0, b.playbackTotal))
        self.slider.setValue(b.playbackStep)
        self.slider.blockSignals(False)
        self.solve.setEnabled(not b.busy)
        self.stop.setEnabled(b.stopEnabled)
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
