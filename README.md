<div align="center">

# 🐍 WorldBuilder

### A Comprehensive Worldbuilding & Universe Creation Tool

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-UI_Framework-41CD52?logo=qt)](https://www.riverbankcomputing.com/software/pyqt/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Empower your storytelling with a powerful desktop application designed for authors, storytellers, and creators to build and manage detailed fictional universes.*

[Features](#-features) • [Quick Start](QUICKSTART.md) • [User Guide](USER_GUIDE.md) • [Developer Guide](DEVELOPER_GUIDE.md) • [Roadmap](ROADMAP.md)

</div>

---

## 📖 Overview

**WorldBuilder** is a cross-platform desktop application that helps you create, organize, and maintain consistency across your fictional worlds. Whether you're writing novels, developing serial stories, or creating any narrative content, WorldBuilder provides the tools you need to keep track of every detail in your universe.

### 🎯 Perfect For

- 📚 **Authors** - Maintain consistency across book series
- ✍️ **Storytellers** - Organize complex narratives and plot lines
- 🎮 **Game Masters** - Build rich RPG campaign worlds
- 🎬 **Screenwriters** - Track characters, locations, and events
- 🎨 **Worldbuilding Enthusiasts** - Create detailed fictional universes

---

## ✨ Features

### Core Entity Management

<table>
<tr>
<td width="50%">

#### 👥 Notable Figures
- Create detailed character profiles
- Species/race assignment (defaults to human)
- Track relationships and connections
- Custom attributes and traits
- Image/portrait support

#### 🗺️ Hierarchical Locations
- Nested location structures
- Parent-child relationships
- Visual tree navigation
- From continents to rooms
- Breadcrumb navigation

#### 🧬 Species & Races
- Define custom species
- Physical traits and abilities
- Lifespan and cultural characteristics
- Sentient and non-sentient types
- Template library

</td>
<td width="50%">

#### 📅 Events & Timeline
- Flexible date/time support
- Multiple timeline views
- Event categorization
- Duration tracking
- Entity relationships

#### 🏛️ Organizations
- Factions and groups
- Member management
- Hierarchies and structures
- Relationships to other entities

#### 🏺 Artifacts & Lore
- Important objects and relics
- Mythology and religions
- Cultural elements
- Rich text descriptions

</td>
</tr>
</table>

### Advanced Features

- 🔗 **Relationship Mapping** - Visualize connections between entities with interactive graphs
- ⏳ **Timeline Visualization** - Multiple view modes (linear, branching, calendar, era-based)
- 🔍 **Advanced Search & Filtering** - Find anything quickly with smart filters and saved presets
- 📝 **Rich Text Editor** - Format descriptions with markdown and inline images
- 🗂️ **Tagging System** - Organize entities with custom tags and categories
- 📊 **Data Management** - Export, import, backup, and restore your universes
- 🎨 **Customizable UI** - Themes, layouts, and keyboard shortcuts
- 📅 **Custom Calendars** - Support for fictional calendar systems

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | PyQt6 | Modern cross-platform desktop UI framework |
| **Backend** | Python 3.11+ | Core business logic and services |
| **Database** | SQLite | Embedded, file-based data storage |
| **Architecture** | MVC Pattern | Separation of concerns with Model-View-Controller |
| **Platform** | Windows / macOS / Linux | Cross-platform desktop application |

---

## 📁 Project Structure

```
WorldBuilder/
├── requirements.txt              # Python dependencies
├── setup.py                      # Package configuration
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── docs/                         # Additional documentation
│   ├── quick_start.md           # Getting started guide
│   ├── api_reference.md         # API documentation
│   └── architecture.md          # Architecture overview
└── src/
   ├── worldbuilder/            # Main package
   │   ├── models/              # Domain entities and data models
   │   ├── services/            # Business logic and services
   │   ├── database/            # Data access layer and repositories
   │   ├── utils/               # Shared utilities and helpers
   │   ├── views/               # PyQt6 UI views and windows
   │   ├── controllers/         # Controller logic (MVC pattern)
   │   ├── widgets/             # Custom Qt widgets
   │   ├── resources/           # Icons, images, and assets
   │   └── main.py              # Application entry point
   └── tests/                   # Unit and integration tests
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or later** - [Download here](https://www.python.org/downloads/)
- **pip** (Python package installer)
- **Qt6** libraries (installed automatically with PyQt6)

### Installation & Quick Start

📚 **[See Quick Start Guide →](QUICKSTART.md)** for detailed installation and getting started instructions.

**Quick Steps**:
1. Clone repository and install dependencies
2. Launch WorldBuilder
3. Create your first universe
4. Start building your world!

> 📦 **Coming Soon**: Standalone installation packages will be available when the first release is published.

---

## 💻 Development

📖 **[See Developer Guide →](DEVELOPER_GUIDE.md)** for comprehensive technical documentation.

### Quick Development Setup

```bash
# Clone repository
git clone https://github.com/MrFrey75/WorldBuilder.git
cd WorldBuilder

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/worldbuilder/main.py
```

### Running Tests

```bash
python -m pytest src/tests/ -v
```

---

## 🗺️ Development Roadmap

### Current Status: **All Core Phases Complete** ✓

We're building WorldBuilder through a carefully planned 14-phase development approach. Each phase contains specific, actionable tasks organized into sub-phases.

**[📋 View Complete Roadmap →](ROADMAP.md)**

### Quick Overview

- **Phase 1**: Foundation & Setup ✓ Complete
- **Phase 2**: Universe Management ✓ Complete
- **Phase 3**: Location System with Hierarchical Structure ✓ Complete
- **Phase 4**: Species & Races System ✓ Complete
- **Phase 5**: Notable Figures System ✓ Complete
- **Phase 6**: Relationships & Connections ✓ Complete
- **Phase 7**: Events & Timeline System ✓ Complete
- **Phase 8**: Search & Filter ✓ Complete
- **Phase 9**: Additional Entity Types (Organizations, Artifacts, Lore) ✓ Complete
- **Phase 10**: Visualization ✓ Complete
- **Phase 11**: Rich Content ✓ Complete
- **Phase 12**: Polish & UX ✓ Complete
- **Phase 13**: Data Management (Import/Export, Backup) ✓ Complete
- **Phase 14**: Testing ✓ Complete
- **Deployment**: Post-development (separate from main roadmap)

See the **[detailed roadmap](ROADMAP.md)** for complete task breakdowns and progress tracking.

---

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Write clear, descriptive commit messages
- Add unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact & Support

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Developer Guide**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/MrFrey75/WorldBuilder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MrFrey75/WorldBuilder/discussions)

---

## 🙏 Acknowledgments

Special thanks to:
- The Python and PyQt development community
- All contributors and testers
- Worldbuilding enthusiasts who inspire this project

---

## 📊 Project Status

> ⚠️ **Early Development**: This project is currently in the foundation phase. Features and documentation will be updated as development progresses.

**Last Updated**: October 29, 2025

---

<div align="center">

**[⬆ Back to Top](#-worldbuilder)**

Made with ❤️ for storytellers and worldbuilders everywhere

</div>
