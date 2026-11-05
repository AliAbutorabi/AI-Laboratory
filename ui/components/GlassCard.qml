import QtQuick
import ".."

/* White / translucent rounded card with a soft layered blue-purple shadow.
   Children added by callers are parented to the visible surface so their
   coordinates are relative to the card itself. */
Item {
    id: root
    default property alias contents: surface.data

    property color fillColor: Theme.card
    property color borderColor: Theme.border
    property real borderWidth: 1
    property real cardRadius: Theme.cardRadius
    property bool shadow: true
    property real shadowStrength: 0.055

    Rectangle {
        x: -5; y: 6
        width: root.width + 10; height: root.height + 1
        radius: root.cardRadius + 5
        color: Qt.rgba(0.23, 0.29, 0.62, root.shadowStrength * 0.35)
        visible: root.shadow
    }
    Rectangle {
        x: -3; y: 4
        width: root.width + 6; height: root.height
        radius: root.cardRadius + 3
        color: Qt.rgba(0.23, 0.29, 0.62, root.shadowStrength * 0.55)
        visible: root.shadow
    }
    Rectangle {
        x: -1; y: 2
        width: root.width + 2; height: root.height
        radius: root.cardRadius + 1
        color: Qt.rgba(0.23, 0.29, 0.62, root.shadowStrength * 0.8)
        visible: root.shadow
    }
    Rectangle {
        id: surface
        anchors.fill: parent
        radius: root.cardRadius
        color: root.fillColor
        border.color: root.borderColor
        border.width: root.borderWidth
    }
}
