/* One consistent 24x24 stroke-style icon family (Lucide-like path data).
   Kept as path strings so QML can render any icon in any colour through
   QtQuick.Shapes / PathSvg without external image assets. */

/* Static icon table.  Qt 6 no longer accepts ``pragma library`` here; each
   QML file gets its own lightweight copy, which is fine for read-only data. */

var ICONS = {
    "gear": {
        path: "M10.3 2h3.4l.5 2.3 1.7.7 2.1-1.1 2.4 2.4-1.1 2.1.7 1.7 2.3.5v3.4l-2.3.5-.7 1.7 1.1 2.1-2.4 2.4-2.1-1.1-1.7.7-.5 2.3h-3.4l-.5-2.3-1.7-.7-2.1 1.1-2.4-2.4 1.1-2.1-.7-1.7L2 13.7v-3.4l2.3-.5.7-1.7L3.9 6l2.4-2.4 2.1 1.1 1.7-.7L10.3 2z M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z",
        fill: false, stroke: 1.9
    },
    "sliders": {
        path: "M4 21v-7 M4 10V3 M12 21v-9 M12 8V3 M20 21v-5 M20 12V3 M1 14h6 M9 8h6 M17 16h6",
        fill: false, stroke: 1.9
    },
    "play": { path: "M8 5v14l11-7z", fill: true, stroke: 0 },
    "pause": { path: "M7 5h3v14H7z M14 5h3v14h-3z", fill: true, stroke: 0 },
    "shuffle": {
        path: "M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.7-1.1 2-1.7 3.3-1.7H22 M18 2l4 4-4 4 M2 6h1.9c1.5 0 2.9.9 3.6 2.2 M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8 M18 14l4 4-4 4",
        fill: false, stroke: 1.9
    },
    "sparkles": {
        path: "M12 2l1.9 5.1L19 9l-5.1 1.9L12 16l-1.9-5.1L5 9l5.1-1.9L12 2z M19 15l.8 2.2 2.2.8-2.2.8L19 21l-.8-2.2-2.2-.8 2.2-.8L19 15z M5 2l.6 1.6L7.2 4.2 5.6 4.8 5 6.4 4.4 4.8 2.8 4.2l1.6-.6L5 2z",
        fill: true, stroke: 0
    },
    "pencil": {
        path: "M12 20h9 M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z",
        fill: false, stroke: 1.9
    },
    "chevronDown": { path: "m6 9 6 6 6-6", fill: false, stroke: 2.1 },
    "chevronUp": { path: "m6 15 6-6 6 6", fill: false, stroke: 2.1 },
    "chevronLeft": { path: "m15 18-6-6 6-6", fill: false, stroke: 2.1 },
    "chevronRight": { path: "m9 18 6-6-6-6", fill: false, stroke: 2.1 },
    "first": { path: "M18 5v14L8 12l10-7z M4 5h2v14H4z", fill: true, stroke: 0 },
    "last": { path: "M6 5v14l10-7L6 5z M18 5h2v14h-2z", fill: true, stroke: 0 },
    "minus": { path: "M5 12h14", fill: false, stroke: 2.1 },
    "plus": { path: "M12 5v14 M5 12h14", fill: false, stroke: 2.1 },
    "network": {
        path: "M9 3h6v6H9z M3 15h6v6H3z M15 15h6v6h-6z M12 9v3 M6 15v-3h12v3",
        fill: false, stroke: 1.8
    },
    "clock": {
        path: "M12 7v5l3 2 M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z",
        fill: false, stroke: 1.8
    },
    "trophy": {
        path: "M7 3h10v6a5 5 0 0 1-10 0V3z M4 4h3v4a3 3 0 0 1-3-3V4z M17 4h3v1a3 3 0 0 1-3 3V4z M10 13h4v4h-4z M8 20h8v2H8z M11 17h2v3h-2z",
        fill: true, stroke: 0
    },
    "check": { path: "m5 12 4 4L19 6", fill: false, stroke: 2.4 },
    "x": { path: "M18 6 6 18 M6 6l12 12", fill: false, stroke: 2.2 },
    "info": {
        path: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z M12 11v5 M12 8h.01",
        fill: false, stroke: 1.8
    },
    "bulb": {
        path: "M12 2a7 7 0 0 0-4 12.8V17h8v-2.2A7 7 0 0 0 12 2z M9 18h6v1.5H9z M10 20.5h4V22h-4z",
        fill: true, stroke: 0
    },
    "expand": {
        path: "M4 9V4h5 M20 15v5h-5 M4 4l6 6 M20 20l-6-6",
        fill: false, stroke: 1.9
    },
    "stop": { path: "M6 6h12v12H6z", fill: true, stroke: 0 },
    "help": {
        path: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3 M12 17h.01",
        fill: false, stroke: 1.9
    },
    "close": { path: "M18 6 6 18 M6 6l12 12", fill: false, stroke: 1.8 },
    "minimize": { path: "M5 12h14", fill: false, stroke: 1.5 },
    "maximize": { path: "M5 5h14v14H5z", fill: false, stroke: 1.5 },
    "restore": { path: "M9 3h12v12H9z M3 9h12v12H3z", fill: false, stroke: 1.5 },
    "alert": {
        path: "M12 3 2 20h20L12 3z M12 9v5 M12 17h.01",
        fill: false, stroke: 1.9
    },
    "refresh": {
        path: "M3 12a9 9 0 0 1 15-6.7L21 8 M21 3v5h-5 M21 12a9 9 0 0 1-15 6.7L3 16 M3 21v-5h5",
        fill: false, stroke: 1.9
    },
    "keyboard": {
        path: "M3 6h18v12H3z M7 10h.01 M11 10h.01 M15 10h.01 M18 10h.01 M7 14h10",
        fill: false, stroke: 1.8
    },
    "lock": {
        path: "M5 11h14v10H5z M8 11V7a4 4 0 0 1 8 0v4",
        fill: false, stroke: 1.9
    }
};

function get(name) {
    return ICONS[name] || ICONS["info"];
}
