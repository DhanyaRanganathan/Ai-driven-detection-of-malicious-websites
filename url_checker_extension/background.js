chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    const url = tab.url;
    let risk = url.includes("example") ? "High" : "Low";

    // Send URL info to backend
    fetch("http://localhost:5000/add_history", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: "user@example.com", site: url, risk: risk })
    });
  }
});