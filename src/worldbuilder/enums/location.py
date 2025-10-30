"""Location-related enumerations."""
from enum import Enum


class LocationType(Enum):
    """Types of locations in hierarchical order."""
    UNKWNOWN = "unknown"
    UNIVERSE = "Universe"
    GALAXY = "Galaxy"
    STAR_SYSTEM = "Star System"
    PLANET = "Planet"
    CONTINENT = "Continent"
    REGION = "Region"
    COUNTRY = "Country"
    STATE = "State/Province"
    CITY = "City"
    DISTRICT = "District"
    BUILDING = "Building"
    ROOM = "Room"
    OTHER = "Other"
