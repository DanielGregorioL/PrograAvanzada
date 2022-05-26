""" This module implements a number of iterator building blocks"""
import itertools
import pickle
import networkx as nx


def token(graph1, k):
    """
       Construct the k-token graph of a graph graph1
       ----------
       graph1: Graph
       k : Integer

       Returns
       --------
           The k-token graph of graph1
    """
    token_graph = nx.Graph()
    vertices_number = len(graph1.nodes())
    vertices = set(range(vertices_number))
    tuples = list(itertools.combinations(vertices, k))
    vert = []
    for element in tuples:
        vert.append(set(element))
    token_graph.add_nodes_from(list(range(0, len(vert))))

    for number1, element_1 in enumerate(vert):
        for number2, element_2 in enumerate(vert):
            arista = element_1 ^ element_2
            if len(arista) == 2:
                ari = list(arista)
                arist = (ari[0], ari[1])
                if arist in graph1.edges():
                    token_graph.add_edge(number1, number2)
    return token_graph


def connectivity(graph1):
    """
       determine the algebraic connectivity of graph1, and also
       the algebraic connectivity of 2-token graph of graph1
       ----------
       graph1: Graph

       Returns
       --------
           A list [a, b] with the algebraic connectivity of graph1 (a) and its
           k-token graph (b)
    """
    algebraic_1 = nx.algebraic_connectivity(graph1, method='lanczos')
    algebraic_2 = nx.algebraic_connectivity(token(graph1, 2), method='lanczos')
    list_algebraic = [algebraic_1, algebraic_2]
    return list_algebraic


data = []
for j in range(4, 8):
    cycle = nx.cycle_graph(j)
    data.append(connectivity(cycle))
print(data)
list_string = pickle.dumps(data)
print(list_string)

recover_list = pickle.loads(list_string)
print(recover_list)

with open("data.txt", "wb") as file_1:
    pickle.dump(data, file_1)

with open("data.txt", "rb") as file_1:
    data_2 = pickle.load(file_1)
    print(data_2)
