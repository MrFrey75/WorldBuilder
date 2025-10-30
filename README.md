<div align="center">

# 🐍 WorldBuilder

### A Comprehensive Worldbuilding & Universe Creation Tool

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-UI_Framework-41CD52?logo=qt)](https://www.riverbankcomputing.com/software/pyqt/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-TBD-green.svg)](LICENSE)

*Empower your storytelling with a powerful desktop application designed for authors, storytellers, and creators to build and manage detailed fictional universes.*

[Features](#-features) • [Getting Started](#-getting-started) • [Development](#-development) • [Roadmap](ROADMAP.md) • [Contributing](#-contributing)

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

### Installation

> 📦 **Coming Soon**: Installation packages will be available when the first release is published.

For now, you can build from source (see [Development Setup](#development-setup) below).

### Quick Start

1. **Launch WorldBuilder**
2. **Create a New Universe** - Start with a blank canvas
3. **Add Your First Entity** - Create a character, location, or event
4. **Build Relationships** - Connect entities to establish your world's structure
5. **Explore & Expand** - Use the timeline, search, and visualization tools

---

## 💻 Development

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MrFrey75/WorldBuilder.git
   cd WorldBuilder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/worldbuilder/main.py
   ```

### Building for Release

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --windowed --onefile --name WorldBuilder src/worldbuilder/main.py
```

---

## 🗺️ Development Roadmap

### Current Status: **Phase 1 - Foundation** 🏗️

We're building WorldBuilder through a carefully planned 14-phase development approach. Each phase contains specific, actionable tasks organized into sub-phases.

**[📋 View Complete Roadmap →](ROADMAP.md)**

### Quick Overview

- **Phase 1**: Foundation & Setup *(Current - 60% Complete)*
- **Phase 2**: Universe Management
- **Phase 3**: Location System with Hierarchical Structure
- **Phase 4**: Species & Races System
- **Phase 5**: Notable Figures System
- **Phase 6**: Search & Filter
- **Phase 7**: Relationships & Connections
- **Phase 8**: Events & Timeline System
- **Phase 9**: Additional Entity Types (Organizations, Artifacts, Lore)
- **Phase 10**: Rich Content (Text Editor, Media)
- **Phase 11**: Timeline Visualization & Graphs
- **Phase 12**: Data Management (Import/Export, Backup)
- **Phase 13**: Polish & UX
- **Phase 14**: Testing & Deployment

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

*License information to be added*

---

## 📞 Contact & Support

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

### A Comprehensive Worldbuilding & Universe Creation Tool

[![.NET](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![WPF](https://img.shields.io/badge/WPF-Windows-0078D4?logo=windows)](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-TBD-green.svg)](LICENSE)

*Empower your storytelling with a powerful desktop application designed for authors, storytellers, and creators to build and manage detailed fictional universes.*

[Features](#-features) • [Getting Started](#-getting-started) • [Development](#-development) • [Roadmap](ROADMAP.md) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**WorldBuilder** is a desktop application that helps you create, organize, and maintain consistency across your fictional worlds. Whether you're writing novels, developing serial stories, or creating any narrative content, WorldBuilder provides the tools you need to keep track of every detail in your universe.

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
| **Frontend** | WPF (Windows Presentation Foundation) | Rich desktop UI with MVVM pattern |
| **Backend** | .NET 8 / C# | Core business logic and services |
| **Database** | SQLite | Embedded, file-based data storage |
| **Architecture** | Clean Architecture | Separation of concerns with Core + Presentation layers |
| **Platform** | Windows 10+ | Desktop application for Windows |

---

## 📁 Project Structure

```
WorldBuilder/
├── WorldBuilder.sln              # .NET solution file
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
├── docs/                          # Additional documentation
│   ├── quick_start.md            # Getting started guide
│   ├── api_reference.md          # API documentation
│   └── architecture.md           # Architecture overview
└── src/
    ├── WorldBuilder.Core/        # Core C# class library
    │   ├── Models/               # Domain entities and data models
    │   ├── Services/             # Business logic and services
    │   ├── Database/             # Data access layer and repositories
    │   ├── Common/               # Shared utilities and helpers
    │   └── Interfaces/           # Contracts and abstractions
    └── WorldBuilder.Creator/     # WPF MVVM application
        ├── Views/                # XAML views and windows
        ├── ViewModels/           # View models implementing MVVM
        ├── Commands/             # Relay commands and command handlers
        ├── Converters/           # Value converters for data binding
        ├── Resources/            # Styles, templates, and assets
        └── App.xaml              # Application entry point
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Windows 10 or later**
- **.NET 8.0 SDK** - [Download here](https://dotnet.microsoft.com/download/dotnet/8.0)
- **Visual Studio 2022** (for development) - [Community Edition](https://visualstudio.microsoft.com/vs/community/) is free

### Installation

> 📦 **Coming Soon**: Installation packages will be available when the first release is published.

For now, you can build from source (see [Development Setup](#development-setup) below).

### Quick Start

1. **Launch WorldBuilder**
2. **Create a New Universe** - Start with a blank canvas
3. **Add Your First Entity** - Create a character, location, or event
4. **Build Relationships** - Connect entities to establish your world's structure
5. **Explore & Expand** - Use the timeline, search, and visualization tools

---

## 💻 Development

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MrFrey75/WorldBuilder.git
   cd WorldBuilder
   ```

2. **Open the solution**
   - Launch Visual Studio 2022
   - Open `WorldBuilder.sln`

3. **Restore NuGet packages**
   ```bash
   dotnet restore
   ```

4. **Build the solution**
   ```bash
   dotnet build
   ```

5. **Run the application**
   ```bash
   dotnet run --project src/WorldBuilder.Creator
   ```
   Or press `F5` in Visual Studio to start debugging.

### Building for Release

```bash
dotnet publish src/WorldBuilder.Creator -c Release -r win-x64 --self-contained
```

---

## 🗺️ Development Roadmap

### Current Status: **Phase 1 - Foundation** 🏗️

We're building WorldBuilder through a carefully planned 14-phase development approach. Each phase contains specific, actionable tasks organized into sub-phases.

**[📋 View Complete Roadmap →](ROADMAP.md)**

### Quick Overview

- **Phase 1**: Foundation & Setup *(Current - 60% Complete)*
- **Phase 2**: Universe Management
- **Phase 3**: Location System with Hierarchical Structure
- **Phase 4**: Species & Races System
- **Phase 5**: Notable Figures System
- **Phase 6**: Search & Filter
- **Phase 7**: Relationships & Connections
- **Phase 8**: Events & Timeline System
- **Phase 9**: Additional Entity Types (Organizations, Artifacts, Lore)
- **Phase 10**: Rich Content (Text Editor, Media)
- **Phase 11**: Timeline Visualization & Graphs
- **Phase 12**: Data Management (Import/Export, Backup)
- **Phase 13**: Polish & UX
- **Phase 14**: Testing & Deployment

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

- Follow the existing code style and conventions
- Write clear, descriptive commit messages
- Add unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 📄 License

*License information to be added*

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/MrFrey75/WorldBuilder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MrFrey75/WorldBuilder/discussions)

---

## 🙏 Acknowledgments

Special thanks to:
- The .NET and WPF development community
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
