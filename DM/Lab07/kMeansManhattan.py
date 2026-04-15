import pandas as pd
import random

file_path = ".\\IrisDataset.csv"
data = pd.read_csv(file_path)
X = data.iloc[:,0:4].values.tolist()
k = 3
max_iter = 100
centroids = random.sample(X, k)

def manhattan(p1, p2):
    return sum(abs(a-b) for a,b in zip(p1,p2))

for _ in range(max_iter):
    clusters = [[] for _ in range(k)]
    for point in X:
        distances = [manhattan(point, c) for c in centroids]
        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(point)
    new_centroids = []
    for cluster in clusters:
        centroid = [sum(dim)/len(cluster) for dim in zip(*cluster)]
        new_centroids.append(centroid)
    if new_centroids == centroids:
        break
    centroids = new_centroids

print("Final Centroids:\n")
for c in centroids:
    print(c)

print("\nCluster Sizes:\n")
for i,cluster in enumerate(clusters):
    print("Cluster",i+1,"=",len(cluster),"points")