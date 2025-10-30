# 📚 WorldBuilder User Guide

Complete guide to using WorldBuilder for creating and managing your fictional universes.

## Table of Contents

- [Getting Started](#getting-started)
- [Universe Management](#universe-management)
- [Locations](#locations)
- [Species & Races](#species--races)
- [Notable Figures](#notable-figures)
- [Relationships](#relationships)
- [Events & Timeline](#events--timeline)
- [Organizations](#organizations)
- [Artifacts & Lore](#artifacts--lore)
- [Search & Filter](#search--filter)
- [Visualization](#visualization)
- [Data Management](#data-management)
- [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### Installation

See [QUICKSTART.md](QUICKSTART.md) for installation instructions.

### Understanding Universes

A **Universe** is the top-level container for your fictional world. Each universe contains:
- Locations (places in your world)
- Species/Races (types of beings)
- Notable Figures (characters)
- Organizations (groups, factions)
- Artifacts (important objects)
- Lore (mythology, religions)
- Events (historical occurrences)
- Relationships (connections between entities)

---

## Universe Management

### Creating a Universe

1. Click **File → New Universe** or press `Ctrl+N`
2. Fill in the details:
   - **Name**: Your universe's name (required)
   - **Author**: Your name or pen name
   - **Genre**: Fantasy, Sci-Fi, Historical Fiction, etc.
   - **Status**: Active, Archived, Planning
   - **Description**: Overview of your world
3. Click **Create**

### Opening a Universe

- **From Main Menu**: File → Open Universe (`Ctrl+O`)
- **Recent Universes**: Click on a recently opened universe from the list
- **Quick Open**: Double-click a universe in the recent list

### Universe Settings

Access: **File → Universe Settings** or `Ctrl+Shift+S`

**Calendar System**:
- Gregorian (real-world calendar)
- Custom (define your own calendar)
- None (no calendar system)

**Timeline Settings**:
- Timeline units (years, eras, custom)
- Enable negative dates (BCE-style dating)

**Display Settings**:
- Show entity counts
- Default sort order

**Backup Settings**:
- Enable automatic backups
- Set backup frequency (days)

---

## Locations

Locations are places in your world, organized hierarchically from continents down to individual rooms.

### Location Types

- **Continent**: Largest landmass
- **Region**: Areas within continents
- **Country**: Nations and territories
- **City**: Urban settlements
- **Town**: Smaller settlements
- **Village**: Small communities
- **Building**: Structures
- **Room**: Interior spaces
- **Other**: Custom location types

### Creating Locations

1. Click **Locations** in the main menu
2. Click **+ Add Location** button
3. Fill in details:
   - **Name**: Location name
   - **Type**: Select from dropdown
   - **Parent Location**: Optional - place within hierarchy
   - **Description**: Details about the location
4. Click **Save**

### Hierarchical Structure

Build your world from large to small:
```
Continent: Etheria
  └─ Region: Northern Wastes
      └─ City: Frostholm
          └─ Building: The Ice Palace
              └─ Room: Throne Room
```

### Navigation

- **Tree View**: Browse locations hierarchically
- **Breadcrumbs**: See location's full path
- **Expand/Collapse**: Click arrows to navigate tree

---

## Species & Races

Define the different types of beings that inhabit your world.

### Creating Species

1. Click **Species** in the main menu
2. Click **+ Add Species**
3. Fill in details:
   - **Name**: Species name (e.g., "Elves")
   - **Type**: Sentient, Non-Sentient, Magical, etc.
   - **Description**: General overview
   - **Physical Traits**: Appearance, size, features
   - **Average Lifespan**: Life expectancy
   - **Abilities**: Special capabilities
   - **Culture**: Social characteristics
4. Click **Save**

### Default Species

Every universe includes a default "Human" species. You can edit or delete this if desired.

### Using Templates

WorldBuilder includes templates for common fantasy and sci-fi species:
- Elves
- Dwarves
- Orcs
- Dragonborn
- And more...

Click **Use Template** when creating a species to start with pre-filled data.

---

## Notable Figures

Create characters and important individuals in your world.

### Creating Figures

1. Click **Notable Figures** in the main menu
2. Click **+ Add Figure**
3. Fill in details:
   - **Name**: Character's name
   - **Species**: Select from your species list
   - **Current Location**: Optional
   - **Born**: Birth date/event
   - **Occupation**: Job or role
   - **Description**: Background, personality, appearance
4. Click **Save**

### Figure Attributes

Track various attributes:
- Name and aliases
- Species assignment
- Age and lifespan
- Physical description
- Personality traits
- Skills and abilities
- Current status (alive, dead, unknown)

### Portraits

Add images to your figures:
1. Open figure details
2. Click **Add Portrait**
3. Select image file
4. Image is stored with your universe

---

## Relationships

Connect entities to build depth and context.

### Relationship Types

**Family**:
- Parent/Child
- Sibling
- Spouse
- Extended Family

**Social**:
- Friend
- Ally
- Enemy
- Rival
- Mentor/Student

**Political**:
- Rules/Ruled By
- Ally/Enemy (political)
- Member Of

**Other**:
- Creator/Creation
- Custom relationships

### Creating Relationships

1. Select an entity (figure, location, etc.)
2. Click **Relationships** tab
3. Click **+ Add Relationship**
4. Select:
   - **Related Entity**: Who/what is connected
   - **Relationship Type**: How they're connected
   - **Strength**: Weak, Moderate, Strong
   - **Description**: Details about the relationship
5. Click **Save**

### Relationship Visualization

View connections graphically:
1. Click **Visualize** on any entity
2. See connected entities as a graph
3. Click nodes to navigate
4. Filter by relationship type

---

## Events & Timeline

Track historical events and build your world's history.

### Creating Events

1. Click **Timeline** in the main menu
2. Click **+ Add Event**
3. Fill in details:
   - **Name**: Event title
   - **Date**: When it occurred (see Date Precision below)
   - **Type**: Battle, Birth, Death, Discovery, etc.
   - **Location**: Where it happened
   - **Participants**: Figures involved
   - **Description**: What happened
4. Click **Save**

### Date Precision

**Exact Date**: Specific day, month, year
**Year Only**: Only the year is known
**Approximate**: "Around 1500", "Early 3rd Age"
**Relative**: "100 years after the Great War"

### Multiple Timelines

Create separate timelines for different storylines:
- Main Historical Timeline
- Character-specific timelines
- Alternative timelines
- Story arcs

### Timeline Views

**Linear View**: Events in chronological order
**Calendar View**: Events on a calendar grid
**List View**: Sortable event list
**Era View**: Group events by historical periods

---

## Organizations

Create factions, guilds, governments, and other groups.

### Organization Types

- Government
- Military
- Religious
- Guild/Trade
- Criminal
- Academic
- Social
- Other

### Creating Organizations

1. Click **Organizations** in the main menu
2. Click **+ Add Organization**
3. Fill in details:
   - **Name**: Organization name
   - **Type**: Select from list
   - **Founded**: Date of founding
   - **Location**: Headquarters or territory
   - **Leader**: Current leader
   - **Members**: Notable members
   - **Purpose**: Goals and activities
4. Click **Save**

---

## Artifacts & Lore

### Artifacts

Track important items, weapons, relics, and objects.

**Creating Artifacts**:
1. Click **Artifacts** in the main menu
2. Click **+ Add Artifact**
3. Fill in details:
   - **Name**: Item name
   - **Type**: Weapon, Relic, Document, etc.
   - **Current Owner**: Who possesses it
   - **Location**: Where it is
   - **Powers**: Special abilities
   - **History**: Item's backstory
4. Click **Save**

### Lore

Document myths, religions, legends, and cultural elements.

**Lore Types**:
- Mythology
- Religion
- Legend
- Folklore
- Cultural Tradition
- Historical Account

**Creating Lore**:
1. Click **Lore** in the main menu
2. Click **+ Add Lore**
3. Fill in details:
   - **Title**: Name of the myth/religion/etc.
   - **Type**: Select from list
   - **Culture**: Which people believe this
   - **Content**: The actual myth/story/belief
4. Click **Save**

---

## Search & Filter

### Global Search

**Basic Search**:
1. Press `Ctrl+F` or click **Search** button
2. Enter search term
3. Results show across all entity types

**Search by Entity Type**:
- Filter results to specific types
- Check/uncheck entity types in filter panel

### Advanced Filtering

**Filter Panel**:
- By Tags
- By Location
- By Species
- By Date Range
- By Timeline
- By Status

**Saved Filters**:
1. Configure filters
2. Click **Save Filter**
3. Name your filter preset
4. Reuse anytime from Filter menu

---

## Visualization

### Timeline Visualization

**Features**:
- Zoom from millennia to days
- Multiple timeline tracks
- Era background shading
- Event clustering
- Interactive event details

**Navigation**:
- Scroll to pan
- Zoom controls
- Jump to date
- Bookmarks

### Relationship Graphs

**View Modes**:
- Force-directed layout
- Hierarchical layout
- Circular layout

**Interactions**:
- Click nodes to select
- Drag to reposition
- Filter by relationship type
- Focus on specific entity

---

## Data Management

### Export

**Full Export**:
1. File → Export Universe
2. Choose location
3. Select JSON format
4. Click **Export**

**Selective Export**:
1. Select entities to export
2. File → Export Selected
3. Choose format and location

### Import

1. File → Import
2. Select JSON file
3. Review import preview
4. Click **Import**
5. Resolve any conflicts

### Backup

**Automatic Backups**:
- Enable in Universe Settings
- Set frequency (daily, weekly, etc.)
- Backups stored in universe folder

**Manual Backup**:
1. File → Create Backup
2. Backup saved with timestamp
3. Stored in `backups/` folder

**Restore**:
1. File → Restore from Backup
2. Select backup file
3. Confirm restoration
4. Universe restored to backup state

---

## Tips & Best Practices

### Organization

1. **Use Hierarchies**: Organize locations from large to small
2. **Tag Everything**: Tags make searching easier
3. **Link Entities**: Use relationships to build connections
4. **Multiple Timelines**: Separate main history from character arcs

### Workflow

1. **Start Big**: Create continents and major locations first
2. **Add Key Figures**: Main characters before minor ones
3. **Build History**: Major events before minor details
4. **Connect Relationships**: Link as you go

### Data Management

1. **Save Frequently**: Use `Ctrl+S` often
2. **Regular Backups**: Enable automatic backups
3. **Export Periodically**: Keep external copies
4. **Use Descriptions**: Rich details help you remember

### Performance

1. **Use Search**: Don't scroll through thousands of entities
2. **Filter Views**: Narrow results for faster loading
3. **Archive Old Data**: Set status to "Archived" for unused content
4. **Clean Up**: Delete unused entities periodically

---

## Keyboard Shortcuts

### File Operations
- `Ctrl+N` - New Universe
- `Ctrl+O` - Open Universe
- `Ctrl+S` - Save
- `Ctrl+Q` - Quit

### Navigation
- `Ctrl+F` - Search
- `Ctrl+1` through `Ctrl+9` - Switch tabs
- `F1` - Help

### Editing
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste

### Universe
- `Ctrl+Shift+S` - Universe Settings
- `Ctrl+Shift+E` - Export
- `Ctrl+Shift+I` - Import

---

## Troubleshooting

### Application Won't Start

- Ensure Python 3.11+ is installed
- Check PYTHONPATH is set correctly
- Verify all dependencies are installed

### Data Not Saving

- Check file permissions
- Ensure universe directory is writable
- Try manual save (`Ctrl+S`)

### Performance Issues

- Reduce visible entities (use filters)
- Enable lazy loading in settings
- Archive old/unused data

### Display Issues

- Try different themes (Settings)
- Check Qt6 libraries are installed
- Update graphics drivers

---

## Getting Help

- **In-App Help**: Press `F1`
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Developer Guide**: See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Report Issues**: [GitHub Issues](https://github.com/MrFrey75/WorldBuilder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MrFrey75/WorldBuilder/discussions)

---

**Happy Worldbuilding!** 🌍✨

[← Back to README](README.md)
