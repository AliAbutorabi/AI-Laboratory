"""Run puzzle search in a worker thread and report results through a queue."""

import time

import core


FRAME_DELAY_MS = 28


class SolverWorker:
    def __init__(self, algorithm, puzzle, goal, max_nodes, events):
        self.algorithm = algorithm
        self.puzzle = core.copy_puzzle(puzzle)
        self.goal = core.copy_puzzle(goal)
        self.max_nodes = max_nodes
        self.events = events

    def run(self):
        generator = None
        checked = 0
        try:
            solver = core.SOLVERS.get(self.algorithm)
            if solver is None:
                self.events.put(
                    ("failed", f"الگوریتم پشتیبانی نمی‌شود: {self.algorithm}")
                )
                return

            generator = solver(self.puzzle, self.goal)
            last_frame = 0.0
            for event in generator:
                kind = event["type"]
                checked = event.get("checked_nodes", checked)
                if kind == "checked":
                    if checked > self.max_nodes:
                        self.events.put(
                            (
                                "aborted",
                                f"محدودیت گره‌ها ({self.max_nodes:,}) پر شد.",
                                checked,
                            )
                        )
                        return
                    now = time.monotonic()
                    if now - last_frame >= FRAME_DELAY_MS / 1000:
                        last_frame = now
                        self.events.put(("progress", event["state"], checked))
                elif kind == "solved":
                    self.events.put(("solved", event["solution"], checked))
                    return
                elif kind == "finished":
                    self.events.put(("finished", checked))
                    return
                else:
                    self.events.put(("failed", f"رویداد حل‌گر ناشناخته است: {kind}"))
                    return
        except Exception as exc:
            self.events.put(
                ("failed", f"خطای داخلی ({type(exc).__name__}): {exc}")
            )
        finally:
            if generator is not None:
                generator.close()
            self.events.put(("done",))
