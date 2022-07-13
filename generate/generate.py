import numpy as np
from preprocess.process import get_subgraph_cluster
from preprocess.properties import get_edge_list
import snap
import pandas as pd

#================================== GRAPH GENERATION ================================== # 
# All high level functions for generation will be handled here                          #
#====================================================================================== # 

def generate_graph(graph, dendogram, num_nodes, df_aggregate):
#=========SETUP VARIABLES=========#
    total_nodes = len(dendogram)
    new_graph = snap.ConvertGraph(type(graph), graph)

    df_aggregate_temp = df_aggregate.copy()
    np.fill_diagonal(df_aggregate_temp.values, 0)
    labels_unique, counts = np.unique(dendogram, return_counts=True)

    # Form probability distribution of nodes in clusters
    cluster_distribution = [count / total_nodes for count in counts]
    
    # Form probability distribution of edges between clusters
    df_aggregate_temp = df_aggregate_temp.div(df_aggregate_temp.sum(axis=1), axis=0)
    
    new_nodes = []
    for i in range(total_nodes, num_nodes):
        new_nodes.append(i)
#==================================#
    
    for node in new_nodes:
    #============ADD NODE==============#
        new_graph.AddNode(node)
    #==================================#

    #========CLUSTER ASSIGNMENT========#
        # Sample from cluster probability distribution
        cluster_assignment = np.random.choice(labels_unique, p=cluster_distribution)
    #==================================#

    #========BETWEEN  CLUSTERS=========#
        ### Decide which clusters to form edges with
        cluster = cluster_assignment
        # Sample from probability distribution
        b_cluster = np.random.choice(labels_unique, p=df_aggregate_temp.iloc[cluster])

        ### Decide whether an edge should indeed be formed
        edges_cluster_b_cluster = int(df_aggregate.iloc[[cluster],[cluster,b_cluster]].sum(axis=1)) 
        edges_to_b_cluster = df_aggregate.iloc[cluster][b_cluster]
        prob = edges_to_b_cluster/edges_cluster_b_cluster
        edges_b_cluster = np.random.choice([True, False], p=[prob, 1 - prob])
    #==================================#

    ##=========WITHIN CLUSTERS==========#
        graph_cluster = get_subgraph_cluster(dendogram, get_edge_list(graph), cluster)
        cluster_graph = graph.GetSubGraph(list(map(int, graph_cluster)))
        OutDegToCntV = cluster_graph.GetOutDegCnt()
        InDegToCntV = cluster_graph.GetInDegCnt()

        # Ensures that no isolated nodes exist 
        edges_w_clusters = 0
        edges_w_clusters_in = 0
        while(edges_w_clusters + edges_w_clusters_in == 0):
            out_degrees = []
            counts = []
            for item in OutDegToCntV:
                out_degrees.append(item.GetVal1())
                counts.append(item.GetVal2())

            sum_counts = sum(counts)
            counts_distribution = [count / sum_counts for count in counts]

            # Sample from probability distribution
            edges_w_clusters = np.random.choice(out_degrees, p=counts_distribution)

            in_degrees = []
            counts = []

            for item in InDegToCntV:
                in_degrees.append(item.GetVal1())
                counts.append(item.GetVal2())

            sum_counts = sum(counts)
            counts_distribution = [count / sum_counts for count in counts]

            # Sample from probability distribution
            edges_w_clusters_in = np.random.choice(in_degrees, p=counts_distribution)
    # #==================================#

    #============ADD EDGES=============#
        # If edges between cluster exist, add the edge to other cluster
        if(edges_b_cluster):
            graph_b_cluster = get_subgraph_cluster(dendogram, get_edge_list(graph), b_cluster)
            other_node = int(np.random.choice(graph_b_cluster))
            new_graph.AddEdge(node, other_node)
        
        # Find nodes to connect to that are in the same cluster
        # np.setdiff1d - ensures no self-cycles are present
        used_nodes = [node]
        for i in range(0, edges_w_clusters):
            other_node = int(np.random.choice(np.setdiff1d(graph_cluster, used_nodes)))
            used_nodes.append(other_node)
            new_graph.AddEdge(node ,other_node)

        used_nodes = [node]
        for i in range(0, edges_w_clusters_in):
            other_node = int(np.random.choice(np.setdiff1d(graph_cluster, used_nodes)))
            used_nodes.append(other_node)
            new_graph.AddEdge(other_node ,node)
    #==================================#
    return new_graph