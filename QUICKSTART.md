# 🚀 WorldBuilder Quick Start Guide

Get up and running with WorldBuilder in just a few minutes!

## Installation

### Prerequisites

- Python 3.11 or later
- pip (Python package installer)
- Git (to clone the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/MrFrey75/WorldBuilder.git
cd WorldBuilder
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run WorldBuilder

```bash
# Set PYTHONPATH (Linux/macOS)
export PYTHONPATH=/path/to/WorldBuilder/src:$PYTHONPATH

# Run the application
python src/worldbuilder/main.py
```

Or use the simpler approach:

```bash
python -m worldbuilder.main
```

## First Time Use

### Create Your First Universe

1. **Launch WorldBuilder** - The application window will appear
2. **Create New Universe** - Click "File" → "New Universe" or press `Ctrl+N`
3. **Fill in Details**:
   - **Name**: Give your universe a memorable name
   - **Author**: Your name or pen name
   - **Genre**: Fantasy, Sci-Fi, Historical, etc.
   - **Description**: Brief overview of your world
4. **Click "Create"** - Your universe is ready!

### Add Your First Location

1. **Open Locations** - Click "Locations" in the main menu
2. **Create Location** - Click the "+" button or press `Ctrl+Shift+L`
3. **Enter Details**:
   - **Name**: e.g., "The Kingdom of Avalon"
   - **Type**: Select from Continent, Region, City, etc.
   - **Description**: Describe your location
4. **Save** - Your location is now part of your world!

### Add Your First Character

1. **Open Notable Figures** - Click "Notable Figures" in the main menu
2. **Create Figure** - Click the "+" button
3. **Enter Details**:
   - **Name**: Character's name
   - **Species**: Defaults to Human (you can create custom species!)
   - **Description**: Background, personality, etc.
4. **Save** - Your character exists!

### Create Relationships

1. **Select a Figure or Location**
2. **Click "Relationships" Tab**
3. **Add Relationship** - Connect entities together
4. **Choose Type**: Family, Ally, Enemy, etc.
5. **Visualize** - View the relationship graph

## Common Tasks

### Searching

- **Global Search**: `Ctrl+F` - Search across all entities
- **Filter by Type**: Use the filter panel to narrow results
- **Advanced Filters**: Filter by tags, species, location, date

### Creating Events

1. **Open Timeline** - Click "Timeline" in the main menu
2. **Add Event** - Click "New Event"
3. **Set Date**: Choose precision (exact, year-only, approximate)
4. **Link Entities**: Connect the event to figures, locations, etc.
5. **View Timeline**: See your world's history unfold

### Exporting Your Work

1. **File Menu** → "Export"
2. **Choose Format**: JSON export
3. **Select Entities**: Export everything or specific items
4. **Save** - Keep backups of your work!

### Backup & Restore

- **Automatic Backups**: Enable in Universe Settings
- **Manual Backup**: File → Create Backup
- **Restore**: File → Restore from Backup

## Tips & Tricks

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Universe |
| `Ctrl+O` | Open Universe |
| `Ctrl+S` | Save |
| `Ctrl+F` | Search |
| `Ctrl+Q` | Quit |
| `Ctrl+Shift+S` | Universe Settings |
| `F1` | Help |

### Organizing Your World

1. **Use Tags**: Organize entities with custom tags
2. **Hierarchical Locations**: Build from continents down to rooms
3. **Multiple Timelines**: Track different storylines separately
4. **Relationship Types**: Define how entities connect

### Best Practices

- **Save Often**: Use `Ctrl+S` frequently
- **Enable Auto-Backup**: Set it in Universe Settings
- **Be Descriptive**: Rich descriptions make worldbuilding easier
- **Link Everything**: Use relationships to build depth
- **Use the Timeline**: Track historical events chronologically

## Need Help?

- **In-App Help**: Press `F1` for context-sensitive help
- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md) for detailed documentation
- **Developer Guide**: See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for technical details
- **Report Issues**: [GitHub Issues](https://github.com/MrFrey75/WorldBuilder/issues)

## What's Next?

### Explore Features

- **Custom Species**: Create unique races for your world
- **Organizations**: Build factions, guilds, governments
- **Artifacts**: Track important items and relics
- **Lore**: Document myths, religions, and cultural elements
- **Visualizations**: Use timeline and relationship graphs

### Learn More

- Read the [User Guide](USER_GUIDE.md) for comprehensive documentation
- Check the [Roadmap](ROADMAP.md) to see what features exist
- Join discussions on [GitHub](https://github.com/MrFrey75/WorldBuilder/discussions)

---

**Happy Worldbuilding!** 🌍✨

[← Back to README](README.md)
