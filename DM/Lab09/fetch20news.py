from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

train_data = fetch_20newsgroups(
    subset="train",
    remove=("headers", "footers", "quotes"),
    shuffle=True,
    random_state=42
)

test_data = fetch_20newsgroups(
    subset="test",
    remove=("headers", "footers", "quotes"),
    shuffle=True,
    random_state=42
)

X_train = train_data.data
y_train = train_data.target
X_test = test_data.data
y_test = test_data.target

model = Pipeline([
    ("vectorizer", CountVectorizer(stop_words="english", min_df=2)),
    ("classifier", MultinomialNB(alpha=0.5))
])

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
cm = confusion_matrix(y_test, y_pred)

print("===== 20 Newsgroups : Multinomial Naive Bayes =====")
print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print("\nConfusion Matrix:")
print(cm)
print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=train_data.target_names,
    zero_division=0
))

print("\nFew sample predictions:")
for i in range(5):
    text_preview = X_test[i][:250].replace("\n", " ")
    actual_label = train_data.target_names[y_test[i]]
    predicted_label = train_data.target_names[y_pred[i]]
    print(f"\nSample {i+1}")
    print(f"Actual   : {actual_label}")
    print(f"Predicted: {predicted_label}")
    print(f"Text     : {text_preview}...")