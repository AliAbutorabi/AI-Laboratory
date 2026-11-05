import QtQuick
import ".."

/* Light-lavender informational strip with a leading icon.  Content scrolls
   when the solution sequence is long instead of growing the window. */
Rectangle {
    id: root
    property string text: ""
    property string iconName: "info"
    property color iconColor: Theme.purple
    property color textColor: Theme.textMuted
    property real fontSize: 12
    property real padding: 10

    radius: 12
    color: "#F1F3FF"
    border.color: "#E3E7FF"
    border.width: 1

    Flickable {
        id: flick
        anchors.fill: parent
        anchors.margins: root.padding
        clip: true
        contentWidth: width
        contentHeight: rowItem.height
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height
        Row {
            id: rowItem
            width: flick.width
            spacing: 9
            Icon {
                name: root.iconName
                width: 15; height: 15
                color: root.iconColor
            }
            Text {
                width: rowItem.width - 24
                text: root.text
                color: root.textColor
                font.pixelSize: root.fontSize
                font.family: Theme.fontFamily
                wrapMode: Text.Wrap
                lineHeight: 1.25
            }
        }
    }
}
