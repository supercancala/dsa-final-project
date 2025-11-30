from src.algorithms.dijkstra import dijkstra, dijkstra_opt
from src.algorithms.bellman_ford import bellman_ford, bellman_ford_opt
from src.algorithms.graph_generator import createGraph
from time import perf_counter



def run_single_benchmrk(algorithm_func, V, graph, source_node):
    """
    Runs a single algorithm and returns Time in seconds
    """

    start_time = perf_counter()

    try:
        algorithm_func(V, graph, source_node)
    except Exception as e:
        print(f"Error running {algorithm_func.__name__}: {e}")
        return 0
    
    end_time = perf_counter()

    return end_time - start_time

    
def run_complexity_benchmark(algorithm_name, progress_callback):
    
    dataset_sizes = [10000, 50000, 100000, 200000, 300000, 400000, 500000]

    total_steps = len(dataset_sizes)

    results = {
        "sizes" : dataset_sizes,
        "times" : []
    }

    if algorithm_name == "dijkstra":
        algorithm_function = dijkstra_opt
    elif algorithm_name == "bellman":
        algorithm_function = bellman_ford_opt
    else:
        raise ValueError(f"Unknow algorithm for {algorithm_name}")

    for i, size in enumerate(dataset_sizes):
        G = createGraph(size)

        duration = run_single_benchmrk(algorithm_function, size, G, 0)
        results['times'].append(duration)

        if progress_callback:
            # Calculate percentage (0 to 100)
            percent = int(((i + 1) / total_steps) * 100)
            progress_callback(percent)

    return results

    