"""Build the standalone executable for the lightweight edition.

Everything generated stays INSIDE this project directory (never one level up):

    <project>/build/              PyInstaller work files
    <project>/dist/               PuzzleSolver.exe
    <project>/PuzzleSolver.spec   generated spec

Usage::

    .venv\\Scripts\\python.exe build.py
"""
import os
import sys
from pathlib import Path

# Resolve from this file, so running the script from any working directory
# still produces build/dist next to it, not in the parent folder.
PROJECT = Path(__file__).resolve().parent
BUILD_DIR = PROJECT / "build"
DIST_DIR = PROJECT / "dist"
EXE = DIST_DIR / "PuzzleSolver.exe"
MAX_EXE_SIZE = 20 * 1024 * 1024


def retire_existing_exe():
    """Keep the old binary as a rollback copy instead of deleting it."""
    if not EXE.exists():
        return None
    previous = EXE.with_suffix(".exe.previous")
    os.replace(EXE, previous)
    return previous


def main():
    try:
        import PyInstaller.__main__ as pyinstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is missing. Run: python -m pip install pyinstaller")
        return 1

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    args = [
        str(PROJECT / "main.py"),
        "--name=PuzzleSolver",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--paths={PROJECT}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={PROJECT}",
        "--exclude-module=django",
        "--exclude-module=numpy",
        "--exclude-module=PIL",
        "--exclude-module=matplotlib",
        "--exclude-module=PySide6",
        "--exclude-module=pytest",
        "--log-level=WARN",
    ]

    previous = retire_existing_exe()
    print(f"Project : {PROJECT}")
    print(f"Work dir: {BUILD_DIR}")
    print(f"Output  : {EXE}")

    try:
        pyinstaller.run(args)
    except Exception as exc:
        if previous is not None and previous.exists() and not EXE.exists():
            os.replace(previous, EXE)
        print(f"Build failed: {type(exc).__name__}: {exc}")
        return 1

    if EXE.exists():
        size = EXE.stat().st_size
        if size >= MAX_EXE_SIZE:
            EXE.unlink()
            if previous is not None and previous.exists():
                os.replace(previous, EXE)
            print(
                f"Build failed: executable is {size / 1024 / 1024:.1f} MiB; "
                "the maximum is under 20 MiB."
            )
            return 1
        print(f"OK: {EXE} ({size / 1024 / 1024:.1f} MiB)")
        return 0
    if previous is not None and previous.exists():
        os.replace(previous, EXE)
    print("Build finished but the executable was not found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
