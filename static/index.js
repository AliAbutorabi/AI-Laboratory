let puzzle = [];

let isShuffling = false;
let isSolving = false;

let eventSource = null;

let nodeQueue = [];
let processingQueue = false;


function renderPuzzle() {

    const container =
        document.getElementById("puzzle");

    const size = puzzle.length;

    container.innerHTML = "";

    container.style.gridTemplateColumns =
        `repeat(${size}, minmax(0, 1fr))`;

    container.style.gridTemplateRows =
        `repeat(${size}, minmax(0, 1fr))`;


    puzzle.forEach(row => {

        row.forEach(value => {

            const cell =
                document.createElement("div");

            cell.className =
                "flex items-center justify-center " +
                "rounded-xl text-2xl font-bold " +
                "bg-blue-500 text-white " +
                "shadow-sm transition";


            if (value === null) {

                cell.className =
                    "rounded-xl bg-slate-100";

            } else {

                cell.textContent = value;

            }


            container.appendChild(cell);

        });

    });

}


function updatePuzzle(data) {

    puzzle = data.puzzle;

    renderPuzzle();

}


function setupModeChanged() {

    const isManual =
        document.getElementById("setup-mode").value === "manual";

    document.getElementById("manual-help").classList.toggle(
        "hidden",
        !isManual
    );

    document.getElementById("manual-grid").classList.toggle(
        "hidden",
        !isManual
    );

    if (isManual) {
        renderManualGrid();
    }

}


function renderManualGrid() {

    const grid = document.getElementById("manual-grid");
    const size = Number(document.getElementById("size").value);

    grid.replaceChildren();

    if (!Number.isInteger(size) || size < 2 || size > 10) {
        return;
    }

    grid.style.gridTemplateColumns = `repeat(${size}, minmax(0, 1fr))`;

    for (let position = 0; position < size * size; position++) {
        const input = document.createElement("input");
        input.type = "number";
        input.min = "1";
        input.max = String(size * size - 1);
        input.step = "1";
        input.setAttribute("aria-label", `Puzzle cell ${position + 1}`);
        input.className =
            "w-full min-w-0 rounded-lg border border-slate-300 px-2 py-3 text-center";
        grid.appendChild(input);
    }

}


function getCSRFToken() {

    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

}


function delay(ms) {

    return new Promise(
        resolve => setTimeout(resolve, ms)
    );

}


function setStatus(message, type = "normal") {

    const status =
        document.getElementById("status");

    const indicator =
        document.getElementById("status-indicator");


    status.textContent = message;


    if (type === "success") {

        status.className =
            "text-sm text-green-700";

        indicator.className =
            "w-2.5 h-2.5 rounded-full bg-green-500";

    } else if (type === "error") {

        status.className =
            "text-sm text-red-700";

        indicator.className =
            "w-2.5 h-2.5 rounded-full bg-red-500";

    } else if (type === "working") {

        status.className =
            "text-sm text-blue-700";

        indicator.className =
            "w-2.5 h-2.5 rounded-full bg-blue-500";

    } else {

        status.className =
            "text-sm text-slate-600";

        indicator.className =
            "w-2.5 h-2.5 rounded-full bg-slate-400";
    }

}


function setControlsDisabled(disabled) {

    document.getElementById(
        "create-button"
    ).disabled = disabled;

    document.getElementById(
        "shuffle-button"
    ).disabled = disabled;

    document.getElementById(
        "solve-button"
    ).disabled = disabled;

    document.getElementById(
        "size"
    ).disabled = disabled;

    document.getElementById(
        "setup-mode"
    ).disabled = disabled;

    document.querySelectorAll(
        "#manual-grid input"
    ).forEach(input => {
        input.disabled = disabled;
    });

    document.getElementById(
        "shuffle-moves"
    ).disabled = disabled;

    document.getElementById(
        "algorithm"
    ).disabled = disabled;

}


async function loadPuzzle() {

    const response =
        await fetch("/api/puzzle/state/");

    const data =
        await response.json();

    updatePuzzle(data);

}


async function createPuzzle() {

    if (isShuffling || isSolving) {
        return;
    }


    const size =
        document.getElementById("size").value;

    const mode =
        document.getElementById("setup-mode").value;

    const requestData = { size, mode };

    if (mode === "manual") {
        const values = Array.from(
            document.querySelectorAll("#manual-grid input"),
            input => input.value.trim()
        );
        const sizeNumber = Number(size);
        const expectedTiles = sizeNumber * sizeNumber - 1;
        const tiles = values.filter(value => value !== "").map(Number);

        if (
            values.length !== sizeNumber * sizeNumber ||
            values.filter(value => value === "").length !== 1 ||
            tiles.some(
                value => !Number.isInteger(value) || value < 1 || value > expectedTiles
            ) ||
            new Set(tiles).size !== expectedTiles
        ) {
            setStatus(
                `Enter each number from 1 to ${expectedTiles} once and leave one cell empty.`,
                "error"
            );
            return;
        }

        requestData.puzzle = [];
        for (let row = 0; row < sizeNumber; row++) {
            requestData.puzzle.push(
                values.slice(row * sizeNumber, (row + 1) * sizeNumber)
                    .map(value => value === "" ? null : Number(value))
            );
        }
    }


    const response =
        await fetch(
            "/api/puzzle/create/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },

                body: JSON.stringify(requestData),
            }
        );


    const data =
        await response.json();

    if (!response.ok) {
        setStatus(data.error || "Unable to create puzzle.", "error");
        return;
    }


    document.getElementById(
        "checked-nodes"
    ).textContent = 0;


    updatePuzzle(data);

    setStatus("New puzzle created");

}


async function shufflePuzzle() {

    if (isShuffling || isSolving) {
        return;
    }


    isShuffling = true;

    setControlsDisabled(true);

    setStatus(
        "Shuffling puzzle...",
        "working"
    );


    const moves =
        Number(
            document.getElementById(
                "shuffle-moves"
            ).value
        );


    document.getElementById(
        "checked-nodes"
    ).textContent = 0;


    for (let i = 0; i < moves; i++) {

        const response =
            await fetch(
                "/api/puzzle/shuffle/",
                {
                    method: "POST",

                    headers: {
                        "X-CSRFToken":
                            getCSRFToken(),
                    },
                }
            );


        if (!response.ok) {
            break;
        }


        const data =
            await response.json();


        updatePuzzle(data);


        await delay(10);
    }


    setStatus(
        "Puzzle is ready"
    );


    setControlsDisabled(false);

    isShuffling = false;
}


async function processNodeQueue() {

    if (processingQueue) {
        return;
    }


    processingQueue = true;


    while (nodeQueue.length > 0) {

        const event =
            nodeQueue.shift();


        if (event.type === "checked") {

            puzzle = event.state;

            document.getElementById(
                "checked-nodes"
            ).textContent =
                event.checked_nodes;

            renderPuzzle();

            await delay(10);
        }


        if (event.type === "solved") {

            document.getElementById(
                "checked-nodes"
            ).textContent =
                event.checked_nodes;

            setStatus(
                `Puzzle solved! ${event.checked_nodes} nodes checked.`,
                "success"
            );
        }


        if (event.type === "finished") {

            setStatus(
                "Search finished without solution.",
                "error"
            );
        }


        if (event.type === "error") {

            setStatus(
                event.message,
                "error"
            );
        }

    }


    processingQueue = false;


    if (
        !eventSource &&
        nodeQueue.length === 0
    ) {
        isSolving = false;
        setControlsDisabled(false);
    }

}


function solvePuzzle() {

    if (isShuffling || isSolving) {
        return;
    }


    const algorithm =
        document.getElementById(
            "algorithm"
        ).value;


    if (!algorithm) {

        setStatus(
            "Please select an algorithm.",
            "error"
        );

        return;
    }


    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }


    nodeQueue = [];

    processingQueue = false;

    isSolving = true;

    setControlsDisabled(true);

    document.getElementById(
        "checked-nodes"
    ).textContent = 0;


    setStatus(
        `Running ${algorithm}...`,
        "working"
    );


    const url =
        `/api/puzzle/solve/?algorithm=` +
        encodeURIComponent(algorithm);


    eventSource =
        new EventSource(url);


    eventSource.onmessage = function(event) {

        const data =
            JSON.parse(event.data);


        nodeQueue.push(data);

        processNodeQueue();


        if (
            data.type === "solved" ||
            data.type === "finished" ||
            data.type === "error"
        ) {

            eventSource.close();

            eventSource = null;

            if (data.type !== "checked") {
                setTimeout(() => {
                    if (!processingQueue && nodeQueue.length === 0) {
                        isSolving = false;
                        setControlsDisabled(false);
                    }
                }, 0);
            }
        }

    };


    eventSource.onerror = function() {

        if (eventSource) {
            eventSource.close();
            eventSource = null;
        }


        if (processingQueue || nodeQueue.length > 0) {
            return;
        }


        isSolving = false;

        setControlsDisabled(false);

        setStatus(
            "Connection to solver was interrupted.",
            "error"
        );

    };

}


loadPuzzle();