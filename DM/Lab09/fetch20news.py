import re
import math
import numpy as np
from collections import Counter
from sklearn.datasets import fetch_20newsgroups

ENGLISH_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "just", "let", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

class CountVectorizerManual:
    def __init__(self, stop_words=None, min_df=1):
        self.stop_words = stop_words if stop_words is not None else set()
        self.min_df = min_df
        self.vocabulary_ = {}
        self.feature_names_ = []

    def _tokenize(self, text):
        text = text.lower()
        tokens = re.findall(r"[a-z]+", text)
        tokens = [tok for tok in tokens if tok not in self.stop_words and len(tok) > 1]
        return tokens

    def fit(self, documents):
        doc_freq = Counter()
        for doc in documents:
            tokens = set(self._tokenize(doc))
            doc_freq.update(tokens)

        vocab_tokens = [token for token, df in doc_freq.items() if df >= self.min_df]
        vocab_tokens.sort()

        self.vocabulary_ = {token: idx for idx, token in enumerate(vocab_tokens)}
        self.feature_names_ = vocab_tokens
        return self

    def transform(self, documents):
        transformed_docs = []
        for doc in documents:
            tokens = self._tokenize(doc)
            counts = Counter()
            for token in tokens:
                if token in self.vocabulary_:
                    token_id = self.vocabulary_[token]
                    counts[token_id] += 1
            transformed_docs.append(counts)
        return transformed_docs

    def fit_transform(self, documents):
        self.fit(documents)
        return self.transform(documents)

class MultinomialNBManual:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.classes_ = None
        self.class_log_prior_ = {}
        self.feature_log_prob_ = {}
        self.vocab_size_ = 0

    def fit(self, X, y, vocab_size):
        self.classes_ = np.unique(y)
        self.vocab_size_ = vocab_size
        class_doc_counts = Counter(y)
        n_docs = len(y)
        token_counts_per_class = {cls: Counter() for cls in self.classes_}
        total_tokens_per_class = {cls: 0 for cls in self.classes_}
        for doc_counts, label in zip(X, y):
            for token_id, count in doc_counts.items():
                token_counts_per_class[label][token_id] += count
                total_tokens_per_class[label] += count
        for cls in self.classes_:
            self.class_log_prior_[cls] = math.log(class_doc_counts[cls] / n_docs)
            denominator = total_tokens_per_class[cls] + self.alpha * self.vocab_size_
            log_probs = {}
            for token_id in range(self.vocab_size_):
                numerator = token_counts_per_class[cls][token_id] + self.alpha
                log_probs[token_id] = math.log(numerator / denominator)
            self.feature_log_prob_[cls] = log_probs
        return self

    def _predict_log_proba_one(self, doc_counts):
        scores = {}
        for cls in self.classes_:
            score = self.class_log_prior_[cls]
            for token_id, count in doc_counts.items():
                score += count * self.feature_log_prob_[cls][token_id]
            scores[cls] = score
        return scores
    
    def predict(self, X):
        predictions = []
        for doc_counts in X:
            scores = self._predict_log_proba_one(doc_counts)
            pred_class = max(scores, key=scores.get)
            predictions.append(pred_class)
        return np.array(predictions)

def confusion_matrix_manual(y_true, y_pred, labels=None):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if labels is None:
        labels = np.unique(np.concatenate([y_true, y_pred]))
    label_to_index = {label: i for i, label in enumerate(labels)}
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    for yt, yp in zip(y_true, y_pred):
        cm[label_to_index[yt], label_to_index[yp]] += 1
    return cm

def accuracy_score_manual(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return np.mean(y_true == y_pred)

def precision_recall_from_confusion_matrix(cm, zero_division=0):
    n_classes = cm.shape[0]
    precisions = []
    recalls = []
    supports = []
    for i in range(n_classes):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        support = cm[i, :].sum()
        precision = tp / (tp + fp) if (tp + fp) != 0 else zero_division
        recall = tp / (tp + fn) if (tp + fn) != 0 else zero_division
        precisions.append(precision)
        recalls.append(recall)
        supports.append(support)
    precisions = np.array(precisions, dtype=float)
    recalls = np.array(recalls, dtype=float)
    supports = np.array(supports, dtype=float)
    weighted_precision = np.average(precisions, weights=supports)
    weighted_recall = np.average(recalls, weights=supports)
    return precisions, recalls, supports, weighted_precision, weighted_recall

def classification_report_manual(y_true, y_pred, target_names=None, zero_division=0):
    labels = np.unique(np.concatenate([y_true, y_pred]))
    cm = confusion_matrix_manual(y_true, y_pred, labels=labels)
    precisions = []
    recalls = []
    f1s = []
    supports = []
    for i in range(len(labels)):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        support = cm[i, :].sum()
        precision = tp / (tp + fp) if (tp + fp) != 0 else zero_division
        recall = tp / (tp + fn) if (tp + fn) != 0 else zero_division
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else zero_division
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
        supports.append(support)
    precisions = np.array(precisions)
    recalls = np.array(recalls)
    f1s = np.array(f1s)
    supports = np.array(supports)
    if target_names is None:
        target_names = [str(label) for label in labels]
    accuracy = accuracy_score_manual(y_true, y_pred)
    macro_precision = np.mean(precisions)
    macro_recall = np.mean(recalls)
    macro_f1 = np.mean(f1s)
    weighted_precision = np.average(precisions, weights=supports)
    weighted_recall = np.average(recalls, weights=supports)
    weighted_f1 = np.average(f1s, weights=supports)
    lines = []
    lines.append(f"{'':>25}{'precision':>12}{'recall':>12}{'f1-score':>12}{'support':>12}")
    for name, p, r, f1, s in zip(target_names, precisions, recalls, f1s, supports):
        lines.append(f"{name:>25}{p:>12.4f}{r:>12.4f}{f1:>12.4f}{int(s):>12}")
    lines.append("")
    lines.append(f"{'accuracy':>25}{'':>12}{'':>12}{accuracy:>12.4f}{int(np.sum(supports)):>12}")
    lines.append(f"{'macro avg':>25}{macro_precision:>12.4f}{macro_recall:>12.4f}{macro_f1:>12.4f}{int(np.sum(supports)):>12}")
    lines.append(f"{'weighted avg':>25}{weighted_precision:>12.4f}{weighted_recall:>12.4f}{weighted_f1:>12.4f}{int(np.sum(supports)):>12}")
    return "\n".join(lines)


# Load 20 Newsgroups dataset
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
y_train = np.array(train_data.target)
X_test = test_data.data
y_test = np.array(test_data.target)
target_names = train_data.target_names

# Text vectorization
vectorizer = CountVectorizerManual(
    stop_words=ENGLISH_STOP_WORDS,
    min_df=2
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Multinomial Naive Bayes classifier
model = MultinomialNBManual(alpha=0.5)
model.fit(X_train_vec, y_train, vocab_size=len(vectorizer.vocabulary_))

# Predict on test data
y_pred = model.predict(X_test_vec)

# Confusion matrix
labels = np.arange(len(target_names))
cm = confusion_matrix_manual(y_test, y_pred, labels=labels)

# Metrics derived from predictions / confusion matrix
accuracy = accuracy_score_manual(y_test, y_pred)
_, _, _, weighted_precision, weighted_recall = precision_recall_from_confusion_matrix(cm)

print("===== 20 Newsgroups : Multinomial Naive Bayes =====")
print("\nTask: Text Classification on 20 Newsgroups Dataset")
print(f"\nNumber of training documents : {len(X_train)}")
print(f"Number of testing documents  : {len(X_test)}")
print(f"Vocabulary size              : {len(vectorizer.vocabulary_)}")
print("\nConfusion Matrix:")
print(cm)
print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {weighted_precision:.4f}")
print(f"Recall   : {weighted_recall:.4f}")
print("\nClassification Report:")
print(classification_report_manual(
    y_test,
    y_pred,
    target_names=target_names,
    zero_division=0
))
print("\nFew sample predictions:")
for i in range(5):
    text_preview = X_test[i][:250].replace("\n", " ")
    actual_label = target_names[y_test[i]]
    predicted_label = target_names[y_pred[i]]
    print(f"\nSample {i+1}")
    print(f"Actual   : {actual_label}")
    print(f"Predicted: {predicted_label}")
    print(f"Text     : {text_preview}...")