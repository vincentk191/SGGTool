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

    return labels, df

def get_subgraph_cluster(dendrogram, nodelist, cluster):
    indices = []
    for i,x in enumerate(dendrogram):
        if x == cluster:
            indices.append(i)
    res_list = [nodelist[i] for i in indices]
    return res_list

def get_edge_list(graph): 
    edge_list = []
    for node in graph.Nodes():
        edge_list.append(node.GetId())
    return edge_list

def plot_graph(G):
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)

    fig = plt.figure("Degree Distribution", figsize=(8, 8))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 4)

    #=======DRAWS NODES & EDGES=======#
    # ax0 = fig.add_subplot(axgrid[0:3, :])
    # Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    # pos = nx.spring_layout(Gcc, seed=10396953)
    # nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
    # nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
    # ax0.set_title("Connected components of G")
    # ax0.set_axis_off()

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()

def shrink_graph(data_edge_list, size):
    i = len(data_edge_list.nodes) - 1
    while(i >= size):
        data_edge_list.remove_node(i)
        i = i - 1
    nx.write_edgelist(data_edge_list, f"dataset/{size}k.txt", delimiter=' ')
