# 🗺️ WorldBuilder Development Roadmap

## Current Status: **Phase 9 - Additional Entity Types** ✓ Complete

This document outlines the complete development roadmap for WorldBuilder. The project is organized into 14 distinct phases, each containing multiple sub-phases with specific, actionable tasks.

> **Last Updated**: October 30, 2025
> **Phase Reordering**: Phase 6 (Search & Filter) moved to Phase 8 - will be implemented after Events & Timeline System
> 
> **Platform**: Python 3.11+ Desktop Application (PyQt6)

---

## Overview

WorldBuilder is being developed in a phased approach to ensure:
- ✅ Solid foundation before adding complexity
- ✅ Incremental delivery of functionality
- ✅ Maintainable and testable codebase
- ✅ Clear milestones and progress tracking

### Phase Ordering Note

**Phase 6 has been reordered** to come after Phase 7 (Events & Timeline). This change was made because:
- Search & Filter functionality benefits from having all major entity types implemented first
- Timeline/Event search filters require the timeline system to exist
- More comprehensive and useful search can be implemented once Relationships and Events are in place
- This creates a more logical development flow: Core Entities → Relationships → Events → Search

**New Phase Order:**
- Phase 6: Relationships & Connections (formerly Phase 7)
- Phase 7: Events & Timeline System (formerly Phase 8)
- Phase 8: Search & Filter (formerly Phase 6)

---

<details open>
<summary><b>Phase 1: Foundation & Setup</b> ✓ (Current)</summary>

### 1.1 Project Infrastructure ✓
- [x] Create project directory structure
- [x] Set up Python package structure (worldbuilder/)
- [x] Create requirements.txt with dependencies
- [x] Set up version control and .gitignore
- [x] Initialize PyQt6 UI framework
- [x] Create setup.py for package configuration

### 1.2 Core Architecture ✓
- [x] Design database schema (tables for entities, relationships)
- [x] Create base entity models (BaseEntity, Universe)
- [x] Implement repository pattern interfaces (IRepository, BaseRepository)
- [x] Set up SQLAlchemy ORM layer
- [x] Create DatabaseManager for session management
- [x] Create base Controller class (MVC pattern)

### 1.3 Basic UI Framework ✓
- [x] Create main application window (MainWindow)
- [x] Implement navigation/menu system (File, Edit, View, Help)
- [x] Set up signal/slot infrastructure (PyQt6 signals)
- [x] Create ThemeManager for styling
- [x] Implement theme support (light/dark modes)
- [x] Create status bar for user feedback

</details>

---

<details>
<summary><b>Phase 2: Universe Management</b> ✓</summary>

### 2.1 Universe CRUD ✓
- [x] Create Universe model and database table
- [x] Implement UniverseRepository with CRUD methods
- [x] Create UniverseService for business logic
- [x] Create Universe creation dialog/view
- [x] Implement Universe selection/switching
- [x] Add Universe edit functionality
- [x] Add Universe deletion with confirmation

### 2.2 Universe UI ✓
- [x] Design Universe management view (PyQt6 widget)
- [x] Create Universe list view/grid (table with actions)
- [x] Implement Universe details panel
- [x] Add recent universes list
- [x] Create Universe settings page

</details>

---

<details>
<summary><b>Phase 3: Location System</b> ✓</summary>

### 3.1 Location Data Layer ✓
- [x] Create Location model with parent reference
- [x] Design location hierarchy database schema (self-referencing)
- [x] Implement LocationRepository with hierarchy methods
- [x] Create LocationService for business logic
- [x] Add location parent-child relationship methods
- [x] Create location type enumeration (Continent, Region, City, Building, etc.)

### 3.2 Location CRUD Operations ✓
- [x] Implement Create Location functionality
- [x] Implement Read/View Location details
- [x] Implement Update Location functionality
- [x] Implement Delete Location (with cascade options)
- [x] Add location parent selection/assignment

### 3.3 Location UI ✓
- [x] Create Location list view
- [x] Design Location detail editor dialog
- [x] Implement hierarchical tree widget for locations
- [x] Add location type selector
- [x] Create location parent picker
- [x] Implement location breadcrumb navigation
- [x] Add expand/collapse tree functionality

</details>

---

<details>
<summary><b>Phase 4: Species & Races System</b> ✓</summary>

### 4.1 Species Data Layer ✓
- [x] Create Species/Race model
- [x] Implement species type classification (sentient, non-sentient, magical, etc.)
- [x] Add species attributes (physical traits, average lifespan, size, etc.) as JSON
- [x] Create species abilities and special characteristics
- [x] Implement SpeciesRepository with query methods
- [x] Create SpeciesService for business logic
- [x] Add default "Human" species to new universes

### 4.2 Species CRUD Operations ✓
- [x] Implement Create Species functionality
- [x] Implement Read/View Species details
- [x] Implement Update Species functionality
- [x] Implement Delete Species functionality (with safeguards)
- [x] Add species templates (common fantasy/sci-fi races)

### 4.3 Species UI ✓
- [x] Create Species list view (table/grid)
- [x] Design Species detail editor dialog
- [x] Add species trait/attribute editor
- [x] Implement species image/illustration support
- [x] Create species comparison view

</details>
- [ ] Implement SpeciesRepository with query methods
- [ ] Create SpeciesService for business logic
- [ ] Add default "Human" species to new universes

### 4.2 Species CRUD Operations
- [ ] Implement Create Species functionality
- [ ] Implement Read/View Species details
- [ ] Implement Update Species functionality
- [ ] Implement Delete Species functionality (with safeguards)
- [ ] Add species templates (common fantasy/sci-fi races)

### 4.3 Species UI
- [ ] Create Species list view (table/grid)
- [ ] Design Species detail editor dialog
- [ ] Add species trait/attribute editor
- [ ] Implement species image/illustration support
- [ ] Create species comparison view

</details>

---

<details>
<summary><b>Phase 5: Notable Figures System</b> ✓</summary>

### 5.1 Figure Data Layer ✓
- [x] Create Notable Figure model
- [x] Add species assignment field (defaults to Human)
- [x] Implement NotableFigureRepository with query methods
- [x] Create NotableFigureService for business logic
- [x] Add figure-location relationships
- [x] Create figure attribute fields (age, occupation, etc.)
- [x] Implement species-specific attributes for figures

### 5.2 Figure CRUD Operations ✓
- [x] Implement Create Figure functionality
- [x] Implement Read/View Figure details
- [x] Implement Update Figure functionality
- [x] Implement Delete Figure functionality
- [x] Add figure image/portrait support
- [x] Add species selection/assignment during figure creation

### 5.3 Figure UI ✓
- [x] Create Figure list view (table/grid/card view)
- [x] Design Figure detail editor dialog
- [x] Add species indicator/badge in figure lists
- [x] Implement Figure search/filter (including by species)
- [x] Add Figure card/tile view option
- [x] Create Figure relationship visualizer widget
- [x] Add species-specific field display based on assigned species

</details>

</details>

---

<details>
<summary><b>Phase 6: Relationships & Connections</b> ✓</summary>

### 6.1 Relationship Data ✓
- [x] Create Relationship model
- [x] Design relationship type system (enum)
- [x] Implement RelationshipRepository
- [x] Create RelationshipService for business logic
- [x] Add bidirectional relationship support
- [x] Create relationship strength/type properties

### 6.2 Relationship UI ✓
- [x] Create relationship editor dialog
- [x] Implement relationship list view widget
- [x] Add quick relationship creation UI
- [x] Design relationship graph visualization widget
- [x] Implement relationship filtering

</details>

---

<details>
<summary><b>Phase 7: Events & Timeline System</b> ✓</summary>

### 7.1 Event Data Model ✓
- [x] Create Event model with flexible date/time structure
- [x] Implement date precision levels (exact, year-only, approximate, relative)
- [x] Add event duration support (instant vs. span of time)
- [x] Create event type/category system (enum)
- [x] Implement event importance/significance levels
- [x] Add event-entity relationship support (figures, locations, organizations)

### 7.2 Event CRUD Operations ✓
- [x] Implement Create Event functionality
- [x] Implement Read/View Event details
- [x] Implement Update Event functionality
- [x] Implement Delete Event functionality
- [x] Add event duplication feature
- [x] Create event templates for common event types
- [x] Create EventService for business logic

### 7.3 Timeline Management ✓
- [x] Create Timeline model (multiple timelines per universe)
- [x] Implement custom timeline creation (e.g., "Main History", "Character A's Story", "War Timeline")
- [x] Add event-to-timeline assignment (events can exist on multiple timelines)
- [x] Implement timeline filtering and grouping
- [x] Create timeline era/period definitions
- [x] Add timeline merging and comparison features

### 7.4 Event UI ✓
- [x] Design Event list view with sorting/filtering
- [x] Create Event detail editor dialog
- [x] Implement quick event creation dialog
- [x] Add event date picker widget with precision options
- [x] Create event-entity linking interface
- [x] Implement event search with date range filters

</details>


---

<details>
<summary><b>Phase 9: Additional Entity Types</b> ✓</summary>

### 9.1 Organizations System ✓
- [x] Create Organization model
- [x] Implement OrganizationRepository
- [x] Create OrganizationService for business logic
- [x] Create Organization CRUD operations
- [x] Design Organization detail view dialog
- [x] Add member/figure relationships

### 9.2 Artifacts & Lore ✓
- [x] Create Artifact model
- [x] Create Lore/Mythology model with LoreType enum
- [x] Implement respective repositories
- [x] Create services for business logic
- [x] Create CRUD operations for each
- [x] Design detail view dialogs

</details>
---

<details>
<summary><b>Phase 8: Search & Filter</b> ✓</summary>

### 8.1 Basic Search ✓
- [x] Implement global text search across entities
- [x] Create search results view widget
- [x] Add search by entity type filter
- [x] Implement search highlighting in results
- [x] Create SearchService for query logic

### 8.2 Advanced Filtering ✓
- [x] Create filter panel UI widget
- [x] Implement filter by tags
- [x] Add filter by location
- [x] Add filter by species/race
- [x] Add filter by date/timeline
- [x] Implement saved filter presets (stored in database)

</details>

---

<details>
<summary><b>Phase 10: Rich Content</b></summary>

### 10.1 Rich Text Editor
- [ ] Integrate rich text editor widget (QTextEdit with formatting or third-party)
- [ ] Implement formatting toolbar (bold, italic, underline, etc.)
- [ ] Add markdown parsing/rendering
- [ ] Implement inline image support
- [ ] Add spell check functionality

### 10.2 Media Management
- [ ] Create media storage system (filesystem-based in universe directory)
- [ ] Implement image upload/attachment dialog
- [ ] Add image gallery view widget
- [ ] Create media library browser
- [ ] Implement media compression/optimization on upload

</details>

---

<details>
<summary><b>Phase 11: Timeline Visualization</b></summary>

### 11.1 Timeline View Component
- [ ] Create interactive timeline widget (canvas-based or using matplotlib)
- [ ] Implement event plotting with visual markers
- [ ] Add timeline zoom/pan controls (from millennia to days)
- [ ] Create swimlane view for multiple timelines
- [ ] Implement era/period background shading
- [ ] Add "now" marker for current story point

### 11.2 Timeline Interaction
- [ ] Implement click-to-view event details
- [ ] Add drag-and-drop event repositioning
- [ ] Create event clustering for dense time periods
- [ ] Implement timeline filtering by entity/type
- [ ] Add timeline bookmarks and navigation
- [ ] Create timeline snapshot/versioning

### 11.3 Timeline Display Modes
- [ ] Implement linear timeline view
- [ ] Create branching timeline view (alternate timelines/what-ifs)
- [ ] Add calendar view mode
- [ ] Create list view with chronological sorting
- [ ] Implement relative timeline (event-to-event relationships)
- [ ] Add timeline export (image, PDF, HTML)

### 11.4 Date & Time System
- [ ] Create custom calendar system support
- [ ] Implement date conversion between calendar systems
- [ ] Add support for fictional calendars (custom months, days, years)
- [ ] Create date calculator (time between events)
- [ ] Implement recurring events support
- [ ] Add age calculation for figures based on event dates

### 11.5 Relationship Graphs
- [ ] Implement graph visualization library (networkx + matplotlib/pyvis)
- [ ] Create entity relationship graph view widget
- [ ] Add graph layout algorithms
- [ ] Implement interactive node selection
- [ ] Add graph filtering and focusing

</details>

---

<details>
<summary><b>Phase 12: Data Management</b></summary>

### 12.1 Import/Export
- [ ] Design export format (JSON or custom binary format)
- [ ] Implement full universe export service
- [ ] Implement selective entity export
- [ ] Create import functionality with validation
- [ ] Add export templates support

### 12.2 Backup & Restore
- [ ] Implement automatic backup system (scheduled background task)
- [ ] Create manual backup functionality
- [ ] Design restore wizard dialog
- [ ] Add backup scheduling configuration
- [ ] Implement backup compression (ZIP)

</details>

---

<details>
<summary><b>Phase 13: Polish & UX</b></summary>

### 13.1 User Preferences
- [ ] Create settings/preferences dialog
- [ ] Implement theme selection (light/dark mode)
- [ ] Add UI customization options
- [ ] Create keyboard shortcut configuration UI
- [ ] Implement auto-save preferences to config file

### 13.2 Performance & Optimization
- [ ] Implement lazy loading for large datasets
- [ ] Add entity caching system (in-memory)
- [ ] Optimize database queries (indexing, eager loading)
- [ ] Implement virtual scrolling for large lists
- [ ] Add loading indicators and progress bars

### 13.3 Help & Documentation
- [ ] Create in-app help system (help browser widget)
- [ ] Write user guide documentation
- [ ] Add tooltips throughout UI
- [ ] Create getting started wizard
- [ ] Record tutorial videos (optional)

</details>

---

<details>
<summary><b>Phase 14: Testing & Deployment</b></summary>

### 14.1 Testing
- [ ] Write unit tests for core services and repositories (pytest)
- [ ] Create integration tests with SQLite test database
- [ ] Perform UI/UX testing (manual)
- [ ] Conduct performance testing (large datasets)
- [ ] Fix all identified bugs

### 14.2 Deployment
- [ ] Create executable package (PyInstaller/py2exe)
- [ ] Set up auto-update mechanism (optional)
- [ ] Prepare deployment documentation
- [ ] Create release notes
- [ ] Publish initial release (GitHub Releases)

</details>

---

## Progress Tracking

| Phase | Status | Completion |
|-------|--------|------------|
| Phase 1: Foundation & Setup | 🟢 Complete | 100% |
| Phase 2: Universe Management | 🟢 Complete | 100% |
| Phase 3: Location System | 🟢 Complete | 100% |
| Phase 4: Species & Races | 🟢 Complete | 100% |
| Phase 5: Notable Figures | 🟢 Complete | 100% |
| Phase 6: Relationships & Connections | 🟢 Complete | 100% |
| Phase 7: Events & Timeline | 🟢 Complete | 100% |
| Phase 8: Search & Filter | 🟢 Complete | 100% |
| Phase 9: Additional Entities | 🟢 Complete | 100% |
| Phase 10: Rich Content | ⚪ Not Started | 0% |
| Phase 11: Visualization | ⚪ Not Started | 0% |
| Phase 12: Data Management | ⚪ Not Started | 0% |
| Phase 13: Polish & UX | ⚪ Not Started | 0% |
| Phase 14: Testing & Deployment | ⚪ Not Started | 0% |

**Legend**: 🟢 Complete | 🟡 In Progress | ⚪ Not Started

---

## Notes

- Tasks are listed in recommended order but can be adjusted based on priorities
- Some tasks may be worked on in parallel
- Completed tasks will be checked off as development progresses
- This roadmap is subject to change based on feedback and requirements

---

[← Back to Main README](README.md)
