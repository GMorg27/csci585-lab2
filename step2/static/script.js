async function onSplitClick() {
    const secret = parseInt(document.getElementById("secret-input").value);
    const threshold = parseInt(document.getElementById("threshold-input").value);
    const total = parseInt(document.getElementById("total-input").value);
    if (!validateSplitInput(secret, threshold, total)) {
        alert("Values of (k) and (n) must be positive, with (k) not exceeding (n)")
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/split", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                d: secret,
                k: threshold,
                n: total
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error; status: ${response.status}`);
        }
        const result = await response.json();
        console.log(result); // TODO
    }
    catch (error) {
        console.error("Split error:", error);
    }
}

function validateSplitInput(secret, threshold, total) {
    return threshold > 0 && total > 0 && threshold <= total;
}

async function onJoinClick() {
    const sharesText = document.getElementById("shares-input").value;
    const shares = parseShares(sharesText);
    if (shares.length === 0) {
        alert("Enter one share per line in format (k, n)")
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/join", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(shares)
        });

        if (!response.ok) {
            throw new Error(`HTTP error; status: ${response.status}`);
        }
        const result = await response.json();
        const secret = parseInt(result.secret);
        console.log(secret); // TODO
    }
    catch (error) {
        console.error("Join error:", error);
    }
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
