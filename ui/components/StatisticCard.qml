import QtQuick
import ".."

/* Compact header statistic card with a purple glyph and a live value. */
GlassCard {
    id: root
    property string label: ""
    property string value: "0"
    property string iconName: "network"

    cardRadius: 16
    borderColor: "#E5E9FF"
    shadowStrength: 0.07
    width: 146
    height: 72

    Row {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 10
        Icon {
            name: root.iconName
            width: 21; height: 21
            color: Theme.purple
            anchors.verticalCenter: parent.verticalCenter
        }
        Column {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 1
            Text {
                text: root.label
                color: Theme.textMuted
                font.pixelSize: 11
                font.family: Theme.fontFamily
            }
            Text {
                text: root.value
                color: Theme.text
                font.pixelSize: 19
                font.bold: true
                font.family: Theme.fontFamily
            }
        }
    }
}
