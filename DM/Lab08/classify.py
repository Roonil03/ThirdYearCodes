from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Node:
    attribute: Optional[str] = None
    label: Optional[str] = None
    majority_class: Optional[str] = None
    children: Dict[Any, "Node"] = field(default_factory=dict)
    def is_leaf(self) -> bool:
        return self.label is not None


def entropy(labels: List[str]) -> float:
    total = len(labels)
    if total == 0:
        return 0.0
    counts = Counter(labels)
    ent = 0.0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent


def majority_class(rows: List[Dict[str, Any]], target: str) -> str:
    counts = Counter(row[target] for row in rows)
    return counts.most_common(1)[0][0]


def information_gain(rows: List[Dict[str, Any]], attribute: str, target: str) -> float:
    total_entropy = entropy([row[target] for row in rows])
    values = sorted({row[attribute] for row in rows})
    weighted_entropy = 0.0
    for value in values:
        subset = [row for row in rows if row[attribute] == value]
        weighted_entropy += (len(subset) / len(rows)) * entropy([row[target] for row in subset])
    return total_entropy - weighted_entropy


def id3(rows: List[Dict[str, Any]], attributes: List[str], target: str) -> Node:
    labels = [row[target] for row in rows]
    current_majority = majority_class(rows, target)
    if len(set(labels)) == 1:
        return Node(label=labels[0], majority_class=labels[0])
    if not attributes:
        return Node(label=current_majority, majority_class=current_majority)
    gains = {attr: information_gain(rows, attr, target) for attr in attributes}
    best_attr = max(sorted(attributes), key=lambda a: (gains[a], a))
    node = Node(attribute=best_attr, majority_class=current_majority)
    values = sorted({row[best_attr] for row in rows})
    remaining_attrs = [attr for attr in attributes if attr != best_attr]
    for value in values:
        subset = [row for row in rows if row[best_attr] == value]
        if not subset:
            node.children[value] = Node(label=current_majority, majority_class=current_majority)
        else:
            node.children[value] = id3(subset, remaining_attrs, target)
    return node


def print_rules(node: Node, target_name: str, conditions: Optional[List[str]] = None) -> None:
    if conditions is None:
        conditions = []
    if node.is_leaf():
        rule = " AND ".join(conditions) if conditions else "TRUE"
        print(f"IF {rule} THEN {target_name} = {node.label}")
        return
    for value, child in node.children.items():
        print_rules(child, target_name, conditions + [f"{node.attribute} = {value}"])


def predict(node: Node, sample: Dict[str, Any]) -> str:
    current = node
    while not current.is_leaf():
        attr = current.attribute
        value = sample.get(attr)
        if value not in current.children:
            return current.majority_class
        current = current.children[value]
    return current.label  # type: ignore


def predict_with_trace(node: Node, sample: Dict[str, Any]) -> Tuple[str, List[str]]:
    current = node
    trace = []
    while not current.is_leaf():
        attr = current.attribute
        value = sample.get(attr)
        trace.append(f"{attr} = {value}")
        if value not in current.children:
            trace.append(f"(unseen value, fallback to majority class = {current.majority_class})")
            return current.majority_class, trace
        current = current.children[value]
    trace.append(f"Predicted class = {current.label}")
    return current.label, trace


def main() -> None:
    data = [
        {"Day": "D1",  "Outlook": "Sunny",    "Temperature": "Hot",  "Humidity": "High",   "Wind": "Weak",   "Play ball": "No"},
        {"Day": "D2",  "Outlook": "Sunny",    "Temperature": "Hot",  "Humidity": "High",   "Wind": "Strong", "Play ball": "No"},
        {"Day": "D3",  "Outlook": "Overcast", "Temperature": "Hot",  "Humidity": "High",   "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D4",  "Outlook": "Rain",     "Temperature": "Mild", "Humidity": "High",   "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D5",  "Outlook": "Rain",     "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D6",  "Outlook": "Rain",     "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play ball": "No"},
        {"Day": "D7",  "Outlook": "Overcast", "Temperature": "Cool", "Humidity": "Normal", "Wind": "Strong", "Play ball": "Yes"},
        {"Day": "D8",  "Outlook": "Sunny",    "Temperature": "Mild", "Humidity": "High",   "Wind": "Weak",   "Play ball": "No"},
        {"Day": "D9",  "Outlook": "Sunny",    "Temperature": "Cool", "Humidity": "Normal", "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D10", "Outlook": "Rain",     "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D11", "Outlook": "Sunny",    "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong", "Play ball": "Yes"},
        {"Day": "D12", "Outlook": "Overcast", "Temperature": "Mild", "Humidity": "High",   "Wind": "Strong", "Play ball": "Yes"},
        {"Day": "D13", "Outlook": "Overcast", "Temperature": "Hot",  "Humidity": "Normal", "Wind": "Weak",   "Play ball": "Yes"},
        {"Day": "D14", "Outlook": "Rain",     "Temperature": "Mild", "Humidity": "High",   "Wind": "Strong", "Play ball": "No"},
    ]

    target = "Play ball"
    attributes = [col for col in data[0].keys() if col != target]
    tree = id3(data, attributes, target)
    print("=" * 60)
    print("RULES OBTAINED FROM THE DECISION TREE")
    print("=" * 60)
    print_rules(tree, target)
    print("\n" + "=" * 60)
    print("CLASSIFYING NEW SAMPLES")
    print("=" * 60)

    new_samples = [
        {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High",   "Wind": "Strong"},
        {"Outlook": "Rain",  "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak"},
        {"Outlook": "Overcast", "Temperature": "Hot", "Humidity": "High", "Wind": "Strong"},
    ]

    for i, sample in enumerate(new_samples, start=1):
        prediction, trace = predict_with_trace(tree, sample)
        print(f"\nSample {i}: {sample}")
        for step in trace:
            print("  " + step)
        print(f"  Final classification: {prediction}")

    print("\n" + "=" * 60)
    print("INTERACTIVE CLASSIFICATION")
    print("=" * 60)
    print("Enter a new sample using the following values:")
    print("Outlook     : Sunny / Overcast / Rain")
    print("Temperature : Hot / Mild / Cool")
    print("Humidity    : High / Normal")
    print("Wind        : Weak / Strong")
    sample = {
        "Outlook": input("Outlook: ").strip(),
        "Temperature": input("Temperature: ").strip(),
        "Humidity": input("Humidity: ").strip(),
        "Wind": input("Wind: ").strip(),
    }
    prediction, trace = predict_with_trace(tree, sample)
    print("\nDecision path:")
    for step in trace:
        print("  " + step)
    print(f"\nPredicted class for your sample: {prediction}")


if __name__ == "__main__":
    main()