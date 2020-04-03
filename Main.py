import tsplib95 as tsp
import networkx as nx
# from numpy import *
from AntColonyOptimization import AntColonyOptimization

def readNet(fileName):
    f = open(fileName, "r")
    net = {}
    n = int(f.readline())
    net['noNodes'] = n
    mat = []
    for i in range(n):
        mat.append([])
        line = f.readline()
        elems = line.split(",")
        for j in range(n):
            mat[-1].append(int(elems[j]))
    net["mat"] = mat
    f.close()
    return net

def read_tsp_file(file_name):
    tsp_problem = tsp.load_problem(file_name)
    g = tsp_problem.get_graph()
    number_of_cities = len(g.nodes())
    matrix = nx.to_numpy_matrix(g)
    graph = []
    net={}
    for i in range(number_of_cities):
        graph.append([])
        for j in range(number_of_cities):
            value = matrix.item((i, j))
            if value == 0:
                value += 1
            graph[i].append(value)
    net['noNodes']=number_of_cities
    net['mat']=graph
    return net

net=read_tsp_file("150p_eil51.txt")
#net=readNet("100p_fricker26.txt")
#net=readNet("50p_easy_01_tsp.txt")
# net=readNet("50p_medium_01_tsp.txt")
#net=readNet("50p_hard_01_tsp.txt")
acoParam={'c':1.0,'alpha':1,'beta':5,'evaporation':0.5,'Q':500,'antFactor':0.8, 'randomFactor':0.01}
problParam={'noOfCities':net['noNodes'], 'maxIterations':50}
aco=AntColonyOptimization(net['mat'],acoParam,problParam)
aco.solve()
