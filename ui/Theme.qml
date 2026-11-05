pragma Singleton
import QtQuick

/* Centralised design tokens.  Every QML file imports this singleton through
   the directory qmldir, so no hex value is repeated in the components. */
QtObject {
    // Surfaces
    property color bgTop: "#EEF1FF"
    property color bgBottom: "#DCE4FB"
    property color waveBlue: "#9DB8FF"
    property color wavePurple: "#B9A3F7"
    property color titleBar: "#141A38"
    property color card: "#FFFFFF"
    property color sidebar: "#F8F9FF"
    property color panel: "#F1F3FF"
    property color inputBg: "#F5F7FF"
    property color lavender: "#E9E2FE"
    property color lavenderSoft: "#F0EDFF"
    property color border: "#DCE2FF"
    property color divider: "#E4E8FB"

    // Text
    property color text: "#111A4B"
    property color textMuted: "#52618F"
    property color textFaint: "#8792BE"
    property color textOnDark: "#EAEDFF"

    // Accents
    property color purple: "#6245F5"
    property color purpleLight: "#8655FF"
    property color purpleDeep: "#5638E8"
    property color blueTileTop: "#06ACF2"
    property color blueTileBottom: "#0468C8"
    property color blueGoalTop: "#3D6BF0"
    property color blueGoalBottom: "#2244CF"
    property color greenTileTop: "#2FD39B"
    property color greenTileBottom: "#0E9E6E"
    property color success: "#18C978"
    property color successBg: "#C9F8DC"
    property color successText: "#0E8A52"
    property color dangerBg: "#FFE1E5"
    property color dangerText: "#D82436"
    property color stopBg: "#FFC3C9"
    property color stopText: "#D82436"
    property color orange: "#F5A524"
    property color yellow: "#FFC53D"
    property color shadow: "#3B4A9E"
    property color blankBg: "#EEF1FE"
    property color blankBorder: "#C8D0F0"
    property color disabled: "#E7EAFB"
    property color sliderTrack: "#DDE2F8"

    // Typography
    property string fontFamily: "Segoe UI"
    property int titleSize: 31
    property int sectionSize: 18
    property int sidebarHeading: 15
    property int bodySize: 13
    property int smallSize: 12
    property int tinySize: 11

    // Geometry
    property int cardRadius: 20
    property int controlRadius: 11
    property int smallRadius: 9
    property int controlHeight: 42
}
