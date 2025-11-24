import numpy as np

def createGraph(n: int) -> list:
    """
    Generates a raw list of edges using NumPy for maximum speed.
    Returns: List of lists [[u, v, weight], ...]
    """
    
    # -----------------------------------------
    # PART 1: The Spanning Tree (Guaranteed Connectivity)
    # -----------------------------------------
    # We need to connect nodes 1..N-1 to a random previous node.
    
    # Create source nodes [1, 2, ..., n-1]
    sources = np.arange(1, n)
    
    # Vectorized trick to pick a target < source:
    # Generate floats [0.0, 1.0), multiply by the source index, and floor it.
    # E.g., for node 10, random 0.4 -> 4.0 -> connects to node 4.
    targets = (np.random.random(n - 1) * sources).astype(int)
    
    # Random weights for these edges (1-19)
    weights = np.random.randint(1, 20, size=n - 1)
    
    # Stack them into columns: [[1, 0, w], [2, 1, w]...]
    spanning_edges = np.column_stack((sources, targets, weights))

    # -----------------------------------------
    # PART 2: Extra Random Edges
    # -----------------------------------------
    extra_count = np.random.randint(n // 2, n)
    
    # Generate all random sources, targets, and weights at once
    ex_u = np.random.randint(0, n, size=extra_count)
    ex_v = np.random.randint(0, n, size=extra_count)
    ex_w = np.random.randint(1, 20, size=extra_count)
    
    # Filter out self-loops (where u == v) efficiently using boolean masking
    mask = ex_u != ex_v
    random_edges = np.column_stack((ex_u[mask], ex_v[mask], ex_w[mask]))

    # -----------------------------------------
    # PART 3: Merge and Export
    # -----------------------------------------
    # Combine the mandatory edges with the random edges
    all_edges_np = np.vstack((spanning_edges, random_edges))
    
    # Convert numpy array back to python list of lists for your algorithm
    # (Dijkstra expects standard python types)
    return all_edges_np.tolist()