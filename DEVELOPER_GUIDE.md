# 💻 WorldBuilder Developer Guide

Technical documentation for developers contributing to or extending WorldBuilder.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Core Components](#core-components)
- [Database Layer](#database-layer)
- [Service Layer](#service-layer)
- [UI Layer](#ui-layer)
- [Testing](#testing)
- [Adding New Features](#adding-new-features)
- [Code Style](#code-style)
- [Contributing](#contributing)

---

## Architecture Overview

WorldBuilder follows the **Model-View-Controller (MVC)** architecture pattern with a layered approach:

```
┌─────────────────────────────────────────┐
│          Views (PyQt6 Widgets)          │  User Interface
├─────────────────────────────────────────┤
│         Controllers (Business Logic)     │  Application Logic
├─────────────────────────────────────────┤
│         Services (Domain Logic)          │  Business Rules
├─────────────────────────────────────────┤
│    Repositories (Data Access Layer)      │  Data Operations
├─────────────────────────────────────────┤
│         Models (Domain Entities)         │  Data Models
├─────────────────────────────────────────┤
│      Database (SQLite + SQLAlchemy)      │  Data Storage
└─────────────────────────────────────────┘
```

### Key Principles

- **Separation of Concerns**: Each layer has a specific responsibility
- **Loose Coupling**: Components interact through interfaces
- **High Cohesion**: Related functionality grouped together
- **Dependency Injection**: Services and repositories are injected
- **Repository Pattern**: Abstracts data access logic

---

## Project Structure

```
WorldBuilder/
├── src/
│   ├── worldbuilder/           # Main application package
│   │   ├── __init__.py
│   │   ├── main.py            # Application entry point
│   │   ├── models/            # Domain models (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Base entity model
│   │   │   ├── universe.py
│   │   │   ├── location.py
│   │   │   ├── species.py
│   │   │   ├── notable_figure.py
│   │   │   ├── relationship.py
│   │   │   ├── event.py
│   │   │   ├── timeline.py
│   │   │   ├── organization.py
│   │   │   ├── artifact.py
│   │   │   └── lore.py
│   │   ├── database/          # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── manager.py     # DatabaseManager
│   │   │   ├── repositories/  # Repository implementations
│   │   │   │   ├── base_repository.py
│   │   │   │   ├── universe_repository.py
│   │   │   │   └── ...
│   │   ├── services/          # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── universe_service.py
│   │   │   ├── location_service.py
│   │   │   ├── species_service.py
│   │   │   └── ...
│   │   ├── controllers/       # Application controllers
│   │   │   ├── __init__.py
│   │   │   ├── base_controller.py
│   │   │   └── ...
│   │   ├── views/             # PyQt6 views/windows
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py
│   │   │   ├── universe_dialog.py
│   │   │   └── ...
│   │   ├── widgets/           # Custom PyQt6 widgets
│   │   │   ├── __init__.py
│   │   │   ├── timeline_widget.py
│   │   │   ├── relationship_graph_widget.py
│   │   │   └── ...
│   │   ├── enums/             # Enumerations
│   │   │   ├── __init__.py
│   │   │   ├── location.py
│   │   │   ├── species.py
│   │   │   └── ...
│   │   ├── utils/             # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── date_utils.py
│   │   │   └── ...
│   │   └── resources/         # Assets (icons, images)
│   └── tests/                 # Test suite
│       ├── test_database.py
│       ├── test_phase*.py
│       └── ...
├── requirements.txt           # Python dependencies
├── setup.py                   # Package configuration
├── README.md                  # Project overview
├── ROADMAP.md                 # Development roadmap
├── QUICKSTART.md              # Quick start guide
├── USER_GUIDE.md              # User documentation
├── DEVELOPER_GUIDE.md         # This file
├── TESTING.md                 # Testing guide
└── LICENSE                    # MIT License
```

---

## Development Setup

### Prerequisites

- Python 3.11 or later
- Git
- Virtual environment tool (venv)

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/MrFrey75/WorldBuilder.git
   cd WorldBuilder
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Development Tools** (optional)
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

5. **Set PYTHONPATH**
   ```bash
   export PYTHONPATH=/path/to/WorldBuilder/src:$PYTHONPATH
   ```

6. **Run Application**
   ```bash
   python src/worldbuilder/main.py
   ```

---

## Core Components

### Models

Domain models represent entities in the system using SQLAlchemy ORM.

**Base Entity** (`models/base.py`):
```python
class BaseEntity:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
```

**Example Model** (`models/location.py`):
```python
class Location(BaseEntity, Base):
    __tablename__ = 'locations'
    
    universe_id = Column(Integer, ForeignKey('universes.id'))
    parent_id = Column(Integer, ForeignKey('locations.id'))
    location_type = Column(String)
    
    # Relationships
    universe = relationship("Universe", back_populates="locations")
    parent = relationship("Location", remote_side=[id])
    children = relationship("Location", back_populates="parent")
```

### Repositories

Repositories handle all database operations for a specific entity.

**Interface** (`database/repositories/base_repository.py`):
```python
class IRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
```

**Implementation**:
```python
class LocationRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Location, session)
    
    def get_by_parent(self, parent_id: int) -> List[Location]:
        return self.session.query(Location)\
            .filter(Location.parent_id == parent_id).all()
    
    def get_roots(self, universe_id: int) -> List[Location]:
        return self.session.query(Location)\
            .filter(Location.universe_id == universe_id)\
            .filter(Location.parent_id == None).all()
```

### Services

Services contain business logic and orchestrate operations.

**Example** (`services/location_service.py`):
```python
class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def create_location(self, universe_id: int, name: str, 
                       location_type: str, parent_id: Optional[int] = None) -> Location:
        # Validation
        if not name:
            raise ValueError("Name is required")
        
        # Business logic
        location = Location(
            universe_id=universe_id,
            name=name,
            location_type=location_type,
            parent_id=parent_id
        )
        
        return self.repository.add(location)
    
    def get_hierarchy(self, location_id: int) -> List[Location]:
        # Build full hierarchy path
        path = []
        current = self.repository.get_by_id(location_id)
        while current:
            path.insert(0, current)
            current = current.parent if current.parent_id else None
        return path
```

### Views

PyQt6 views handle UI presentation.

**Example** (`views/location_dialog.py`):
```python
class LocationDialog(QDialog):
    def __init__(self, parent=None, location_service=None):
        super().__init__(parent)
        self.location_service = location_service
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Name field
        self.name_input = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        
        # Type selector
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.value for t in LocationType])
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_combo)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self) -> dict:
        return {
            'name': self.name_input.text(),
            'location_type': self.type_combo.currentText()
        }
```

---

## Database Layer

### Database Manager

**Singleton Pattern** (`database/manager.py`):
```python
class DatabaseManager:
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'DatabaseManager':
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
    
    def initialize(self, db_path: str):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        return self.session_factory()
```

### Migrations

Schema changes are handled manually. To add a new field:

1. Update model in `models/`
2. Add migration logic in `database/migrations.py`
3. Run migration on application start
4. Test thoroughly

---

## Service Layer

### Service Pattern

Services encapsulate business logic:

```python
class EntityService:
    def __init__(self, repository: EntityRepository):
        self.repository = repository
    
    def create(self, data: dict) -> Entity:
        # 1. Validate input
        self.validate_data(data)
        
        # 2. Apply business rules
        entity = self.apply_business_rules(data)
        
        # 3. Persist
        return self.repository.add(entity)
    
    def validate_data(self, data: dict):
        # Validation logic
        pass
    
    def apply_business_rules(self, data: dict) -> Entity:
        # Business logic
        pass
```

### Dependency Injection

Services are injected into views:

```python
# In main.py
db_manager = DatabaseManager.get_instance()
session = db_manager.get_session()

# Create repositories
location_repo = LocationRepository(session)

# Create services
location_service = LocationService(location_repo)

# Create views with services
main_window = MainWindow(
    location_service=location_service,
    # ... other services
)
```

---

## UI Layer

### PyQt6 Signals & Slots

**Custom Signals**:
```python
class EntityListWidget(QWidget):
    entity_selected = pyqtSignal(int)  # Signal emits entity ID
    
    def on_item_clicked(self, item):
        entity_id = item.data(Qt.UserRole)
        self.entity_selected.emit(entity_id)
```

**Connecting Signals**:
```python
# In parent widget
self.entity_list.entity_selected.connect(self.on_entity_selected)

def on_entity_selected(self, entity_id: int):
    # Handle selection
    pass
```

### Custom Widgets

Create reusable components:

```python
class EntityCard(QWidget):
    clicked = pyqtSignal(int)
    
    def __init__(self, entity, parent=None):
        super().__init__(parent)
        self.entity = entity
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(self.entity.name)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Description preview
        desc = QLabel(self.entity.description[:100] + "...")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.entity.id)
```

---

## Testing

### Test Structure

```python
# test_location_service.py
import pytest
from worldbuilder.services.location_service import LocationService
from worldbuilder.database.repositories.location_repository import LocationRepository

@pytest.fixture
def db_session():
    # Create in-memory database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def location_service(db_session):
    repository = LocationRepository(db_session)
    return LocationService(repository)

def test_create_location(location_service):
    location = location_service.create_location(
        universe_id=1,
        name="Test Location",
        location_type="City"
    )
    assert location.name == "Test Location"
    assert location.location_type == "City"

def test_location_hierarchy(location_service):
    parent = location_service.create_location(1, "Continent", "Continent")
    child = location_service.create_location(1, "City", "City", parent.id)
    
    hierarchy = location_service.get_hierarchy(child.id)
    assert len(hierarchy) == 2
    assert hierarchy[0].id == parent.id
    assert hierarchy[1].id == child.id
```

### Running Tests

```bash
# All tests
python -m pytest src/tests/

# Specific test file
python -m pytest src/tests/test_location_service.py

# With coverage
python -m pytest --cov=worldbuilder src/tests/

# Verbose output
python -m pytest -v src/tests/
```

---

## Adding New Features

### Adding a New Entity Type

1. **Create Model** (`models/new_entity.py`):
   ```python
   class NewEntity(BaseEntity, Base):
       __tablename__ = 'new_entities'
       
       universe_id = Column(Integer, ForeignKey('universes.id'))
       custom_field = Column(String)
       
       universe = relationship("Universe", back_populates="new_entities")
   ```

2. **Create Repository** (`database/repositories/new_entity_repository.py`):
   ```python
   class NewEntityRepository(BaseRepository):
       def __init__(self, session: Session):
           super().__init__(NewEntity, session)
   ```

3. **Create Service** (`services/new_entity_service.py`):
   ```python
   class NewEntityService:
       def __init__(self, repository: NewEntityRepository):
           self.repository = repository
       
       def create_entity(self, data: dict) -> NewEntity:
           # Implementation
           pass
   ```

4. **Create View** (`views/new_entity_view.py`):
   ```python
   class NewEntityView(QWidget):
       def __init__(self, service: NewEntityService):
           super().__init__()
           self.service = service
           self.setup_ui()
   ```

5. **Write Tests** (`tests/test_new_entity.py`):
   ```python
   def test_create_new_entity(service):
       entity = service.create_entity({'name': 'Test'})
       assert entity.name == 'Test'
   ```

6. **Update Main Window** - Add menu items and navigation

7. **Update Documentation** - Add to USER_GUIDE.md

---

## Code Style

### Python Style Guide

Follow **PEP 8** with these guidelines:

- **Indentation**: 4 spaces
- **Line Length**: 100 characters max
- **Imports**: Grouped (stdlib, third-party, local)
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: `_leading_underscore`

### Type Hints

Use type hints for better IDE support:

```python
def create_location(self, universe_id: int, name: str, 
                   location_type: str) -> Location:
    pass

def get_locations(self) -> List[Location]:
    pass

def find_location(self, id: int) -> Optional[Location]:
    pass
```

### Documentation

Use docstrings for public APIs:

```python
def create_location(self, universe_id: int, name: str, 
                   location_type: str) -> Location:
    """
    Create a new location in the universe.
    
    Args:
        universe_id: ID of the parent universe
        name: Name of the location
        location_type: Type of location (City, Region, etc.)
    
    Returns:
        The newly created Location object
    
    Raises:
        ValueError: If name is empty or invalid
    """
    pass
```

---

## Contributing

### Workflow

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make Changes**
4. **Write Tests**
5. **Run Tests**
   ```bash
   python -m pytest src/tests/
   ```
6. **Commit Changes**
   ```bash
   git commit -m "Add new feature: description"
   ```
7. **Push to Fork**
   ```bash
   git push origin feature/my-new-feature
   ```
8. **Create Pull Request**

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

Examples:
```
feat: Add artifact search by owner
fix: Location hierarchy infinite loop
docs: Update installation instructions
test: Add species service tests
refactor: Extract validation logic
```

### Pull Request Guidelines

- Describe what the PR does
- Reference related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation if needed

---

## Resources

### Documentation
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Python 3.11 Documentation](https://docs.python.org/3.11/)

### Tools
- **Black**: Code formatter
- **Flake8**: Linter
- **MyPy**: Type checker
- **Pytest**: Testing framework

### Project Links
- [GitHub Repository](https://github.com/MrFrey75/WorldBuilder)
- [Issue Tracker](https://github.com/MrFrey75/WorldBuilder/issues)
- [Discussions](https://github.com/MrFrey75/WorldBuilder/discussions)

---

## Getting Help

- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Roadmap**: See [ROADMAP.md](ROADMAP.md)
- **Issues**: [GitHub Issues](https://github.com/MrFrey75/WorldBuilder/issues)

---

**Happy Coding!** 🚀

[← Back to README](README.md)
