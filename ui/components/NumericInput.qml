import QtQuick
import ".."

/* Numeric field with integrated decrease / increase controls.
   mode "stepper" shows - and + (puzzle size, shuffle moves);
   mode "spin" shows stacked chevrons (node limit). */
Item {
    id: root
    property int value: 0
    property int minValue: 0
    property int maxValue: 999999
    property int step: 1
    property string mode: "stepper"
    property color fillColor: "#FFFFFF"
    property color borderColor: Theme.border
    property color textColor: Theme.text
    property color controlColor: Theme.text
    property real fontSize: 15
    property real horizontalPadding: 14
    signal valueEdited(int newValue)

    height: Theme.controlHeight

    function commit(v) {
        root.valueEdited(Math.max(root.minValue, Math.min(root.maxValue, v)));
    }
    function syncText() {
        if (!input.activeFocus)
            input.text = String(root.value);
    }

    onValueChanged: syncText()
    Component.onCompleted: syncText()

    Rectangle {
        anchors.fill: parent
        radius: Theme.controlRadius
        color: root.fillColor
        border.color: root.borderColor
        border.width: 1
    }

    TextInput {
        id: input
        anchors.left: parent.left
        anchors.leftMargin: root.horizontalPadding
        anchors.verticalCenter: parent.verticalCenter
        width: Math.max(20, parent.width - controls.width
                            - root.horizontalPadding * 2 - 6)
        color: root.textColor
        font.pixelSize: root.fontSize
        font.family: Theme.fontFamily
        font.bold: root.mode === "stepper"
        validator: IntValidator { bottom: root.minValue; top: root.maxValue }
        selectByMouse: true
        onEditingFinished: {
            var n = parseInt(input.text, 10);
            if (isNaN(n)) {
                root.syncText();
                return;
            }
            root.commit(n);
            input.text = String(Math.max(root.minValue,
                                         Math.min(root.maxValue, n)));
        }
    }

    Row {
        id: controls
        anchors.right: parent.right
        anchors.rightMargin: 9
        anchors.verticalCenter: parent.verticalCenter
        spacing: 4

        Row {
            visible: root.mode === "stepper"
            spacing: 6
            Repeater {
                model: ["minus", "plus"]
                Item {
                    width: 24; height: 30
                    Icon {
                        anchors.centerIn: parent
                        name: modelData
                        width: 15; height: 15
                        color: root.controlColor
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.commit(root.value
                                               + (modelData === "plus"
                                                  ? root.step : -root.step))
                    }
                }
            }
        }

        Column {
            visible: root.mode === "spin"
            spacing: 0
            Repeater {
                model: ["chevronUp", "chevronDown"]
                Item {
                    width: 20; height: 15
                    Icon {
                        anchors.centerIn: parent
                        name: modelData
                        width: 12; height: 12
                        color: Theme.textMuted
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.commit(root.value
                                               + (modelData === "chevronUp"
                                                  ? root.step : -root.step))
                    }
                }
            }
        }
    }
}
