import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

file_path = "diabetes.csv"

df = pd.read_csv(file_path)

# If the CSV does not already have column names, assign them
expected_cols = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

if list(df.columns) != expected_cols and len(df.columns) == 9:
    # If the first row is actually data, reload without header
    if df.columns[0] != "Pregnancies":
        df = pd.read_csv(file_path, header=None, names=expected_cols)

# Optional but common preprocessing:
# In this dataset, zero values in some medical fields are treated as missing
zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in zero_as_missing:
    df[col] = df[col].replace(0, np.nan)
    df[col] = df[col].fillna(df[col].median())

# Features and target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Model
model = GaussianNB()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

# Metrics
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp) if (tp + fp) != 0 else 0
recall = tp / (tp + fn) if (tp + fn) != 0 else 0
print("Confusion Matrix:")
print(cm)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")

print("===== Pima Indians Diabetes : Gaussian Naive Bayes =====")
print("\nConfusion Matrix:")
print(cm)
print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))
results = X_test.copy()
results["Actual"] = y_test.values
results["Predicted"] = y_pred
results["P(Non-Diabetic=0)"] = y_prob[:, 0]
results["P(Diabetic=1)"] = y_prob[:, 1]
print("\nFew test data predictions:")
print(results.head(10))