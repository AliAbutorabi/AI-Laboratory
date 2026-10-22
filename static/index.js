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


    const response =
        await fetch(
            "/api/puzzle/create/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },

                body: JSON.stringify({
                    size: size,
                }),
            }
        );


    const data =
        await response.json();


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