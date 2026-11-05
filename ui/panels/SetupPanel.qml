import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic
import ".."
import "../components"

/* Setup tab: creation mode, size, shuffling, algorithm and solve controls.
   Every control is bound to the Python backend - no local puzzle state. */
ColumnLayout {
    id: root
    spacing: 0
    Layout.fillWidth: true

    // ---------------------------------------------------------- setup mode
    SectionHeader {
        label: "Setup Mode"
        iconName: "play"
        iconColor: Theme.purple
        Layout.topMargin: 2
    }
    CustomDropdown {
        Layout.fillWidth: true
        Layout.topMargin: 11
        options: backend.setupModes
        currentIndex: backend.setupModeIndex
        enabled: !backend.busy
        onOptionSelected: function(index) { backend.setSetupMode(index) }
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "Choose how to set up your puzzle"
        color: Theme.textMuted
        font.pixelSize: Theme.smallSize
        font.family: Theme.fontFamily
    }

    // Manual mode: enter every tile exactly once; blank cell stays empty.
    ColumnLayout {
        visible: backend.setupModeIndex === 1
        Layout.fillWidth: true
        Layout.topMargin: 12
        spacing: 8
        Text {
            Layout.fillWidth: true
            text: "Enter 1 - " + (backend.puzzleSize * backend.puzzleSize - 1)
                  + " once each. Leave one cell empty for the blank."
            color: Theme.textMuted
            font.pixelSize: Theme.tinySize
            font.family: Theme.fontFamily
            wrapMode: Text.Wrap
        }
        Grid {
            id: manualGrid
            columns: Math.max(1, backend.puzzleSize)
            spacing: 4
            Layout.fillWidth: true
            Layout.preferredHeight: backend.puzzleSize * 30
                                    + (backend.puzzleSize - 1) * 4
            Repeater {
                model: backend.puzzleSize * backend.puzzleSize
                Rectangle {
                    width: Math.min(44, (root.width
                                        - (backend.puzzleSize - 1) * 4)
                                        / Math.max(1, backend.puzzleSize))
                    height: 30
                    radius: 6
                    color: "#FFFFFF"
                    border.color: Theme.border
                    border.width: 1
                    TextInput {
                        anchors.fill: parent
                        anchors.margins: 3
                        horizontalAlignment: TextInput.AlignHCenter
                        verticalAlignment: TextInput.AlignVCenter
                        color: Theme.text
                        font.pixelSize: 12
                        font.family: Theme.fontFamily
                        text: backend.manualCells[index] || ""
                        validator: IntValidator {
                            bottom: 1
                            top: Math.max(1, backend.puzzleSize * backend.puzzleSize - 1)
                        }
                        onEditingFinished: backend.setManualCell(index, text)
                    }
                }
            }
        }
        SecondaryButton {
            Layout.fillWidth: true
            height: 32
            label: "Clear cells"
            iconName: "refresh"
            fontSize: 12
            enabled: !backend.busy
            onClicked: backend.clearManualCells()
        }
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    // ---------------------------------------------------------- puzzle size
    SectionHeader {
        label: "Puzzle Size (2 - 10)"
        iconName: "shuffle"
    }
    Item {
        Layout.fillWidth: true
        Layout.topMargin: 10
        Layout.preferredHeight: Theme.controlHeight
        NumericInput {
            x: 0
            width: parent.width * 0.44
            value: backend.puzzleSize
            minValue: 2
            maxValue: 10
            enabled: !backend.busy
            onValueEdited: function(v) { backend.setPuzzleSize(v) }
        }
        GradientButton {
            x: parent.width * 0.47
            width: parent.width * 0.53
            label: "Create Puzzle"
            iconName: "sparkles"
            iconSize: 14
            fontSize: 13
            enabled: !backend.busy
            onClicked: backend.createPuzzle()
        }
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    // ------------------------------------------------------------- shuffle
    SectionHeader {
        label: "Shuffle"
        iconName: "shuffle"
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "Number of random legal moves"
        color: Theme.textMuted
        font.pixelSize: Theme.smallSize
        font.family: Theme.fontFamily
    }
    NumericInput {
        Layout.fillWidth: true
        Layout.topMargin: 9
        value: backend.shuffleMoves
        minValue: 1
        maxValue: 2000
        enabled: !backend.busy
        onValueEdited: function(v) { backend.setShuffleMoves(v) }
    }
    SecondaryButton {
        Layout.fillWidth: true
        Layout.topMargin: 10
        label: "Shuffle Puzzle"
        iconName: "shuffle"
        fillColor: Theme.lavender
        labelColor: Theme.purple
        iconColor: Theme.purple
        showBorder: false
        enabled: !backend.busy
        onClicked: backend.shufflePuzzle()
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    // --------------------------------------------------- solving algorithm
    SectionHeader {
        label: "Solving Algorithm"
        iconName: "pencil"
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "Select Algorithm"
        color: Theme.textMuted
        font.pixelSize: Theme.smallSize
        font.family: Theme.fontFamily
    }
    CustomDropdown {
        Layout.fillWidth: true
        Layout.topMargin: 7
        options: backend.algorithms
        currentIndex: backend.algorithmIndex
        enabled: !backend.busy
        onOptionSelected: function(index) { backend.setAlgorithmIndex(index) }
    }

    Row {
        Layout.fillWidth: true
        Layout.topMargin: 13
        Layout.preferredHeight: 24
        spacing: 9
        ToggleSwitch {
            checked: backend.liveVisualization
            enabled: !backend.busy
            anchors.verticalCenter: parent.verticalCenter
            onToggled: function(v) { backend.setLiveVisualization(v) }
        }
        Text {
            text: "Live search visualization"
            color: Theme.text
            font.pixelSize: 13
            font.family: Theme.fontFamily
            anchors.verticalCenter: parent.verticalCenter
        }
        Item {
            width: 17; height: 17
            anchors.verticalCenter: parent.verticalCenter
            Icon {
                anchors.centerIn: parent
                name: "help"
                width: 15; height: 15
                color: Theme.textFaint
            }
            MouseArea {
                id: helpArea
                anchors.fill: parent
                hoverEnabled: true
            }
            ToolTip.visible: helpArea.containsMouse
            ToolTip.text: "Turn off for large boards: only the node counter is updated."
            ToolTip.delay: 250
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.topMargin: 10
        Layout.preferredHeight: 18
        Text {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            text: "Animation delay"
            color: Theme.textMuted
            font.pixelSize: Theme.smallSize
            font.family: Theme.fontFamily
        }
        Text {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            text: backend.animationDelay + " ms"
            color: Theme.text
            font.pixelSize: Theme.smallSize
            font.family: Theme.fontFamily
        }
    }
    CustomSlider {
        Layout.fillWidth: true
        Layout.topMargin: 2
        from: 10
        to: 400
        value: backend.animationDelay
        enabled: !backend.busy
        onValueEdited: function(v) { backend.setAnimationDelay(v) }
    }

    Item {
        Layout.fillWidth: true
        Layout.topMargin: 8
        Layout.preferredHeight: 36
        Text {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            text: "Node limit"
            color: Theme.textMuted
            font.pixelSize: Theme.smallSize
            font.family: Theme.fontFamily
        }
        NumericInput {
            anchors.right: parent.right
            width: parent.width * 0.62
            height: 36
            mode: "spin"
            fontSize: 13
            value: backend.nodeLimit
            minValue: 1000
            maxValue: 5000000
            step: 50000
            enabled: !backend.busy
            onValueEdited: function(v) { backend.setNodeLimit(v) }
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.topMargin: 12
        Layout.preferredHeight: Theme.controlHeight
        GradientButton {
            x: 0
            width: parent.width * 0.62
            label: "Solve Puzzle"
            iconName: "play"
            iconSize: 13
            enabled: !backend.busy
            onClicked: backend.solve()
        }
        SecondaryButton {
            x: parent.width * 0.66
            width: parent.width * 0.34
            label: "Stop"
            iconName: "stop"
            iconSize: 12
            fillColor: Theme.stopBg
            borderColor: Theme.stopBg
            labelColor: Theme.stopText
            iconColor: Theme.stopText
            showBorder: false
            enabled: backend.stopEnabled
            onClicked: backend.stopSolve()
        }
    }

    Row {
        Layout.fillWidth: true
        Layout.topMargin: 14
        Layout.bottomMargin: 4
        spacing: 7
        Icon {
            name: "bulb"
            width: 14; height: 14
            color: Theme.yellow
        }
        Text {
            width: parent.width - 21
            text: "Tip: Click a tile next to the blank (or use the arrow keys)."
            color: Theme.textMuted
            font.pixelSize: 12
            font.family: Theme.fontFamily
            wrapMode: Text.Wrap
        }
    }
}
