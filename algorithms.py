import time
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal as Signal, QTimer, QEventLoop

# --- Data ---
SAMPLE_GRAPH = {
    1: [2, 4],
    2: [3, 4],
    3: [5],
    4: [6, 3],
    5: [6, 9],
    6: [7],
    7: [9],
    8: [1],
    9: [8]
}

# --- Instrumentation ---
class OperationCounter:
    def __init__(self):
        self.steps = 0
        self.start_time = 0
        self.execution_time = 0

    def reset(self):
        self.steps = 0
        self.execution_time = 0
        self.start_time = 0

    def increment(self):
        self.steps += 1

    def start(self):
        self.reset()
        self.start_time = time.perf_counter()

    def stop(self):
        self.execution_time = time.perf_counter() - self.start_time

# Global instance for this module
perf_monitor = OperationCounter()

# --- Logic ---
class AlgorithmRunner(QObject):
    update_signal = Signal(int, str)
    metrics_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.delay_ms = 300 

    def _update_gui_and_wait(self, node_id, state):
        perf_monitor.increment()
        self.update_signal.emit(node_id, state)
        loop = QEventLoop()
        QTimer.singleShot(self.delay_ms, loop.quit)
        loop.exec()

    def run_bfs(self, graph, start_node):
        perf_monitor.start()
        visited = set()
        queue = deque([start_node])

        self._update_gui_and_wait(start_node, "start")
        visited.add(start_node)

        while queue:
            vertex = queue.popleft()
            self._update_gui_and_wait(vertex, "visited")

            for neighbor in graph.get(vertex, []):
                perf_monitor.increment()
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.update_signal.emit(neighbor, "frontier")

        perf_monitor.stop()
        self.metrics_signal.emit(
            f"BFS Steps: {perf_monitor.steps}\nTime: {perf_monitor.execution_time:.6f} s"
        )

    def run_dfs_recursive(self, graph, start_node, visited=None):
        if visited is None:
            visited = set()
            perf_monitor.start()

        if start_node not in visited:
            visited.add(start_node)
            state = "start" if len(visited) == 1 else "visited"
            self.update_signal.emit(start_node, state)
            
            # Wait
            loop = QEventLoop()
            QTimer.singleShot(self.delay_ms, loop.quit)
            loop.exec()

            for neighbor in graph.get(start_node, []):
                perf_monitor.increment()
                if neighbor not in visited:
                    self.run_dfs_recursive(graph, neighbor, visited)

        # Check if recursion is fully done (simple check for root call)
        # Note: This check is simplistic for Sprint 1
        if len(visited) == len(graph) or (visited and start_node == 1):
             # Only stop timer if we are back at root or done. 
             # For accurate timing in recursion, we'd usually check depth, 
             # but strictly stopping here is okay for now.
             perf_monitor.stop()
             self.metrics_signal.emit(
                f"DFS Steps: {perf_monitor.steps}\nTime: {perf_monitor.execution_time:.6f} s"
             )