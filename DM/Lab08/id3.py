from __future__ import annotations

import math
import csv
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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


def id3(
    rows: List[Dict[str, Any]],
    attributes: List[str],
    target: str,
    depth: int = 0,
    verbose: bool = True,
) -> Node:
    labels = [row[target] for row in rows]
    current_majority = majority_class(rows, target)

    if len(set(labels)) == 1:
        if verbose:
            print("  " * depth + f"Leaf -> {labels[0]}")
        return Node(label=labels[0], majority_class=labels[0])

    if not attributes:
        if verbose:
            print("  " * depth + f"Leaf (majority) -> {current_majority}")
        return Node(label=current_majority, majority_class=current_majority)

    gains = {attr: information_gain(rows, attr, target) for attr in attributes}
    best_attr = max(sorted(attributes), key=lambda a: (gains[a], a))

    if verbose:
        print("  " * depth + f"Current set size = {len(rows)}")
        print("  " * depth + f"Class counts     = {dict(Counter(labels))}")
        print("  " * depth + f"Entropy          = {entropy(labels):.4f}")
        print("  " * depth + "Information Gain:")
        for attr in attributes:
            print("  " * depth + f"  {attr:12s} -> {gains[attr]:.4f}")
        print("  " * depth + f"Best attribute   = {best_attr}\n")

    node = Node(attribute=best_attr, majority_class=current_majority)
    values = sorted({row[best_attr] for row in rows})
    remaining_attrs = [attr for attr in attributes if attr != best_attr]

    for value in values:
        subset = [row for row in rows if row[best_attr] == value]
        if not subset:
            node.children[value] = Node(label=current_majority, majority_class=current_majority)
        else:
            if verbose:
                print("  " * depth + f"Branch: {best_attr} = {value}")
            node.children[value] = id3(subset, remaining_attrs, target, depth + 1, verbose)

    return node


def print_tree(node: Node, indent: str = "") -> None:
    if node.is_leaf():
        print(indent + f"-> {node.label}")
        return

    print(indent + f"[{node.attribute}]")
    for value, child in node.children.items():
        print(indent + f"  {node.attribute} = {value}")
        print_tree(child, indent + "    ")


def print_rules(node: Node, target_name: str, conditions: Optional[List[str]] = None) -> None:
    if conditions is None:
        conditions = []

    if node.is_leaf():
        rule = " AND ".join(conditions) if conditions else "TRUE"
        print(f"IF {rule} THEN {target_name} = {node.label}")
        return

    for value, child in node.children.items():
        print_rules(child, target_name, conditions + [f"{node.attribute} = {value}"])


def load_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def main() -> None:
    file_path = ".\\PlayBall.csv"
    data = load_csv(file_path)
    target = "Play ball"
    attributes = ["Outlook", "Temperature", "Humidity", "Wind"]
    print("ID3 DECISION TREE USING CSV DATA")
    base_entropy = entropy([row[target] for row in data])
    print(f"\nEntropy(S) = {base_entropy:.4f}\n")
    tree = id3(data, attributes, target, verbose=True)
    print("\nFINAL DECISION TREE")
    print_tree(tree)
    print("\nRULES")
    print_rules(tree, target)

if __name__ == "__main__":
    main()