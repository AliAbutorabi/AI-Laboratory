import QtQuick
import QtQuick.Layouts
import ".."
import "../components"

/* Settings tab.  It edits exactly the same backend state as the Setup tab,
   so switching tabs never desynchronises the two views. */
ColumnLayout {
    id: root
    spacing: 0
    Layout.fillWidth: true

    SectionHeader {
        label: "Preferences"
        iconName: "sliders"
        Layout.topMargin: 2
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "Tune how the search runs. These settings are shared with the Setup tab."
        color: Theme.textMuted
        font.pixelSize: Theme.smallSize
        font.family: Theme.fontFamily
        wrapMode: Text.Wrap
    }
    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    Text {
        text: "Default algorithm"
        color: Theme.text
        font.pixelSize: 13
        font.bold: true
        font.family: Theme.fontFamily
    }
    CustomDropdown {
        Layout.fillWidth: true
        Layout.topMargin: 9
        options: backend.algorithms
        currentIndex: backend.algorithmIndex
        enabled: !backend.busy
        onOptionSelected: function(index) { backend.setAlgorithmIndex(index) }
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "A* is recommended for boards 4 x 4 and larger."
        color: Theme.textFaint
        font.pixelSize: Theme.tinySize
        font.family: Theme.fontFamily
        wrapMode: Text.Wrap
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    Row {
        Layout.fillWidth: true
        Layout.preferredHeight: 26
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
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 4
        text: "Stream explored states to the board while solving."
        color: Theme.textFaint
        font.pixelSize: Theme.tinySize
        font.family: Theme.fontFamily
        wrapMode: Text.Wrap
    }

    Item {
        Layout.fillWidth: true
        Layout.topMargin: 16
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

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    Text {
        text: "Node limit"
        color: Theme.text
        font.pixelSize: 13
        font.bold: true
        font.family: Theme.fontFamily
    }
    NumericInput {
        Layout.fillWidth: true
        Layout.topMargin: 9
        mode: "spin"
        value: backend.nodeLimit
        minValue: 1000
        maxValue: 5000000
        step: 50000
        enabled: !backend.busy
        onValueEdited: function(v) { backend.setNodeLimit(v) }
    }
    Text {
        Layout.fillWidth: true
        Layout.topMargin: 8
        text: "Shuffle moves"
        color: Theme.text
        font.pixelSize: 13
        font.bold: true
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
        Layout.topMargin: 16
        label: "Restore defaults"
        iconName: "refresh"
        enabled: !backend.busy
        onClicked: backend.resetSettings()
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 1
        Layout.topMargin: 16
        Layout.bottomMargin: 14
        color: Theme.divider
    }

    SectionHeader {
        label: "About"
        iconName: "info"
    }
    InfoCard {
        Layout.fillWidth: true
        Layout.topMargin: 10
        Layout.preferredHeight: 74
        text: "The goal is the arrangement you created. Shuffle the board, "
              + "then solve it with BFS, DFS or A* to return to that exact state."
        iconName: "lock"
    }
    InfoCard {
        Layout.fillWidth: true
        Layout.topMargin: 10
        Layout.bottomMargin: 4
        Layout.preferredHeight: 56
        text: "Arrow keys move the blank. Click any tile next to it."
        iconName: "keyboard"
    }
}
