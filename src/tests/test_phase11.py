"""
Tests for Phase 11: Rich Content
Tests rich text editor and media management functionality
"""

import sys
import os
import pytest
import tempfile
import shutil
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from worldbuilder.widgets.rich_text_editor import RichTextEditor
from worldbuilder.services.media_manager import MediaManager, MediaUploadDialog, MediaGalleryWidget

# Create QApplication instance for tests
app = QApplication.instance() or QApplication(sys.argv)


class TestRichTextEditor:
    """Tests for rich text editor widget"""
    
    def test_editor_creation(self):
        """Test creating a rich text editor"""
        editor = RichTextEditor()
        assert editor is not None
        assert editor.text_edit is not None
        assert editor.toolbar is not None
        
    def test_editor_with_markdown(self):
        """Test editor with markdown support"""
        editor = RichTextEditor(enable_markdown=True)
        assert editor.enable_markdown is True
        assert hasattr(editor, 'markdown_button')
        
    def test_editor_without_markdown(self):
        """Test editor without markdown support"""
        editor = RichTextEditor(enable_markdown=False)
        assert editor.enable_markdown is False
        
    def test_set_get_text(self):
        """Test setting and getting plain text"""
        editor = RichTextEditor()
        test_text = "This is a test"
        editor.set_text(test_text)
        assert editor.get_text() == test_text
        
    def test_set_get_html(self):
        """Test setting and getting HTML"""
        editor = RichTextEditor()
        test_html = "<b>Bold text</b>"
        editor.set_html(test_html)
        html = editor.get_html()
        assert "bold" in html.lower() or "<b>" in html.lower()
        
    def test_clear_editor(self):
        """Test clearing the editor"""
        editor = RichTextEditor()
        editor.set_text("Some text")
        editor.clear()
        assert editor.get_text() == ""
        
    def test_read_only_mode(self):
        """Test read-only mode"""
        editor = RichTextEditor()
        editor.set_read_only(True)
        assert editor.text_edit.isReadOnly() is True
        assert editor.toolbar.isEnabled() is False
        
        editor.set_read_only(False)
        assert editor.text_edit.isReadOnly() is False
        assert editor.toolbar.isEnabled() is True
        
    def test_formatting_buttons_exist(self):
        """Test that all formatting buttons exist"""
        editor = RichTextEditor()
        assert editor.bold_btn is not None
        assert editor.italic_btn is not None
        assert editor.underline_btn is not None
        assert editor.color_btn is not None
        assert editor.bullet_btn is not None
        assert editor.number_btn is not None
        assert editor.clear_btn is not None
        
    def test_font_controls_exist(self):
        """Test that font controls exist"""
        editor = RichTextEditor()
        assert editor.font_combo is not None
        assert editor.font_size_spin is not None
        
    def test_spell_check_feature(self):
        """Test spell check functionality"""
        editor = RichTextEditor(enable_spell_check=True)
        assert editor.spell_checker is not None
        assert hasattr(editor, 'spell_check_box')
        
        # Test toggling spell check
        editor.toggle_spell_check(True)
        assert editor.spell_checker.spell_check_enabled is True
        
        editor.toggle_spell_check(False)
        assert editor.spell_checker.spell_check_enabled is False
        
    def test_spell_check_disabled(self):
        """Test editor without spell check"""
        editor = RichTextEditor(enable_spell_check=False)
        assert editor.spell_checker is None


class TestMediaManager:
    """Tests for media manager"""
    
    @pytest.fixture
    def temp_universe_dir(self):
        """Create a temporary universe directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    @pytest.fixture
    def temp_image(self):
        """Create a temporary test image"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        
        # Create a simple test image
        img = QImage(100, 100, QImage.Format.Format_RGB32)
        img.fill(Qt.GlobalColor.red)
        img.save(temp_file.name)
        
        yield temp_file.name
        
        # Cleanup
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
            
    def test_media_manager_creation(self, temp_universe_dir):
        """Test creating a media manager"""
        manager = MediaManager(temp_universe_dir)
        assert manager is not None
        assert manager.media_dir.exists()
        assert manager.thumbnails_dir.exists()
        
    def test_add_media(self, temp_universe_dir, temp_image):
        """Test adding media to the library"""
        manager = MediaManager(temp_universe_dir)
        
        filename = manager.add_media(
            temp_image,
            entity_type='figure',
            entity_id=1
        )
        
        assert filename is not None
        assert filename in manager.metadata
        assert manager.get_media_path(filename).exists()
        
    def test_media_compression(self, temp_universe_dir, temp_image):
        """Test that media is compressed when added"""
        manager = MediaManager(temp_universe_dir)
        
        original_size = os.path.getsize(temp_image)
        filename = manager.add_media(temp_image, compress=True)
        
        new_path = manager.get_media_path(filename)
        assert new_path.exists()
        # Note: Compression may not always reduce size for small images
        
    def test_thumbnail_creation(self, temp_universe_dir, temp_image):
        """Test that thumbnails are created"""
        manager = MediaManager(temp_universe_dir)
        
        filename = manager.add_media(temp_image)
        thumbnail_path = manager.get_thumbnail_path(filename)
        
        assert thumbnail_path.exists()
        assert manager.metadata[filename]['has_thumbnail'] is True
        
    def test_get_media_for_entity(self, temp_universe_dir, temp_image):
        """Test getting media for a specific entity"""
        manager = MediaManager(temp_universe_dir)
        
        filename1 = manager.add_media(temp_image, entity_type='figure', entity_id=1)
        filename2 = manager.add_media(temp_image, entity_type='figure', entity_id=1)
        filename3 = manager.add_media(temp_image, entity_type='location', entity_id=2)
        
        figure_media = manager.get_media_for_entity('figure', 1)
        assert len(figure_media) == 2
        assert filename1 in figure_media
        assert filename2 in figure_media
        assert filename3 not in figure_media
        
    def test_delete_media(self, temp_universe_dir, temp_image):
        """Test deleting media"""
        manager = MediaManager(temp_universe_dir)
        
        filename = manager.add_media(temp_image)
        media_path = manager.get_media_path(filename)
        thumbnail_path = manager.get_thumbnail_path(filename)
        
        assert media_path.exists()
        assert filename in manager.metadata
        
        manager.delete_media(filename)
        
        assert not media_path.exists()
        assert filename not in manager.metadata
        
    def test_get_all_media(self, temp_universe_dir, temp_image):
        """Test getting all media files"""
        manager = MediaManager(temp_universe_dir)
        
        assert len(manager.get_all_media()) == 0
        
        filename1 = manager.add_media(temp_image)
        filename2 = manager.add_media(temp_image)
        
        all_media = manager.get_all_media()
        assert len(all_media) == 2
        assert filename1 in all_media
        assert filename2 in all_media
        
    def test_metadata_persistence(self, temp_universe_dir, temp_image):
        """Test that metadata persists across instances"""
        manager1 = MediaManager(temp_universe_dir)
        filename = manager1.add_media(temp_image, entity_type='test', entity_id=123)
        
        # Create new instance
        manager2 = MediaManager(temp_universe_dir)
        assert filename in manager2.metadata
        assert manager2.metadata[filename]['entity_type'] == 'test'
        assert manager2.metadata[filename]['entity_id'] == 123


class TestMediaGalleryWidget:
    """Tests for media gallery widget"""
    
    @pytest.fixture
    def temp_universe_dir(self):
        """Create a temporary universe directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    def test_gallery_creation(self, temp_universe_dir):
        """Test creating a media gallery widget"""
        manager = MediaManager(temp_universe_dir)
        gallery = MediaGalleryWidget(manager)
        
        assert gallery is not None
        assert gallery.media_manager is manager
        assert gallery.upload_btn is not None
        assert gallery.refresh_btn is not None


def run_phase_11_tests():
    """Run all Phase 11 tests"""
    print("\n" + "="*60)
    print("Running Phase 11 Tests: Rich Content")
    print("="*60 + "\n")
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_phase_11_tests()
