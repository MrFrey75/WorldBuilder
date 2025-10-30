"""Species-related enumerations."""
from enum import Enum


class SpeciesType(Enum):
    """Classification types for species."""
    UNKWNOWN = "unknown"
    SENTIENT = "Sentient"
    NON_SENTIENT = "Non-Sentient"
    MAGICAL = "Magical"
    DIVINE = "Divine"
    UNDEAD = "Undead"
    CONSTRUCT = "Construct"
    HYBRID = "Hybrid"
    OTHER = "Other"
