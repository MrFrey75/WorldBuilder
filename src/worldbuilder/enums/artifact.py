"""Artifact-related enumerations."""
from enum import Enum


class ArtifactType(str, Enum):
    """Types of artifacts."""
    UNKWNOWN = "unknown"
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    TOOL = "tool"
    BOOK = "book"
    SCROLL = "scroll"
    POTION = "potion"
    RELIC = "relic"
    ARTIFACT = "artifact"
    MAGICAL_ITEM = "magical_item"
    TECHNOLOGY = "technology"
    VEHICLE = "vehicle"
    BUILDING = "building"
    TREASURE = "treasure"
    ART = "art"
    JEWELRY = "jewelry"
    OTHER = "other"
