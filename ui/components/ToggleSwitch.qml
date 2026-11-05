import QtQuick
import ".."

Item {
    id: root
    property bool checked: true
    signal toggled(bool newValue)

    width: 40
    height: 22
    opacity: root.enabled ? 1 : 0.5

    Rectangle {
        anchors.fill: parent
        radius: root.height / 2
        color: root.checked ? Theme.purple : "#C9D0EC"
        Behavior on color { ColorAnimation { duration: 160 } }
    }
    Rectangle {
        id: knob
        width: 16; height: 16
        radius: 8
        color: "#FFFFFF"
        y: 3
        x: root.checked ? 21 : 3
        Behavior on x {
            NumberAnimation { duration: 160; easing.type: Easing.OutCubic }
        }
    }
    MouseArea {
        anchors.fill: parent
        cursorShape: root.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (root.enabled) root.toggled(!root.checked)
    }
}
