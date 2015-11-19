import sys
import pydot
from suurballe import *


def print_graph(graph, fileName, result=None):
    pydotGraph = pydot.Dot(graph_type='graph')
    size = len(graph)
    for i in range(size):
        for j in range(i, size):
            if graph[i][j] >= 0:
                edge = pydot.Edge(str(i+1), str(j+1))
                edge.set_label(str(graph[i][j]))
                if result != None:
                    if result[i][j] >= 0:
                        edge.set_color('red')
                pydotGraph.add_edge(edge)
    pydotGraph.write_png(fileName)


def print_digraph(digraph, fileName):
    pydotDigraph = pydot.Dot(graph_type='digraph')
    size = len(digraph)
    for i in range(size):
        for j in range(size):
            if digraph[i][j] >= 0:
                edge = pydot.Edge(str(i+1), str(j+1))
                edge.set_label(str(digraph[i][j]))
                pydotDigraph.add_edge(edge)
    pydotDigraph.write_png(fileName);


def read_graph(inputFileName):
    inputFile = open(inputFileName)
    line = inputFile.readline()
    size = int(line)
    graph = [[-1 for x in range(size)] for x in range(size)]
    for line in inputFile:
        values = line.split()
        v1 = int(values[0]) - 1
        v2 = int(values[1]) - 1
        weight = 1
        if len(values) > 2:
            weight = float(values[2])
        if v1 < v2:
            graph[v1][v2] = weight
        else:
            graph[v2][v1] = weight
    return graph


def graph_to_digraph(graph):
    size = len(graph)
    digraph = [[-1 for x in range(size)] for x in range(size)]
    for i in range(size):
        for j in range(i, size):
            digraph[i][j] = graph[i][j]
            digraph[j][i] = graph[i][j]
    return digraph


def transform_digraph(digraph):
    size = len(digraph)
    newSize = size * 2
    transformed = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(size):
        for j in range(size):
            if digraph[i][j] >= 0:
                transformed[2*i][2*j+1] = digraph[i][j]
                transformed[2*i+1][2*j] = digraph[i][j]
    return transformed


def transform_unique_vertex(digraph):
    size = len(digraph)
    newSize = size * 2
    transformed = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(size):
        for j in range(size):
            if digraph[i][j] >= 0:
                    transformed[2*i+1][2*j] = digraph[i][j]
        transformed[2*i][2*i+1] = 0
    return transformed


def detransform(paths):
    size = len(paths)
    newSize = size / 4
    result = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(size):
        for j in range(size):
            if paths[i][j] >= 0:
                result[i/4][j/4] = paths[i][j]
    return result


def print_lp_data(graph, fileName):
    output = open(fileName, 'w');
    output.write("data;\n\nset N :=\n");
    size = len(graph)
    for i in range(size):
        output.write(str(i+1))
        if i != size-1:
            output.write(',')
    output.write(';\n\nparam: A: a c :=\n')
    for i in range(size):
        for j in range(size):
            if graph[i][j] >= 0:
                output.write(str(i+1) + ',' + str(j+1) + ' ' + str(graph[i][j]) + ' 1\n')
    output.write(';\n\nparam r :=\n')
    for i in range(size):
        if i == 0:
            output.write(str(i+1) + ' 2\n')
        elif i == size-1:
            output.write(str(i+1) + ' -2\n')
        else:
            output.write(str(i+1) + ' 0\n')
    output.write(';\n\nend;')
    output.close()

if __name__ == '__main__':
    graph = read_graph(sys.argv[1])
    print_graph(graph, 'graph1_original.png')
    digraph = graph_to_digraph(graph)
    print_graph(digraph, 'graph2_digraph.png')
    transformed = transform_digraph(digraph)
    print_graph(transformed, 'graph3_transformed.png')
    transformed2 = transform_unique_vertex(transformed)
    transformed3 = [row[:] for row in transformed2]
    print_graph(transformed2, 'graph4_transformed2.png')
    print_lp_data(transformed2, 'minimum_cost_flow.dat')
    initial = 1
    destination1 = len(transformed2) - 4
    destination2 = len(transformed2) - 2
    resultT1 = suurballe(transformed2, initial, destination1)
    print_digraph(resultT1, 'graph5_path1.png')
    resultT2 = suurballe(transformed3, initial, destination2)
    print_digraph(resultT2, 'graph6_path2.png')
    result1 = detransform(resultT1)
    result2 = detransform(resultT2)
    print_graph(graph, 'graph7_result1.png', result1)
    print_graph(graph, 'graph8_result2.png', result2)
    # result = suurballe(digraph)
    # print_graph(graph, 'graph3_result.png', result)
