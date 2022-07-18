# SGGTool

This repository provides a preliminary design and implementation of an SGG tool using clustering algorithms to create pre-defined clusters as a basis for the propagation of the graph. 
## How to install dependencies
Since the project runs on mainly python it is important that Python version 3.8.3 or higher is installed before proceeding with the following commands:
```
$ pip install -r requirements.txt
```
## How to select initial file
Use the -file tag when running the main.py script as such:
```
$ python main.py -file filename.txt
```
## Generation Options
After providing the initial graph to scale, 3 options are given to continue to clustering the graph, listing the properties, or plotting the current graph. Simply enter 1 and proceed to give the number of the corresponding algorithms, e.g 3.
```
Cluster Algorithm: [Enter: 1,2,3]
1. Louvain
2. Kmeans
3. Propagation
$3
```
## Scaling Sizes
The scale size input receives the new size of the synthetic graph and NOT the number of nodes to add to the current graph.
```
New graph size (Number of Nodes): [Enter: 1,2,3,..]
$ 5000
```



