import QtQuick
import ".."
import "../components"

/* Application title, subtitle and the two live statistics cards. */
Item {
    id: root
    height: 88

    function formatCount(n) {
        return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    Row {
        anchors.left: parent.left
        anchors.leftMargin: 4
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -7
        spacing: 16
        Logo {
            width: 36; height: 36
            anchors.verticalCenter: parent.verticalCenter
        }
        Column {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 2
            Text {
                text: "Puzzle Solver"
                color: Theme.text
                font.pixelSize: Theme.titleSize
                font.bold: true
                font.family: Theme.fontFamily
            }
            Text {
                text: "Create, shuffle and solve your puzzle — BFS / DFS / A*"
                color: Theme.textMuted
                font.pixelSize: 14
                font.family: Theme.fontFamily
            }
        }
    }

    Row {
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -7
        spacing: 12
        StatisticCard {
            label: "Checked Nodes"
            value: root.formatCount(backend.checkedNodes)
            iconName: "network"
        }
        StatisticCard {
            label: "Manual Moves"
            value: String(backend.manualMoves)
            iconName: "clock"
        }
    }
}
