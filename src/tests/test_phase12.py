"""
Tests for Phase 12: Polish & UX
Tests user preferences, performance utilities, and help system
"""

import sys
import os
import pytest
import tempfile
import shutil
import json
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from worldbuilder.views.preferences_dialog import PreferencesDialog, PreferencesManager
from worldbuilder.utils.performance import (EntityCache, LazyLoader, BatchLoader,
                                           ProgressTracker, cached_method)
from worldbuilder.widgets.help_system import HelpBrowser, GettingStartedWizard

# Create QApplication instance for tests
app = QApplication.instance() or QApplication(sys.argv)


class TestPreferencesDialog:
    """Tests for preferences dialog"""
    
    def test_dialog_creation(self):
        """Test creating preferences dialog"""
        dialog = PreferencesDialog()
        assert dialog is not None
        assert dialog.tab_widget is not None
        
    def test_default_preferences(self):
        """Test default preferences"""
        dialog = PreferencesDialog()
        defaults = dialog._default_preferences()
        
        assert 'theme' in defaults
        assert 'auto_save' in defaults
        assert 'shortcuts' in defaults
        assert defaults['theme'] == 'light'
        assert defaults['auto_save'] is True
        
    def test_get_preferences(self):
        """Test getting preferences from UI"""
        dialog = PreferencesDialog()
        preferences = dialog.get_preferences()
        
        assert isinstance(preferences, dict)
        assert 'theme' in preferences
        assert 'auto_save' in preferences
        assert 'font_size' in preferences
        
    def test_load_preferences(self):
        """Test loading preferences into UI"""
        custom_prefs = {
            'theme': 'dark',
            'auto_save': False,
            'font_size': 14,
            'shortcuts': {}
        }
        
        dialog = PreferencesDialog(current_preferences=custom_prefs)
        assert dialog.theme_combo.currentText().lower() == 'dark'
        assert dialog.auto_save_check.isChecked() is False
        assert dialog.font_size_spin.value() == 14


class TestPreferencesManager:
    """Tests for preferences manager"""
    
    @pytest.fixture
    def temp_config_path(self):
        """Create temporary config file path"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        temp_file.close()
        yield temp_file.name
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
            
    def test_manager_creation(self, temp_config_path):
        """Test creating preferences manager"""
        manager = PreferencesManager(config_path=temp_config_path)
        assert manager is not None
        assert manager.preferences is not None
        
    def test_save_and_load(self, temp_config_path):
        """Test saving and loading preferences"""
        manager = PreferencesManager(config_path=temp_config_path)
        
        test_prefs = {
            'theme': 'dark',
            'auto_save': True,
            'font_size': 12
        }
        
        success = manager.save_preferences(test_prefs)
        assert success is True
        
        # Create new manager instance to test loading
        manager2 = PreferencesManager(config_path=temp_config_path)
        assert manager2.preferences['theme'] == 'dark'
        assert manager2.preferences['font_size'] == 12
        
    def test_get_preference(self, temp_config_path):
        """Test getting individual preference"""
        manager = PreferencesManager(config_path=temp_config_path)
        
        theme = manager.get_preference('theme')
        assert theme is not None
        
        # Test with default
        custom = manager.get_preference('nonexistent', 'default_value')
        assert custom == 'default_value'
        
    def test_set_preference(self, temp_config_path):
        """Test setting individual preference"""
        manager = PreferencesManager(config_path=temp_config_path)
        
        manager.set_preference('custom_key', 'custom_value')
        assert manager.preferences['custom_key'] == 'custom_value'


class TestEntityCache:
    """Tests for entity cache"""
    
    def test_cache_creation(self):
        """Test creating entity cache"""
        cache = EntityCache(max_size=10)
        assert cache is not None
        assert cache.max_size == 10
        assert cache.get_size() == 0
        
    def test_cache_put_get(self):
        """Test putting and getting from cache"""
        cache = EntityCache()
        
        test_entity = {'id': 1, 'name': 'Test Entity'}
        cache.put('figure', 1, test_entity)
        
        retrieved = cache.get('figure', 1)
        assert retrieved is not None
        assert retrieved['name'] == 'Test Entity'
        
    def test_cache_miss(self):
        """Test cache miss"""
        cache = EntityCache()
        
        result = cache.get('figure', 999)
        assert result is None
        
    def test_cache_remove(self):
        """Test removing from cache"""
        cache = EntityCache()
        
        cache.put('figure', 1, {'id': 1})
        assert cache.get('figure', 1) is not None
        
        cache.remove('figure', 1)
        assert cache.get('figure', 1) is None
        
    def test_cache_clear(self):
        """Test clearing cache"""
        cache = EntityCache()
        
        cache.put('figure', 1, {'id': 1})
        cache.put('location', 2, {'id': 2})
        assert cache.get_size() == 2
        
        cache.clear()
        assert cache.get_size() == 0
        
    def test_cache_eviction(self):
        """Test cache eviction when max size reached"""
        cache = EntityCache(max_size=3)
        
        cache.put('figure', 1, {'id': 1})
        cache.put('figure', 2, {'id': 2})
        cache.put('figure', 3, {'id': 3})
        assert cache.get_size() == 3
        
        # Adding fourth should evict oldest
        cache.put('figure', 4, {'id': 4})
        assert cache.get_size() == 3


class TestLazyLoader:
    """Tests for lazy loader"""
    
    def test_lazy_loader_creation(self):
        """Test creating lazy loader"""
        loader = LazyLoader(lambda: "test value")
        assert loader is not None
        assert loader.is_loaded() is False
        
    def test_lazy_loading(self):
        """Test lazy loading behavior"""
        call_count = [0]
        
        def expensive_operation():
            call_count[0] += 1
            return "loaded value"
            
        loader = LazyLoader(expensive_operation)
        
        # Not loaded yet
        assert loader.is_loaded() is False
        assert call_count[0] == 0
        
        # Load first time
        value1 = loader.get()
        assert value1 == "loaded value"
        assert loader.is_loaded() is True
        assert call_count[0] == 1
        
        # Get again (should not reload)
        value2 = loader.get()
        assert value2 == "loaded value"
        assert call_count[0] == 1
        
    def test_lazy_loader_reset(self):
        """Test resetting lazy loader"""
        call_count = [0]
        
        def counter():
            call_count[0] += 1
            return call_count[0]
            
        loader = LazyLoader(counter)
        
        value1 = loader.get()
        assert value1 == 1
        
        loader.reset()
        assert loader.is_loaded() is False
        
        value2 = loader.get()
        assert value2 == 2


class TestBatchLoader:
    """Tests for batch loader"""
    
    def test_batch_loader_creation(self):
        """Test creating batch loader"""
        loader = BatchLoader(lambda ids: {id: f"entity_{id}" for id in ids}, batch_size=10)
        assert loader is not None
        assert loader.batch_size == 10
        
    def test_batch_loading(self):
        """Test batch loading"""
        def load_batch(ids):
            return {id: f"entity_{id}" for id in ids}
            
        loader = BatchLoader(load_batch, batch_size=5)
        
        # Add items
        for i in range(1, 8):
            loader.add(i)
            
        # Load all
        results = loader.load()
        
        assert len(results) == 7
        assert results[1] == "entity_1"
        assert results[7] == "entity_7"
        
    def test_batch_clear(self):
        """Test clearing batch"""
        loader = BatchLoader(lambda ids: {})
        
        loader.add(1)
        loader.add(2)
        assert len(loader.pending) == 2
        
        loader.clear()
        assert len(loader.pending) == 0


class TestProgressTracker:
    """Tests for progress tracker"""
    
    def test_progress_tracker_creation(self):
        """Test creating progress tracker"""
        tracker = ProgressTracker(total=100)
        assert tracker is not None
        assert tracker.total == 100
        assert tracker.current == 0
        
    def test_progress_update(self):
        """Test updating progress"""
        tracker = ProgressTracker(total=10)
        
        tracker.update(1)
        assert tracker.current == 1
        
        tracker.update(5)
        assert tracker.current == 6
        
    def test_progress_completion(self):
        """Test progress completion"""
        tracker = ProgressTracker(total=5)
        
        assert tracker.is_complete() is False
        
        for _ in range(5):
            tracker.update()
            
        assert tracker.is_complete() is True
        
    def test_progress_callback(self):
        """Test progress callback"""
        callback_data = []
        
        def callback(current, total, percentage, elapsed):
            callback_data.append({
                'current': current,
                'total': total,
                'percentage': percentage
            })
            
        tracker = ProgressTracker(total=10, callback=callback)
        tracker.update(5)
        
        assert len(callback_data) == 1
        assert callback_data[0]['current'] == 5
        assert callback_data[0]['percentage'] == 50.0
        
    def test_progress_reset(self):
        """Test resetting progress"""
        tracker = ProgressTracker(total=10)
        
        tracker.update(5)
        assert tracker.current == 5
        
        tracker.reset()
        assert tracker.current == 0


class TestCachedMethod:
    """Tests for cached method decorator"""
    
    def test_cached_method(self):
        """Test method caching"""
        call_count = [0]
        
        class TestClass:
            @cached_method(max_size=10)
            def expensive_method(self, x):
                call_count[0] += 1
                return x * 2
                
        obj = TestClass()
        
        # First call
        result1 = obj.expensive_method(5)
        assert result1 == 10
        assert call_count[0] == 1
        
        # Second call with same arg (should use cache)
        result2 = obj.expensive_method(5)
        assert result2 == 10
        assert call_count[0] == 1
        
        # Call with different arg
        result3 = obj.expensive_method(10)
        assert result3 == 20
        assert call_count[0] == 2


class TestHelpBrowser:
    """Tests for help browser"""
    
    def test_help_browser_creation(self):
        """Test creating help browser"""
        browser = HelpBrowser()
        assert browser is not None
        assert browser.browser is not None
        
    def test_help_content_loaded(self):
        """Test that help content is loaded"""
        browser = HelpBrowser()
        content = browser.browser.toHtml()
        
        assert len(content) > 0
        assert "WorldBuilder" in content


class TestGettingStartedWizard:
    """Tests for getting started wizard"""
    
    def test_wizard_creation(self):
        """Test creating wizard"""
        wizard = GettingStartedWizard()
        assert wizard is not None
        assert wizard.pageIds() is not None
        
    def test_wizard_pages(self):
        """Test wizard has pages"""
        wizard = GettingStartedWizard()
        page_count = len(wizard.pageIds())
        
        assert page_count >= 3  # At least welcome, features, and final pages
        
    def test_show_again_option(self):
        """Test show again checkbox"""
        wizard = GettingStartedWizard()
        
        # Default should be True
        assert wizard.should_show_again() is True


def run_phase_12_tests():
    """Run all Phase 12 tests"""
    print("\n" + "="*60)
    print("Running Phase 12 Tests: Polish & UX")
    print("="*60 + "\n")
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_phase_12_tests()
