import networkx as nx
from PyQt6.QtWidgets import (
    QGraphicsSimpleTextItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QBrush, QPen, QColor, QFont, QPainter

class GraphNode(QGraphicsEllipseItem):
    COLOR_DEFAULT = QColor("#007ACC")   # Blue
    COLOR_VISITED = QColor("#28A745")   # Green (Processed)
    COLOR_FRONTIER = QColor("#FFC107")  # Yellow (In Priority Queue)
    COLOR_START = QColor("#DC3545")     # Red
    COLOR_UPDATING = QColor("#E83E8C")  # Pink (Distance Changing)

    def __init__(self, node_id, x, y, radius=25):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.node_id = node_id
        self.setPen(QPen(QColor("#000000"), 2))
        self.setBrush(QBrush(self.COLOR_DEFAULT))

        # ID Label (Top)
        self.id_text = QGraphicsSimpleTextItem(f"Node {node_id}", self)
        font = QFont("Arial", 10, QFont.Weight.Bold)
        self.id_text.setFont(font)
        
        # Distance Label (Center) - Starts at Infinity
        self.dist_text = QGraphicsSimpleTextItem("∞", self)
        self.dist_text.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.dist_text.setBrush(QBrush(QColor("white")))

        self.align_text()

    def align_text(self):
        # Center the ID above the node
        rect = self.boundingRect()
        id_rect = self.id_text.boundingRect()
        self.id_text.setPos(
            rect.center().x() - id_rect.width() / 2, 
            rect.top() - id_rect.height() - 2
        )

        # Center the Distance inside the node
        dist_rect = self.dist_text.boundingRect()
        self.dist_text.setPos(
            rect.center().x() - dist_rect.width() / 2, 
            rect.center().y() - dist_rect.height() / 2
        )

    def update_distance(self, new_dist):
        """Updates the text inside the bubble"""
        text = str(new_dist) if new_dist != float('inf') else "∞"
        self.dist_text.setText(text)
        self.align_text()

    def set_state(self, state):
        if state == "start": self.setBrush(QBrush(self.COLOR_START))
        elif state == "visited": self.setBrush(QBrush(self.COLOR_VISITED))
        elif state == "frontier": self.setBrush(QBrush(self.COLOR_FRONTIER))
        elif state == "updating": self.setBrush(QBrush(self.COLOR_UPDATING))
        elif state == "default": self.setBrush(QBrush(self.COLOR_DEFAULT))


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        scene = QGraphicsScene()
        super().__init__(scene, parent)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor("#F8F9FA")))
        self.node_items = {}
        self.resize(780, 500)

    def draw_graph(self, graph_data):
        self.scene().clear()
        self.node_items.clear()

        # 1. Use NetworkX to calculate "Natural" positions
        G = nx.DiGraph()
        for u, neighbors in graph_data.items():
            G.add_node(u)
            for v, weight in neighbors.items():
                G.add_edge(u, v, weight=weight)

        # "Spring Layout" makes it look natural
        pos = nx.spring_layout(G, seed=42, k=2) 

        # Scale positions to fit visual area
        scale_x, scale_y = 600, 400
        offset_x, offset_y = 50, 50

        # 2. Draw Edges (Lines + Weights)
        pen = QPen(QColor("#555555"), 2)
        font = QFont("Arial", 9)
        
        for u, v, data in G.edges(data=True):
            x1, y1 = pos[u][0] * scale_x + offset_x, pos[u][1] * scale_y + offset_y
            x2, y2 = pos[v][0] * scale_x + offset_x, pos[v][1] * scale_y + offset_y
            
            # Line
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(pen)
            self.scene().addItem(line)

            # Weight Text (Midpoint)
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            weight_text = QGraphicsSimpleTextItem(str(data['weight']))
            weight_text.setFont(font)
            # Add a small white background to text so line doesn't strike through
            weight_text.setBrush(QBrush(QColor("black")))
            bg_rect = self.scene().addRect(
                mid_x, mid_y, weight_text.boundingRect().width(), 
                weight_text.boundingRect().height(), 
                pen=QPen(Qt.PenStyle.NoPen), brush=QBrush(QColor("#F8F9FA"))
            )
            weight_text.setPos(mid_x, mid_y)
            bg_rect.setZValue(0.5)
            weight_text.setZValue(0.6)
            self.scene().addItem(weight_text)

        # 3. Draw Nodes
        for node_id, (x, y) in pos.items():
            sx = x * scale_x + offset_x
            sy = y * scale_y + offset_y
            node_item = GraphNode(node_id, sx, sy)
            self.scene().addItem(node_item)
            self.node_items[node_id] = node_item
            node_item.setZValue(1)
            
# Helper import needed for the rect background
from PyQt6.QtCore import Qt