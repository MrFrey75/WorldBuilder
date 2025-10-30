"""Event-related enumerations."""
from enum import Enum


class EventType(Enum):

    UNKWNOWN = "Unknown"
    OTHER = "Other"

    """Types/categories of events."""
    BIRTH = "Birth"
    DEATH = "Death"
    BATTLE = "Battle"
    WAR = "War"
    CORONATION = "Coronation"
    MARRIAGE = "Marriage"
    DISCOVERY = "Discovery"
    INVENTION = "Invention"
    FOUNDING = "Founding"
    DESTRUCTION = "Destruction"
    MEETING = "Meeting"
    TREATY = "Treaty"
    PROPHECY = "Prophecy"
    QUEST = "Quest"
    NATURAL_DISASTER = "Natural Disaster"
    POLITICAL = "Political Event"
    CULTURAL = "Cultural Event"
    RELIGIOUS = "Religious Event"


class EventImportance(Enum):
    """Significance levels for events."""
    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    CRITICAL = "Critical"
    LEGENDARY = "Legendary"


class DatePrecision(Enum):
    """Precision levels for event dates."""
    EXACT = "Exact Date/Time"
    DAY = "Specific Day"
    MONTH = "Specific Month"
    YEAR = "Specific Year"
    DECADE = "Decade"
    CENTURY = "Century"
    ERA = "Era/Period"
    APPROXIMATE = "Approximate"
    RELATIVE = "Relative to Other Event"
    UNKNOWN = "Unknown"
