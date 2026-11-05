import QtQuick
import ".."
import "../components"

/* Large white current-puzzle card with the interactive square board. */
GlassCard {
    id: root

    Row {
        x: 20
        y: 17
        spacing: 10
        Logo {
            width: 19; height: 19
            gap: 1.5
            corner: 2
            shade1: "#6E5BF8"
            shade2: "#5B47EE"
            shade4: "#3E2BCE"
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: "Current Puzzle"
            color: Theme.text
            font.pixelSize: 18
            font.bold: true
            font.family: Theme.fontFamily
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    RoundIconButton {
        anchors.right: parent.right
        anchors.rightMargin: 16
        y: 13
        diameter: 28
        iconSize: 14
        iconName: "expand"
        iconColor: Theme.purple
        fillColor: "#F1F3FF"
        onClicked: backend.toggleBoardExpanded()
    }

    Item {
        x: 18
        y: 58
        width: root.width - 36
        height: Math.max(80, root.height - 58 - 16)
        PuzzleBoard {
            anchors.centerIn: parent
            width: Math.min(parent.width, parent.height)
            height: width
            interactive: !backend.busy
            animate: !backend.busy
        }
    }
}
