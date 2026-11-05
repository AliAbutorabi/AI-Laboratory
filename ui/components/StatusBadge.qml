import QtQuick
import ".."

/* Green "Solvable" pill (or red "Unsolvable"). */
Rectangle {
    id: root
    property bool okay: true
    property string label: ""
    property real fontSize: 12
    width: row.width + 22
    height: 28
    radius: 14
    color: root.okay ? Theme.successBg : Theme.dangerBg

    Row {
        id: row
        anchors.centerIn: parent
        spacing: 5
        Icon {
            name: root.okay ? "check" : "x"
            width: 13; height: 13
            color: root.okay ? Theme.successText : Theme.dangerText
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: root.label.length ? root.label
                                    : (root.okay ? "Solvable" : "Unsolvable")
            color: root.okay ? Theme.successText : Theme.dangerText
            font.pixelSize: root.fontSize
            font.bold: true
            font.family: Theme.fontFamily
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
