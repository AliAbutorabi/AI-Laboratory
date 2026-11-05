import QtQuick
import ".."

/* Modal alert / confirmation used for validation errors, solver errors and
   the "unsolvable - run anyway?" confirmation. */
Item {
    id: root
    property string title: "Notice"
    property string message: ""
    property bool confirmMode: false
    property string acceptLabel: "Run anyway"
    signal accepted()
    signal dismissed()

    Rectangle {
        anchors.fill: parent
        color: "#66111A4B"
    }
    MouseArea {
        anchors.fill: parent
        onClicked: root.dismissed()
    }

    GlassCard {
        width: Math.min(450, root.width - 60)
        height: 196
        anchors.centerIn: parent
        MouseArea { anchors.fill: parent }   // clicks stay inside the card

        Column {
            anchors.fill: parent
            anchors.margins: 22
            spacing: 12
            Row {
                spacing: 10
                Icon {
                    name: root.confirmMode ? "alert" : "info"
                    width: 20; height: 20
                    color: root.confirmMode ? Theme.dangerText : Theme.purple
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    text: root.title
                    color: Theme.text
                    font.pixelSize: 17
                    font.bold: true
                    font.family: Theme.fontFamily
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
            Text {
                width: parent.width
                text: root.message
                color: Theme.textMuted
                font.pixelSize: 13
                font.family: Theme.fontFamily
                wrapMode: Text.Wrap
                lineHeight: 1.35
            }
        }

        Row {
            anchors.right: parent.right
            anchors.rightMargin: 22
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 18
            spacing: 10
            SecondaryButton {
                width: 96; height: 38
                label: "Cancel"
                visible: root.confirmMode
                onClicked: root.dismissed()
            }
            GradientButton {
                width: root.confirmMode ? 128 : 88
                height: 38
                label: root.confirmMode ? root.acceptLabel : "OK"
                onClicked: root.confirmMode ? root.accepted() : root.dismissed()
            }
        }
    }
}
