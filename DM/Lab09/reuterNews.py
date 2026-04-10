import nltk
from nltk.corpus import reuters
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

nltk.download("reuters")
nltk.download("punkt")

all_fileids = reuters.fileids()

train_ids = [fid for fid in all_fileids if fid.startswith("training/")]
test_ids = [fid for fid in all_fileids if fid.startswith("test/")]

def get_single_label_docs(fileids):
    texts = []
    labels = []

    for fid in fileids:
        cats = reuters.categories(fid)
        if len(cats) == 1:
            texts.append(reuters.raw(fid))
            labels.append(cats[0])

    return texts, labels
X_train, y_train = get_single_label_docs(train_ids)
X_test, y_test = get_single_label_docs(test_ids)
print("Training documents:", len(X_train))
print("Testing documents :", len(X_test))
print("Number of classes :", len(set(y_train)))

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
cm = confusion_matrix(y_test, y_pred, labels=sorted(set(y_train)))

print("\n===== Reuters Dataset : Multinomial Naive Bayes =====")
print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print("\nConfusion Matrix:")
print(cm)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nFew sample predictions:")
for i in range(5):
    print(f"\nSample {i+1}")
    print("Actual   :", y_test[i])
    print("Predicted:", y_pred[i])
    print("Text     :", X_test[i][:250].replace("\n", " "), "...")