import QtQuick
import ".."

/* Small purple icon + bold sidebar section heading. */
Row {
    id: root
    property string label: ""
    property string iconName: "sliders"
    property color iconColor: Theme.purple
    property color labelColor: Theme.text
    property real iconSize: 16
    property real fontSize: Theme.sidebarHeading
    spacing: 9
    height: 24

    Icon {
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
