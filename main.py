#======================================== MAIN ======================================== # 
# This is the main app. Main user interface will be supplied here.                      #
#====================================================================================== # 

from generate.generate import generate_graph
import networkx as nx
import snap
import numpy as np
import argparse
import time
from preprocess.properties import cluster_props, graph_prop
from preprocess.process import kmean, louvain, propagation, shrink_graph, plot_graph

def main(args): 
    # ---------Loading in File---------
    file = open(args['file'], 'r')
    data_edge_list = nx.read_edgelist(file)

    mapping = {old_label:new_label for new_label, old_label in enumerate(data_edge_list.nodes())}
    data_edge_list = nx.relabel_nodes(data_edge_list, mapping)

    # shrink_graph(data_edge_list, 100000)      # Initial Stages to format dataset
    # ---------Clustering Options---------
    options = "1. Cluster\n2. List Graph Properties\n3. Plot graph\n"

    userInput = input(f"User options: [Enter: 1,2,3]\n{options}")
    if(userInput == "1"):
        options = "1. Louvain\n2. KMeans\n3. Propagation\n"
        userInput = input(f"Clustering Algorithms: [Enter: 1,2,3]\n{options}")
        if(userInput == "1"):
            dendrogram, df_aggregate = louvain(nx.adjacency_matrix(data_edge_list))
        elif(userInput == "2"):
            clusters = input("Clusters for KMeans: [Enter: 1,2,3,..]\n")
            dendrogram, df_aggregate = kmean(nx.adjacency_matrix(data_edge_list), int(clusters))
        elif(userInput == "3"):
            dendrogram, df_aggregate = propagation(nx.adjacency_matrix(data_edge_list))
    elif(userInput == "2"):
        graph = snap.LoadEdgeList(snap.TNGraph, args['file'], 0, 1)
        graph = graph.ConvertGraph(snap.TNGraph, True)
        graph.PrintInfo("Original Python type TNEANet")
        graph_prop(graph)
        return
    elif(userInput == "3"):
        plot_graph(data_edge_list)
        return

    labels_unique, counts = np.unique(dendrogram, return_counts=True)
    print(f"number of clusters: {str(len(set(dendrogram)))}\nnodes per clusters: {counts}")

    # ---------Graph Properties---------
    graph = snap.LoadEdgeList(snap.TNGraph, args['file'], 0, 1)
    graph = graph.ConvertGraph(snap.TNGraph, True)

    userInput = input(f"New graph size (Number of Nodes): [Enter: 1,2,3,..]\n")

    start_time = time.time()
    new_graph = generate_graph(graph, dendrogram,int(userInput),df_aggregate)

    print("--- %s seconds ---" % (time.time() - start_time))

    graph.PrintInfo("Original Python type TNEANet")
    graph_prop(graph)


    new_graph.PrintInfo("Synthetic Python type TNEANet")
    graph_prop(new_graph)

    filename = input(f"Synthetic Graph Name: ")
    new_graph.SaveEdgeList(f"synthetic graphs/{filename}.txt", "Save as tab-separated list of edges")

    file.close   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments to add to SGG:')

    # test.txt for smaller dataset // Amazon0302.txt for original
    parser.add_argument('-file', default="dataset/1k.txt",help='File to propogate. \n')
    args = parser.parse_args()
    main(vars(args))