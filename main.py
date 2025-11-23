import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QTabWidget, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# --- Import our custom modules ---
from visuals import GraphView
from algorithms import AlgorithmRunner, perf_monitor, SAMPLE_GRAPH

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSA Final Project - Graph Algorithms Sprint 1")
        self.resize(1000, 700)
        
        self.runner = AlgorithmRunner()
        self.runner.update_signal.connect(self.handle_node_update)
        self.runner.metrics_signal.connect(self.handle_metrics_update)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_viz = QWidget()
        self.setup_visualization_tab()
        self.tabs.addTab(self.tab_viz, "Graph Visualization (FDD Feature)")

        self.tab_math = QWidget()
        self.setup_complexity_tab()
        self.tabs.addTab(self.tab_math, "Complexity Analysis (Experiment Harness)")

    def setup_visualization_tab(self):
        main_layout = QVBoxLayout()
        
        # Initialize GraphView from visuals.py
        self.graph_view = GraphView()
        self.graph_view.draw_graph(SAMPLE_GRAPH)
        main_layout.addWidget(self.graph_view)

        controls_layout = QHBoxLayout()
        
        self.btn_run_bfs = QPushButton("Run BFS")
        self.btn_run_bfs.clicked.connect(lambda: self.run_algorithm("bfs"))
        self.btn_run_bfs.setStyleSheet("background-color: #007ACC; color: white; padding: 10px; border-radius: 5px;")

        self.btn_run_dfs = QPushButton("Run DFS (Recursive)")
        self.btn_run_dfs.clicked.connect(lambda: self.run_algorithm("dfs"))
        self.btn_run_dfs.setStyleSheet("background-color: #DC3545; color: white; padding: 10px; border-radius: 5px;")

        self.btn_reset = QPushButton("Reset Graph")
        self.btn_reset.clicked.connect(self.reset_graph)
        self.btn_reset.setStyleSheet("background-color: #6C757D; color: white; padding: 10px; border-radius: 5px;")

        controls_layout.addWidget(self.btn_run_bfs)
        controls_layout.addWidget(self.btn_run_dfs)
        controls_layout.addWidget(self.btn_reset)

        self.metrics_label = QLabel("Ready. Select an algorithm to run.")
        self.metrics_label.setFont(QFont("Arial", 12))
        self.metrics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.metrics_label)

        main_layout.addLayout(controls_layout)
        self.tab_viz.setLayout(main_layout)

    def setup_complexity_tab(self):
        layout = QVBoxLayout()
        label = QLabel("Experiment Harness (v1) - Data Logging Ready")
        label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        info = QLabel("This tab is for the **Experiment Harness**.\n\n- Sprint 1 Goal: Setup structure.\n- Current: Logic separated into algorithms.py.")
        layout.addWidget(info)
        self.tab_math.setLayout(layout)

    def handle_node_update(self, node_id, state):
        if node_id in self.graph_view.node_items:
            self.graph_view.node_items[node_id].set_state(state)
            self.graph_view.scene().update() # type: ignore

    def handle_metrics_update(self, metrics_text):
        self.metrics_label.setText(metrics_text)

    def reset_graph(self):
        for node_item in self.graph_view.node_items.values():
            node_item.set_state("default")
        self.metrics_label.setText("Graph Reset. Ready to run another algorithm.")
        perf_monitor.reset()
        self.graph_view.scene().update() # type: ignore

    def run_algorithm(self, algo_type):
        self.reset_graph()
        self.metrics_label.setText(f"Running {algo_type.upper()}...")
        self.btn_run_bfs.setEnabled(False)
        self.btn_run_dfs.setEnabled(False)
        self.btn_reset.setEnabled(False)

        def start_task():
            if algo_type == "bfs":
                self.runner.run_bfs(SAMPLE_GRAPH, 1)
            elif algo_type == "dfs":
                self.runner.run_dfs_recursive(SAMPLE_GRAPH, 1)
            
            self.btn_run_bfs.setEnabled(True)
            self.btn_run_dfs.setEnabled(True)
            self.btn_reset.setEnabled(True)

        QTimer.singleShot(100, start_task)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())