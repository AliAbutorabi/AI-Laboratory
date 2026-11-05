"""Persian Tkinter interface for the puzzle solver."""

import tkinter as tk
from tkinter import ttk

from backend import PuzzleBackend


ALGORITHM_LABELS = (
    "جست‌وجوی سطحی",
    "جست‌وجوی عمقی",
    "جست‌وجوی A*",
)


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.b = PuzzleBackend()
        self.title("علی ابوترابی - پروژه پازل")
        self.minsize(1080, 620)
        self.geometry("1180x650")

        self._configure_style()
        self._build_setup()
        self._build_search()
        self._build_boards()
        self.refresh()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def _configure_style(self):
        self.option_add("*Font", "{Segoe UI} 10")
        self.option_add("*Label.justify", "right")
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", anchor="e")
        style.configure("Board.TButton", padding=0)

    def _build_setup(self):
        box = ttk.LabelFrame(self, text="پازل", labelanchor="ne", padding=10)
        box.pack(fill="x", padx=12, pady=(12, 5))

        self.setup_mode = ttk.Combobox(
            box, state="readonly", width=10, values=("استاندارد", "تصادفی")
        )
        self.setup_mode.current(self.b.setupModeIndex)
        self.size = tk.Spinbox(box, from_=2, to=10, width=5, justify="right")
        self.size.delete(0, "end")
        self.size.insert(0, str(self.b.puzzleSize))
        self.shuffle_moves = tk.Spinbox(
            box, from_=1, to=2000, width=7, justify="right"
        )
        self.shuffle_moves.delete(0, "end")
        self.shuffle_moves.insert(0, str(self.b.shuffleMoves))

        self._field(box, "نوع ایجاد", self.setup_mode)
        self._field(box, "اندازه", self.size)
        ttk.Button(box, text="ساخت پازل", command=self.create_puzzle).pack(
            side="right", padx=4
        )
        self._field(box, "تعداد حرکت", self.shuffle_moves)
        ttk.Button(box, text="به‌هم‌ریختن", command=self.shuffle_puzzle).pack(
            side="right", padx=4
        )

    def _build_search(self):
        box = ttk.LabelFrame(self, text="جست‌وجو", labelanchor="ne", padding=10)
        box.pack(fill="x", padx=12, pady=5)

        self.algorithm = ttk.Combobox(
            box, state="readonly", width=20, values=ALGORITHM_LABELS
        )
        self.algorithm.current(self.b.algorithmIndex)
        self.node_limit = tk.Spinbox(
            box, from_=1000, to=5000000, increment=50000,
            width=10, justify="right",
        )
        self.node_limit.delete(0, "end")
        self.node_limit.insert(0, str(self.b.nodeLimit))

        self._field(box, "الگوریتم", self.algorithm)
        self._field(box, "محدودیت گره‌ها", self.node_limit)
        self.solve_button = ttk.Button(
            box, text="حل پازل", command=self.solve
        )
        self.solve_button.pack(side="right", padx=4)

    def _build_boards(self):
        boards = ttk.LabelFrame(
            self, text="صفحه‌های پازل", labelanchor="ne", padding=10
        )
        boards.pack(fill="both", expand=True, padx=12, pady=(5, 12))

        current = ttk.LabelFrame(
            boards, text="پازل فعلی", labelanchor="ne", padding=8
        )
        current.grid(row=0, column=0, sticky="n", padx=5)
        goal = ttk.LabelFrame(
            boards, text="وضعیت هدف", labelanchor="ne", padding=8
        )
        goal.grid(row=0, column=1, sticky="n", padx=5)
        boards.columnconfigure(0, weight=1)
        boards.columnconfigure(1, weight=1)
        boards.columnconfigure(2, weight=1)

        self.cells = self._make_grid(current)
        self.goal_cells = self._make_grid(goal)

        info = ttk.Frame(boards)
        info.grid(row=0, column=2, sticky="ne", padx=8)
        ttk.Label(info, text="وضعیت:", anchor="e").grid(
            row=0, column=1, sticky="e", padx=(8, 0), pady=4
        )
        self.status = ttk.Label(info, anchor="e", justify="right", wraplength=250)
        self.status.grid(row=0, column=0, sticky="e", pady=4)
        ttk.Label(info, text="گره‌های بررسی‌شده:", anchor="e").grid(
            row=1, column=1, sticky="e", padx=(8, 0), pady=4
        )
        self.nodes = ttk.Label(info, anchor="e", justify="right")
        self.nodes.grid(row=1, column=0, sticky="e", pady=4)

    @staticmethod
    def _field(parent, label, widget):
        ttk.Label(parent, text=label, anchor="e").pack(
            side="right", padx=(10, 4)
        )
        widget.pack(side="right", padx=4)

    @staticmethod
    def _make_grid(parent):
        cells = []
        for row in range(10):
            line = []
            for column in range(10):
                cell = ttk.Button(parent, style="Board.TButton", width=4)
                cell.grid(row=row, column=column, padx=1, pady=1)
                line.append(cell)
            cells.append(line)
        return cells

    def create_puzzle(self):
        self.b.setPuzzleSize(int(self.size.get()))
        self.b.setSetupMode(self.setup_mode.current())
        self.b.createPuzzle()
        self.refresh()

    def shuffle_puzzle(self):
        self.b.setShuffleMoves(int(self.shuffle_moves.get()))
        self.b.shufflePuzzle()
        self.refresh()

    def solve(self):
        self.b.setAlgorithmIndex(self.algorithm.current())
        self.b.setNodeLimit(int(self.node_limit.get()))
        self.b.solve()
        self.refresh()

    def refresh(self):
        self.b.process_events()
        for puzzle, cells in (
            (self.b.displayPuzzle, self.cells),
            (self.b.goalPuzzle, self.goal_cells),
        ):
            size = len(puzzle)
            for row in range(10):
                for column in range(10):
                    cell = cells[row][column]
                    if row < size and column < size:
                        value = puzzle[row][column]
                        cell.configure(
                            text="" if value is None else str(value)
                        )
                        cell.grid()
                    else:
                        cell.grid_remove()

        self.status.configure(text=self.b.statusText)
        self.nodes.configure(text="{:,}".format(self.b.checkedNodes))
        self.solve_button.configure(
            state="disabled" if self.b.busy else "normal"
        )
        if self.winfo_exists():
            self.after(50, self.refresh)

    def close(self):
        self.b.shutdown()
        self.destroy()


if __name__ == "__main__":
    Window().mainloop()
