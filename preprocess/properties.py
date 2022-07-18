import networkx as nx
from preprocess.process import get_edge_list, get_subgraph_cluster
import snap
import numpy as np
import pandas as pd
from time import sleep
import os

def graph_prop(graph):
    CntV = graph.GetWccSzCnt()
    print("  Weakly Connected Components:")
    for p in CntV:
        print("    size %d: number of similar components %d" % (p.GetVal1(), p.GetVal2()))
    print(f"  diameter of G: {graph.GetBfsFullDiam(100)}")
    print(f"  count the number of triads in G: {graph.GetTriads()}")
    print(f"  clustering coefficient: {graph.GetClustCf()}")

def cluster_props(graph, dendrogram):
    # Get graph props of x cluster
    clusters = np.unique(dendrogram)
    for x in clusters:
        graph_cluster = get_subgraph_cluster(dendrogram, get_edge_list(graph), x)
        snap_subgraph = graph.GetSubGraph(list(map(int, graph_cluster)))
        snap_subgraph.PrintInfo(f"Python subgraph {x}")
        graph_prop(snap_subgraph)