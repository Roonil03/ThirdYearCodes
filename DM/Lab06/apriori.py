import pandas as pd
from itertools import combinations

file_path = ".\\GroceriesDataset.csv"
transactions = []
with open(file_path) as f:
    for line in f:
        transactions.append(line.strip().split(","))
num_transactions = len(transactions)

def get_support(itemset):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count / num_transactions

def generate_candidates(prev_freq_itemsets, k):
    candidates = set()
    prev_list = list(prev_freq_itemsets)
    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union_set = prev_list[i].union(prev_list[j])
            if len(union_set) == k:
                candidates.add(frozenset(union_set))
    return candidates

min_support = 0.02
min_confidence = 0.3

items = set()
for transaction in transactions:
    for item in transaction:
        items.add(frozenset([item]))
freq_itemsets = {}
L1 = set()
for item in items:
    support = get_support(item)
    if support >= min_support:
        L1.add(item)
        freq_itemsets[item] = support
Lk = L1
k = 2

while Lk:
    candidates = generate_candidates(Lk, k)
    new_Lk = set()
    for candidate in candidates:
        support = get_support(candidate)
        if support >= min_support:
            new_Lk.add(candidate)
            freq_itemsets[candidate] = support
    Lk = new_Lk
    k += 1

print("Frequent Itemsets:\n")
for itemset, support in freq_itemsets.items():
    print(set(itemset), "Support:", round(support, 3))

print("\nAssociation Rules:\n")
for itemset in freq_itemsets:
    if len(itemset) < 2:
        continue
    for i in range(1, len(itemset)):
        for antecedent in combinations(itemset, i):
            antecedent = frozenset(antecedent)
            consequent = itemset - antecedent
            support_itemset = freq_itemsets[itemset]
            support_antecedent = freq_itemsets.get(antecedent, get_support(antecedent))
            support_consequent = freq_itemsets.get(consequent, get_support(consequent))
            confidence = support_itemset / support_antecedent
            lift = confidence / support_consequent
            if confidence >= min_confidence:
                print(
                    set(antecedent), "->", set(consequent),
                    "| Support:", round(support_itemset,3),
                    "| Confidence:", round(confidence,3),
                    "| Lift:", round(lift,3)
                )