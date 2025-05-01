# Goal is to find reachable cities from a source node via BFS (e.g. Trip Planner App)
from collections import deque

def bfs(graph, start):
    visited = set()  # Set to track visited cities
    queue = deque([start])  # Queue for BFS starting from the given city
    print("\nBFS Traversal Order:")
    while queue:
        city = queue.popleft()  # Dequeue a city
        if city not in visited:
            print(city, end=" ")  # Printing visited cities
            visited.add(city)  # Marking as a visited city
            for neighbor in graph.get(city, []):  # Traverse neighbors
                if neighbor not in visited:
                    queue.append(neighbor)

# Define the DFS function using recursion
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(graph, neighbor, visited)  # Recursive DFS call for the neighbor

# Main block of code
if __name__ == "__main__":
    graph = {}
    
    # For BFS
    print("Enter number of Connections:")
    edges = int(input())
    print("Enter each connection (city1 city2):")
    for _ in range(edges):
        u, v = input().split()
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    print("Enter starting city for BFS:")
    start_city = input()
    bfs(graph, start_city)

    # For DFS
    graph = {}
    print("\nEnter number of connections in the graph (edges):")
    edges = int(input())
    print("Now enter each connection in the format: node1 node2")
    print("This will assume the graph is undirected (2-way connections)")
    for _ in range(edges):
        u, v = input().split()
        if u not in graph:
            graph[u] = []
        graph[u].append(v)
        if v not in graph:
            graph[v] = []
        graph[v].append(u)

    print("Enter the starting node for DFS Traversal:")
    start_node = input()
    print("\nDFS Traversal Order:")
    dfs(graph, start_node)
