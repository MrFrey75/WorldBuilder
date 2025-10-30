"""
Timeline visualization widget for WorldBuilder.
Displays events on an interactive timeline with zoom, pan, and multiple view modes.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, 
    QSlider, QLabel, QScrollArea, QToolBar, QSplitter, QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF, QSize
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle


class TimelineCanvas(FigureCanvas):
    """
    Matplotlib-based canvas for rendering timeline visualization.
    """
    event_clicked = pyqtSignal(object)  # Emits Event object
    
    def __init__(self, parent=None, width=12, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.events = []
        self.timelines = []
        self.selected_timeline_ids = []
        self.view_mode = "linear"  # linear, swimlane, calendar
        self.zoom_level = 1.0
        self.current_marker_date = None
        
        # Connect click event
        self.mpl_connect('button_press_event', self._on_click)
        
    def set_events(self, events: List, timelines: List = None):
        """Set events and optional timelines to display."""
        self.events = events or []
        self.timelines = timelines or []
        self.render_timeline()
        
    def set_timeline_filter(self, timeline_ids: List):
        """Filter events by timeline IDs."""
        self.selected_timeline_ids = timeline_ids
        self.render_timeline()
        
    def set_view_mode(self, mode: str):
        """Set timeline view mode: linear, swimlane, or calendar."""
        self.view_mode = mode
        self.render_timeline()
        
    def set_zoom(self, level: float):
        """Set zoom level (0.1 to 10.0)."""
        self.zoom_level = max(0.1, min(10.0, level))
        self.render_timeline()
        
    def set_current_marker(self, date: Optional[datetime]):
        """Set the 'now' marker position."""
        self.current_marker_date = date
        self.render_timeline()
        
    def render_timeline(self):
        """Render the timeline based on current settings."""
        self.axes.clear()
        
        if not self.events:
            self.axes.text(0.5, 0.5, 'No events to display', 
                          ha='center', va='center', transform=self.axes.transAxes)
            self.draw()
            return
        
        # Filter events by selected timelines if filter is active
        display_events = self._filter_events()
        
        if not display_events:
            self.axes.text(0.5, 0.5, 'No events match filter', 
                          ha='center', va='center', transform=self.axes.transAxes)
            self.draw()
            return
        
        if self.view_mode == "linear":
            self._render_linear(display_events)
        elif self.view_mode == "swimlane":
            self._render_swimlane(display_events)
        elif self.view_mode == "calendar":
            self._render_calendar(display_events)
        
        self.draw()
        
    def _filter_events(self):
        """Filter events based on selected timelines."""
        if not self.selected_timeline_ids:
            return self.events
        
        filtered = []
        for event in self.events:
            # Check if event is in any of the selected timelines
            event_timeline_ids = [t.id for t in getattr(event, 'timelines', [])]
            if any(tid in self.selected_timeline_ids for tid in event_timeline_ids):
                filtered.append(event)
        return filtered
        
    def _render_linear(self, events: List):
        """Render linear timeline view."""
        # Sort events by date
        sorted_events = sorted(events, key=lambda e: self._get_event_date(e))
        
        dates = []
        names = []
        colors = []
        
        for event in sorted_events:
            date = self._get_event_date(event)
            if date:
                dates.append(date)
                names.append(event.name[:30])  # Truncate long names
                colors.append(self._get_event_color(event))
        
        if not dates:
            return
        
        # Plot events
        y_positions = list(range(len(dates)))
        self.axes.scatter(dates, y_positions, s=100, c=colors, alpha=0.7, edgecolors='black')
        
        # Add event labels
        for i, (date, name) in enumerate(zip(dates, names)):
            self.axes.text(date, i, f'  {name}', va='center', fontsize=8)
        
        # Add current marker if set
        if self.current_marker_date:
            self.axes.axvline(self.current_marker_date, color='red', linestyle='--', 
                            linewidth=2, label='Current Point')
        
        # Format x-axis
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.fig.autofmt_xdate()
        
        self.axes.set_ylabel('Events')
        self.axes.set_title('Timeline - Linear View')
        self.axes.grid(True, alpha=0.3)
        
        if self.current_marker_date:
            self.axes.legend()
        
    def _render_swimlane(self, events: List):
        """Render swimlane timeline view with separate lanes per timeline."""
        if not self.timelines:
            self._render_linear(events)
            return
        
        # Group events by timeline
        timeline_events = {}
        for timeline in self.timelines:
            timeline_events[timeline.id] = []
        
        for event in events:
            event_timelines = getattr(event, 'timelines', [])
            for timeline in event_timelines:
                if timeline.id in timeline_events:
                    timeline_events[timeline.id].append(event)
        
        # Plot each timeline as a lane
        lane_height = 1.0
        timeline_names = []
        
        for i, timeline in enumerate(self.timelines):
            y_base = i * lane_height
            timeline_names.append(timeline.name[:20])
            
            # Draw lane background
            if i % 2 == 0:
                self.axes.axhspan(y_base - 0.4, y_base + 0.4, 
                                 facecolor='lightgray', alpha=0.2)
            
            # Plot events in this lane
            lane_events = timeline_events.get(timeline.id, [])
            for event in lane_events:
                date = self._get_event_date(event)
                if date:
                    color = self._get_event_color(event)
                    self.axes.scatter(date, y_base, s=100, c=color, 
                                    alpha=0.7, edgecolors='black')
                    self.axes.text(date, y_base, f'  {event.name[:15]}', 
                                 va='center', fontsize=7)
        
        # Add current marker
        if self.current_marker_date:
            self.axes.axvline(self.current_marker_date, color='red', 
                            linestyle='--', linewidth=2, label='Current Point')
        
        # Format axes
        self.axes.set_yticks([i * lane_height for i in range(len(self.timelines))])
        self.axes.set_yticklabels(timeline_names)
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.fig.autofmt_xdate()
        
        self.axes.set_title('Timeline - Swimlane View')
        self.axes.grid(True, alpha=0.3, axis='x')
        
        if self.current_marker_date:
            self.axes.legend()
        
    def _render_calendar(self, events: List):
        """Render calendar view showing events by month."""
        # Group events by month
        month_events = {}
        for event in events:
            date = self._get_event_date(event)
            if date:
                month_key = date.strftime('%Y-%m')
                if month_key not in month_events:
                    month_events[month_key] = []
                month_events[month_key].append(event)
        
        # Create bar chart of event counts per month
        months = sorted(month_events.keys())
        counts = [len(month_events[m]) for m in months]
        
        if months:
            month_dates = [datetime.strptime(m, '%Y-%m') for m in months]
            colors = ['steelblue' for _ in months]
            
            self.axes.bar(month_dates, counts, width=20, color=colors, alpha=0.7)
            
            # Format
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            self.fig.autofmt_xdate()
            self.axes.set_ylabel('Number of Events')
            self.axes.set_title('Timeline - Calendar View')
            self.axes.grid(True, alpha=0.3, axis='y')
        
    def _get_event_date(self, event) -> Optional[datetime]:
        """Extract date from event."""
        if hasattr(event, 'exact_date') and event.exact_date:
            return event.exact_date
        elif hasattr(event, 'year') and event.year:
            return datetime(event.year, 1, 1)
        return None
        
    def _get_event_color(self, event) -> str:
        """Get color for event based on type or importance."""
        # Color mapping for event types
        type_colors = {
            'birth': 'green',
            'death': 'black',
            'battle': 'red',
            'meeting': 'blue',
            'discovery': 'purple',
            'creation': 'orange',
            'political': 'darkblue',
            'cultural': 'pink',
            'natural': 'brown',
        }
        
        event_type = getattr(event, 'type', '').lower()
        return type_colors.get(event_type, 'gray')
        
    def _on_click(self, mpl_event):
        """Handle click on timeline event."""
        if mpl_event.inaxes != self.axes:
            return
        
        # Find closest event to click
        click_x = mpl_event.xdata
        if not click_x:
            return
        
        try:
            click_date = mdates.num2date(click_x).replace(tzinfo=None)
        except:
            return
        
        closest_event = None
        min_distance = float('inf')
        
        for event in self.events:
            event_date = self._get_event_date(event)
            if event_date:
                distance = abs((event_date - click_date).total_seconds())
                if distance < min_distance:
                    min_distance = distance
                    closest_event = event
        
        if closest_event and min_distance < 86400 * 365:  # Within 1 year
            self.event_clicked.emit(closest_event)


class TimelineWidget(QWidget):
    """
    Complete timeline visualization widget with controls.
    """
    event_selected = pyqtSignal(object)  # Emits Event object
    
    def __init__(self, event_service=None, timeline_service=None, parent=None):
        super().__init__(parent)
        self.event_service = event_service
        self.timeline_service = timeline_service
        self.current_universe_id = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)
        
        # Main area with canvas and event list
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Timeline canvas
        self.canvas = TimelineCanvas(self, width=10, height=6)
        self.canvas.event_clicked.connect(self.event_selected.emit)
        splitter.addWidget(self.canvas)
        
        # Event list
        self.event_list = QListWidget()
        self.event_list.itemDoubleClicked.connect(self._on_event_list_clicked)
        splitter.addWidget(self.event_list)
        
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
    def _create_toolbar(self):
        """Create toolbar with controls."""
        toolbar = QToolBar()
        
        # View mode selector
        toolbar.addWidget(QLabel("View: "))
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Linear", "Swimlane", "Calendar"])
        self.view_combo.currentTextChanged.connect(self._on_view_changed)
        toolbar.addWidget(self.view_combo)
        
        toolbar.addSeparator()
        
        # Zoom controls
        toolbar.addWidget(QLabel("Zoom: "))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(1)
        self.zoom_slider.setMaximum(100)
        self.zoom_slider.setValue(10)
        self.zoom_slider.setMaximumWidth(150)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        toolbar.addWidget(self.zoom_slider)
        
        toolbar.addSeparator()
        
        # Timeline filter
        toolbar.addWidget(QLabel("Timeline: "))
        self.timeline_combo = QComboBox()
        self.timeline_combo.addItem("All Timelines", None)
        self.timeline_combo.currentIndexChanged.connect(self._on_timeline_filter_changed)
        toolbar.addWidget(self.timeline_combo)
        
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
        """Refresh timeline data from services."""
        if not self.current_universe_id:
            return
        
        try:
            # Load events
            if self.event_service:
                events = self.event_service.get_by_universe(self.current_universe_id)
                # Sort by date
                events.sort(key=lambda e: e.exact_date or datetime(e.year or 1, 1, 1) 
                           if hasattr(e, 'exact_date') or hasattr(e, 'year') else datetime.min)
            else:
                events = []
            
            # Load timelines
            if self.timeline_service:
                timelines = self.timeline_service.get_by_universe(self.current_universe_id)
                # Update timeline combo
                self.timeline_combo.clear()
                self.timeline_combo.addItem("All Timelines", None)
                for timeline in timelines:
                    self.timeline_combo.addItem(timeline.name, timeline.id)
            else:
                timelines = []
            
            # Update canvas
            self.canvas.set_events(events, timelines)
            
            # Update event list
            self._update_event_list(events)
            
        except Exception as e:
            print(f"Error refreshing timeline: {e}")
            
    def _update_event_list(self, events):
        """Update the event list widget."""
        self.event_list.clear()
        for event in events:
            date_str = ""
            if hasattr(event, 'exact_date') and event.exact_date:
                date_str = event.exact_date.strftime('%Y-%m-%d')
            elif hasattr(event, 'year') and event.year:
                date_str = str(event.year)
            
            item = QListWidgetItem(f"{date_str} - {event.name}")
            item.setData(Qt.ItemDataRole.UserRole, event)
            self.event_list.addItem(item)
            
    def _on_view_changed(self, view_text):
        """Handle view mode change."""
        mode_map = {"Linear": "linear", "Swimlane": "swimlane", "Calendar": "calendar"}
        self.canvas.set_view_mode(mode_map.get(view_text, "linear"))
        
    def _on_zoom_changed(self, value):
        """Handle zoom change."""
        zoom_level = value / 10.0  # Convert to 0.1-10.0 range
        self.canvas.set_zoom(zoom_level)
        
    def _on_timeline_filter_changed(self, index):
        """Handle timeline filter change."""
        timeline_id = self.timeline_combo.itemData(index)
        if timeline_id:
            self.canvas.set_timeline_filter([timeline_id])
        else:
            self.canvas.set_timeline_filter([])
            
    def _on_event_list_clicked(self, item):
        """Handle event list item click."""
        event = item.data(Qt.ItemDataRole.UserRole)
        if event:
            self.event_selected.emit(event)
