import heapq
from PyQt6.QtCore import QObject, pyqtSignal as Signal, QTimer, QEventLoop
from counter import perf_monitor

# --- Weighted Graph Data {Source: {Target: Weight}} ---
SAMPLE_GRAPH = {
    "A": {"B": 1, "C": 4},
    "B": {"C": 2, "D": 5},
    "C": {"D": 1},
    "D": {},
}


class AlgorithmRunner(QObject):
    # Signals:
    # update_state: node_id, color_state
    # update_dist: node_id, new_distance_value
    update_state = Signal(str, str)
    update_dist = Signal(str, object)
    metrics_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.delay_ms = 400

    def wait(self):
        """Helper to create a visual delay"""
        loop = QEventLoop()
        QTimer.singleShot(self.delay_ms, loop.quit)
        loop.exec()

    def run_dijkstra(self, graph, start_node):
        perf_monitor.start()

        # Distances map
        distances = {node: float("inf") for node in graph}
        distances[start_node] = 0

        # Update GUI with initial distances
        for node in graph:
            self.update_dist.emit(node, float("inf"))
        self.update_dist.emit(start_node, 0)

        # Priority Queue: (current_dist, node_id)
        pq = [(0, start_node)]
        visited = set()

        self.update_state.emit(start_node, "start")
        self.wait()

        while pq:
            current_dist, u = heapq.heappop(pq)
            perf_monitor.increment()

            if u in visited:
                continue
            visited.add(u)
            self.update_state.emit(u, "visited")
            self.wait()

            # Check neighbors
            for v, weight in graph[u].items():
                perf_monitor.increment()
                new_dist = current_dist + weight

                # Highlighting edge check
                self.update_state.emit(v, "updating")
                self.wait()

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    self.update_dist.emit(v, new_dist)
                    heapq.heappush(pq, (new_dist, v))
                    self.update_state.emit(v, "frontier")
                else:
                    # Revert color if not updated
                    if v not in visited:
                        self.update_state.emit(v, "default")

                self.wait()

        perf_monitor.stop()
        self.metrics_signal.emit(
            f"Dijkstra Steps: {perf_monitor.steps}\nTime: {perf_monitor.execution_time:.4f}s"
        )

    def run_bellman_ford(self, graph, start_node):
        perf_monitor.start()

        distances = {node: float("inf") for node in graph}
        distances[start_node] = 0

        # Reset GUI
        for node in graph:
            self.update_dist.emit(node, float("inf"))
        self.update_dist.emit(start_node, 0)
        self.update_state.emit(start_node, "start")
        self.wait()

        nodes = list(graph.keys())
        num_vertices = len(nodes)

        # Relax edges |V| - 1 times
        for i in range(num_vertices - 1):
            changed = False
            for u in graph:
                for v, weight in graph[u].items():
                    perf_monitor.increment()

                    # Highlight checking
                    self.update_state.emit(u, "visited")  # Current source
                    self.update_state.emit(v, "updating")  # Checking target
                    self.wait()

                    if (
                        distances[u] != float("inf")
                        and distances[u] + weight < distances[v]
                    ):
                        distances[v] = distances[u] + weight
                        self.update_dist.emit(v, distances[v])
                        self.update_state.emit(v, "frontier")  # Updated
                        changed = True
                    else:
                        if v != start_node:
                            self.update_state.emit(v, "default")

                    self.wait()
                    # Reset source color
                    if u != start_node:
                        self.update_state.emit(u, "default")

            if not changed:
                break

        perf_monitor.stop()
        self.metrics_signal.emit(
            f"Bellman-Ford Steps: {perf_monitor.steps}\nTime: {perf_monitor.execution_time:.4f}s"
        )
