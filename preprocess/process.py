import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from sknetwork.clustering import KMeans
from sknetwork.clustering import Louvain
from sknetwork.clustering import PropagationClustering
from sknetwork.utils import membership_matrix
from sknetwork.linalg import normalize
import numpy as np

def kmean(data, n_clusters):
    kmeans = KMeans(n_clusters)
    labels = kmeans.fit_transform(data)
    average = normalize(membership_matrix(labels).T)
    adjacency_aggregate = kmeans.aggregate_
    df = pd.DataFrame(data=adjacency_aggregate.toarray())
    return labels, df

def louvain(data): 
    cluster = Louvain()
    labels = cluster.fit_transform(data)
    average = normalize(membership_matrix(labels).T)
    adjacency_aggregate = cluster.aggregate_
    df = pd.DataFrame(data=adjacency_aggregate.toarray())
    print(adjacency_aggregate)
    return labels, df

def propagation(data): 
    cluster = PropagationClustering()
    labels = cluster.fit_transform(data)
    average = normalize(membership_matrix(labels).T)
    adjacency_aggregate = cluster.aggregate_
    df = pd.DataFrame(data=adjacency_aggregate.toarray())
    print(adjacency_aggregate)
    print(df)

    return labels, df

def get_subgraph_cluster(dendogram, nodelist, cluster):
    indices = []
    for i,x in enumerate(dendogram):
        if x == cluster:
            indices.append(i)
    res_list = [nodelist[i] for i in indices]
    return res_list

def shrink_graph(data_edge_list, size):
    i = len(data_edge_list.nodes) - 1
    while(i > size):
        data_edge_list.remove_node(i)
        i = i - 1
    nx.write_edgelist(data_edge_list, f"dataset/{size}k.txt", delimiter=' ')
