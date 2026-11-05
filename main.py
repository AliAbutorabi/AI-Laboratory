"""Persian Qt widget interface for the puzzle solver."""
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout,
)

from backend import PuzzleBackend


class Window(QWidget):
    def __init__(self):
        super().__init__()
        app = QApplication.instance()
        if app is not None:
            app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.b = PuzzleBackend()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setWindowTitle("علی ابوترابی - پروژه پازل")
        self.setMinimumSize(1080, 620)
        self.resize(1180, 650)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        # ------------------------------------------------------------ setup
        setup = QGroupBox("پازل")
        row = QHBoxLayout(setup)
        row.setContentsMargins(10, 12, 10, 10)
        row.setSpacing(8)
        self.setupMode = QComboBox()
        self.setupMode.addItems(["استاندارد", "تصادفی"])
        self.setupMode.setCurrentIndex(
            0 if self.b.setupModeIndex == 0 else 1
        )
        self.size = QSpinBox()
        self.size.setRange(2, 10)
        self.size.setFixedWidth(100)
        self.size.setValue(self.b.puzzleSize)
        create = QPushButton("ساخت پازل")
        self.shuffles = QSpinBox()
        self.shuffles.setRange(1, 2000)
        self.shuffles.setFixedWidth(100)
        self.shuffles.setValue(self.b.shuffleMoves)
        shuffle = QPushButton("به‌هم‌ریختن")
        for widget in (QLabel("نوع ایجاد"), self.setupMode,
                       QLabel("اندازه"), self.size, create,
                       QLabel("تعداد حرکت"), self.shuffles, shuffle):
            row.addWidget(widget)
        row.addStretch(1)
        root.addWidget(setup)

        # ----------------------------------------------------------- search
        search = QGroupBox("جست‌وجو")
        row = QHBoxLayout(search)
        row.setContentsMargins(10, 12, 10, 10)
        row.setSpacing(8)
        self.algorithm = QComboBox()
        self.algorithm.addItems(["جست‌وجوی سطحی", "جست‌وجوی عمقی", "جست‌وجوی A*"])
        self.algorithm.setCurrentIndex(self.b.algorithmIndex)
        self.algorithm.setMinimumWidth(180)
        self.nodeLimit = QSpinBox()
        self.nodeLimit.setRange(1000, 5000000)
        self.nodeLimit.setSingleStep(50000)
        self.nodeLimit.setFixedWidth(120)
        self.nodeLimit.setValue(self.b.nodeLimit)
        self.solve = QPushButton("حل پازل")
        for widget in (QLabel("الگوریتم"), self.algorithm,
                       QLabel("محدودیت گره‌ها"), self.nodeLimit, self.solve):
            row.addWidget(widget)
        row.addStretch(1)
        root.addWidget(search)

        # -------------------------------------------------- boards + readouts
        boardBox = QGroupBox("صفحه‌های پازل")
        body = QHBoxLayout(boardBox)
        body.setContentsMargins(10, 12, 10, 10)
        body.setSpacing(12)

        self.cells = []
        self.goalCells = []
        for title, cells in (("پازل فعلی", self.cells),
                             ("وضعیت هدف", self.goalCells)):
            panel = QGroupBox(title)
            panel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            panel.setAlignment(Qt.AlignmentFlag.AlignRight)
            panel_layout = QHBoxLayout(panel)
            panel_layout.addStretch(1)
            grid = QGridLayout()
            grid.setHorizontalSpacing(2)
            grid.setVerticalSpacing(2)
            for r in range(10):
                line = []
                for c in range(10):
                    button = QPushButton()
                    button.setFixedSize(40, 34)
                    grid.addWidget(button, r, c)
                    line.append(button)
                cells.append(line)
            panel_layout.addLayout(grid)
            panel_layout.setAlignment(grid, Qt.AlignmentFlag.AlignTop)
            panel_layout.addStretch(1)
            body.addWidget(panel, 1)

        self.status = QLabel()
        self.nodes = QLabel()
        for label in (self.status, self.nodes):
            label.setWordWrap(True)
            label.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
        info = QFormLayout()
        info.setSpacing(8)
        info.addRow("وضعیت:", self.status)
        info.addRow("گره‌های بررسی‌شده:", self.nodes)
        body.addLayout(info, 2)
        root.addWidget(boardBox, 1)

        # ----------------------------------------------------------- wiring
        self.setupMode.currentIndexChanged.connect(
            self.b.setSetupMode
        )
        create.clicked.connect(
            lambda: (self.b.setPuzzleSize(self.size.value()),
                     self.b.createPuzzle())
        )
        shuffle.clicked.connect(
            lambda: (self.b.setShuffleMoves(self.shuffles.value()),
                     self.b.shufflePuzzle())
        )
        self.algorithm.currentIndexChanged.connect(self.b.setAlgorithmIndex)
        self.nodeLimit.valueChanged.connect(self.b.setNodeLimit)
        self.solve.clicked.connect(self.b.solve)

        # Backend state may change on a worker thread; update widgets here.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(50)
        self.refresh()

    def refresh(self):
        b = self.b
        for puzzle, cells in ((b.displayPuzzle, self.cells),
                              (b.goalPuzzle, self.goalCells)):
            size = len(puzzle)
            for r in range(10):
                for c in range(10):
                    cell = cells[r][c]
                    cell.setVisible(r < size and c < size)
                    if r < size and c < size:
                        value = puzzle[r][c]
                        cell.setText("" if value is None else str(value))

        self.status.setText(b.statusText)
        self.nodes.setText("{:,}".format(b.checkedNodes))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = Window()
    window.show()
    app.aboutToQuit.connect(window.b.shutdown)
    sys.exit(app.exec())
