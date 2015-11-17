import sys
import pydot

def print_graph(graph, fileName):
    pydotGraph = pydot.Dot(graph_type='graph')
    size = len(graph)
    for i in range(size):
        for j in range(i, size):
            if graph[i][j] >= 0:
                edge = pydot.Edge(str(i+1), str(j+1))
                edge.set_label(str(graph[i][j]))
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
    newSize = size * 2 + 2
    transformed = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(size):
        for j in range(size):
            if digraph[i][j] >= 0:
                transformed[1+2*i][1+2*j] = digraph[i][j]
                transformed[1+2*i+1][1+2*j+1] = digraph[i][j]
        transformed[1+2*i][1+2*i+1] = 0
        transformed[1+2*i+1][1+2*i] = 0
    transformed[0][1] = 0
    transformed[0][2] = 0
    transformed[newSize-2][newSize-1] = 0
    transformed[newSize-3][newSize-1] = 0
    return transformed

def transform_unique_vertex(digraph):
    size = len(digraph)
    newSize = size * 2 - 2
    transformed = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(size):
        for j in range(size):
            if digraph[i][j] >= 0:
                if i == 0:
                    transformed[i][2*j-1] = digraph[i][j]
                else:
                    if j == size-1:
                        transformed[2*i][newSize-1] = digraph[i][j]
                    else:
                        transformed[2*i][2*j-1] = digraph[i][j]
        if i != 0 and i != size-1:
            transformed[2*i-1][2*i] = 0
    return transformed

def detransform(paths):
    size = len(paths)
    newSize = (size - 2) / 4
    result = [[-1 for x in range(newSize)] for x in range(newSize)]
    for i in range(1,size-1):
        for j in range(1,size-1):
            if paths[i][j] >= 0:
                result[(i-1)/4][(j-1)/4] = 1
    return result

def dijkstra(graph, initial, destination):
    size = len(graph)
    visited = {initial: 0}
    path = {}
    nodes = {x for x in range(size)}

    while nodes:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node] < visited[minNode]:
                    minNode = node
        if minNode is None:
            break

        nodes.remove(minNode)
        currentWeight = visited[minNode]

        for i in range(size):
            if graph[minNode][i] >= 0:
                weight = currentWeight + graph[minNode][i]
                if i not in visited or weight < visited[i]:
                    visited[i] = weight
                    path[i] = minNode

    path1 = {}
    current = destination
    while current != initial:
        path1[current] = path[current]
        current = path[current]

    return visited, path1

def suurballe(graph):
    initial = 0
    destination = len(graph) - 1
    visited, path1 = dijkstra(graph, initial, destination)
    # Update costs:
    size = len(graph)
    for i in range(size):
        for j in range(size):
            graph[i][j] += visited[i] - visited[j]
    # Create residual graph
    # Remove edges directed into s and reversing the direction of the zero length edges along path1
    for j, i in path1.iteritems():
        graph[j][i] = graph[i][j]
        graph[i][j] = -1
    # Find second path
    visited, path2 = dijkstra(graph, initial, destination)
    # Discard the reversed edges of path2 from both paths.
    for j, i in path2.iteritems():
        if i in path1:
            if path1[i] == j:
                del path1[i]
                del path2[j]
    # Remaining edges:
    result = [[-1 for x in range(size)] for x in range(size)]
    for j, i in path1.iteritems():
        result[i][j] = 1
    for j, i in path2.iteritems():
        result[i][j] = 1
    return result

    # tree = [[-1 for x in range(size)] for x in range(size)]
    # for i in range(size):
    #     if i != initial:
    #         tree[path[i]][i] = visited[i]
    # return tree


if __name__ == '__main__':
    graph = read_graph(sys.argv[1])
    print_graph(graph, 'graph1_original.png')
    digraph = graph_to_digraph(graph)
    print_digraph(digraph, 'graph2_digraph.png')
    transformed = transform_digraph(digraph)
    print_digraph(transformed, 'graph3_transformed.png')
    transformed2 = transform_unique_vertex(transformed)
    print_digraph(transformed2, 'graph4_transformed2.png')
    resultT2 = suurballe(transformed2)
    print_digraph(resultT2, 'graph5_paths.png')
    result = detransform(resultT2)
    print_graph(result, 'graph6_result.png')
