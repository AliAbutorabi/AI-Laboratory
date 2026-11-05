import QtQuick
import QtQuick.Shapes
import ".."
import "../IconData.js" as IconData

/* Renders a 24x24 vector path scaled into ``width`` x ``height``. */
Item {
    id: root
    property string name: "info"
    property color color: Theme.purple
    property real strokeWidth: 2
    property bool forceFilled: false
    readonly property var definition: IconData.get(root.name)
    readonly property bool filled: root.forceFilled || root.definition.fill

    width: 18
    height: 18
    antialiasing: true

    Shape {
        width: 24
        height: 24
        antialiasing: true
        transform: Scale {
            xScale: root.width / 24
            yScale: root.height / 24
        }
        ShapePath {
            strokeColor: root.filled ? "transparent" : root.color
            strokeWidth: root.definition.stroke > 0
                         ? root.definition.stroke * (root.strokeWidth / 2)
                         : 0
            fillColor: root.filled ? root.color : "transparent"
            capStyle: ShapePath.RoundCap
            joinStyle: ShapePath.RoundJoin
            PathSvg { path: root.definition.path }
        }
    }
}
