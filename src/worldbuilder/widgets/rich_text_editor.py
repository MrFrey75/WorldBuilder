"""
Rich Text Editor Widget with Formatting Toolbar
Supports bold, italic, underline, lists, and basic markdown
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QToolBar, QToolButton, QFontComboBox, QSpinBox,
                             QColorDialog, QLabel, QCheckBox)
from PyQt6.QtGui import (QTextCharFormat, QFont, QColor, QTextCursor, 
                         QTextListFormat, QAction, QIcon, QTextDocument,
                         QSyntaxHighlighter, QTextFormat)
from PyQt6.QtCore import Qt, pyqtSignal, QRegularExpression
import markdown
import re


class SpellCheckHighlighter(QSyntaxHighlighter):
    """Basic spell checker using simple word list"""
    
    def __init__(self, document):
        super().__init__(document)
        self.spell_check_enabled = False
        # Basic English word pattern (words with letters and apostrophes)
        self.word_pattern = QRegularExpression(r"\b[A-Za-z']+\b")
        
        # Simple common words dictionary (expandable)
        self.known_words = self._load_basic_dictionary()
        
    def _load_basic_dictionary(self):
        """Load a basic dictionary of common words"""
        # This is a minimal set - in production, load from a file
        common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            'is', 'was', 'are', 'been', 'has', 'had', 'were', 'said', 'did', 'having',
            'may', 'should', 'am', 'being', 'does', 'done', 'world', 'character', 'story',
            'location', 'species', 'figure', 'event', 'timeline', 'universe', 'relationship'
        }
        return common_words
        
    def set_enabled(self, enabled):
        """Enable or disable spell checking"""
        self.spell_check_enabled = enabled
        self.rehighlight()
        
    def highlightBlock(self, text):
        """Highlight misspelled words"""
        if not self.spell_check_enabled:
            return
            
        # Format for misspelled words (red underline)
        misspelled_format = QTextCharFormat()
        misspelled_format.setUnderlineColor(QColor(Qt.GlobalColor.red))
        misspelled_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        
        # Find all words
        iterator = self.word_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            word = match.captured(0).lower()
            
            # Check if word is unknown (simple check - not in dictionary)
            if len(word) > 2 and word not in self.known_words:
                # Check if it's a proper noun (starts with capital)
                if not match.captured(0)[0].isupper():
                    self.setFormat(match.capturedStart(0), 
                                 match.capturedLength(0), 
                                 misspelled_format)


class RichTextEditor(QWidget):
    """Rich text editor with formatting toolbar and markdown support"""
    
    textChanged = pyqtSignal()
    
    def __init__(self, parent=None, enable_markdown=True, enable_spell_check=True):
        super().__init__(parent)
        self.enable_markdown = enable_markdown
        self.enable_spell_check_option = enable_spell_check
        self.spell_checker = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the editor UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create toolbar
        self.toolbar = self.create_toolbar()
        layout.addWidget(self.toolbar)
        
        # Create text editor
        self.text_edit = QTextEdit()
        self.text_edit.setAcceptRichText(True)
        self.text_edit.textChanged.connect(self.textChanged.emit)
        self.text_edit.cursorPositionChanged.connect(self.update_format_buttons)
        layout.addWidget(self.text_edit)
        
        # Set up spell checker if enabled
        if self.enable_spell_check_option:
            self.spell_checker = SpellCheckHighlighter(self.text_edit.document())
        
        # Bottom controls layout
        bottom_layout = QHBoxLayout()
        
        # Markdown mode toggle (if enabled)
        if self.enable_markdown:
            self.markdown_label = QLabel("Markdown Mode:")
            self.markdown_button = QToolButton()
            self.markdown_button.setCheckable(True)
            self.markdown_button.setText("MD")
            self.markdown_button.setToolTip("Toggle Markdown Mode")
            self.markdown_button.toggled.connect(self.toggle_markdown_mode)
            bottom_layout.addWidget(self.markdown_label)
            bottom_layout.addWidget(self.markdown_button)
            
        # Spell check toggle (if enabled)
        if self.enable_spell_check_option and self.spell_checker:
            self.spell_check_box = QCheckBox("Spell Check")
            self.spell_check_box.setChecked(False)
            self.spell_check_box.toggled.connect(self.toggle_spell_check)
            bottom_layout.addWidget(self.spell_check_box)
            
        bottom_layout.addStretch()
        
        if bottom_layout.count() > 1:  # Only add if there are controls
            layout.addLayout(bottom_layout)
            
    def create_toolbar(self):
        """Create the formatting toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        
        # Font family
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.change_font_family)
        toolbar.addWidget(self.font_combo)
        
        toolbar.addSeparator()
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(11)
        self.font_size_spin.setSuffix(" pt")
        self.font_size_spin.valueChanged.connect(self.change_font_size)
        toolbar.addWidget(self.font_size_spin)
        
        toolbar.addSeparator()
        
        # Bold
        self.bold_btn = QToolButton()
        self.bold_btn.setCheckable(True)
        self.bold_btn.setText("B")
        self.bold_btn.setFont(QFont("", -1, QFont.Weight.Bold))
        self.bold_btn.setToolTip("Bold (Ctrl+B)")
        self.bold_btn.clicked.connect(self.toggle_bold)
        toolbar.addWidget(self.bold_btn)
        
        # Italic
        self.italic_btn = QToolButton()
        self.italic_btn.setCheckable(True)
        self.italic_btn.setText("I")
        font = QFont()
        font.setItalic(True)
        self.italic_btn.setFont(font)
        self.italic_btn.setToolTip("Italic (Ctrl+I)")
        self.italic_btn.clicked.connect(self.toggle_italic)
        toolbar.addWidget(self.italic_btn)
        
        # Underline
        self.underline_btn = QToolButton()
        self.underline_btn.setCheckable(True)
        self.underline_btn.setText("U")
        font = QFont()
        font.setUnderline(True)
        self.underline_btn.setFont(font)
        self.underline_btn.setToolTip("Underline (Ctrl+U)")
        self.underline_btn.clicked.connect(self.toggle_underline)
        toolbar.addWidget(self.underline_btn)
        
        toolbar.addSeparator()
        
        # Text color
        self.color_btn = QToolButton()
        self.color_btn.setText("A")
        self.color_btn.setToolTip("Text Color")
        self.color_btn.clicked.connect(self.change_text_color)
        toolbar.addWidget(self.color_btn)
        
        toolbar.addSeparator()
        
        # Bullet list
        self.bullet_btn = QToolButton()
        self.bullet_btn.setText("•")
        self.bullet_btn.setToolTip("Bullet List")
        self.bullet_btn.clicked.connect(self.insert_bullet_list)
        toolbar.addWidget(self.bullet_btn)
        
        # Numbered list
        self.number_btn = QToolButton()
        self.number_btn.setText("1.")
        self.number_btn.setToolTip("Numbered List")
        self.number_btn.clicked.connect(self.insert_numbered_list)
        toolbar.addWidget(self.number_btn)
        
        toolbar.addSeparator()
        
        # Clear formatting
        self.clear_btn = QToolButton()
        self.clear_btn.setText("Clear")
        self.clear_btn.setToolTip("Clear Formatting")
        self.clear_btn.clicked.connect(self.clear_formatting)
        toolbar.addWidget(self.clear_btn)
        
        return toolbar
        
    def update_format_buttons(self):
        """Update toolbar buttons based on current cursor position"""
        fmt = self.text_edit.currentCharFormat()
        
        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())
        
        # Update font combo and size
        self.font_combo.setCurrentFont(fmt.font())
        if fmt.font().pointSize() > 0:
            self.font_size_spin.setValue(int(fmt.font().pointSize()))
            
    def toggle_bold(self):
        """Toggle bold formatting"""
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.bold_btn.isChecked() else QFont.Weight.Normal)
        self.merge_format(fmt)
        
    def toggle_italic(self):
        """Toggle italic formatting"""
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.merge_format(fmt)
        
    def toggle_underline(self):
        """Toggle underline formatting"""
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.merge_format(fmt)
        
    def change_font_family(self, font):
        """Change font family"""
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.merge_format(fmt)
        
    def change_font_size(self, size):
        """Change font size"""
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format(fmt)
        
    def change_text_color(self):
        """Change text color"""
        color = QColorDialog.getColor(Qt.GlobalColor.black, self, "Select Text Color")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format(fmt)
            
    def insert_bullet_list(self):
        """Insert a bullet list"""
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()
        
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDisc)
        cursor.createList(list_format)
        
        cursor.endEditBlock()
        
    def insert_numbered_list(self):
        """Insert a numbered list"""
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()
        
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDecimal)
        cursor.createList(list_format)
        
        cursor.endEditBlock()
        
    def clear_formatting(self):
        """Clear all formatting from selected text"""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.setCharFormat(QTextCharFormat())
            
    def merge_format(self, fmt):
        """Merge character format with current selection"""
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.text_edit.mergeCurrentCharFormat(fmt)
        
    def toggle_markdown_mode(self, enabled):
        """Toggle between rich text and markdown mode"""
        if enabled:
            # Convert to plain markdown
            html = self.text_edit.toHtml()
            # Basic HTML to Markdown conversion (simplified)
            text = self.text_edit.toPlainText()
            self.text_edit.setAcceptRichText(False)
            self.text_edit.setPlainText(text)
            self.toolbar.setEnabled(False)
        else:
            # Convert markdown to HTML
            markdown_text = self.text_edit.toPlainText()
            try:
                html = markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
                self.text_edit.setAcceptRichText(True)
                self.text_edit.setHtml(html)
                self.toolbar.setEnabled(True)
            except Exception as e:
                print(f"Markdown parsing error: {e}")
                self.text_edit.setAcceptRichText(True)
                self.toolbar.setEnabled(True)
                
    def get_html(self):
        """Get content as HTML"""
        return self.text_edit.toHtml()
        
    def get_text(self):
        """Get content as plain text"""
        return self.text_edit.toPlainText()
        
    def set_html(self, html):
        """Set content from HTML"""
        self.text_edit.setHtml(html)
        
    def set_text(self, text):
        """Set content from plain text"""
        self.text_edit.setPlainText(text)
        
    def clear(self):
        """Clear the editor"""
        self.text_edit.clear()
        
    def set_read_only(self, read_only):
        """Set read-only mode"""
        self.text_edit.setReadOnly(read_only)
        self.toolbar.setEnabled(not read_only)
        
    def toggle_spell_check(self, enabled):
        """Toggle spell checking"""
        if self.spell_checker:
            self.spell_checker.set_enabled(enabled)
