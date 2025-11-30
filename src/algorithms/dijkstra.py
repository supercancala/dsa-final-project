import heapq
import sys
from .graph_generator import createGraph
from time import time

# ---------------------------------------------------------
# ALGORITHM IMPLEMENTATION
# ---------------------------------------------------------

def constructAdj(edges, V):
    """
    Helper to convert raw edge list into Adjacency List.
    Optimized to use tuples for memory efficiency.
    """
    adj = [[] for _ in range(V)]
    for u, v, wt in edges:
        adj[u].append((v, wt))
        adj[v].append((u, wt))
    return adj

def dijkstra_opt(V, edges, src):
    """
    Optimized Dijkstra for large datasets.
    Input: Raw edge list (to maintain strict separation).
    """
    # 1. Parsing Input (Included in time complexity as per requirements)
    adj = constructAdj(edges, V)

    # 2. Initialization
    # Use tuples (distance, node) for heap efficiency
    pq = [(0, src)]
    
    dist = [sys.maxsize] * V
    dist[src] = 0

    # 3. The Loop
    while pq:
        # Pop smallest distance
        d, u = heapq.heappop(pq)

        # OPTIMIZATION: Stale Node Check (Lazy Deletion)
        # If we popped a path that is longer than one we already found, skip it.
        if d > dist[u]:
            continue

        # Iterate neighbors
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist

def dijkstra(V, edges, src):
    # Create adjacency list
    adj = constructAdj(edges, V)

    # Create a priority queue to store vertices that
    # are being preprocessed.
    pq = []
    
    # Create a list for distances and initialize all
    # distances as infinite
    dist = [sys.maxsize] * V

    # Insert source itself in priority queue and initialize
    # its distance as 0.
    heapq.heappush(pq, [0, src])
    dist[src] = 0

    # Looping till priority queue becomes empty (or all
    # distances are not finalized) 
    while pq:
        # The first vertex in pair is the minimum distance
        # vertex, extract it from priority queue.
        u = heapq.heappop(pq)[1]

        # Get all adjacent of u.
        for x in adj[u]:
            # Get vertex label and weight of current
            # adjacent of u.
            v, weight = x[0], x[1]

            
            # If there is shorter path to v through u.
            if dist[v] > dist[u] + weight:
                # Updating distance of v
                dist[v] = dist[u] + weight

                heapq.heappush(pq, [dist[v], v])

    # Return the shortest distance array
    return dist

# ---------------------------------------------------------
# DRIVER CODE
# ---------------------------------------------------------
if __name__ == "__main__":
    
    src = 0
    
    try:
        val = input("Enter number of nodes (e.g. 50000): ")
        v = int(val)
    except ValueError:
        v = 1000 # Default

    # This just returns the list [[u,v,w]...], no processing
    edges = createGraph(v) 

    print(f"Running Base Dijkstra Algorithm...")
    start = time()
    # Timer starts exactly when we pass the raw data to the algorithm
    result = dijkstra(v, edges, src)
    end = time()

    print("-" * 30)
    print(f"Algorithm Finished.")
    print(f"Time Taken: {end-start:.4f} seconds")
    print("-" * 30)

    print(f"Running Opt Dijkstra Algorithm...")
    start = time()
    # Timer starts exactly when we pass the raw data to the algorithm
    result = dijkstra_opt(v, edges, src)
    end = time()

    print("-" * 30)
    print(f"Algorithm Finished.")
    print(f"Time Taken: {end-start:.4f} seconds")
    print("-" * 30)
    