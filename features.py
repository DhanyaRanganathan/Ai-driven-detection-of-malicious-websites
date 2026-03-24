def extract_features(url):
    suspicious_words = ["login", "secure", "bank", "verify", "account"]
    features = {}

    # 1. URL length
    features["url_length"] = len(url)

    # 2. HTTPS check
    features["has_https"] = 1 if url.startswith("https") else 0

    # 3. Count digits
    features["num_digits"] = sum(c.isdigit() for c in url)

    # 4. Count special characters
    features["num_special_chars"] = sum(c in "@-_=.?&" for c in url)

    # 5. Count suspicious words
    features["suspicious_words"] = sum(word in url.lower() for word in suspicious_words)

    return features