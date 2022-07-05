#======================================== MAIN ======================================== # 
# This is the main app. Main user interface will be supplied here.                      #
#====================================================================================== # 


from generate.generate import generate_graph
import networkx as nx
import snap
import matplotlib.pyplot as plt
import numpy as np
import argparse
import timeit
from preprocess.properties import graph_prop, cluster_props
from preprocess.process import kmean, get_subgraph_cluster, louvain, propagation, shrink_graph

def main(args): 
    # ---------Loading in File---------
    file = open(args['file'], 'r')
    data_edge_list = nx.read_edgelist(file)

    mapping = {old_label:new_label for new_label, old_label in enumerate(data_edge_list.nodes())}
    data_edge_list = nx.relabel_nodes(data_edge_list, mapping)

    # shrink_graph(data_edge_list, 100000)      # Initial Stages to format dataset
    # ---------Clustering Options---------
    options = "1. Louvain\n2. KMeans\n3. Propagation\n4. List Graph Properties\n"
    userInput = input(f"Cluster Algorithm: [Enter: 1,2,3,..]\n{options}")
    if(userInput == "1"):
        dendogram, df_aggregate = louvain(nx.adjacency_matrix(data_edge_list))
    elif(userInput == "2"):
        clusters = input("Clusters for KMeans: [Enter: 1,2,3,..]\n")
        dendogram, df_aggregate = kmean(nx.adjacency_matrix(data_edge_list), int(clusters))
    elif(userInput == "3"):
        dendogram, df_aggregate = propagation(nx.adjacency_matrix(data_edge_list))
    elif(userInput == "4"):
        graph = snap.LoadEdgeList(snap.TNGraph, args['file'], 0, 1)
        graph = graph.ConvertGraph(snap.TNGraph, True)
        graph.PrintInfo("Original Python type TNEANet")
        graph_prop(graph)
        return

    labels_unique, counts = np.unique(dendogram, return_counts=True)
    print(f"number of clusters: {str(len(set(dendogram)))}\n nodes per clusters: {counts}")

    # ---------Graph Properties---------
    graph = snap.LoadEdgeList(snap.TNGraph, args['file'], 0, 1)
    graph = graph.ConvertGraph(snap.TNGraph, True)

    userInput = input(f"New graph size (Number of Nodes): [Enter: 1,2,3,..]\n")

    new_graph = generate_graph(graph, dendogram,int(userInput),df_aggregate)

    graph.PrintInfo("Original Python type TNEANet")
    graph_prop(graph)

    new_graph.SaveEdgeList("test.txt", "Save as tab-separated list of edges")

    new_graph.PrintInfo("Synthetic Python type TNEANet")
    graph_prop(new_graph)

    file.close   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments to add to SGG:')

    # test.txt for smaller dataset // Amazon0302.txt for original
    parser.add_argument('-file', default="dataset/1k.txt",help='File to propogate. \n')
    args = parser.parse_args()
    main(vars(args))