"""
Media Management System for WorldBuilder
Handles image upload, storage, compression, and gallery display
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from PIL import Image
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QFileDialog, QLabel, QScrollArea, QGridLayout,
                             QDialog, QMessageBox, QSizePolicy)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class MediaManager:
    """Manages media storage and organization for a universe"""
    
    def __init__(self, universe_path):
        """
        Initialize media manager
        
        Args:
            universe_path: Path to universe directory (will create media/ subdirectory)
        """
        self.universe_path = Path(universe_path)
        self.media_dir = self.universe_path / "media"
        self.thumbnails_dir = self.media_dir / "thumbnails"
        self.metadata_file = self.media_dir / "metadata.json"
        
        # Create directories if they don't exist
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnails_dir.mkdir(exist_ok=True)
        
        # Load or initialize metadata
        self.metadata = self._load_metadata()
        
    def _load_metadata(self):
        """Load media metadata from JSON file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
        
    def _save_metadata(self):
        """Save media metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
            
    def add_media(self, source_path, entity_type=None, entity_id=None, 
                  compress=True, max_size=(1920, 1080)):
        """
        Add a media file to the library
        
        Args:
            source_path: Path to the source image file
            entity_type: Type of entity (e.g., 'figure', 'location', 'species')
            entity_id: ID of the entity this media belongs to
            compress: Whether to compress/optimize the image
            max_size: Maximum dimensions for compression (width, height)
            
        Returns:
            str: Filename of the stored media
        """
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
            
        # Generate unique filename with microseconds for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        extension = source_path.suffix.lower()
        filename = f"{timestamp}_{source_path.stem}{extension}"
        dest_path = self.media_dir / filename
        
        # Copy and optionally compress
        if compress and extension in ['.jpg', '.jpeg', '.png', '.bmp']:
            self._compress_image(source_path, dest_path, max_size)
        else:
            shutil.copy2(source_path, dest_path)
            
        # Create thumbnail
        thumbnail_path = self.thumbnails_dir / filename
        self._create_thumbnail(dest_path, thumbnail_path)
        
        # Store metadata
        self.metadata[filename] = {
            'original_name': source_path.name,
            'added_date': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id,
            'file_size': dest_path.stat().st_size,
            'has_thumbnail': thumbnail_path.exists()
        }
        self._save_metadata()
        
        return filename
        
    def _compress_image(self, source_path, dest_path, max_size):
        """Compress and optimize an image"""
        try:
            with Image.open(source_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                # Resize if larger than max_size
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                # Save with optimization
                img.save(dest_path, optimize=True, quality=85)
        except Exception as e:
            # Fallback to simple copy if compression fails
            print(f"Image compression failed: {e}, using copy instead")
            shutil.copy2(source_path, dest_path)
            
    def _create_thumbnail(self, source_path, thumbnail_path, size=(200, 200)):
        """Create a thumbnail for an image"""
        try:
            with Image.open(source_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(thumbnail_path, optimize=True, quality=75)
        except Exception as e:
            print(f"Thumbnail creation failed: {e}")
            
    def get_media_path(self, filename):
        """Get the full path to a media file"""
        return self.media_dir / filename
        
    def get_thumbnail_path(self, filename):
        """Get the full path to a thumbnail"""
        return self.thumbnails_dir / filename
        
    def get_media_for_entity(self, entity_type, entity_id):
        """Get all media files for a specific entity"""
        return [
            filename for filename, meta in self.metadata.items()
            if meta.get('entity_type') == entity_type and 
               meta.get('entity_id') == entity_id
        ]
        
    def delete_media(self, filename):
        """Delete a media file and its thumbnail"""
        media_path = self.media_dir / filename
        thumbnail_path = self.thumbnails_dir / filename
        
        if media_path.exists():
            media_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
            
        if filename in self.metadata:
            del self.metadata[filename]
            self._save_metadata()
            
    def get_all_media(self):
        """Get list of all media files"""
        return list(self.metadata.keys())


class MediaUploadDialog(QDialog):
    """Dialog for uploading media files"""
    
    media_uploaded = pyqtSignal(str)  # Emits filename
    
    def __init__(self, media_manager, entity_type=None, entity_id=None, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the dialog UI"""
        self.setWindowTitle("Upload Media")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Preview area
        self.preview_label = QLabel("No image selected")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(300, 300)
        self.preview_label.setStyleSheet("border: 2px dashed #ccc; background: #f9f9f9;")
        layout.addWidget(self.preview_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.select_btn = QPushButton("Select Image...")
        self.select_btn.clicked.connect(self.select_image)
        btn_layout.addWidget(self.select_btn)
        
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_image)
        btn_layout.addWidget(self.upload_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.selected_path = None
        
    def select_image(self):
        """Open file dialog to select an image"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        
        if filename:
            self.selected_path = filename
            self.show_preview(filename)
            self.upload_btn.setEnabled(True)
            
    def show_preview(self, filename):
        """Show preview of selected image"""
        pixmap = QPixmap(filename)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
        else:
            self.preview_label.setText("Unable to load image")
            
    def upload_image(self):
        """Upload the selected image"""
        if self.selected_path:
            try:
                filename = self.media_manager.add_media(
                    self.selected_path,
                    entity_type=self.entity_type,
                    entity_id=self.entity_id
                )
                self.media_uploaded.emit(filename)
                QMessageBox.information(self, "Success", "Image uploaded successfully!")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload image: {str(e)}")


class MediaGalleryWidget(QWidget):
    """Widget for displaying media gallery"""
    
    media_selected = pyqtSignal(str)  # Emits filename
    
    def __init__(self, media_manager, parent=None):
        super().__init__(parent)
        self.media_manager = media_manager
        self.setup_ui()
        self.refresh()
        
    def setup_ui(self):
        """Set up the gallery UI"""
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_media)
        toolbar.addWidget(self.upload_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(self.refresh_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Gallery area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_widget)
        self.gallery_layout.setSpacing(10)
        
        scroll_area.setWidget(self.gallery_widget)
        layout.addWidget(scroll_area)
        
    def refresh(self):
        """Refresh the gallery display"""
        # Clear existing items
        while self.gallery_layout.count():
            item = self.gallery_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add media items
        media_files = self.media_manager.get_all_media()
        
        if not media_files:
            label = QLabel("No images in gallery")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.gallery_layout.addWidget(label, 0, 0)
            return
            
        row, col = 0, 0
        max_cols = 4
        
        for filename in media_files:
            thumbnail_path = self.media_manager.get_thumbnail_path(filename)
            
            # Create thumbnail button
            btn = QPushButton()
            if thumbnail_path.exists():
                pixmap = QPixmap(str(thumbnail_path))
                btn.setIcon(pixmap.scaled(150, 150, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation))
                btn.setIconSize(QSize(150, 150))
            else:
                btn.setText(filename)
                
            btn.setFixedSize(160, 160)
            btn.clicked.connect(lambda checked, f=filename: self.media_selected.emit(f))
            
            self.gallery_layout.addWidget(btn, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def upload_media(self):
        """Open upload dialog"""
        dialog = MediaUploadDialog(self.media_manager, parent=self)
        dialog.media_uploaded.connect(lambda: self.refresh())
        dialog.exec()
