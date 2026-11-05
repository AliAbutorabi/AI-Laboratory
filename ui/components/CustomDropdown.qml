import QtQuick
import QtQuick.Controls.Basic as Controls
import ".."

/* Light-lavender dropdown with a custom overlay list.  The popup is parented
   to this item (so it follows the field) but is drawn in the window overlay,
   which means it is never clipped by the sidebar's scroll area. */
Item {
    id: root
    property var options: []
    property int currentIndex: 0
    property string placeholder: ""
    property color fillColor: Theme.inputBg
    property color borderColor: Theme.border
    property color textColor: Theme.text
    property real fontSize: 14
    property real rowHeight: 36
    signal optionSelected(int index)

    height: Theme.controlHeight
    readonly property real listHeight:
        Math.min(Math.max(root.options.length, 1), 6) * root.rowHeight + 8

    Rectangle {
        id: field
        anchors.fill: parent
        radius: Theme.controlRadius
        color: root.fillColor
        border.color: root.borderColor
        border.width: 1
        Text {
            anchors.left: parent.left
            anchors.leftMargin: 14
            anchors.right: parent.right
            anchors.rightMargin: 38
            anchors.verticalCenter: parent.verticalCenter
            elide: Text.ElideRight
            text: (root.options.length > root.currentIndex
                   && root.currentIndex >= 0)
                  ? root.options[root.currentIndex] : root.placeholder
            color: root.textColor
            font.pixelSize: root.fontSize
            font.family: Theme.fontFamily
        }
        Icon {
            anchors.right: parent.right
            anchors.rightMargin: 13
            anchors.verticalCenter: parent.verticalCenter
            name: "chevronDown"
            width: 16; height: 16
            color: Theme.text
        }
        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: popup.opened ? popup.close() : popup.open()
        }
    }

    Controls.Popup {
        id: popup
        parent: root
        x: 0
        y: root.height + 4
        width: root.width
        height: root.listHeight
        padding: 4
        modal: false
        dim: false
        background: Rectangle {
            radius: 12
            color: "#FFFFFF"
            border.color: Theme.border
            border.width: 1
        }
        contentItem: ListView {
            clip: true
            model: root.options
            delegate: Rectangle {
                width: ListView.view.width
                height: root.rowHeight
                radius: 8
                color: index === root.currentIndex
                       ? "#EEE9FF"
                       : (hover.containsMouse ? "#F5F3FF" : "transparent")
                Text {
                    x: 10
                    anchors.verticalCenter: parent.verticalCenter
                    text: modelData
                    color: index === root.currentIndex
                           ? Theme.purple : Theme.text
                    font.pixelSize: 13
                    font.family: Theme.fontFamily
                }
                MouseArea {
                    id: hover
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        root.optionSelected(index);
                        popup.close();
                    }
                }
            }
        }
    }
}
