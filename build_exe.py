"""Build the standalone Windows executable.

Usage (from anywhere)::

    python desktop/build_exe.py

With the project virtual environment (recommended)::

    .\\.venv\\Scripts\\python.exe build_exe.py

Output: ``dist/PuzzleSolver.exe`` (single file, no console window).
Requires: PySide6, PyInstaller, Pillow (see requirements.txt;
Pillow is only used to draw the icon).

An existing exe is renamed to ``dist/PuzzleSolver.exe.previous`` before the
build (a rollback copy) rather than deleted, because some managed shells
refuse PyInstaller's ``os.remove`` of the old binary. If the build fails the
previous exe is restored automatically.
"""

import os
import sys
from pathlib import Path


def retire_existing_exe(exe):
    """Move the previous binary aside without deleting it.

    PyInstaller calls ``os.remove()`` on an existing output exe. Some managed
    shells intercept that delete operation, so a rename is used instead. The
    old binary is kept as a rollback copy next to the new one.
    """
    if not exe.exists():
        return None
    previous = exe.with_suffix(".exe.previous")
    os.replace(exe, previous)
    return previous

DESKTOP = Path(__file__).resolve().parent
ROOT = DESKTOP.parent
ASSETS = DESKTOP / "assets"
ICON = ASSETS / "icon.ico"


def make_icon():
    """Draw a small 3x3 sliding-puzzle icon (used for the exe and window)."""
    from PIL import Image, ImageDraw, ImageFont

    ASSETS.mkdir(parents=True, exist_ok=True)
    scale = 4
    canvas = 256 * scale
    image = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    pad = 22 * scale
    gap = 10 * scale
    cell = (canvas - 2 * pad - 2 * gap) // 3
    radius = 14 * scale
    try:
        font = ImageFont.truetype("segoeuib.ttf", 52 * scale)
    except OSError:
        font = ImageFont.load_default()

    for index in range(9):
        row, column = divmod(index, 3)
        x0 = pad + column * (cell + gap)
        y0 = pad + row * (cell + gap)
        x1, y1 = x0 + cell, y0 + cell
        blank = index == 8
        if blank:
            draw.rounded_rectangle(
                (x0, y0, x1, y1),
                radius=radius,
                fill=(226, 232, 240, 255),
                outline=(148, 163, 184, 255),
                width=2 * scale,
            )
            # A little arrow hinting at the tile that slides into the blank.
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            arrow = 20 * scale
            draw.line(
                (cx - arrow, cy, cx + arrow, cy),
                fill=(37, 99, 235, 255),
                width=7 * scale,
            )
            draw.line(
                (cx + arrow, cy, cx + arrow - 12 * scale, cy - 12 * scale),
                fill=(37, 99, 235, 255),
                width=7 * scale,
            )
            draw.line(
                (cx + arrow, cy, cx + arrow - 12 * scale, cy + 12 * scale),
                fill=(37, 99, 235, 255),
                width=7 * scale,
            )
        else:
            draw.rounded_rectangle(
                (x0, y0, x1, y1),
                radius=radius,
                fill=(37, 99, 235, 255),
                outline=(29, 78, 216, 255),
                width=2 * scale,
            )
            text = str(index + 1)
            box = draw.textbbox((0, 0), text, font=font)
            tw, th = box[2] - box[0], box[3] - box[1]
            draw.text(
                ((x0 + x1 - tw) // 2 - box[0], (y0 + y1 - th) // 2 - box[1]),
                text,
                font=font,
                fill=(255, 255, 255, 255),
            )

    image = image.resize((256, 256), Image.LANCZOS)
    image.save(
        ICON,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )
    return ICON


def main():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is missing. Run: python -m pip install pyinstaller")
        return 1

    UI = DESKTOP / "ui"
    icon = make_icon()
    print(f"Icon: {icon}")

    import PyInstaller.__main__ as pyinstaller

    args = [
        str(DESKTOP / "main.py"),
        "--name=PuzzleSolver",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--icon={icon}",
        f"--add-data={icon}{os.pathsep}assets",
        # Qt Quick reads these at runtime; they must ship next to the exe.
        f"--add-data={UI}{os.pathsep}ui",
        f"--paths={DESKTOP}",
        # main.py imports QtQuick / QtQml / QtQuickControls2 explicitly so
        # PyInstaller's PySide6 hooks collect the QML runtime modules.
        f"--distpath={ROOT / 'dist'}",
        f"--workpath={ROOT / 'build'}",
        f"--specpath={DESKTOP}",
        "--exclude-module=django",
        "--exclude-module=numpy",
        "--exclude-module=PIL",
        "--exclude-module=tkinter",
        "--exclude-module=matplotlib",
        "--exclude-module=pytest",
        "--log-level=INFO",
    ]
    exe = ROOT / "dist" / "PuzzleSolver.exe"
    previous = retire_existing_exe(exe)
    if previous is not None:
        print(f"Previous exe kept as rollback: {previous}")

    print("Building dist/PuzzleSolver.exe ...")
    try:
        pyinstaller.run(args)
    except Exception as exc:
        if not exe.exists() and previous is not None and previous.exists():
            os.replace(previous, exe)
            print("Restored the previous exe.")
        print(f"Build failed: {type(exc).__name__}: {exc}")
        return 1

    if exe.exists():
        print(f"OK: {exe} ({exe.stat().st_size / 1024 / 1024:.1f} MiB)")
        return 0
    if previous is not None and previous.exists():
        os.replace(previous, exe)
        print("Restored the previous exe.")
    print("Build finished but the executable was not found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
