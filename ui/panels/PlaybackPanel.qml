import QtQuick
import ".."
import "../components"

/* Wide solution playback card: step controls, timeline and move sequence. */
GlassCard {
    id: root

    Item {
        x: 18
        y: 12
        width: root.width - 36
        height: 26
        Row {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10
            Rectangle {
                width: 24; height: 24
                radius: 12
                color: Theme.purple
                Icon {
                    anchors.centerIn: parent
                    name: "play"
                    width: 12; height: 12
                    color: "#FFFFFF"
                }
            }
            Text {
                text: "Solution Playback"
                color: Theme.text
                font.pixelSize: 16
                font.bold: true
                font.family: Theme.fontFamily
                anchors.verticalCenter: parent.verticalCenter
            }
        }
        Text {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            text: "Step " + backend.playbackStep + " / " + backend.playbackTotal
            color: Theme.textMuted
            font.pixelSize: Theme.smallSize
            font.family: Theme.fontFamily
        }
    }

    Item {
        x: 18
        y: 46
        width: root.width - 36
        height: 44
        readonly property real controlsWidth: 5 * 44 + 4 * 10

        Row {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10
            RoundIconButton {
                iconName: "first"
                enabled: backend.playbackAvailable
                onClicked: backend.firstStep()
            }
            RoundIconButton {
                iconName: "chevronLeft"
                enabled: backend.playbackAvailable
                onClicked: backend.stepBy(-1)
            }
            RoundIconButton {
                iconName: backend.playing ? "pause" : "play"
                fillColor: backend.playing ? "#E5DEFF" : Theme.panel
                iconColor: Theme.purpleDeep
                emphasized: true
                enabled: backend.playbackAvailable
                onClicked: backend.playPause()
            }
            RoundIconButton {
                iconName: "chevronRight"
                enabled: backend.playbackAvailable
                onClicked: backend.stepBy(1)
            }
            RoundIconButton {
                iconName: "last"
                enabled: backend.playbackAvailable
                onClicked: backend.lastStep()
            }
        }

        CustomSlider {
            anchors.left: parent.left
            anchors.leftMargin: parent.controlsWidth + 18
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            from: 0
            to: Math.max(1, backend.playbackTotal)
            value: backend.playbackStep
            enabled: backend.playbackAvailable
            onValueEdited: function(v) { backend.seekStep(v) }
        }
    }

    InfoCard {
        x: 18
        y: 98
        width: root.width - 36
        height: 44
        padding: 9
        fontSize: 12
        text: backend.solutionText.length
              ? backend.solutionText
              : "The move sequence will appear here after solving."
    }
}
