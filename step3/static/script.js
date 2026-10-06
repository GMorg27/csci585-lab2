async function onSaveClick() {
    const website = document.getElementById("site-input-r").value;
    const username = document.getElementById("username-input-r").value;
    const password = document.getElementById("password-input-r").value;
    if (website == "" || username == "" || password == "") {
        alert("Website, username, password fields must not be empty");
        return;
    }

    try {
        const response = await fetch("/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                website: website,
                username: username,
                password: password
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error; status: ${response.status}`);
        }
        console.log(`Registered login configuration for ${website}`);
    }
    catch (error) {
        console.error("Save error:", error);
    }
}

async function onAutofillClick() {
    const website = document.getElementById("site-input-a").value;
    const username = document.getElementById("username-input-a").value;
    if (website == "" || username == "") {
        alert("Website, username fields must not be empty");
        return;
    }

    try {
        const response = await fetch("/autofill", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                website: website,
                username: username,
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error; status: ${response.status}`);
        }

        const result = await response.json();
        const password = result.password;
        const passwordDisplay = document.getElementById("password-display-a");
        passwordDisplay.value = password;
    }
    catch (error) {
        console.error("Autofill error:", error);
    }
}

document.getElementById("save-button").addEventListener("click", onSaveClick);
document.getElementById("autofill-button").addEventListener("click", onAutofillClick);
