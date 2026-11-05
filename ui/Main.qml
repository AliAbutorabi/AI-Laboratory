import QtQuick
import QtQuick.Window
import QtQuick.Controls.Basic
import QtQuick.Layouts
import "."
import "components"
import "panels"

ApplicationWindow {
    id: win
    width: 1648
    height: 900
    minimumWidth: 1180
    minimumHeight: 720
    visible: true
    color: "transparent"
    flags: Qt.Window | Qt.FramelessWindowHint
    title: "Puzzle Solver — AI Sliding Puzzle Desktop"

    background: Item {
        clip: true
        Rectangle {
            anchors.fill: parent
            gradient: Gradient {
                GradientStop { position: 0; color: Theme.bgTop }
                GradientStop { position: 1; color: Theme.bgBottom }
            }
        }
        // Soft blue-purple wave sweeping in from the top right.
        Rectangle {
            x: parent.width * 0.55
            y: -300
            width: parent.width * 0.64
            height: 460
            radius: 230
            rotation: -16
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0;   color: "#00A9C2FF" }
                GradientStop { position: 0.45; color: "#9AAFC8FF" }
                GradientStop { position: 1;   color: "#CCB7A1F5" }
            }
        }
        Rectangle {
            x: parent.width * 0.75
            y: -270
            width: parent.width * 0.46
            height: 380
            radius: 190
            rotation: -10
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: "#668CB4FF" }
                GradientStop { position: 1; color: "#BBA38CF5" }
            }
        }
    }

    function statusColor(kind) {
        if (kind === "success") return Theme.success;
        if (kind === "error") return Theme.dangerText;
        if (kind === "warning") return Theme.orange;
        if (kind === "working") return Theme.purple;
        return Theme.success;
    }

    Item {
        id: appRoot
        anchors.fill: parent
        focus: true

        Component.onCompleted: appRoot.forceActiveFocus()

        MouseArea {
            anchors.fill: parent
            z: -1
            onPressed: appRoot.forceActiveFocus()
        }

        Keys.onPressed: function(event) {
            var direction = "";
            switch (event.key) {
                case Qt.Key_Up:    direction = "up"; break;
                case Qt.Key_Down:  direction = "down"; break;
                case Qt.Key_Left:  direction = "left"; break;
                case Qt.Key_Right: direction = "right"; break;
            }
            if (direction !== "") {
                backend.moveBlank(direction);
                event.accepted = true;
            }
        }

        Column {
            anchors.fill: parent

            CustomTitleBar {
                width: parent.width
                height: 32
            }

            Item {
                id: body
                width: parent.width
                height: parent.height - 32

                readonly property real sidebarWidth:
                    Math.min(395, Math.max(310, (body.width - 36) * 0.27))

                Row {
                    id: mainRow
                    anchors.fill: parent
                    anchors.leftMargin: 18
                    anchors.rightMargin: 18
                    anchors.topMargin: 12
                    anchors.bottomMargin: 26
                    spacing: 38

                    Sidebar {
                        width: body.sidebarWidth
                        height: parent.height
                    }

                    ColumnLayout {
                        width: mainRow.width - body.sidebarWidth - mainRow.spacing
                        height: parent.height
                        spacing: 14

                        WorkspaceHeader {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 88
                            Layout.minimumHeight: 76
                        }

                        Item {
                            id: boardsRow
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.minimumHeight: 330
                            Row {
                                anchors.fill: parent
                                spacing: 16
                                PuzzleCard {
                                    width: (parent.width - 16) * 0.58
                                    height: parent.height
                                }
                                GoalPanel {
                                    width: (parent.width - 16) * 0.42
                                    height: parent.height
                                }
                            }
                        }

                        PlaybackPanel {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 158
                            Layout.minimumHeight: 150
                        }
                    }
                }

                Row {
                    x: 24
                    y: body.height - 21
                    spacing: 8
                    Rectangle {
                        width: 8; height: 8
                        radius: 4
                        color: win.statusColor(backend.statusKind)
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: backend.statusText
                        color: Theme.textMuted
                        font.pixelSize: Theme.smallSize
                        font.family: Theme.fontFamily
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }
        }

        // ------------------------------------------------ frameless resize grips
        MouseArea {
            x: 0; y: 0; width: 12; height: 12
            z: 300
            cursorShape: Qt.SizeFDiagCursor
            onPressed: backend.startWindowResize(3)
        }
        MouseArea {
            x: 12; y: 0; width: Math.max(10, win.width - 160); height: 4
            z: 300
            cursorShape: Qt.SizeVerCursor
            onPressed: backend.startWindowResize(1)
        }
        MouseArea {
            x: 0; y: 12; width: 5; height: Math.max(10, win.height - 24)
            z: 300
            cursorShape: Qt.SizeHorCursor
            onPressed: backend.startWindowResize(2)
        }
        MouseArea {
            x: win.width - 5; y: 12; width: 5
            height: Math.max(10, win.height - 24)
            z: 300
            cursorShape: Qt.SizeHorCursor
            onPressed: backend.startWindowResize(4)
        }
        MouseArea {
            x: 0; y: win.height - 12; width: 12; height: 12
            z: 300
            cursorShape: Qt.SizeBDiagCursor
            onPressed: backend.startWindowResize(10)
        }
        MouseArea {
            x: 12; y: win.height - 5
            width: Math.max(10, win.width - 24); height: 5
            z: 300
            cursorShape: Qt.SizeVerCursor
            onPressed: backend.startWindowResize(8)
        }
        MouseArea {
            x: win.width - 12; y: win.height - 12; width: 12; height: 12
            z: 300
            cursorShape: Qt.SizeFDiagCursor
            onPressed: backend.startWindowResize(12)
        }

        // ---------------------------------------------------- enlarged board view
        Rectangle {
            anchors.fill: parent
            z: 400
            visible: backend.boardExpanded
            color: "#88111A4B"
            MouseArea {
                anchors.fill: parent
                onClicked: backend.toggleBoardExpanded()
            }
            GlassCard {
                anchors.centerIn: parent
                width: Math.min(720, parent.width - 120)
                height: Math.min(720, parent.height - 100)
                Row {
                    x: 22; y: 18
                    spacing: 10
                    Icon {
                        name: "expand"
                        width: 18; height: 18
                        color: Theme.purple
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: "Current Puzzle - enlarged"
                        color: Theme.text
                        font.pixelSize: 18
                        font.bold: true
                        font.family: Theme.fontFamily
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                RoundIconButton {
                    anchors.right: parent.right
                    anchors.rightMargin: 18
                    y: 14
                    diameter: 30
                    iconName: "close"
                    iconSize: 14
                    onClicked: backend.toggleBoardExpanded()
                }
                Item {
                    x: 20; y: 58
                    width: parent.width - 40
                    height: Math.max(80, parent.height - 58 - 20)
                    PuzzleBoard {
                        anchors.centerIn: parent
                        width: Math.min(parent.width, parent.height)
                        height: width
                        interactive: !backend.busy
                        animate: !backend.busy
                    }
                }
            }
        }

        // ---------------------------------------------------------- modal dialog
        DialogOverlay {
            anchors.fill: parent
            z: 500
            visible: backend.alertVisible || backend.confirmVisible
            confirmMode: backend.confirmVisible
            title: backend.confirmVisible ? backend.confirmTitle : "Puzzle Solver"
            message: backend.confirmVisible ? backend.confirmText : backend.alertText
            onAccepted: backend.confirmSolve()
            onDismissed: backend.confirmVisible
                         ? backend.cancelSolve() : backend.dismissAlert()
        }
    }
}
