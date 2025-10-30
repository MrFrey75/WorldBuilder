"""
Relationship graph visualization widget for WorldBuilder.
Displays entity relationships as an interactive network graph.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, 
    QLabel, QCheckBox, QToolBar, QSlider, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional, Set


class RelationshipGraphCanvas(FigureCanvas):
    """
    Matplotlib-based canvas for rendering relationship graphs using NetworkX.
    """
    node_clicked = pyqtSignal(object)  # Emits entity object
    
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.graph = nx.Graph()
        self.entities = []
        self.relationships = []
        self.entity_types = set()
        self.filtered_types = set()
        self.layout_algorithm = 'spring'
        self.show_labels = True
        self.focused_entity_id = None
        
        # Connect click event
        self.mpl_connect('button_press_event', self._on_click)
        
    def set_data(self, entities: List, relationships: List):
        """Set entities and relationships to visualize."""
        self.entities = entities or []
        self.relationships = relationships or []
        
        # Extract entity types
        self.entity_types = set()
        for entity in self.entities:
            entity_type = type(entity).__name__
            self.entity_types.add(entity_type)
        
        self.build_graph()
        self.render_graph()
        
    def set_layout(self, algorithm: str):
        """Set graph layout algorithm."""
        self.layout_algorithm = algorithm
        self.render_graph()
        
    def set_show_labels(self, show: bool):
        """Toggle node labels."""
        self.show_labels = show
        self.render_graph()
        
    def set_type_filter(self, filtered_types: Set[str]):
        """Filter graph by entity types."""
        self.filtered_types = filtered_types
        self.build_graph()
        self.render_graph()
        
    def focus_on_entity(self, entity_id):
        """Focus graph on specific entity and its connections."""
        self.focused_entity_id = entity_id
        self.build_graph()
        self.render_graph()
        
    def clear_focus(self):
        """Clear entity focus and show full graph."""
        self.focused_entity_id = None
        self.build_graph()
        self.render_graph()
        
    def build_graph(self):
        """Build NetworkX graph from entities and relationships."""
        self.graph = nx.Graph()
        
        # Filter entities by type
        filtered_entities = []
        for entity in self.entities:
            entity_type = type(entity).__name__
            if not self.filtered_types or entity_type not in self.filtered_types:
                filtered_entities.append(entity)
        
        # If focused on an entity, only show it and its connections
        if self.focused_entity_id:
            # Find the focused entity
            focused_entity = None
            for entity in filtered_entities:
                if entity.id == self.focused_entity_id:
                    focused_entity = entity
                    break
            
            if focused_entity:
                # Add focused entity
                self.graph.add_node(focused_entity.id, 
                                   entity=focused_entity,
                                   label=focused_entity.name,
                                   type=type(focused_entity).__name__)
                
                # Add directly connected entities
                connected_ids = set()
                for rel in self.relationships:
                    if hasattr(rel, 'from_figure_id') and hasattr(rel, 'to_figure_id'):
                        if rel.from_figure_id == self.focused_entity_id:
                            connected_ids.add(rel.to_figure_id)
                        elif rel.to_figure_id == self.focused_entity_id:
                            connected_ids.add(rel.from_figure_id)
                
                for entity in filtered_entities:
                    if entity.id in connected_ids:
                        self.graph.add_node(entity.id, 
                                           entity=entity,
                                           label=entity.name,
                                           type=type(entity).__name__)
                
                # Add edges
                for rel in self.relationships:
                    if hasattr(rel, 'from_figure_id') and hasattr(rel, 'to_figure_id'):
                        if (rel.from_figure_id == self.focused_entity_id or 
                            rel.to_figure_id == self.focused_entity_id):
                            if (self.graph.has_node(rel.from_figure_id) and 
                                self.graph.has_node(rel.to_figure_id)):
                                edge_attrs = {
                                    'relationship': rel,
                                    'type': getattr(rel, 'type', 'unknown'),
                                    'weight': getattr(rel, 'strength', 5)
                                }
                                self.graph.add_edge(rel.from_figure_id, rel.to_figure_id, 
                                                   **edge_attrs)
        else:
            # Add all filtered entities as nodes
            for entity in filtered_entities:
                self.graph.add_node(entity.id, 
                                   entity=entity,
                                   label=entity.name,
                                   type=type(entity).__name__)
            
            # Add relationships as edges
            for rel in self.relationships:
                if hasattr(rel, 'from_figure_id') and hasattr(rel, 'to_figure_id'):
                    # Only add edge if both nodes exist
                    if (self.graph.has_node(rel.from_figure_id) and 
                        self.graph.has_node(rel.to_figure_id)):
                        edge_attrs = {
                            'relationship': rel,
                            'type': getattr(rel, 'type', 'unknown'),
                            'weight': getattr(rel, 'strength', 5)
                        }
                        self.graph.add_edge(rel.from_figure_id, rel.to_figure_id, 
                                           **edge_attrs)
        
    def render_graph(self):
        """Render the relationship graph."""
        self.axes.clear()
        
        if not self.graph.nodes():
            self.axes.text(0.5, 0.5, 'No relationships to display', 
                          ha='center', va='center', transform=self.axes.transAxes)
            self.draw()
            return
        
        # Choose layout algorithm
        if self.layout_algorithm == 'spring':
            pos = nx.spring_layout(self.graph, k=1, iterations=50)
        elif self.layout_algorithm == 'circular':
            pos = nx.circular_layout(self.graph)
        elif self.layout_algorithm == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(self.graph)
        elif self.layout_algorithm == 'shell':
            pos = nx.shell_layout(self.graph)
        else:
            pos = nx.spring_layout(self.graph)
        
        # Get node colors based on entity type
        node_colors = []
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            entity_type = node_data.get('type', 'Unknown')
            color = self._get_type_color(entity_type)
            
            # Highlight focused entity
            if node_id == self.focused_entity_id:
                color = 'gold'
            
            node_colors.append(color)
        
        # Get edge colors based on relationship type
        edge_colors = []
        edge_widths = []
        for u, v, data in self.graph.edges(data=True):
            rel_type = data.get('type', 'unknown')
            color = self._get_relationship_color(rel_type)
            edge_colors.append(color)
            
            weight = data.get('weight', 5)
            edge_widths.append(weight / 2.0)
        
        # Draw graph
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color=node_colors,
                              node_size=500,
                              alpha=0.9,
                              ax=self.axes)
        
        nx.draw_networkx_edges(self.graph, pos,
                              edge_color=edge_colors,
                              width=edge_widths,
                              alpha=0.6,
                              ax=self.axes)
        
        # Draw labels if enabled
        if self.show_labels:
            labels = nx.get_node_attributes(self.graph, 'label')
            nx.draw_networkx_labels(self.graph, pos, labels,
                                   font_size=8,
                                   ax=self.axes)
        
        self.axes.set_title('Relationship Graph')
        self.axes.axis('off')
        
        # Add legend for entity types
        if self.entity_types:
            legend_elements = []
            for entity_type in sorted(self.entity_types):
                color = self._get_type_color(entity_type)
                legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                                  markerfacecolor=color, markersize=8,
                                                  label=entity_type))
            self.axes.legend(handles=legend_elements, loc='upper left', fontsize=8)
        
        self.draw()
        
    def _get_type_color(self, entity_type: str) -> str:
        """Get color for entity type."""
        type_colors = {
            'NotableFigure': 'skyblue',
            'Location': 'lightgreen',
            'Organization': 'lightcoral',
            'Artifact': 'plum',
            'Species': 'wheat',
        }
        return type_colors.get(entity_type, 'lightgray')
        
    def _get_relationship_color(self, rel_type: str) -> str:
        """Get color for relationship type."""
        rel_colors = {
            'family': 'green',
            'friend': 'blue',
            'enemy': 'red',
            'ally': 'purple',
            'romantic': 'pink',
            'professional': 'orange',
            'mentor': 'brown',
            'rival': 'darkred',
        }
        return rel_colors.get(rel_type.lower(), 'gray')
        
    def _on_click(self, mpl_event):
        """Handle click on graph node."""
        if mpl_event.inaxes != self.axes:
            return
        
        # Find closest node to click
        click_x = mpl_event.xdata
        click_y = mpl_event.ydata
        
        if click_x is None or click_y is None:
            return
        
        # Get node positions
        if self.layout_algorithm == 'spring':
            pos = nx.spring_layout(self.graph, k=1, iterations=50)
        elif self.layout_algorithm == 'circular':
            pos = nx.circular_layout(self.graph)
        elif self.layout_algorithm == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(self.graph)
        elif self.layout_algorithm == 'shell':
            pos = nx.shell_layout(self.graph)
        else:
            pos = nx.spring_layout(self.graph)
        
        closest_node = None
        min_distance = float('inf')
        
        for node_id, (x, y) in pos.items():
            distance = ((x - click_x) ** 2 + (y - click_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_node = node_id
        
        # Threshold for clicking (0.1 in normalized coordinates)
        if closest_node and min_distance < 0.1:
            node_data = self.graph.nodes[closest_node]
            entity = node_data.get('entity')
            if entity:
                self.node_clicked.emit(entity)


class RelationshipGraphWidget(QWidget):
    """
    Complete relationship graph widget with controls.
    """
    entity_selected = pyqtSignal(object)  # Emits entity object
    
    def __init__(self, relationship_service=None, figure_service=None, parent=None):
        super().__init__(parent)
        self.relationship_service = relationship_service
        self.figure_service = figure_service
        self.current_universe_id = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)
        
        # Canvas
        self.canvas = RelationshipGraphCanvas(self, width=10, height=8)
        self.canvas.node_clicked.connect(self._on_node_clicked)
        layout.addWidget(self.canvas)
        
    def _create_toolbar(self):
        """Create toolbar with controls."""
        toolbar = QToolBar()
        
        # Layout selector
        toolbar.addWidget(QLabel("Layout: "))
        self.layout_combo = QComboBox()
        self.layout_combo.addItems(["Spring", "Circular", "Kamada-Kawai", "Shell"])
        self.layout_combo.currentTextChanged.connect(self._on_layout_changed)
        toolbar.addWidget(self.layout_combo)
        
        toolbar.addSeparator()
        
        # Show labels checkbox
        self.labels_checkbox = QCheckBox("Show Labels")
        self.labels_checkbox.setChecked(True)
        self.labels_checkbox.stateChanged.connect(self._on_labels_changed)
        toolbar.addWidget(self.labels_checkbox)
        
        toolbar.addSeparator()
        
        # Clear focus button
        clear_focus_btn = QPushButton("Show All")
        clear_focus_btn.clicked.connect(self.clear_focus)
        toolbar.addWidget(clear_focus_btn)
        
        toolbar.addSeparator()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)
        
        return toolbar
        
    def set_universe(self, universe_id):
        """Set the current universe and load data."""
        self.current_universe_id = universe_id
        self.refresh()
        
    def refresh(self):
        """Refresh graph data from services."""
        if not self.current_universe_id:
            return
        
        try:
            # Load relationships
            if self.relationship_service:
                relationships = self.relationship_service.get_by_universe(self.current_universe_id)
            else:
                relationships = []
            
            # Load figures (entities)
            if self.figure_service:
                figures = self.figure_service.get_by_universe(self.current_universe_id)
            else:
                figures = []
            
            # Update canvas
            self.canvas.set_data(figures, relationships)
            
        except Exception as e:
            print(f"Error refreshing relationship graph: {e}")
            
    def focus_on_entity(self, entity_id):
        """Focus graph on specific entity."""
        self.canvas.focus_on_entity(entity_id)
        
    def clear_focus(self):
        """Clear entity focus."""
        self.canvas.clear_focus()
        
    def _on_layout_changed(self, layout_text):
        """Handle layout algorithm change."""
        layout_map = {
            "Spring": "spring",
            "Circular": "circular",
            "Kamada-Kawai": "kamada_kawai",
            "Shell": "shell"
        }
        self.canvas.set_layout(layout_map.get(layout_text, "spring"))
        
    def _on_labels_changed(self, state):
        """Handle labels checkbox change."""
        self.canvas.set_show_labels(state == Qt.CheckState.Checked.value)
        
    def _on_node_clicked(self, entity):
        """Handle node click."""
        self.entity_selected.emit(entity)
        # Also focus on this entity
        self.focus_on_entity(entity.id)
