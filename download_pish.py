import requests

# Download phishing URLs from OpenPhish
url = "https://openphish.com/feed.txt"
response = requests.get(url)

# Save to file
with open("malicious_urls.txt", "w") as f:
    f.write(response.text)

print("Phishing URLs downloaded and saved in malicious_urls.txt")