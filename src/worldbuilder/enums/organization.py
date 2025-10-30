"""Organization-related enumerations."""
from enum import Enum


class OrganizationType(str, Enum):
    """Types of organizations."""
    UNKWNOWN = "unknown"
    KINGDOM = "kingdom"
    EMPIRE = "empire"
    NATION = "nation"
    CITY_STATE = "city_state"
    GUILD = "guild"
    RELIGIOUS = "religious"
    MILITARY = "military"
    CRIMINAL = "criminal"
    MERCHANT = "merchant"
    ACADEMIC = "academic"
    SECRET_SOCIETY = "secret_society"
    TRIBAL = "tribal"
    NOBLE_HOUSE = "noble_house"
    CLAN = "clan"
    FACTION = "faction"
    POLITICAL = "political"
    OTHER = "other"
