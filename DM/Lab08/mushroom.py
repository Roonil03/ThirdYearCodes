from __future__ import annotations

import math
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

UCI_DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"

COLUMNS = [
    "class",
    "cap-shape",
    "cap-surface",
    "cap-color",
    "bruises",
    "odor",
    "gill-attachment",
    "gill-spacing",
    "gill-size",
    "gill-color",
    "stalk-shape",
    "stalk-root",
    "stalk-surface-above-ring",
    "stalk-surface-below-ring",
    "stalk-color-above-ring",
    "stalk-color-below-ring",
    "veil-type",
    "veil-color",
    "ring-number",
    "ring-type",
    "spore-print-color",
    "population",
    "habitat",
]

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
    base_entropy = entropy([row[target] for row in rows])
    values = {row[attribute] for row in rows}
    weighted_entropy = 0.0
    for value in values:
        subset = [row for row in rows if row[attribute] == value]
        weighted_entropy += (len(subset) / len(rows)) * entropy([row[target] for row in subset])
    return base_entropy - weighted_entropy

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
    remaining_attrs = [attr for attr in attributes if attr != best_attr]
    for value in sorted({row[best_attr] for row in rows}):
        subset = [row for row in rows if row[best_attr] == value]
        if not subset:
            node.children[value] = Node(label=current_majority, majority_class=current_majority)
        else:
            node.children[value] = id3(subset, remaining_attrs, target)
    return node

def predict(node: Node, sample: Dict[str, Any]) -> str:
    current = node
    while not current.is_leaf():
        attr = current.attribute
        value = sample.get(attr)
        if value not in current.children:
            return current.majority_class
        current = current.children[value]
    return current.label

def accuracy(node: Node, rows: List[Dict[str, Any]], target: str) -> float:
    correct = 0
    for row in rows:
        if predict(node, row) == row[target]:
            correct += 1
    return correct / len(rows)

def count_nodes(node: Node) -> int:
    if node.is_leaf():
        return 1
    return 1 + sum(count_nodes(child) for child in node.children.values())

def count_leaves(node: Node) -> int:
    if node.is_leaf():
        return 1
    return sum(count_leaves(child) for child in node.children.values())

def print_tree(node: Node, indent: str = "", max_depth: int = 3, current_depth: int = 0) -> None:
    if node.is_leaf():
        print(indent + f"-> {node.label}")
        return
    print(indent + f"[{node.attribute}]")
    if current_depth >= max_depth:
        print(indent + "  ... (tree truncated for display)")
        return
    for value, child in node.children.items():
        print(indent + f"  {node.attribute} = {value}")
        print_tree(child, indent + "    ", max_depth, current_depth + 1)

def tree_to_dot(root: Node, target_name: str = "class") -> str:
    lines = [
        "digraph MushroomTree {",
        'rankdir=TB;',
        'node [shape=box, style="rounded,filled", fontname="Helvetica"];',
        'edge [fontname="Helvetica"];'
    ]
    counter = 0

    def walk(node: Node) -> str:
        nonlocal counter
        node_id = f"n{counter}"
        counter += 1

        if node.is_leaf():
            color = "palegreen" if node.label == "edible" else "lightcoral"
            label = f"{target_name} = {node.label}"
            lines.append(f'{node_id} [label="{label}", fillcolor="{color}"];')
        else:
            label = f"{node.attribute}\\nmajority={node.majority_class}"
            lines.append(f'{node_id} [label="{label}", fillcolor="lightblue"];')
            for value, child in node.children.items():
                child_id = walk(child)
                lines.append(f'{node_id} -> {child_id} [label="{value}"];')
        return node_id

    walk(root)
    lines.append("}")
    return "\n".join(lines)

def ensure_local_dataset() -> Path:
    base_dir = Path.cwd()
    base_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = base_dir / "mushrooms.csv"
    if dataset_path.exists():
        print(f"Using existing local dataset: {dataset_path}")
        return dataset_path
    print("Local dataset not found. Downloading from UCI...")
    try:
        urllib.request.urlretrieve(UCI_DATA_URL, dataset_path)
        print(f"Dataset downloaded successfully to: {dataset_path}")
        return dataset_path
    except Exception as e:
        raise RuntimeError(
            f"Could not download dataset automatically.\n"
            f"Error: {e}\n\n"
            f"Manual fix:\n"
            f"1. Open this URL in your browser:\n"
            f"   {UCI_DATA_URL}\n"
            f"2. Save the file as:\n"
            f"   {dataset_path}\n"
            f"3. Run the script again."
        ) from e

def load_dataset() -> pd.DataFrame:
    dataset_path = ensure_local_dataset()
    df = pd.read_csv(dataset_path, header=None, names=COLUMNS)
    df = df.replace("?", "missing")
    df["class"] = df["class"].map({"e": "edible", "p": "poisonous"})
    return df

def main() -> None:
    print("=" * 60)
    print("LOADING UCI MUSHROOM DATASET")
    print("=" * 60)
    df = load_dataset()
    rows = df.to_dict(orient="records")
    target = "class"
    attributes = [col for col in df.columns if col != target]
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution: {dict(df[target].value_counts())}")
    print("\nBuilding ID3 decision tree...")
    tree = id3(rows, attributes, target)
    print("\n" + "=" * 60)
    print("TREE SUMMARY")
    print("=" * 60)
    print(f"Total nodes      : {count_nodes(tree)}")
    print(f"Leaf nodes       : {count_leaves(tree)}")
    print(f"Training accuracy: {accuracy(tree, rows, target):.4f}")
    print("\n" + "=" * 60)
    print("FIRST FEW LEVELS OF THE TREE")
    print("=" * 60)
    print_tree(tree, max_depth=3)
    dot_text = tree_to_dot(tree, target_name=target)
    dot_path = Path.cwd() / "mushroom_tree.dot"
    with open(dot_path, "w", encoding="utf-8") as f:
        f.write(dot_text)
    print(f"\nGraphviz DOT file written to: {dot_path}")
    print("To render it into an image, run:")
    print("  dot -Tpng mushroom_tree.dot -o mushroom_tree.png")
    sample = rows[0].copy()
    true_class = sample.pop(target)
    predicted = predict(tree, sample)
    print("\nExample classification on first sample:")
    print(f"True class     : {true_class}")
    print(f"Predicted class: {predicted}")

if __name__ == "__main__":
    main()