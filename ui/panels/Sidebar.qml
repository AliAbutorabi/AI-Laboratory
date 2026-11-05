import QtQuick
import ".."
import "../components"

/* Left configuration column: segmented tabs + a vertically scrollable body. */
GlassCard {
    id: root
    fillColor: Theme.sidebar
    borderColor: "#E3E7FF"
    cardRadius: 22
    shadowStrength: 0.06

    Row {
        id: tabs
        x: 7
        y: 7
        width: root.width - 14
        height: 46
        Repeater {
            model: 2
            Item {
                width: index === 0 ? tabs.width * 0.42 : tabs.width * 0.58
                height: tabs.height
                property bool active: backend.setupTabIndex === index

                Rectangle {
                    anchors.fill: parent
                    radius: 12
                    color: "#EEF1FE"
                }
                Rectangle {
                    anchors.fill: parent
                    radius: 12
                    opacity: active ? 1 : 0
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0; color: Theme.purple }
                        GradientStop { position: 1; color: Theme.purpleLight }
                    }
                    Behavior on opacity { NumberAnimation { duration: 160 } }
                }
                Row {
                    anchors.centerIn: parent
                    spacing: 8
                    Icon {
                        name: index === 0 ? "gear" : "sliders"
                        width: 16; height: 16
                        color: active ? "#FFFFFF" : Theme.textMuted
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: index === 0 ? "Setup" : "Settings"
                        color: active ? "#FFFFFF" : Theme.textMuted
                        font.pixelSize: 14
                        font.bold: true
                        font.family: Theme.fontFamily
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: backend.setSetupTab(index)
                }
            }
        }
    }

    Flickable {
        id: scroller
        x: 24
        y: 60
        width: root.width - 48
        height: root.height - 60 - 12
        clip: true
        contentWidth: width
        contentHeight: panelLoader.height + 16
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height

        Loader {
            id: panelLoader
            width: scroller.width
            height: panelLoader.item ? panelLoader.item.implicitHeight : 0
            sourceComponent: backend.setupTabIndex === 0
                             ? setupComponent : settingsComponent
        }
    }

    Rectangle {
        x: root.width - 10
        y: 60 + scroller.height * scroller.visibleArea.yPosition
        width: 4
        height: Math.max(28, scroller.height * scroller.visibleArea.heightRatio)
        radius: 2
        color: "#C7CEF0"
        visible: scroller.contentHeight > scroller.height
    }

    Component {
        id: setupComponent
        SetupPanel { width: panelLoader.width }
    }
    Component {
        id: settingsComponent
        SettingsPanel { width: panelLoader.width }
    }
}
