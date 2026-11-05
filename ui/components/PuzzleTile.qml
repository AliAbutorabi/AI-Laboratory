import QtQuick
import QtQuick.Shapes
import ".."

/* One puzzle tile. Blue vertical gradient, white bold number, rounded
   corners; the blank uses a dashed lavender outline instead. Matching tiles
   cross-fade to green. Delegates are keyed by tile number, so x/y animations
   produce real sliding motion. */
Item {
    id: root
    property string number: ""
    property bool isBlank: false
    property bool correct: false
    property bool goalStyle: false
    property real tileRadius: 13
    property real fontPixelSize: 26
    property bool animateMove: true
    property bool interactive: true
    signal clicked()

    width: 100
    height: 100

    Behavior on x {
        enabled: root.animateMove
        NumberAnimation { duration: 165; easing.type: Easing.OutCubic }
    }
    Behavior on y {
        enabled: root.animateMove
        NumberAnimation { duration: 165; easing.type: Easing.OutCubic }
    }

    function roundedPath(w, h, r) {
        return "M" + r + " 0 H" + (w - r)
             + " A" + r + " " + r + " 0 0 1 " + w + " " + r
             + " V" + (h - r)
             + " A" + r + " " + r + " 0 0 1 " + (w - r) + " " + h
             + " H" + r
             + " A" + r + " " + r + " 0 0 1 0 " + (h - r)
             + " V" + r
             + " A" + r + " " + r + " 0 0 1 " + r + " 0 Z";
    }

    Rectangle {
        x: 0; y: 3
        width: root.width; height: root.height
        radius: root.tileRadius
        color: "#241C4FA8"
        visible: !root.isBlank
    }

    Rectangle {
        anchors.fill: parent
        radius: root.tileRadius
        visible: !root.isBlank
        opacity: root.correct ? 0 : 1
        gradient: Gradient {
            GradientStop {
                position: 0
                color: root.goalStyle ? Theme.blueGoalTop : Theme.blueTileTop
            }
            GradientStop {
                position: 1
                color: root.goalStyle ? Theme.blueGoalBottom : Theme.blueTileBottom
            }
        }
        Behavior on opacity { NumberAnimation { duration: 170 } }
    }
    Rectangle {
        anchors.fill: parent
        radius: root.tileRadius
        visible: !root.isBlank
        opacity: root.correct ? 1 : 0
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.greenTileTop }
            GradientStop { position: 1; color: Theme.greenTileBottom }
        }
        Behavior on opacity { NumberAnimation { duration: 170 } }
    }
    Shape {
        anchors.fill: parent
        visible: root.isBlank
        antialiasing: true
        ShapePath {
            strokeColor: Theme.blankBorder
            strokeWidth: 1.4
            strokeStyle: ShapePath.DashLine
            dashPattern: [4, 4]
            fillColor: Theme.blankBg
            PathSvg { path: root.roundedPath(root.width, root.height,
                                             root.tileRadius) }
        }
    }

    Text {
        anchors.centerIn: parent
        visible: !root.isBlank
        text: root.number
        color: "#FFFFFF"
        font.pixelSize: root.fontPixelSize
        font.bold: true
        font.family: Theme.fontFamily
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        enabled: root.interactive && !root.isBlank
        hoverEnabled: true
        cursorShape: (root.interactive && !root.isBlank)
                     ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: root.clicked()
    }

    scale: (mouse.pressed && root.interactive && !root.isBlank) ? 0.95 : 1
    Behavior on scale { NumberAnimation { duration: 110 } }
}
