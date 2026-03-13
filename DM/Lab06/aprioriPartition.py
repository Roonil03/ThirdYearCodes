from itertools import combinations

file_url = "D:\\230911172_DM\\Lab06\\GroceriesDataset.csv"

transactions = []
with open(file_url) as f:
    next(f)
    for line in f:
        transactions.append(set(line.strip().split(",")))

num_transactions = len(transactions)
min_support = 0.02
min_confidence = 0.3
partition_size = 2000
min_support_count = min_support * num_transactions

def support_count(itemset, dataset):
    count = 0
    for transaction in dataset:
        if itemset.issubset(transaction):
            count += 1
    return count

def apriori_partition(dataset, min_support_local):
    items = set()
    for transaction in dataset:
        for item in transaction:
            items.add(frozenset([item]))
    freq_itemsets = set()
    L1 = set()
    for item in items:
        if support_count(item, dataset) >= min_support_local:
            L1.add(item)
    freq_itemsets |= L1
    Lk = L1
    k = 2
    while Lk:
        candidates = set()
        Lk_list = list(Lk)
        for i in range(len(Lk_list)):
            for j in range(i+1, len(Lk_list)):
                union = Lk_list[i] | Lk_list[j]
                if len(union) == k:
                    candidates.add(union)
        new_Lk = set()
        for candidate in candidates:
            if support_count(candidate, dataset) >= min_support_local:
                new_Lk.add(candidate)
        freq_itemsets |= new_Lk
        Lk = new_Lk
        k += 1
    return freq_itemsets

partitions = []
for i in range(0, num_transactions, partition_size):
    partitions.append(transactions[i:i+partition_size])

print("Total partitions:", len(partitions))

candidate_itemsets = set()
for partition in partitions:
    local_support = min_support * len(partition)
    local_freq = apriori_partition(partition, local_support)
    candidate_itemsets |= local_freq

print("Candidate itemsets from partitions:", len(candidate_itemsets))

global_frequent = {}
for itemset in candidate_itemsets:
    count = support_count(itemset, transactions)
    if count >= min_support_count:
        global_frequent[itemset] = count / num_transactions

print("\nFrequent Itemsets:\n")
for itemset, support in global_frequent.items():
    print(set(itemset), "Support:", round(support,3))

print("\nAssociation Rules:\n")

for itemset in global_frequent:
    if len(itemset) < 2:
        continue
    for i in range(1, len(itemset)):
        for antecedent in combinations(itemset, i):
            antecedent = frozenset(antecedent)
            consequent = itemset - antecedent
            sup_item = global_frequent[itemset]
            sup_ant = global_frequent.get(
                antecedent,
                support_count(antecedent, transactions) / num_transactions
            )
            sup_con = global_frequent.get(
                consequent,
                support_count(consequent, transactions) / num_transactions
            )
            confidence = sup_item / sup_ant
            lift = confidence / sup_con
            if confidence >= min_confidence:
                print(
                    set(antecedent),
                    "->",
                    set(consequent),
                    "| Support:", round(sup_item,3),
                    "| Confidence:", round(confidence,3),
                    "| Lift:", round(lift,3)
                )