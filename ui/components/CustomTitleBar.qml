import QtQuick
import ".."

/* Compact dark-navy frameless title bar with working window controls. */
Rectangle {
    id: root
    height: 32
    color: Theme.titleBar

    MouseArea {
        anchors.fill: parent
        onPressed: backend.startWindowMove()
        onDoubleClicked: backend.toggleMaximize()
    }

    Logo {
        x: 13; y: 9.5
        width: 13; height: 13
        gridSize: 3
        gap: 1.5
        corner: 1
        white: true
    }
    Text {
        x: 35
        anchors.verticalCenter: parent.verticalCenter
        text: "Puzzle Solver — AI Sliding Puzzle Desktop"
        color: Theme.textOnDark
        font.pixelSize: 12
        font.family: Theme.fontFamily
    }

    Row {
        anchors.right: parent.right
        anchors.rightMargin: 2
        height: parent.height
        Repeater {
            model: 3
            Item {
                width: 40
                height: 32
                readonly property string glyph:
                    index === 0 ? "minimize"
                    : (index === 1 ? (backend.windowMaximized
                                      ? "restore" : "maximize") : "close")
                Rectangle {
                    anchors.fill: parent
                    color: hover.containsMouse
                           ? (index === 2 ? "#D82436" : "#33FFFFFF")
                           : "transparent"
                }
                Icon {
                    anchors.centerIn: parent
                    name: glyph
                    width: 13; height: 13
                    color: "#E8ECFF"
                }
                MouseArea {
                    id: hover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (index === 0) backend.minimizeWindow();
                        else if (index === 1) backend.toggleMaximize();
                        else backend.closeWindow();
                    }
                }
            }
        }
    }
}
