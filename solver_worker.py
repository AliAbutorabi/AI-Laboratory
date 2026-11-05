"""Run a puzzle search off the UI thread and report periodic progress."""

import time

from PySide6.QtCore import QObject, Signal, Slot

import core


FRAME_DELAY_MS = 28


class SolverWorker(QObject):
    progress = Signal(object, int)      # grid and checked node count
    solved = Signal(object, int)        # solution directions, checked node count
    finished = Signal(int)              # no solution, checked node count
    aborted = Signal(str, int)          # reason, checked node count
    failed = Signal(str)                # exception text
    done = Signal()                     # always emitted at the end of run()

    def __init__(
        self,
        algorithm,
        puzzle,
        goal,
        max_nodes=300000,
        parent=None,
    ):
        super().__init__(parent)
        self.algorithm = algorithm
        self.puzzle = core.copy_puzzle(puzzle)
        self.goal = core.copy_puzzle(goal)
        self.max_nodes = max_nodes
        self.frame_delay = FRAME_DELAY_MS / 1000.0

    @Slot()
    def run(self):
        generator = None
        checked = 0
        try:
            solver = core.SOLVERS.get(self.algorithm)
            if solver is None:
                self.failed.emit(f"الگوریتم پشتیبانی نمی‌شود: {self.algorithm}")
                return

            generator = solver(self.puzzle, self.goal)
            thread = self.thread()
            last_frame = 0.0

            for event in generator:
                if thread is not None and thread.isInterruptionRequested():
                    self.aborted.emit("جست‌وجو به‌درخواست کاربر لغو شد.", checked)
                    return

                kind = event["type"]
                checked = event.get("checked_nodes", checked)

                if kind == "checked":
                    if checked > self.max_nodes:
                        self.aborted.emit(
                            f"محدودیت گره‌ها ({self.max_nodes:,}) پر شد.", checked
                        )
                        return
                    now = time.monotonic()
                    if now - last_frame >= self.frame_delay:
                        last_frame = now
                        self.progress.emit(event["state"], checked)
                    continue

                if kind == "solved":
                    self.solved.emit(event["solution"], checked)
                    return

                if kind == "finished":
                    self.finished.emit(checked)
                    return

                self.failed.emit(f"رویداد حل‌گر ناشناخته است: {kind}")
                return

        except Exception as exc:  # pragma: no cover - defensive
            self.failed.emit(f"خطای داخلی ({type(exc).__name__}): {exc}")
        finally:
            if generator is not None:
                generator.close()
            self.done.emit()
