import QtQuick
import ".."

/* Flat / light action button used for shuffle, stop, playback row, dialogs. */
Rectangle {
    id: root
    property string label: ""
    property string iconName: ""
    property color fillColor: Theme.lavenderSoft
    property color borderColor: Theme.border
    property color labelColor: Theme.text
    property color iconColor: Theme.purple
    property real fontSize: 13
    property real iconSize: 15
    property real cornerRadius: Theme.controlRadius
    property bool showBorder: true
    signal clicked()

    height: Theme.controlHeight
    radius: cornerRadius
    color: root.enabled ? root.fillColor : Theme.disabled
    border.color: root.showBorder ? root.borderColor : "transparent"
    border.width: root.showBorder ? 1 : 0
    opacity: root.enabled ? 1 : 0.55
    scale: (mouse.pressed && root.enabled) ? 0.98 : 1
    Behavior on scale { NumberAnimation { duration: 110; easing.type: Easing.OutQuad } }
    Behavior on opacity { NumberAnimation { duration: 130 } }

    Rectangle {
        anchors.fill: parent
        radius: root.cornerRadius
        color: "#FFFFFF"
        opacity: (mouse.containsMouse && root.enabled) ? 0.35 : 0
        Behavior on opacity { NumberAnimation { duration: 130 } }
    }
    Row {
        anchors.centerIn: parent
        spacing: 8
        Icon {
            visible: root.iconName !== ""
            name: root.iconName
            width: root.iconSize; height: root.iconSize
            color: root.iconColor
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: root.label
            color: root.labelColor
            font.pixelSize: root.fontSize
            font.bold: true
            font.family: Theme.fontFamily
            anchors.verticalCenter: parent.verticalCenter
        }
    }
    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: root.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: if (root.enabled) root.clicked()
    }
}
