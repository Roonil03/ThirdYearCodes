import numpy as np
import pandas as pd

def stratified_train_test_split(X, y, test_size=0.2, random_state=42):
    rng = np.random.default_rng(random_state)
    y_array = np.asarray(y)
    train_indices = []
    test_indices = []
    for cls in np.unique(y_array):
        cls_indices = np.where(y_array == cls)[0]
        rng.shuffle(cls_indices)
        n_test = int(round(len(cls_indices) * test_size))
        if len(cls_indices) > 1:
            n_test = max(1, n_test)
        test_indices.extend(cls_indices[:n_test])
        train_indices.extend(cls_indices[n_test:])
    train_indices = np.array(train_indices)
    test_indices = np.array(test_indices)
    rng.shuffle(train_indices)
    rng.shuffle(test_indices)
    X_train = X.iloc[train_indices].reset_index(drop=True)
    X_test = X.iloc[test_indices].reset_index(drop=True)
    y_train = y.iloc[train_indices].reset_index(drop=True)
    y_test = y.iloc[test_indices].reset_index(drop=True)
    return X_train, X_test, y_train, y_test


class GaussianNBManual:
    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]
        self.mean_ = np.zeros((n_classes, n_features), dtype=float)
        self.var_ = np.zeros((n_classes, n_features), dtype=float)
        self.priors_ = np.zeros(n_classes, dtype=float)
        for i, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.mean_[i, :] = X_c.mean(axis=0)
            self.var_[i, :] = X_c.var(axis=0)
            # avoid division by zero
            self.var_[i, :] = np.where(self.var_[i, :] == 0, 1e-9, self.var_[i, :])
            self.priors_[i] = X_c.shape[0] / X.shape[0]
        return self

    def _joint_log_likelihood(self, X):
        X = np.asarray(X, dtype=float)
        log_probs = []
        for i in range(len(self.classes_)):
            mean = self.mean_[i]
            var = self.var_[i]
            prior = np.log(self.priors_[i])
            # Gaussian log-likelihood
            log_likelihood = -0.5 * np.sum(np.log(2.0 * np.pi * var))
            log_likelihood -= 0.5 * np.sum(((X - mean) ** 2) / var, axis=1)
            log_probs.append(prior + log_likelihood)
        return np.column_stack(log_probs)

    def predict_proba(self, X):
        jll = self._joint_log_likelihood(X)
        # numerical stability
        max_log = np.max(jll, axis=1, keepdims=True)
        probs = np.exp(jll - max_log)
        probs /= probs.sum(axis=1, keepdims=True)
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        class_indices = np.argmax(probs, axis=1)
        return self.classes_[class_indices]

def confusion_matrix_manual(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tp = np.sum((y_true == 1) & (y_pred == 1))
    return np.array([[tn, fp],
                     [fn, tp]])

def classification_report_manual(y_true, y_pred, zero_division=0):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    lines = []
    header = f"{'':>12}{'precision':>12}{'recall':>12}{'f1-score':>12}{'support':>12}"
    lines.append(header)
    precisions = []
    recalls = []
    f1_scores = []
    supports = []
    for cls in [0, 1]:
        tp = np.sum((y_true == cls) & (y_pred == cls))
        fp = np.sum((y_true != cls) & (y_pred == cls))
        fn = np.sum((y_true == cls) & (y_pred != cls))
        support = np.sum(y_true == cls)
        precision = tp / (tp + fp) if (tp + fp) != 0 else zero_division
        recall = tp / (tp + fn) if (tp + fn) != 0 else zero_division
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else zero_division
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        supports.append(support)
        lines.append(f"{str(cls):>12}{precision:>12.4f}{recall:>12.4f}{f1:>12.4f}{support:>12}")
    accuracy = np.mean(y_true == y_pred)
    macro_precision = np.mean(precisions)
    macro_recall = np.mean(recalls)
    macro_f1 = np.mean(f1_scores)
    weighted_precision = np.average(precisions, weights=supports)
    weighted_recall = np.average(recalls, weights=supports)
    weighted_f1 = np.average(f1_scores, weights=supports)
    lines.append("")
    lines.append(f"{'accuracy':>12}{'':>12}{'':>12}{accuracy:>12.4f}{len(y_true):>12}")
    lines.append(f"{'macro avg':>12}{macro_precision:>12.4f}{macro_recall:>12.4f}{macro_f1:>12.4f}{len(y_true):>12}")
    lines.append(f"{'weighted avg':>12}{weighted_precision:>12.4f}{weighted_recall:>12.4f}{weighted_f1:>12.4f}{len(y_true):>12}")
    return "\n".join(lines)

file_path = ".\\diabetes.csv"

df = pd.read_csv(file_path)

# Expected columns for Pima Indians Diabetes dataset
expected_cols = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

# Fix header issue if needed
if list(df.columns) != expected_cols and len(df.columns) == 9:
    if df.columns[0] != "Pregnancies":
        df = pd.read_csv(file_path, header=None, names=expected_cols)

zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

X = df.drop("Outcome", axis=1).copy()
y = df["Outcome"].copy()

test_random_states = [42, 7, 99]   # few different test data sets
all_metrics = []

print("\nPima Indians Diabetes : Gaussian Naive Bayes")
print("=" * 60)

for split_no, rs in enumerate(test_random_states, start=1):
    print(f"\nTEST DATA SET {split_no}  (random_state = {rs})")
    print("-" * 60)

    X_train, X_test, y_train, y_test = stratified_train_test_split(
        X, y,
        test_size=0.2,
        random_state=rs
    )

    # Replace zero values using training-set medians only
    for col in zero_as_missing:
        train_median = X_train[col].replace(0, np.nan).median()
        X_train[col] = X_train[col].replace(0, np.nan).fillna(train_median)
        X_test[col] = X_test[col].replace(0, np.nan).fillna(train_median)

    # Train Gaussian Naive Bayes
    model = GaussianNBManual()
    model.fit(X_train, y_train)

    # Predict on this test set
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    # Confusion matrix and metrics
    cm = confusion_matrix_manual(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0

    all_metrics.append((accuracy, precision, recall))

    print("Confusion Matrix:")
    print(cm)
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")

    print("\nClassification Report:")
    print(classification_report_manual(y_test, y_pred, zero_division=0))

    # Show a few test rows from this test set
    results = X_test.copy()
    results["Actual"] = y_test.values
    results["Predicted"] = y_pred
    results["P(Non-Diabetic=0)"] = y_prob[:, 0]
    results["P(Diabetic=1)"] = y_prob[:, 1]

    print("\nFew test data predictions:")
    print(results.head(5))

# Average metrics over all test data sets
avg_accuracy = np.mean([m[0] for m in all_metrics])
avg_precision = np.mean([m[1] for m in all_metrics])
avg_recall = np.mean([m[2] for m in all_metrics])

print("\n" + "=" * 60)
print("AVERAGE PERFORMANCE OVER FEW TEST DATA SETS")
print("=" * 60)
print(f"Average Accuracy : {avg_accuracy:.4f}")
print(f"Average Precision: {avg_precision:.4f}")
print(f"Average Recall   : {avg_recall:.4f}")