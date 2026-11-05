import QtQuick
import ".."

/* Circular icon-only control used by the playback bar and card headers. */
Item {
    id: root
    property string iconName: "play"
    property real diameter: 44
    property real iconSize: 17
    property color fillColor: Theme.panel
    property color borderColor: "#E1E5FA"
    property color iconColor: Theme.text
    property color hoverColor: "#FFFFFF"
    property bool emphasized: false
    signal clicked()

    width: diameter
    height: diameter
    opacity: root.enabled ? 1 : 0.42
    scale: (mouse.pressed && root.enabled) ? 0.94 : 1
    Behavior on scale { NumberAnimation { duration: 110; easing.type: Easing.OutQuad } }

    Rectangle {
        anchors.fill: parent
        radius: root.diameter / 2
        color: root.fillColor
        border.color: root.borderColor
        border.width: 1
    }
    Rectangle {
        anchors.fill: parent
        radius: root.diameter / 2
        color: root.hoverColor
        opacity: (mouse.containsMouse && root.enabled) ? 0.6 : 0
        Behavior on opacity { NumberAnimation { duration: 120 } }
    }
    Icon {
        anchors.centerIn: parent
        name: root.iconName
        width: root.iconSize; height: root.iconSize
        color: root.iconColor
    }
    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: root.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (root.enabled) root.clicked()
    }
}
