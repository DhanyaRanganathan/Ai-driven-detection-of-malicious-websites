import pandas as pd

# Read malicious URLs
with open("malicious_urls.txt", "r") as f:
    malicious_urls = f.read().splitlines()

malicious_data = pd.DataFrame({
    "url": malicious_urls,
    "label": [1] * len(malicious_urls)   # 1 = phishing
})

# Read safe URLs
with open("safe_urls.txt", "r") as f:
    safe_urls = f.read().splitlines()

safe_data = pd.DataFrame({
    "url": safe_urls,
    "label": [0] * len(safe_urls)   # 0 = safe
})

# Combine both
dataset = pd.concat([malicious_data, safe_data], ignore_index=True)

# Save dataset
dataset.to_csv("url_dataset.csv", index=False)

print("Dataset created successfully: url_dataset.csv")