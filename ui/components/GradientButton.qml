import QtQuick
import ".."

/* Primary action button: horizontal purple gradient, white label + icon. */
Rectangle {
    id: root
    property string label: ""
    property string iconName: ""
    property color gradientFrom: Theme.purple
    property color gradientTo: Theme.purpleLight
    property color labelColor: "#FFFFFF"
    property color iconColor: "#FFFFFF"
    property real fontSize: 14
    property real iconSize: 15
    property real cornerRadius: Theme.controlRadius
    property real contentSpacing: 8
    signal clicked()

    height: Theme.controlHeight
    radius: cornerRadius
    gradient: Gradient {
        orientation: Gradient.Horizontal
        GradientStop { position: 0; color: root.gradientFrom }
        GradientStop { position: 1; color: root.gradientTo }
    }
    opacity: root.enabled ? 1 : 0.5
    scale: (mouse.pressed && root.enabled) ? 0.975 : 1
    Behavior on scale { NumberAnimation { duration: 110; easing.type: Easing.OutQuad } }
    Behavior on opacity { NumberAnimation { duration: 130 } }

    Rectangle {
        anchors.fill: parent
        radius: root.cornerRadius
        color: "#FFFFFF"
        opacity: (mouse.containsMouse && root.enabled) ? 0.12 : 0
        Behavior on opacity { NumberAnimation { duration: 130 } }
    }
    Row {
        anchors.centerIn: parent
        spacing: root.contentSpacing
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
