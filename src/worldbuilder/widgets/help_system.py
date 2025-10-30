"""
Help and Documentation System
Provides in-app help browser and getting started wizard
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextBrowser,
                             QPushButton, QLabel, QWidget, QStackedWidget,
                             QWizard, QWizardPage, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont


class HelpBrowser(QDialog):
    """Help browser dialog with documentation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_help_content()
        
    def setup_ui(self):
        """Set up the help browser UI"""
        self.setWindowTitle("WorldBuilder Help")
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("WorldBuilder Help & Documentation")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Help content browser
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        layout.addWidget(self.browser)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.browser.backward)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton("Forward")
        self.forward_btn.clicked.connect(self.browser.forward)
        self.forward_btn.setEnabled(False)
        nav_layout.addWidget(self.forward_btn)
        
        self.home_btn = QPushButton("Home")
        self.home_btn.clicked.connect(self.load_help_content)
        nav_layout.addWidget(self.home_btn)
        
        nav_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        nav_layout.addWidget(self.close_btn)
        
        layout.addLayout(nav_layout)
        
        # Connect signals
        self.browser.backwardAvailable.connect(self.back_btn.setEnabled)
        self.browser.forwardAvailable.connect(self.forward_btn.setEnabled)
        
    def load_help_content(self):
        """Load main help content"""
        help_html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
                h2 { color: #34495e; margin-top: 20px; }
                .section { margin: 15px 0; }
                .tip { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }
                .shortcut { background: #f5f5f5; padding: 3px 8px; border-radius: 3px; font-family: monospace; }
                ul { line-height: 1.8; }
            </style>
        </head>
        <body>
            <h1>Welcome to WorldBuilder</h1>
            
            <div class="section">
                <h2>Getting Started</h2>
                <p>WorldBuilder helps you create and organize fictional worlds, characters, locations, and timelines.</p>
                <ul>
                    <li>Create a new <strong>Universe</strong> to start your project</li>
                    <li>Add <strong>Locations</strong> to build your world geography</li>
                    <li>Define <strong>Species</strong> and <strong>Races</strong></li>
                    <li>Create <strong>Notable Figures</strong> (characters)</li>
                    <li>Establish <strong>Relationships</strong> between entities</li>
                    <li>Build <strong>Timelines</strong> and track <strong>Events</strong></li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Main Features</h2>
                
                <h3>Universe Management</h3>
                <p>Each universe is a self-contained world with its own entities, relationships, and timeline.</p>
                
                <h3>Location Hierarchy</h3>
                <p>Build complex location hierarchies from continents down to individual buildings.</p>
                
                <h3>Species & Races</h3>
                <p>Define unique species with custom traits, abilities, and characteristics.</p>
                
                <h3>Notable Figures</h3>
                <p>Create characters with relationships, locations, and species assignments.</p>
                
                <h3>Relationships</h3>
                <p>Connect entities with various relationship types (family, alliance, rivalry, etc.).</p>
                
                <h3>Events & Timeline</h3>
                <p>Track historical events with flexible date precision and multiple timeline views.</p>
                
                <h3>Organizations</h3>
                <p>Define factions, governments, guilds, and other organizations.</p>
                
                <h3>Artifacts & Lore</h3>
                <p>Document important items and mythology of your world.</p>
                
                <h3>Search & Filter</h3>
                <p>Quickly find entities using powerful search and filter tools.</p>
            </div>
            
            <div class="section">
                <h2>Keyboard Shortcuts</h2>
                <ul>
                    <li><span class="shortcut">Ctrl+N</span> - Create New Universe</li>
                    <li><span class="shortcut">Ctrl+O</span> - Open Universe</li>
                    <li><span class="shortcut">Ctrl+S</span> - Save</li>
                    <li><span class="shortcut">Ctrl+F</span> - Search</li>
                    <li><span class="shortcut">Ctrl+Shift+L</span> - New Location</li>
                    <li><span class="shortcut">Ctrl+Shift+F</span> - New Figure</li>
                    <li><span class="shortcut">Ctrl+Shift+S</span> - New Species</li>
                    <li><span class="shortcut">Ctrl+Shift+E</span> - New Event</li>
                </ul>
            </div>
            
            <div class="tip">
                <strong>💡 Tip:</strong> Use the Rich Text Editor for detailed descriptions. 
                It supports formatting, markdown, and inline images.
            </div>
            
            <div class="tip">
                <strong>💡 Tip:</strong> Right-click on entities for quick actions and context menus.
            </div>
            
            <div class="section">
                <h2>Data Management</h2>
                <p>Your data is stored in SQLite databases within each universe folder. 
                Media files are organized in a <code>media/</code> subdirectory.</p>
                <ul>
                    <li>Auto-save keeps your work protected</li>
                    <li>Export universes for backup or sharing</li>
                    <li>Import universes from other WorldBuilder instances</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Support</h2>
                <p>For more help, tutorials, and community support:</p>
                <ul>
                    <li>Check the README.md in the project directory</li>
                    <li>View the ROADMAP.md for feature information</li>
                    <li>Report issues on the project repository</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        self.browser.setHtml(help_html)


class GettingStartedWizard(QWizard):
    """Wizard to help new users get started"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_wizard()
        
    def setup_wizard(self):
        """Set up the wizard pages"""
        self.setWindowTitle("Getting Started with WorldBuilder")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        
        # Welcome page
        welcome_page = QWizardPage()
        welcome_page.setTitle("Welcome to WorldBuilder")
        welcome_layout = QVBoxLayout()
        
        welcome_text = QLabel(
            "<h2>Welcome!</h2>"
            "<p>This wizard will help you get started with WorldBuilder.</p>"
            "<p>WorldBuilder is a comprehensive tool for creating and managing "
            "fictional universes, characters, locations, and timelines.</p>"
            "<p>Click 'Next' to learn about the main features.</p>"
        )
        welcome_text.setWordWrap(True)
        welcome_layout.addWidget(welcome_text)
        welcome_page.setLayout(welcome_layout)
        
        self.addPage(welcome_page)
        
        # Features page
        features_page = QWizardPage()
        features_page.setTitle("Key Features")
        features_layout = QVBoxLayout()
        
        features_text = QLabel(
            "<h3>What you can do:</h3>"
            "<ul>"
            "<li><b>Universes:</b> Create separate worlds for different projects</li>"
            "<li><b>Locations:</b> Build hierarchical world geography</li>"
            "<li><b>Species:</b> Define unique races and creatures</li>"
            "<li><b>Characters:</b> Create notable figures with relationships</li>"
            "<li><b>Events:</b> Track historical events on timelines</li>"
            "<li><b>Organizations:</b> Define factions and groups</li>"
            "<li><b>Search:</b> Quickly find anything in your universe</li>"
            "<li><b>Visualization:</b> View timelines and relationship graphs</li>"
            "</ul>"
        )
        features_text.setWordWrap(True)
        features_layout.addWidget(features_text)
        features_page.setLayout(features_layout)
        
        self.addPage(features_page)
        
        # Quick start page
        quickstart_page = QWizardPage()
        quickstart_page.setTitle("Quick Start Guide")
        quickstart_layout = QVBoxLayout()
        
        quickstart_text = QLabel(
            "<h3>Getting Started:</h3>"
            "<ol>"
            "<li>Create a new Universe (File → New Universe)</li>"
            "<li>Add some Locations to build your world</li>"
            "<li>Define Species if you need non-human characters</li>"
            "<li>Create Notable Figures (characters)</li>"
            "<li>Establish Relationships between characters</li>"
            "<li>Add Events to your timeline</li>"
            "</ol>"
            "<p><b>Tip:</b> Start small and build gradually!</p>"
        )
        quickstart_text.setWordWrap(True)
        quickstart_layout.addWidget(quickstart_text)
        quickstart_page.setLayout(quickstart_layout)
        
        self.addPage(quickstart_page)
        
        # Final page
        final_page = QWizardPage()
        final_page.setTitle("Ready to Begin!")
        final_layout = QVBoxLayout()
        
        final_text = QLabel(
            "<h3>You're all set!</h3>"
            "<p>You can access this wizard again from Help → Getting Started.</p>"
            "<p>For detailed help, use Help → Documentation (F1).</p>"
            "<p>Happy worldbuilding!</p>"
        )
        final_text.setWordWrap(True)
        final_layout.addWidget(final_text)
        
        self.show_again_check = QCheckBox("Show this wizard on startup")
        self.show_again_check.setChecked(True)
        final_layout.addWidget(self.show_again_check)
        
        final_page.setLayout(final_layout)
        
        self.addPage(final_page)
        
    def should_show_again(self):
        """Check if wizard should show on next startup"""
        return self.show_again_check.isChecked()
