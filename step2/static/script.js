function onSplitClick() {
    const secret = document.getElementById("secret-input").value;
    const threshold = document.getElementById("threshold-input").value;
    const total = document.getElementById("total-input").value;
    if (!validateSplitInput(secret, threshold, total)) {
        alert("Values of (k) and (n) must be positive, with (k) not exceeding (n)")
        return;
    }

    console.log("fetch"); // TODO
}

function validateSplitInput(secret, threshold, total) {
    return threshold > 0 && total > 0 && threshold <= total;
}

function onJoinClick() {
    const sharesText = document.getElementById("shares-input").value;
    const shares = parseShares(sharesText);
    if (shares.length === 0) {
        alert("Enter one share per line in format (k, n)")
        return;
    }

    console.log("fetch"); // TODO
}

function parseShares(text) {
    const lines = text.split(/\r?\n/).map(line => line.trim()).filter(line => line !== "");
    for (const line of lines) {
        if (!line.match(/\(-?\d+, -?\d+\)/)) {
            return []
        }
    }
    return lines;
}

document.getElementById("split-button").addEventListener("click", onSplitClick);
document.getElementById("join-button").addEventListener("click", onJoinClick);
