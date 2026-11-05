"""Puzzle Solver - Windows desktop edition (PySide6 / Qt Quick).

The presentation layer is QML (``ui/``); all puzzle state, algorithms and the
threaded solver live in Python (``core.py``, ``backend.py``,
``solver_worker.py``).  The two layers communicate through QObject properties,
signals/slots and two QAbstractListModel board models registered as QML
context properties.

Entry point: ``python desktop/main.py``  (or the bundled PuzzleSolver.exe).

Development / verification flags:
    --selftest              headless algorithm verification
    --smoke-ui              headless QML load + backend smoke test
    --screenshot PATH       launch, grab the window and exit
"""

import json
import os
import sys
import tempfile
import traceback

# Works both when launched from source and from the PyInstaller bundle.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtCore import QCoreApplication, QTimer, QUrl
from PySide6.QtGui import QFontDatabase, QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

# Explicit imports so PyInstaller's PySide6 hooks collect the QML runtime
# modules (Qt Quick, Qt Qml, Controls, Layouts, Shapes and Effects).
import PySide6.QtQuick  # noqa: F401
import PySide6.QtQml  # noqa: F401
import PySide6.QtQuickControls2  # noqa: F401

import core
from backend import PuzzleBackend  # noqa: F401  (registers QObject types)
from solver_worker import SolverWorker  # noqa: F401


APP_TITLE = "Puzzle Solver — AI Sliding Puzzle Desktop"


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def _register_offscreen_fonts():
    """Offscreen Qt has no system font database; load Segoe UI for captures.

    This is a no-op in a normal Windows session, where QGuiApplication finds
    the installed fonts by itself.
    """
    if QFontDatabase.families():
        return
    fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    for name in (
        "segoeui.ttf", "segoeuib.ttf", "segoeuii.ttf",
        "seguisb.ttf", "segoeuil.ttf", "segoeuisl.ttf",
    ):
        path = os.path.join(fonts_dir, name)
        if os.path.exists(path):
            QFontDatabase.addApplicationFont(path)


def create_application(argv=None):
    """Build the QGuiApplication, QML engine and Python backend."""
    app = QGuiApplication.instance() or QGuiApplication(argv or sys.argv)
    _register_offscreen_fonts()
    app.setWindowIcon(QIcon(resource_path(os.path.join("assets", "icon.ico"))))

    backend = PuzzleBackend()
    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    context.setContextProperty("backend", backend)
    context.setContextProperty("boardModel", backend.board_model)
    context.setContextProperty("goalModel", backend.goal_model)

    warnings = []

    def collect(items):
        warnings.extend(item.toString() for item in items)

    engine.warnings.connect(collect)
    engine.load(QUrl.fromLocalFile(resource_path(os.path.join("ui", "Main.qml"))))
    if not engine.rootObjects():
        message = "QML failed to load:\n" + "\n".join(warnings)
        raise RuntimeError(message)

    window = engine.rootObjects()[0]
    window.setTitle(APP_TITLE)
    backend.setWindow(window)
    app.aboutToQuit.connect(backend.shutdown)
    return app, engine, window, backend, warnings


def run_selftest():
    """Headless algorithm verification (no window required)."""
    report = {
        "python": sys.version.split()[0],
        "frozen": bool(getattr(sys, "frozen", False)),
        "checks": {},
    }
    try:
        from PySide6.QtCore import qVersion

        report["qt"] = qVersion()
        app = QCoreApplication.instance() or QCoreApplication([])
        report["checks"]["qt_application"] = app is not None

        start = core.create_puzzle(3)
        for _ in range(4):
            start = core.shuffle_puzzle(start)
        results = {}
        for name, solver in core.SOLVERS.items():
            events = list(solver(start, core.create_puzzle(3)))
            last = events[-1]
            reachable = last.get("solution") is not None
            if reachable:
                states = core.solution_states(start, last["solution"])
                reachable = states[-1] == core.create_puzzle(3)
            results[name] = {
                "type": last["type"],
                "checked_nodes": last["checked_nodes"],
                "solution_reaches_goal": reachable,
            }
        report["checks"]["solvers"] = results
        report["checks"]["solvability"] = core.is_solvable(
            core.create_puzzle(3), core.create_puzzle(3)
        )
        report["ok"] = all(
            item["solution_reaches_goal"] for item in results.values()
        )
    except Exception:
        report["ok"] = False
        report["error"] = traceback.format_exc()

    path = os.path.join(tempfile.gettempdir(), "puzzle_solver_selftest.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    return 0 if report["ok"] else 1


def run_smoke_ui():
    """Headless QML + backend check used to validate the frozen executable."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    report = {"frozen": bool(getattr(sys, "frozen", False)), "checks": {}}
    try:
        app, engine, window, backend, warnings = create_application([])
        report["checks"]["qml_loaded"] = True
        report["checks"]["qml_warnings"] = warnings
        report["checks"]["board_tiles"] = backend.board_model.rowCount()
        report["checks"]["goal_tiles"] = backend.goal_model.rowCount()

        backend.setPuzzleSize(4)
        backend.createPuzzle()
        report["checks"]["4x4_board"] = backend.board_model.rowCount()
        report["checks"]["4x4_goal"] = backend.goal_model.rowCount()

        backend.setSetupMode(1)
        report["checks"]["manual_cells"] = len(backend.manualCells)
        backend.setSetupMode(0)

        backend.setShuffleMoves(3)
        backend.shufflePuzzle()
        while backend._shuffling:
            backend._shuffle_step()
        report["checks"]["shuffle_moves"] = backend.manualMoves
        report["checks"]["goal_is_original"] = (
            backend._goal == core.create_puzzle(4)
        )

        backend.solve()
        if backend._worker is not None:
            backend._worker.run()          # drain deterministically
            backend._thread.wait(2000)
        report["checks"]["playback_available"] = backend.playbackAvailable
        report["checks"]["playback_total"] = backend.playbackTotal
        report["checks"]["solved_reaches_goal"] = (
            backend._puzzle == backend._goal
        )
        backend.firstStep()
        backend.lastStep()
        report["checks"]["playback_seek"] = backend.playbackStep

        report["checks"]["no_goal_buttons_in_backend"] = not any(
            hasattr(backend, name)
            for name in ("useCurrentAsGoal", "useCanonicalGoal", "restoreGoal")
        )
        report["ok"] = (
            report["checks"]["board_tiles"] == 16
            and report["checks"]["goal_tiles"] == 16
            and report["checks"]["4x4_board"] == 16
            and report["checks"]["manual_cells"] == 16
            and report["checks"]["shuffle_moves"] == 3
            and report["checks"]["goal_is_original"]
            and report["checks"]["solved_reaches_goal"]
            and report["checks"]["no_goal_buttons_in_backend"]
            and not warnings
        )
        window.close()
    except Exception:
        report["ok"] = False
        report["error"] = traceback.format_exc()

    path = os.path.join(tempfile.gettempdir(), "puzzle_solver_smoke_ui.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    return 0 if report["ok"] else 1


def run_screenshot(argv):
    """Launch, grab the window at a fixed size and exit (visual verification)."""
    path = argv[0]
    width = int(argv[1]) if len(argv) > 1 else 1648
    height = int(argv[2]) if len(argv) > 2 else 900
    app, engine, window, backend, warnings = create_application([])
    window.resize(width, height)
    print(f"Window: {window.width()}x{window.height()}")
    if warnings:
        print("QML warnings:", *warnings, sep="\n  ")

    def grab():
        image = app.primaryScreen().grabWindow(window.winId())
        ok = image.save(path)
        print(f"Screenshot: {path} ok={ok} size={image.width()}x{image.height()}")
        app.quit()

    QTimer.singleShot(900, grab)
    return app.exec()


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return run_selftest()
    if "--smoke-ui" in argv:
        return run_smoke_ui()
    if "--screenshot" in argv:
        index = argv.index("--screenshot")
        return run_screenshot(argv[index + 1:])

    app, engine, window, backend, warnings = create_application(sys.argv)
    if warnings:
        print("QML warnings:", *warnings, sep="\n  ")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
