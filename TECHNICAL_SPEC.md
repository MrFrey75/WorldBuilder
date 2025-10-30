# WorldBuilder - Technical Specification for AI Code Generation

## Project Overview

**Project Name**: WorldBuilder  
**Type**: Desktop Application  
**Platform**: Windows 10+  
**Framework**: .NET 8, WPF (Windows Presentation Foundation)  
**Architecture**: MVVM (Model-View-ViewModel) with Clean Architecture  
**Database**: SQLite (embedded, file-based)  
**Language**: C# 12  
**Repository**: https://github.com/MrFrey75/WorldBuilder.git

---

## Purpose & Context

WorldBuilder is a desktop application for authors, storytellers, and worldbuilders to create and manage detailed fictional universes. The application manages entities (characters, locations, events, etc.) with complex relationships and provides visualization tools (timelines, graphs, hierarchies).

---

## Solution Structure

```
WorldBuilder/
├── WorldBuilder.sln                    # Visual Studio Solution
├── src/
│   ├── WorldBuilder.Core/              # Core Business Logic (Class Library)
│   │   ├── Models/                     # Domain Entities
│   │   ├── Services/                   # Business Logic Services
│   │   ├── Database/                   # Data Access Layer
│   │   │   ├── Repositories/           # Repository Pattern Implementation
│   │   │   ├── Entities/               # EF Core Entity Classes
│   │   │   └── WorldBuilderContext.cs # DbContext
│   │   ├── Common/                     # Shared Utilities
│   │   └── Interfaces/                 # Service Contracts
│   └── WorldBuilder.Creator/           # WPF Application
│       ├── Views/                      # XAML Views (Windows, UserControls)
│       ├── ViewModels/                 # MVVM ViewModels
│       ├── Commands/                   # ICommand Implementations
│       ├── Converters/                 # Value Converters for Data Binding
│       ├── Resources/                  # Styles, Templates, Assets
│       ├── Services/                   # UI-specific Services
│       └── App.xaml                    # Application Entry Point
└── tests/
    ├── WorldBuilder.Core.Tests/
    └── WorldBuilder.Creator.Tests/
```

---

## Technology Stack Details

### Framework & Libraries
- **.NET 8.0** - Target Framework
- **WPF** - UI Framework
- **Entity Framework Core 8.0** - ORM for SQLite
- **CommunityToolkit.Mvvm** - MVVM helpers (RelayCommand, ObservableObject)
- **SQLite** - Database engine

### Recommended NuGet Packages
```xml
<!-- WorldBuilder.Core -->
<PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.*" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="8.0.*" />
<PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.*" />

<!-- WorldBuilder.Creator -->
<PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.*" />
<PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.*" />
```

---

## Core Domain Model

### Entity Hierarchy

All entities inherit from a base entity:

```csharp
public abstract class BaseEntity
{
    public Guid Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? ModifiedAt { get; set; }
    public Guid UniverseId { get; set; }
    public virtual Universe Universe { get; set; }
}
```

### Primary Entities

#### 1. Universe
```csharp
public class Universe : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime? LastAccessedDate { get; set; }
    
    // Navigation Properties
    public virtual ICollection<NotableFigure> Figures { get; set; }
    public virtual ICollection<Location> Locations { get; set; }
    public virtual ICollection<Event> Events { get; set; }
    public virtual ICollection<Species> Species { get; set; }
    public virtual ICollection<Organization> Organizations { get; set; }
    public virtual ICollection<Artifact> Artifacts { get; set; }
    public virtual ICollection<Lore> Lore { get; set; }
    public virtual ICollection<Timeline> Timelines { get; set; }
}
```

#### 2. Location (Hierarchical)
```csharp
public class Location : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public LocationType Type { get; set; }
    
    // Hierarchical Structure
    public Guid? ParentLocationId { get; set; }
    public virtual Location ParentLocation { get; set; }
    public virtual ICollection<Location> ChildLocations { get; set; }
    
    // Additional Properties
    public string ImagePath { get; set; }
    public string Tags { get; set; } // JSON array or comma-separated
    
    // Navigation Properties
    public virtual ICollection<NotableFigure> Figures { get; set; }
    public virtual ICollection<Event> Events { get; set; }
}

public enum LocationType
{
    Continent,
    Region,
    Country,
    State,
    City,
    District,
    Town,
    Village,
    Building,
    Room,
    Landmark,
    Other
}
```

#### 3. Species
```csharp
public class Species : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public SpeciesType Type { get; set; }
    
    // Physical Traits
    public string PhysicalTraits { get; set; } // JSON
    public int? AverageLifespanYears { get; set; }
    public string AverageHeight { get; set; }
    public string AverageWeight { get; set; }
    
    // Characteristics
    public string Abilities { get; set; } // JSON array
    public string CulturalCharacteristics { get; set; }
    public string ImagePath { get; set; }
    
    // Navigation Properties
    public virtual ICollection<NotableFigure> Figures { get; set; }
}

public enum SpeciesType
{
    Sentient,
    NonSentient,
    Magical,
    Technological,
    Hybrid,
    Other
}
```

#### 4. NotableFigure (Character)
```csharp
public class NotableFigure : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    
    // Species Assignment
    public Guid SpeciesId { get; set; }
    public virtual Species Species { get; set; }
    
    // Location Assignment
    public Guid? CurrentLocationId { get; set; }
    public virtual Location CurrentLocation { get; set; }
    
    // Attributes
    public int? Age { get; set; }
    public string Occupation { get; set; }
    public string Traits { get; set; } // JSON
    public string ImagePath { get; set; }
    public DateTime? BirthDate { get; set; }
    public DateTime? DeathDate { get; set; }
    
    // Navigation Properties
    public virtual ICollection<Relationship> RelationshipsFrom { get; set; }
    public virtual ICollection<Relationship> RelationshipsTo { get; set; }
    public virtual ICollection<Event> Events { get; set; }
}
```

#### 5. Event (with Flexible Dating)
```csharp
public class Event : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public EventType Type { get; set; }
    public ImportanceLevel Importance { get; set; }
    
    // Flexible Date/Time
    public DateTime? ExactDate { get; set; }
    public int? Year { get; set; }
    public DatePrecision Precision { get; set; }
    public string ApproximateDescription { get; set; } // "Early spring", "Around 1500"
    
    // Duration
    public DateTime? EndDate { get; set; }
    public TimeSpan? Duration { get; set; }
    
    // Location
    public Guid? LocationId { get; set; }
    public virtual Location Location { get; set; }
    
    // Navigation Properties
    public virtual ICollection<Timeline> Timelines { get; set; }
    public virtual ICollection<NotableFigure> Participants { get; set; }
}

public enum DatePrecision
{
    Exact,      // Full date and time
    YearOnly,   // Just the year
    Approximate, // Rough estimate
    Relative    // "Before Event X", "After Event Y"
}

public enum EventType
{
    Birth,
    Death,
    Battle,
    Meeting,
    Discovery,
    Creation,
    Destruction,
    Political,
    Cultural,
    Natural,
    Other
}

public enum ImportanceLevel
{
    Minor,
    Moderate,
    Major,
    Critical
}
```

#### 6. Timeline
```csharp
public class Timeline : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public bool IsMainTimeline { get; set; }
    
    // Navigation Properties
    public virtual ICollection<Event> Events { get; set; }
}
```

#### 7. Relationship
```csharp
public class Relationship : BaseEntity
{
    // From/To Pattern
    public Guid FromFigureId { get; set; }
    public virtual NotableFigure FromFigure { get; set; }
    
    public Guid ToFigureId { get; set; }
    public virtual NotableFigure ToFigure { get; set; }
    
    // Relationship Details
    public RelationshipType Type { get; set; }
    public string Description { get; set; }
    public int Strength { get; set; } // 1-10 scale
    public bool IsBidirectional { get; set; }
}

public enum RelationshipType
{
    Family,
    Friend,
    Enemy,
    Ally,
    Romantic,
    Professional,
    Mentor,
    Rival,
    Other
}
```

#### 8. Organization
```csharp
public class Organization : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public OrganizationType Type { get; set; }
    public DateTime? FoundedDate { get; set; }
    public DateTime? DisbandedDate { get; set; }
    
    // Location
    public Guid? HeadquartersLocationId { get; set; }
    public virtual Location HeadquartersLocation { get; set; }
    
    // Navigation Properties
    public virtual ICollection<NotableFigure> Members { get; set; }
}

public enum OrganizationType
{
    Government,
    Military,
    Religious,
    Guild,
    Corporation,
    Faction,
    Secret,
    Educational,
    Other
}
```

#### 9. Artifact
```csharp
public class Artifact : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public string ImagePath { get; set; }
    
    // Current Status
    public Guid? CurrentLocationId { get; set; }
    public virtual Location CurrentLocation { get; set; }
    
    public Guid? CurrentOwnerId { get; set; }
    public virtual NotableFigure CurrentOwner { get; set; }
}
```

#### 10. Lore
```csharp
public class Lore : BaseEntity
{
    public string Title { get; set; }
    public string Content { get; set; }
    public LoreType Type { get; set; }
}

public enum LoreType
{
    Mythology,
    Religion,
    Legend,
    History,
    Custom,
    Prophecy,
    Other
}
```

---

## Database Context

```csharp
public class WorldBuilderContext : DbContext
{
    public DbSet<Universe> Universes { get; set; }
    public DbSet<Location> Locations { get; set; }
    public DbSet<Species> Species { get; set; }
    public DbSet<NotableFigure> Figures { get; set; }
    public DbSet<Event> Events { get; set; }
    public DbSet<Timeline> Timelines { get; set; }
    public DbSet<Relationship> Relationships { get; set; }
    public DbSet<Organization> Organizations { get; set; }
    public DbSet<Artifact> Artifacts { get; set; }
    public DbSet<Lore> Lore { get; set; }
    
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite("Data Source=worldbuilder.db");
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure self-referencing relationship for Location hierarchy
        modelBuilder.Entity<Location>()
            .HasOne(l => l.ParentLocation)
            .WithMany(l => l.ChildLocations)
            .HasForeignKey(l => l.ParentLocationId)
            .OnDelete(DeleteBehavior.Restrict);
        
        // Configure bidirectional relationships for NotableFigure
        modelBuilder.Entity<Relationship>()
            .HasOne(r => r.FromFigure)
            .WithMany(f => f.RelationshipsFrom)
            .HasForeignKey(r => r.FromFigureId)
            .OnDelete(DeleteBehavior.Restrict);
            
        modelBuilder.Entity<Relationship>()
            .HasOne(r => r.ToFigure)
            .WithMany(f => f.RelationshipsTo)
            .HasForeignKey(r => r.ToFigureId)
            .OnDelete(DeleteBehavior.Restrict);
        
        // Many-to-many: Timeline <-> Event
        modelBuilder.Entity<Timeline>()
            .HasMany(t => t.Events)
            .WithMany(e => e.Timelines)
            .UsingEntity(j => j.ToTable("TimelineEvents"));
        
        // Many-to-many: Event <-> NotableFigure
        modelBuilder.Entity<Event>()
            .HasMany(e => e.Participants)
            .WithMany(f => f.Events)
            .UsingEntity(j => j.ToTable("EventParticipants"));
        
        // Many-to-many: Organization <-> NotableFigure
        modelBuilder.Entity<Organization>()
            .HasMany(o => o.Members)
            .WithMany()
            .UsingEntity(j => j.ToTable("OrganizationMembers"));
        
        // Indexes for performance
        modelBuilder.Entity<Location>()
            .HasIndex(l => l.ParentLocationId);
        
        modelBuilder.Entity<NotableFigure>()
            .HasIndex(f => f.SpeciesId);
        
        modelBuilder.Entity<Event>()
            .HasIndex(e => e.ExactDate);
    }
}
```

---

## Repository Pattern

### Generic Repository Interface
```csharp
public interface IRepository<T> where T : BaseEntity
{
    Task<T> GetByIdAsync(Guid id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> GetByUniverseAsync(Guid universeId);
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(Guid id);
    Task<bool> ExistsAsync(Guid id);
}

public class Repository<T> : IRepository<T> where T : BaseEntity
{
    protected readonly WorldBuilderContext _context;
    protected readonly DbSet<T> _dbSet;
    
    public Repository(WorldBuilderContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }
    
    public async Task<T> GetByIdAsync(Guid id)
    {
        return await _dbSet.FindAsync(id);
    }
    
    public async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _dbSet.ToListAsync();
    }
    
    public async Task<IEnumerable<T>> GetByUniverseAsync(Guid universeId)
    {
        return await _dbSet.Where(e => e.UniverseId == universeId).ToListAsync();
    }
    
    public async Task<T> AddAsync(T entity)
    {
        entity.Id = Guid.NewGuid();
        entity.CreatedAt = DateTime.UtcNow;
        await _dbSet.AddAsync(entity);
        await _context.SaveChangesAsync();
        return entity;
    }
    
    public async Task UpdateAsync(T entity)
    {
        entity.ModifiedAt = DateTime.UtcNow;
        _dbSet.Update(entity);
        await _context.SaveChangesAsync();
    }
    
    public async Task DeleteAsync(Guid id)
    {
        var entity = await GetByIdAsync(id);
        if (entity != null)
        {
            _dbSet.Remove(entity);
            await _context.SaveChangesAsync();
        }
    }
    
    public async Task<bool> ExistsAsync(Guid id)
    {
        return await _dbSet.AnyAsync(e => e.Id == id);
    }
}
```

### Specialized Repositories
```csharp
public interface ILocationRepository : IRepository<Location>
{
    Task<IEnumerable<Location>> GetChildLocationsAsync(Guid parentId);
    Task<Location> GetWithChildrenAsync(Guid id);
    Task<IEnumerable<Location>> GetRootLocationsAsync(Guid universeId);
}

public interface INotableFigureRepository : IRepository<NotableFigure>
{
    Task<IEnumerable<NotableFigure>> GetBySpeciesAsync(Guid speciesId);
    Task<IEnumerable<NotableFigure>> GetByLocationAsync(Guid locationId);
    Task<NotableFigure> GetWithRelationshipsAsync(Guid id);
}
```

---

## MVVM Implementation

### Base ViewModel
```csharp
public abstract class ViewModelBase : ObservableObject
{
    private bool _isBusy;
    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }
    
    private string _errorMessage;
    public string ErrorMessage
    {
        get => _errorMessage;
        set => SetProperty(ref _errorMessage, value);
    }
}
```

### Example ViewModel
```csharp
public class UniverseListViewModel : ViewModelBase
{
    private readonly IRepository<Universe> _universeRepository;
    private ObservableCollection<Universe> _universes;
    
    public ObservableCollection<Universe> Universes
    {
        get => _universes;
        set => SetProperty(ref _universes, value);
    }
    
    public IAsyncRelayCommand LoadUniversesCommand { get; }
    public IAsyncRelayCommand<Universe> SelectUniverseCommand { get; }
    public IAsyncRelayCommand CreateUniverseCommand { get; }
    public IAsyncRelayCommand<Universe> DeleteUniverseCommand { get; }
    
    public UniverseListViewModel(IRepository<Universe> universeRepository)
    {
        _universeRepository = universeRepository;
        
        LoadUniversesCommand = new AsyncRelayCommand(LoadUniversesAsync);
        SelectUniverseCommand = new AsyncRelayCommand<Universe>(SelectUniverseAsync);
        CreateUniverseCommand = new AsyncRelayCommand(CreateUniverseAsync);
        DeleteUniverseCommand = new AsyncRelayCommand<Universe>(DeleteUniverseAsync);
    }
    
    private async Task LoadUniversesAsync()
    {
        IsBusy = true;
        try
        {
            var universes = await _universeRepository.GetAllAsync();
            Universes = new ObservableCollection<Universe>(universes);
        }
        catch (Exception ex)
        {
            ErrorMessage = $"Failed to load universes: {ex.Message}";
        }
        finally
        {
            IsBusy = false;
        }
    }
    
    private async Task SelectUniverseAsync(Universe universe)
    {
        // Navigate to universe detail or main view
    }
    
    private async Task CreateUniverseAsync()
    {
        // Open create universe dialog
    }
    
    private async Task DeleteUniverseAsync(Universe universe)
    {
        // Confirm and delete
    }
}
```

---

## Dependency Injection Setup

```csharp
// App.xaml.cs
public partial class App : Application
{
    private ServiceProvider _serviceProvider;
    
    public App()
    {
        var services = new ServiceCollection();
        ConfigureServices(services);
        _serviceProvider = services.BuildServiceProvider();
    }
    
    private void ConfigureServices(IServiceCollection services)
    {
        // Database
        services.AddDbContext<WorldBuilderContext>();
        
        // Repositories
        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
        services.AddScoped<ILocationRepository, LocationRepository>();
        services.AddScoped<INotableFigureRepository, NotableFigureRepository>();
        
        // ViewModels
        services.AddTransient<MainWindowViewModel>();
        services.AddTransient<UniverseListViewModel>();
        services.AddTransient<LocationTreeViewModel>();
        services.AddTransient<FigureListViewModel>();
        
        // Views
        services.AddTransient<MainWindow>();
    }
    
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        
        var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();
    }
}
```

---

## WPF View Examples

### MainWindow.xaml Structure
```xml
<Window x:Class="WorldBuilder.Creator.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="WorldBuilder" Height="800" Width="1400">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/> <!-- Menu -->
            <RowDefinition Height="Auto"/> <!-- Toolbar -->
            <RowDefinition Height="*"/>    <!-- Content -->
            <RowDefinition Height="Auto"/> <!-- Status Bar -->
        </Grid.RowDefinitions>
        
        <!-- Menu Bar -->
        <Menu Grid.Row="0">
            <MenuItem Header="_File">
                <MenuItem Header="_New Universe" Command="{Binding CreateUniverseCommand}"/>
                <MenuItem Header="_Open Universe" Command="{Binding OpenUniverseCommand}"/>
                <Separator/>
                <MenuItem Header="_Exit" Command="{Binding ExitCommand}"/>
            </MenuItem>
            <MenuItem Header="_Edit"/>
            <MenuItem Header="_View"/>
            <MenuItem Header="_Help"/>
        </Menu>
        
        <!-- Toolbar -->
        <ToolBar Grid.Row="1">
            <!-- Quick action buttons -->
        </ToolBar>
        
        <!-- Main Content Area -->
        <Grid Grid.Row="2">
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="250"/>  <!-- Navigation Panel -->
                <ColumnDefinition Width="5"/>    <!-- Splitter -->
                <ColumnDefinition Width="*"/>    <!-- Main Content -->
                <ColumnDefinition Width="5"/>    <!-- Splitter -->
                <ColumnDefinition Width="300"/>  <!-- Properties Panel -->
            </Grid.ColumnDefinitions>
            
            <!-- Navigation Tree -->
            <TreeView Grid.Column="0" ItemsSource="{Binding NavigationItems}"/>
            
            <GridSplitter Grid.Column="1" HorizontalAlignment="Stretch"/>
            
            <!-- Main Content (ContentControl for view switching) -->
            <ContentControl Grid.Column="2" Content="{Binding CurrentView}"/>
            
            <GridSplitter Grid.Column="3" HorizontalAlignment="Stretch"/>
            
            <!-- Properties/Details Panel -->
            <ContentControl Grid.Column="4" Content="{Binding SelectedItemDetails}"/>
        </Grid>
        
        <!-- Status Bar -->
        <StatusBar Grid.Row="3">
            <StatusBarItem Content="{Binding StatusMessage}"/>
        </StatusBar>
    </Grid>
</Window>
```

---

## Development Phases - Implementation Order

### Phase 1: Foundation & Setup (CURRENT)
**Priority**: CRITICAL  
**Dependencies**: None

**Tasks**:
1. Create solution structure with two projects
2. Add NuGet packages (EF Core, SQLite, CommunityToolkit.Mvvm)
3. Implement BaseEntity class
4. Implement WorldBuilderContext with basic configuration
5. Create generic Repository<T> and IRepository<T>
6. Set up dependency injection in App.xaml.cs
7. Create MainWindow with basic layout (menu, toolbar, status bar)
8. Create ViewModelBase class
9. Implement basic navigation framework

**Deliverables**:
- Compiled application that launches
- Database connection established
- DI container configured

---

### Phase 2: Universe Management
**Priority**: CRITICAL  
**Dependencies**: Phase 1

**Tasks**:
1. Create Universe entity model
2. Add Universe DbSet to context
3. Create UniverseRepository
4. Implement UniverseListViewModel with CRUD operations
5. Create UniverseListView.xaml with DataGrid
6. Implement Universe creation dialog
7. Implement Universe selection mechanism
8. Store selected universe in application state

**Deliverables**:
- Create, list, select, and delete universes
- Active universe context maintained

---

### Phase 3: Location System (Hierarchical)
**Priority**: HIGH  
**Dependencies**: Phase 2

**Tasks**:
1. Create Location entity with self-referencing navigation
2. Create LocationType enum
3. Configure EF Core for hierarchical relationship
4. Implement ILocationRepository with hierarchy methods
5. Create LocationTreeViewModel with recursive loading
6. Create LocationTreeView with TreeView control
7. Implement location detail view/edit form
8. Add location CRUD operations
9. Implement parent selection dropdown (excluding descendants)
10. Add breadcrumb navigation for current location

**Deliverables**:
- Hierarchical location tree with unlimited nesting
- Location creation with parent assignment
- Location detail editing

---

### Phase 4: Species & Races System
**Priority**: HIGH  
**Dependencies**: Phase 2

**Tasks**:
1. Create Species entity
2. Create SpeciesType enum
3. Add Species DbSet and repository
4. Create default "Human" species on universe creation
5. Implement SpeciesListViewModel
6. Create SpeciesListView with DataGrid
7. Create SpeciesDetailView for editing
8. Add JSON serialization for traits/abilities
9. Implement species templates (presets)

**Deliverables**:
- Species CRUD operations
- Default Human species auto-created
- Species template system

---

### Phase 5: Notable Figures System
**Priority**: HIGH  
**Dependencies**: Phase 3, Phase 4

**Tasks**:
1. Create NotableFigure entity
2. Add foreign keys to Species and Location
3. Implement INotableFigureRepository
4. Create FigureListViewModel with filtering
5. Create FigureListView (DataGrid + Card view toggle)
6. Create FigureDetailView with species/location selectors
7. Implement species dropdown (default to Human)
8. Add location assignment dropdown
9. Implement figure search and filtering
10. Add species indicator badge in list view

**Deliverables**:
- Figure CRUD with species assignment
- Location assignment
- Search and filter by species/location

---

### Phase 6: Search & Filter System
**Priority**: MEDIUM  
**Dependencies**: Phase 3, 4, 5

**Tasks**:
1. Create SearchService with full-text search
2. Implement global search view model
3. Create SearchView with results list
4. Add filter panel (by entity type, species, location, tags)
5. Implement saved filter presets
6. Add search highlighting in results

**Deliverables**:
- Global search across all entities
- Advanced filtering UI
- Saved filter presets

---

### Phase 7: Relationships & Connections
**Priority**: MEDIUM  
**Dependencies**: Phase 5

**Tasks**:
1. Create Relationship entity
2. Create RelationshipType enum
3. Configure bidirectional navigation in EF Core
4. Implement RelationshipRepository
5. Create RelationshipEditorViewModel
6. Create RelationshipEditorView (dialog)
7. Add relationship list to figure detail view
8. Implement quick relationship creation
9. Add relationship strength slider (1-10)

**Deliverables**:
- Create/edit/delete relationships
- Bidirectional relationship support
- Relationship visualization in figure details

---

### Phase 8: Events & Timeline System
**Priority**: HIGH  
**Dependencies**: Phase 3, 5

**Tasks**:
1. Create Event entity with flexible dating
2. Create DatePrecision, EventType, ImportanceLevel enums
3. Create Timeline entity
4. Configure many-to-many relationships
5. Implement EventRepository with date queries
6. Create EventListViewModel with sorting
7. Create EventDetailView with date precision picker
8. Implement timeline creation and management
9. Add event-to-timeline assignment
10. Create custom date picker control supporting precision levels

**Deliverables**:
- Event CRUD with flexible dates
- Multiple timelines per universe
- Event assignment to timelines

---

### Phase 9: Additional Entity Types
**Priority**: MEDIUM  
**Dependencies**: Phase 3, 5

**Tasks**:
1. Create Organization entity and OrganizationType enum
2. Create Artifact entity
3. Create Lore entity and LoreType enum
4. Configure many-to-many for organization members
5. Implement repositories for each
6. Create list and detail views for each entity type
7. Add navigation items to main menu

**Deliverables**:
- Organization, Artifact, Lore CRUD operations
- Integration with figures and locations

---

### Phase 10: Rich Content (Text Editor & Media)
**Priority**: MEDIUM  
**Dependencies**: Phase 2

**Tasks**:
1. Integrate RichTextBox or third-party editor (e.g., AvalonEdit)
2. Implement markdown parsing
3. Create image upload/storage service
4. Implement image picker dialog
5. Add image display in entity detail views
6. Create media library view
7. Implement image compression on upload

**Deliverables**:
- Rich text editing in description fields
- Image attachment to entities
- Media library

---

### Phase 11: Timeline Visualization
**Priority**: MEDIUM  
**Dependencies**: Phase 8

**Tasks**:
1. Design timeline visualization control (custom control or Canvas)
2. Implement timeline rendering with events as markers
3. Add zoom/pan functionality
4. Create swimlane view for multiple timelines
5. Implement era/period background shading
6. Add interactive event selection (click to view details)
7. Create timeline export (PNG, PDF, HTML)
8. Implement branching timeline view
9. Add calendar view mode
10. Create custom calendar system support

**Deliverables**:
- Interactive timeline visualization
- Multiple view modes
- Custom calendar support

---

### Phase 12: Data Management
**Priority**: HIGH  
**Dependencies**: All entity phases

**Tasks**:
1. Implement JSON export service for universe
2. Create export dialog with entity selection
3. Implement import service with validation
4. Create automatic backup service (scheduled)
5. Implement manual backup command
6. Create restore wizard with preview
7. Add backup compression (ZIP)

**Deliverables**:
- Export/import functionality
- Automatic and manual backups
- Restore capability

---

### Phase 13: Polish & UX
**Priority**: MEDIUM  
**Dependencies**: All phases

**Tasks**:
1. Create settings/preferences dialog
2. Implement theme switching (Light/Dark)
3. Add customizable keyboard shortcuts
4. Implement auto-save functionality
5. Add loading indicators and progress bars
6. Optimize database queries with eager/lazy loading
7. Implement entity caching
8. Add tooltips throughout UI
9. Create getting started wizard
10. Write user documentation

**Deliverables**:
- Polished UI/UX
- Performance optimizations
- User documentation

---

### Phase 14: Testing & Deployment
**Priority**: HIGH  
**Dependencies**: All phases

**Tasks**:
1. Write unit tests for repositories
2. Write unit tests for view models
3. Create integration tests
4. Perform UI testing
5. Conduct performance testing
6. Fix all identified bugs
7. Create installer (using WiX or ClickOnce)
8. Set up auto-update mechanism
9. Write deployment documentation
10. Publish release

**Deliverables**:
- Test coverage >70%
- Installer package
- Published release

---

## Coding Standards

### Naming Conventions
- **Classes**: PascalCase (e.g., `NotableFigure`, `LocationRepository`)
- **Interfaces**: I + PascalCase (e.g., `IRepository`, `ILocationRepository`)
- **Methods**: PascalCase (e.g., `GetByIdAsync`, `AddAsync`)
- **Private fields**: _camelCase (e.g., `_context`, `_universeRepository`)
- **Properties**: PascalCase (e.g., `Name`, `Description`)
- **Local variables**: camelCase (e.g., `universe`, `locationId`)
- **Constants**: PascalCase (e.g., `DefaultSpeciesName`)

### Async/Await
- All repository methods should be async
- Use `async Task` for void methods
- Use `async Task<T>` for methods returning values
- Suffix async methods with `Async`

### Error Handling
```csharp
try
{
    // Operation
}
catch (Exception ex)
{
    // Log error
    ErrorMessage = $"Operation failed: {ex.Message}";
    // Optionally rethrow or handle
}
```

### Comments
- Use XML documentation comments for public APIs
```csharp
/// <summary>
/// Gets a location by its unique identifier including all child locations.
/// </summary>
/// <param name="id">The location identifier.</param>
/// <returns>The location with child locations, or null if not found.</returns>
public async Task<Location> GetWithChildrenAsync(Guid id)
```

---

## Key Implementation Notes

1. **All entities inherit from BaseEntity** - Ensures consistent Id, timestamps, and universe reference
2. **Use Guid for all IDs** - Better for distributed systems and security
3. **Async/await everywhere** - All data access is asynchronous
4. **Repository pattern** - Abstracts data access from business logic
5. **MVVM pattern** - Strict separation of concerns
6. **Dependency injection** - All dependencies injected via constructor
7. **ObservableCollection** - Use for lists bound to UI
8. **INotifyPropertyChanged** - Implemented via ObservableObject base class
9. **RelayCommand/AsyncRelayCommand** - For command binding in XAML
10. **EF Core conventions** - Leverage conventions, override only when needed

---

## Performance Considerations

1. Use `.AsNoTracking()` for read-only queries
2. Implement pagination for large lists
3. Use eager loading (`.Include()`) judiciously
4. Cache frequently accessed data (e.g., species list, location trees)
5. Implement virtual scrolling for large lists
6. Use background threads for heavy operations
7. Debounce search input

---

## Testing Strategy

### Unit Tests
- Test all repository methods
- Test all view model command logic
- Mock dependencies using Moq

### Integration Tests
- Test database operations with in-memory SQLite
- Test full CRUD workflows

### UI Tests
- Test critical user workflows
- Test data binding

---

This specification provides all necessary context for AI code generation. Each phase can be implemented independently with clear deliverables and dependencies.
