import QtQuick
import ".."
import "../components"

/* Goal-state area.  The goal is a fixed snapshot of the board the user
   created, so there are deliberately no "set goal" buttons here: the card
   simply shows the target and the real solvability result.  The strip below
   the card carries the application status messages. */
Item {
    id: root
    property real infoHeight: 62
    property real goalPx: Math.min(goalCard.width * 0.62,
                                  goalCard.height * 0.54, 290)

    GlassCard {
        id: goalCard
        width: root.width
        height: Math.max(200, root.height - root.infoHeight - 12)

        Row {
            x: 20
            y: 17
            spacing: 9
            Icon {
                name: "trophy"
                width: 19; height: 19
                color: Theme.orange
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                text: "Goal State"
                color: Theme.text
                font.pixelSize: 18
                font.bold: true
                font.family: Theme.fontFamily
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Column {
            anchors.centerIn: parent
            anchors.verticalCenterOffset: 14
            spacing: 16
            GoalBoard {
                width: root.goalPx
                height: root.goalPx
                anchors.horizontalCenter: parent.horizontalCenter
            }
            StatusBadge {
                okay: backend.solvable
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Your starting arrangement"
                color: Theme.textFaint
                font.pixelSize: Theme.tinySize
                font.family: Theme.fontFamily
            }
        }
    }

    InfoCard {
        y: root.height - root.infoHeight
        width: root.width
        height: root.infoHeight
        text: backend.statusText
        fontSize: 15
        textColor: Theme.text
        padding: 9
    }
}
