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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
