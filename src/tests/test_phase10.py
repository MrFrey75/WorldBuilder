"""
Tests for Phase 10: Visualization
Tests timeline visualization, relationship graphs, and custom calendar systems.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication
import sys

# Ensure QApplication exists
if not QApplication.instance():
    app = QApplication(sys.argv)

from worldbuilder.widgets.timeline_widget import TimelineWidget, TimelineCanvas
from worldbuilder.widgets.relationship_graph_widget import (
    RelationshipGraphWidget, RelationshipGraphCanvas
)
from worldbuilder.utils.calendar_system import (
    CustomCalendar, DateCalculator, CalendarConverter,
    create_calendar_from_preset, PRESET_CALENDARS
)


# Test Fixtures
@pytest.fixture
def sample_events():
    """Create sample events for testing."""
    events = []
    
    for i in range(5):
        event = Mock()
        event.id = f"event-{i}"
        event.name = f"Test Event {i}"
        event.exact_date = datetime(2020 + i, 1, 1)
        event.year = 2020 + i
        event.type = 'meeting'
        event.timelines = []
        events.append(event)
    
    return events


@pytest.fixture
def sample_timelines():
    """Create sample timelines for testing."""
    timelines = []
    
    for i in range(2):
        timeline = Mock()
        timeline.id = f"timeline-{i}"
        timeline.name = f"Timeline {i}"
        timeline.events = []
        timelines.append(timeline)
    
    return timelines


@pytest.fixture
def sample_figures():
    """Create sample figures for testing."""
    figures = []
    
    for i in range(5):
        figure = Mock()
        figure.id = f"figure-{i}"
        figure.name = f"Character {i}"
        figures.append(figure)
    
    return figures


@pytest.fixture
def sample_relationships(sample_figures):
    """Create sample relationships between figures."""
    relationships = []
    
    for i in range(4):
        rel = Mock()
        rel.id = f"rel-{i}"
        rel.from_figure_id = sample_figures[i].id
        rel.to_figure_id = sample_figures[i + 1].id
        rel.type = 'friend'
        rel.strength = 5
        relationships.append(rel)
    
    return relationships


class TestTimelineCanvas:
    """Test timeline canvas functionality."""
    
    def test_canvas_creation(self):
        """Test timeline canvas can be created."""
        canvas = TimelineCanvas()
        assert canvas is not None
        assert canvas.view_mode == "linear"
        assert canvas.zoom_level == 1.0
    
    def test_set_events(self, sample_events, sample_timelines):
        """Test setting events on canvas."""
        canvas = TimelineCanvas()
        canvas.set_events(sample_events, sample_timelines)
        
        assert canvas.events == sample_events
        assert canvas.timelines == sample_timelines
    
    def test_view_modes(self, sample_events):
        """Test different view modes."""
        canvas = TimelineCanvas()
        canvas.set_events(sample_events)
        
        for mode in ["linear", "swimlane", "calendar"]:
            canvas.set_view_mode(mode)
            assert canvas.view_mode == mode
    
    def test_zoom_functionality(self, sample_events):
        """Test zoom levels."""
        canvas = TimelineCanvas()
        canvas.set_events(sample_events)
        
        canvas.set_zoom(2.0)
        assert canvas.zoom_level == 2.0
        
        canvas.set_zoom(0.5)
        assert canvas.zoom_level == 0.5
        
        # Test zoom limits
        canvas.set_zoom(20.0)
        assert canvas.zoom_level == 10.0  # Max zoom
        
        canvas.set_zoom(0.01)
        assert canvas.zoom_level == 0.1  # Min zoom
    
    def test_current_marker(self, sample_events):
        """Test current date marker."""
        canvas = TimelineCanvas()
        canvas.set_events(sample_events)
        
        marker_date = datetime(2022, 6, 1)
        canvas.set_current_marker(marker_date)
        assert canvas.current_marker_date == marker_date
    
    def test_timeline_filtering(self, sample_events, sample_timelines):
        """Test filtering events by timeline."""
        canvas = TimelineCanvas()
        
        # Assign events to timelines
        sample_events[0].timelines = [sample_timelines[0]]
        sample_events[1].timelines = [sample_timelines[1]]
        sample_events[2].timelines = [sample_timelines[0], sample_timelines[1]]
        
        canvas.set_events(sample_events, sample_timelines)
        
        # Filter by timeline 0
        canvas.set_timeline_filter([sample_timelines[0].id])
        filtered = canvas._filter_events()
        
        # Should get events 0 and 2
        assert len(filtered) == 2


class TestTimelineWidget:
    """Test timeline widget functionality."""
    
    def test_widget_creation(self):
        """Test timeline widget can be created."""
        widget = TimelineWidget()
        assert widget is not None
        assert widget.canvas is not None
    
    def test_view_mode_selection(self):
        """Test view mode combo box."""
        widget = TimelineWidget()
        
        widget.view_combo.setCurrentText("Swimlane")
        assert widget.canvas.view_mode == "swimlane"
        
        widget.view_combo.setCurrentText("Calendar")
        assert widget.canvas.view_mode == "calendar"
    
    def test_zoom_slider(self):
        """Test zoom slider functionality."""
        widget = TimelineWidget()
        
        widget.zoom_slider.setValue(50)
        assert widget.canvas.zoom_level == 5.0
        
        widget.zoom_slider.setValue(10)
        assert widget.canvas.zoom_level == 1.0


class TestRelationshipGraphCanvas:
    """Test relationship graph canvas functionality."""
    
    def test_canvas_creation(self):
        """Test graph canvas can be created."""
        canvas = RelationshipGraphCanvas()
        assert canvas is not None
        assert canvas.layout_algorithm == 'spring'
        assert canvas.show_labels is True
    
    def test_set_data(self, sample_figures, sample_relationships):
        """Test setting graph data."""
        canvas = RelationshipGraphCanvas()
        canvas.set_data(sample_figures, sample_relationships)
        
        assert canvas.entities == sample_figures
        assert canvas.relationships == sample_relationships
        assert len(canvas.graph.nodes()) > 0
        assert len(canvas.graph.edges()) > 0
    
    def test_layout_algorithms(self, sample_figures, sample_relationships):
        """Test different layout algorithms."""
        canvas = RelationshipGraphCanvas()
        canvas.set_data(sample_figures, sample_relationships)
        
        for layout in ['spring', 'circular', 'kamada_kawai', 'shell']:
            canvas.set_layout(layout)
            assert canvas.layout_algorithm == layout
    
    def test_label_toggle(self, sample_figures, sample_relationships):
        """Test label visibility toggle."""
        canvas = RelationshipGraphCanvas()
        canvas.set_data(sample_figures, sample_relationships)
        
        canvas.set_show_labels(False)
        assert canvas.show_labels is False
        
        canvas.set_show_labels(True)
        assert canvas.show_labels is True
    
    def test_entity_focus(self, sample_figures, sample_relationships):
        """Test focusing on specific entity."""
        canvas = RelationshipGraphCanvas()
        canvas.set_data(sample_figures, sample_relationships)
        
        # Focus on first figure
        canvas.focus_on_entity(sample_figures[0].id)
        assert canvas.focused_entity_id == sample_figures[0].id
        
        # Should rebuild graph with only focused entity and connections
        assert len(canvas.graph.nodes()) <= len(sample_figures)
        
        # Clear focus
        canvas.clear_focus()
        assert canvas.focused_entity_id is None


class TestRelationshipGraphWidget:
    """Test relationship graph widget functionality."""
    
    def test_widget_creation(self):
        """Test graph widget can be created."""
        widget = RelationshipGraphWidget()
        assert widget is not None
        assert widget.canvas is not None
    
    def test_layout_selection(self):
        """Test layout combo box."""
        widget = RelationshipGraphWidget()
        
        widget.layout_combo.setCurrentText("Circular")
        assert widget.canvas.layout_algorithm == "circular"
        
        widget.layout_combo.setCurrentText("Shell")
        assert widget.canvas.layout_algorithm == "shell"
    
    def test_labels_checkbox(self):
        """Test labels checkbox."""
        widget = RelationshipGraphWidget()
        
        widget.labels_checkbox.setChecked(False)
        assert widget.canvas.show_labels is False
        
        widget.labels_checkbox.setChecked(True)
        assert widget.canvas.show_labels is True


class TestCustomCalendar:
    """Test custom calendar system."""
    
    def test_calendar_creation(self):
        """Test creating custom calendar."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1",
            days_per_week=7,
            months_per_year=12,
            days_per_year=365
        )
        
        assert calendar.id == "cal-1"
        assert calendar.name == "Test Calendar"
        assert calendar.days_per_week == 7
    
    def test_month_names(self):
        """Test month name retrieval."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        assert calendar.get_month_name(1) == "January"
        assert calendar.get_month_name(12) == "December"
    
    def test_days_in_month(self):
        """Test days in month calculation."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        assert calendar.get_days_in_month(1) == 31  # January
        assert calendar.get_days_in_month(2) == 28  # February
        assert calendar.get_days_in_month(4) == 30  # April
    
    def test_date_formatting(self):
        """Test date formatting."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        formatted = calendar.format_date(2024, 3, 15)
        assert "15" in formatted
        assert "March" in formatted
        assert "2024" in formatted
    
    def test_negative_years(self):
        """Test negative year support."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1",
            allow_negative_years=True,
            before_epoch_abbreviation="BCE"
        )
        
        formatted = calendar.format_date(-500, 1, 1)
        assert "500" in formatted
        assert "BCE" in formatted
    
    def test_serialization(self):
        """Test calendar to/from dict."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        data = calendar.to_dict()
        assert data['id'] == "cal-1"
        assert data['name'] == "Test Calendar"
        
        restored = CustomCalendar.from_dict(data)
        assert restored.id == calendar.id
        assert restored.name == calendar.name


class TestDateCalculator:
    """Test date calculator utilities."""
    
    def test_days_between(self):
        """Test days between calculation."""
        date1 = datetime(2024, 1, 1)
        date2 = datetime(2024, 1, 31)
        
        days = DateCalculator.days_between(date1, date2)
        assert days == 30
    
    def test_years_between(self):
        """Test years between calculation."""
        date1 = datetime(2020, 1, 1)
        date2 = datetime(2024, 1, 1)
        
        years = DateCalculator.years_between(date1, date2)
        assert abs(years - 4.0) < 0.1
    
    def test_age_calculation(self):
        """Test age calculation."""
        birth = datetime(2000, 6, 15)
        current = datetime(2024, 6, 20)
        
        age = DateCalculator.calculate_age(birth, current)
        assert age == 24
        
        # Test before birthday
        current = datetime(2024, 6, 10)
        age = DateCalculator.calculate_age(birth, current)
        assert age == 23
    
    def test_custom_calendar_age(self):
        """Test age calculation in custom calendar."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        age = DateCalculator.custom_calculate_age(
            birth_year=2000, birth_month=6, birth_day=15,
            current_year=2024, current_month=6, current_day=20,
            calendar=calendar
        )
        
        assert age == 24
    
    def test_duration_formatting(self):
        """Test duration formatting."""
        assert "5 days" in DateCalculator.format_duration(5)
        assert "week" in DateCalculator.format_duration(7)
        assert "month" in DateCalculator.format_duration(30)
        assert "year" in DateCalculator.format_duration(365)


class TestCalendarConverter:
    """Test calendar conversion utilities."""
    
    def test_standard_to_custom(self):
        """Test standard to custom calendar conversion."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1",
            days_per_year=365
        )
        
        standard_date = datetime(2024, 6, 15)
        year, month, day = CalendarConverter.standard_to_custom(standard_date, calendar)
        
        assert year > 0
        assert 1 <= month <= 12
        assert 1 <= day <= 31
    
    def test_custom_to_standard(self):
        """Test custom to standard calendar conversion."""
        calendar = CustomCalendar(
            id="cal-1",
            name="Test Calendar",
            universe_id="universe-1"
        )
        
        standard_date = CalendarConverter.custom_to_standard(2024, 6, 15, calendar)
        assert isinstance(standard_date, datetime)


class TestCalendarPresets:
    """Test calendar preset templates."""
    
    def test_preset_names(self):
        """Test available presets."""
        assert "gregorian" in PRESET_CALENDARS
        assert "tolkien" in PRESET_CALENDARS
        assert "fantasy_13" in PRESET_CALENDARS
    
    def test_create_from_preset(self):
        """Test creating calendar from preset."""
        calendar = create_calendar_from_preset("gregorian", "universe-1", "cal-1")
        
        assert calendar.id == "cal-1"
        assert calendar.universe_id == "universe-1"
        assert calendar.months_per_year == 12
        assert calendar.days_per_week == 7
    
    def test_tolkien_calendar(self):
        """Test Tolkien Shire calendar preset."""
        calendar = create_calendar_from_preset("tolkien", "universe-1", "cal-1")
        
        assert "Afteryule" in calendar.month_definitions
        assert "Sterday" in calendar.weekday_names
        assert calendar.epoch_abbreviation == "SR"
    
    def test_13month_calendar(self):
        """Test 13-month calendar preset."""
        calendar = create_calendar_from_preset("fantasy_13", "universe-1", "cal-1")
        
        assert calendar.months_per_year == 13
        assert calendar.days_per_year == 364
        assert "Primus" in calendar.month_definitions


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
