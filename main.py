import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from visuals import GraphView
from counter import perf_monitor
from algorithms import AlgorithmRunner, SAMPLE_GRAPH

from src.benchmarking.runner import run_complexity_benchmark
from src.benchmarking.plotter import create_complexity_chart

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QProgressBar


class BenchmarkWorker(QThread):
    """
    Runs the benchmark in the background.
    """
    data_ready = pyqtSignal(dict) # Emits the results
    progress_update = pyqtSignal(int) # Progress bar updates
    
    def __init__(self, algorithm_name):
        super().__init__()
        self.algorithm_name = algorithm_name
        

    def run(self):
        # We just call the function without a callback
        results = run_complexity_benchmark(self.algorithm_name,
                                           self.progress_update.emit)
        self.data_ready.emit(results)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSA Final Project - Dijkstra & Bellman-Ford")
        self.resize(1000, 700)

        self.runner = AlgorithmRunner()
        # Connect signals
        self.runner.update_state.connect(self.handle_state_update)
        self.runner.update_dist.connect(self.handle_dist_update)
        self.runner.metrics_signal.connect(self.handle_metrics_update)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_viz = QWidget()
        self.setup_visualization_tab()
        self.tabs.addTab(self.tab_viz, "Graph Visualization")

        self.tab_math = QWidget()
        self.setup_math_tab()
        self.tabs.addTab(self.tab_math, "Complexity Analysis")

    def setup_visualization_tab(self):
        main_layout = QVBoxLayout()

        self.graph_view = GraphView()
        self.graph_view.draw_graph(SAMPLE_GRAPH)
        main_layout.addWidget(self.graph_view)

        controls_layout = QHBoxLayout()

        self.btn_dijkstra = QPushButton("Run Dijkstra")
        self.btn_dijkstra.clicked.connect(lambda: self.run_algorithm("dijkstra"))
        self.btn_dijkstra.setStyleSheet(
            "background-color: #007ACC; color: white; padding: 10px; border-radius: 5px;"
        )

        self.btn_bellman = QPushButton("Run Bellman-Ford")
        self.btn_bellman.clicked.connect(lambda: self.run_algorithm("bellman"))
        self.btn_bellman.setStyleSheet(
            "background-color: #E83E8C; color: white; padding: 10px; border-radius: 5px;"
        )

        self.btn_reset = QPushButton("Reset Graph")
        self.btn_reset.clicked.connect(self.reset_graph)
        self.btn_reset.setStyleSheet(
            "background-color: #6C757D; color: white; padding: 10px; border-radius: 5px;"
        )

        controls_layout.addWidget(self.btn_dijkstra)
        controls_layout.addWidget(self.btn_bellman)
        controls_layout.addWidget(self.btn_reset)

        self.metrics_label = QLabel("Ready.")
        self.metrics_label.setFont(QFont("Arial", 12))
        self.metrics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.metrics_label)

        main_layout.addLayout(controls_layout)
        self.tab_viz.setLayout(main_layout)

    def handle_state_update(self, node_id, state):
        if node_id in self.graph_view.node_items:
            self.graph_view.node_items[node_id].set_state(state)
            self.graph_view.scene().update()

    def handle_dist_update(self, node_id, new_dist):
        if node_id in self.graph_view.node_items:
            self.graph_view.node_items[node_id].update_distance(new_dist)
            self.graph_view.scene().update()

    def handle_metrics_update(self, metrics_text):
        self.metrics_label.setText(metrics_text)

    def reset_graph(self):
        for node_item in self.graph_view.node_items.values():
            node_item.set_state("default")
            node_item.update_distance("∞")  # Reset text
        self.metrics_label.setText("Graph Reset.")
        perf_monitor.reset()
        self.graph_view.scene().update()

    def run_algorithm(self, algo_type):
        self.reset_graph()
        self.metrics_label.setText(f"Running {algo_type.upper()}...")
        self.btn_dijkstra.setEnabled(False)
        self.btn_bellman.setEnabled(False)
        self.btn_reset.setEnabled(False)

        def start_task():
            if algo_type == "dijkstra":
                self.runner.run_dijkstra(SAMPLE_GRAPH, "A")
            elif algo_type == "bellman":
                self.runner.run_bellman_ford(SAMPLE_GRAPH, "A")

            self.btn_dijkstra.setEnabled(True)
            self.btn_bellman.setEnabled(True)
            self.btn_reset.setEnabled(True)

        QTimer.singleShot(100, start_task)

    def setup_math_tab(self):
        layout = QVBoxLayout()

        # --- Top Controls ---
        controls_layout = QHBoxLayout()
        
        self.btn_bench_dijkstra = QPushButton("Analyze Dijkstra")
        self.btn_bench_dijkstra.clicked.connect(lambda: self.run_benchmark("dijkstra"))
        self.btn_bench_dijkstra.setStyleSheet("background-color: #007ACC; color: white; padding: 8px;")
        
        self.btn_bench_bellman = QPushButton("Analyze Bellman-Ford")
        self.btn_bench_bellman.clicked.connect(lambda: self.run_benchmark("bellman"))
        self.btn_bench_bellman.setStyleSheet("background-color: #E83E8C; color: white; padding: 8px;")

        controls_layout.addWidget(self.btn_bench_dijkstra)
        controls_layout.addWidget(self.btn_bench_bellman)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)

        #Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide() # Initially hidden
        layout.addWidget(self.progress_bar) # Add it to layout

        # --- The Plot Area ---
        # Initialize with a basic placeholder canvas
        self.canvas = FigureCanvas() 
        layout.addWidget(self.canvas)

        self.tab_math.setLayout(layout)

    def run_benchmark(self, algo_name):
        """Starts the background worker thread."""
        self.btn_bench_dijkstra.setEnabled(False)
        self.btn_bench_bellman.setEnabled(False)
        
        # Reset and Show Progress Bar
        self.progress_bar.setValue(0)
        self.progress_bar.show() 

        self.worker = BenchmarkWorker(algo_name)
        
        self.worker.progress_update.connect(self.progress_bar.setValue) # <--- CONNECT HERE
        self.worker.data_ready.connect(lambda data: self.handle_benchmark_results(data, algo_name))
        self.worker.finished.connect(self.cleanup_benchmark)
        
        self.worker.start()

    def handle_benchmark_results(self, data, algo_name):
        """Called when data comes back from the thread."""
        # 1. Generate the Figure using your plotter helper
        fig = create_complexity_chart(data, algo_name)
        
        # 2. Refresh the Canvas
        layout = self.tab_math.layout()
        layout.removeWidget(self.canvas)
        self.canvas.deleteLater() # Clear memory
        
        self.canvas = FigureCanvas(fig)
        layout.insertWidget(1, self.canvas) # Insert below buttons
        
        self.metrics_label.setText(f"Analysis Complete: {algo_name}")

    def cleanup_benchmark(self):
        """Re-enable buttons after thread finishes."""
        self.btn_bench_dijkstra.setEnabled(True)
        self.btn_bench_bellman.setEnabled(True)
        self.progress_bar.hide() # Hide progress when reset.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

