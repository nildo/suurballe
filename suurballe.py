

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
    original = [row[:] for row in graph]
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
        result[i][j] = original[i][j]
    for j, i in path2.iteritems():
        result[i][j] = original[i][j]
    return result
