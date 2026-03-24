import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load feature dataset
data = pd.read_csv("url_features.csv")

# Separate features (X) and labels (y)
X = data.drop("label", axis=1)  # all columns except label
y = data["label"]

# Split dataset: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save the trained model
joblib.dump(model, "url_model.pkl")
print("Trained ML model saved as url_model.pkl")