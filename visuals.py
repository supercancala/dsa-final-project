import math
from PyQt6.QtWidgets import (
    QGraphicsSimpleTextItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
)
# FIX: Added QPainter to imports
from PyQt6.QtGui import QBrush, QPen, QColor, QFont, QPainter

class GraphNode(QGraphicsEllipseItem):
    """
    Represents a visual node on the QGraphicsScene.
    """
    COLOR_DEFAULT = QColor("#007ACC")   # Blue
    COLOR_VISITED = QColor("#28A745")   # Green
    COLOR_FRONTIER = QColor("#FFC107")  # Yellow
    COLOR_START = QColor("#DC3545")     # Red

    def __init__(self, node_id, x, y, radius=20):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.node_id = node_id
        self.setPen(QPen(QColor("#000000"), 2))
        self.setBrush(QBrush(self.COLOR_DEFAULT))

        # Add text label
        self.text_item = QGraphicsSimpleTextItem(str(node_id), self)
        font = QFont("Arial", 10)
        font.setBold(True)
        self.text_item.setFont(font)

        # Center the text
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

    def set_state(self, state):
        if state == "start":
            self.setBrush(QBrush(self.COLOR_START))
        elif state == "visited":
            self.setBrush(QBrush(self.COLOR_VISITED))
        elif state == "frontier":
            self.setBrush(QBrush(self.COLOR_FRONTIER))
        elif state == "default":
            self.setBrush(QBrush(self.COLOR_DEFAULT))


class GraphView(QGraphicsView):
    """The main view for displaying the graph."""

    def __init__(self, parent=None):
        scene = QGraphicsScene()
        super().__init__(scene, parent)
        
        # FIX: Using QPainter.RenderHint for PyQt6 compatibility
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor("#F8F9FA")))
        self.node_items = {}  
        self.resize(780, 500)

    def draw_graph(self, graph):
        self.scene().clear() # type: ignore
        self.node_items.clear()

        nodes = list(graph.keys())
        num_nodes = len(nodes)
        center_x, center_y = 350, 250
        radius = 200

        # 1. Draw Nodes
        for i, node_id in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            node_item = GraphNode(node_id, x, y)
            self.scene().addItem(node_item) # type: ignore
            self.node_items[node_id] = node_item

        # 2. Draw Edges
        pen = QPen(QColor("#555555"), 1.5)
        for source, targets in graph.items():
            source_pos = self.node_items[source].pos()
            source_center = source_pos + self.node_items[source].rect().center()

            for target in targets:
                if target in self.node_items:
                    target_pos = self.node_items[target].pos()
                    target_center = target_pos + self.node_items[target].rect().center()

                    line = QGraphicsLineItem(
                        source_center.x(), source_center.y(),
                        target_center.x(), target_center.y(),
                    )
                    line.setPen(pen)
                    self.scene().addItem(line) # type: ignore

        # Bring nodes to front
        for node in self.node_items.values():
            node.setZValue(1)