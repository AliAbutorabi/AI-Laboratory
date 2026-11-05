import QtQuick
import ".."

/* The 2x2 blue application symbol (or a small white 3x3 title-bar mark). */
Item {
    id: root
    property int gridSize: 2
    property real gap: 3
    property real corner: 3
    property bool white: false
    property color shade1: "#3D8CFF"
    property color shade2: "#2C79F0"
    property color shade3: "#1B5FE0"
    property color shade4: "#1250CE"

    width: 36
    height: 36

    Grid {
        anchors.fill: parent
        columns: root.gridSize
        spacing: root.gap
        Repeater {
            model: root.gridSize * root.gridSize
            Rectangle {
                width: (root.width - (root.gridSize - 1) * root.gap) / root.gridSize
                height: (root.height - (root.gridSize - 1) * root.gap) / root.gridSize
                radius: root.corner
                color: root.white
                       ? "#FFFFFF"
                       : (index === 0 ? root.shade1
                          : index === root.gridSize * root.gridSize - 1
                            ? root.shade4 : root.shade2)
            }
        }
    }
}
