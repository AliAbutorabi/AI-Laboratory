import QtQuick
import ".."

/* Read-only compact rendering of the real goal-state model. */
Item {
    id: root
    property int gridSize: backend.boardSize

    readonly property real boardPx: Math.min(root.width, root.height)
    readonly property real gap:
        Math.max(2, root.boardPx / Math.max(root.gridSize, 1) * 0.10)
    readonly property real cell:
        (root.boardPx - (root.gridSize - 1) * root.gap)
        / Math.max(root.gridSize, 1)

    Repeater {
        model: goalModel
        PuzzleTile {
            width: root.cell
            height: root.cell
            x: model.cellColumn * (root.cell + root.gap)
            y: model.cellRow * (root.cell + root.gap)
            number: model.number
            isBlank: model.blank
            correct: false
            goalStyle: true
            fontPixelSize: Math.max(8, root.cell * 0.34)
            tileRadius: Math.max(3, root.cell * 0.15)
            animateMove: false
            interactive: false
        }
    }
}
