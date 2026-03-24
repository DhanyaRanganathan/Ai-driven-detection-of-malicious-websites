import pandas as pd
from features import extract_features  # Step 4.2-la create pannina function

# Load dataset
data = pd.read_csv("url_dataset.csv")

# Apply feature extraction for each URL
X = pd.DataFrame([list(extract_features(url).values()) for url in data["url"]])
y = data["label"]

# Save the features and labels as new CSV (optional)
X['label'] = y
X.to_csv("url_features.csv", index=False)

print("Feature extraction complete! Saved as url_features.csv")
print(X.head())  # First 5 rows paakkapython -m pip install scikit-learn joblib