// Attach click function
document.getElementById("checkBtn").addEventListener("click", checkURL);
async function checkURL() {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let url = tab.url;

    console.log("Button clicked, URL:", url);

    try {
        let response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });

        let data = await response.json();
        console.log("Response:", data);

        const resultElement = document.getElementById("result");

        if (data.result === "malicious") {
            resultElement.innerText = "Malicious Site";
            resultElement.style.color = "red";
        } else {
            resultElement.innerText = "Safe Site";
            resultElement.style.color = "green";
        }

    } catch (err) {
        console.log("Error:", err);
        document.getElementById("result").innerText = "Error connecting to server";
        document.getElementById("result").style.color = "orange";
    }
}