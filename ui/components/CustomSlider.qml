import QtQuick
import ".."

/* Purple track slider with a draggable round handle and click-to-seek. */
Item {
    id: root
    property real from: 0
    property real to: 100
    property real value: 0
    property color activeColor: Theme.purple
    property color trackColor: Theme.sliderTrack
    property bool dragging: false
    property real dragFraction: 0
    signal valueEdited(real newValue)

    height: 20
    readonly property real fraction:
        root.to > root.from
        ? Math.max(0, Math.min(1, (root.value - root.from) / (root.to - root.from)))
        : 0
    readonly property real effectiveFraction:
        root.dragging ? root.dragFraction : root.fraction
    readonly property real usableWidth: Math.max(1, root.width - 16)

    function setFromX(px) {
        var t = Math.max(0, Math.min(1, (px - 8) / root.usableWidth));
        root.dragFraction = t;
        root.valueEdited(Math.round(root.from + t * (root.to - root.from)));
    }

    Rectangle {
        id: track
        x: 8
        y: (root.height - 6) / 2
        width: root.usableWidth
        height: 6
        radius: 3
        color: root.trackColor
    }
    Rectangle {
        x: 8
        y: (root.height - 6) / 2
        width: Math.max(0, handle.x + handle.width / 2 - 8)
        height: 6
        radius: 3
        color: root.activeColor
    }
    Rectangle {
        id: handle
        x: 8 + root.usableWidth * root.effectiveFraction - 8
        y: (root.height - 16) / 2
        width: 16
        height: 16
        radius: 8
        color: root.activeColor
        border.color: "#FFFFFF"
        border.width: 2
        Behavior on x {
            enabled: !root.dragging
            NumberAnimation { duration: 90 }
        }
    }
    MouseArea {
        anchors.fill: parent
        enabled: root.enabled
        cursorShape: Qt.PointingHandCursor
        onPressed: function(mouse) {
            root.dragging = true;
            root.setFromX(mouse.x);
        }
        onPositionChanged: function(mouse) {
            if (root.dragging)
                root.setFromX(mouse.x);
        }
        onReleased: root.dragging = false
    }
}
