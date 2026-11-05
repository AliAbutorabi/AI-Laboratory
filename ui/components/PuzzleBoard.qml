import QtQuick
import ".."

/* Interactive N x N board driven by the per-tile Python list model.
   Tile size and spacing are derived from the available square, so every
   supported size (2..10) keeps a perfectly square, evenly spaced grid. */
Item {
    id: root
    property int gridSize: backend.boardSize
    property bool interactive: true
    property bool animate: true

    readonly property real boardPx: Math.min(root.width, root.height)
    readonly property real gap:
        Math.max(2, root.boardPx / Math.max(root.gridSize, 1) * 0.11)
    readonly property real cell:
        (root.boardPx - (root.gridSize - 1) * root.gap)
        / Math.max(root.gridSize, 1)

    Repeater {
        model: boardModel
        PuzzleTile {
            width: root.cell
            height: root.cell
            x: model.tileColumn * (root.cell + root.gap)
            y: model.tileRow * (root.cell + root.gap)
            number: model.number
            isBlank: model.blank
            correct: model.correct
            fontPixelSize: Math.max(9, root.cell * 0.30)
            tileRadius: Math.max(4, root.cell * 0.13)
            animateMove: root.animate
            interactive: root.interactive
            onClicked: if (root.interactive)
                           backend.moveTile(model.tileRow, model.tileColumn)
        }
    }
}
