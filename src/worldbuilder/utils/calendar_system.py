"""
Custom calendar system and date utilities for WorldBuilder.
Supports fictional calendars and date calculations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import json


@dataclass
class CustomCalendar:
    """
    Represents a custom calendar system for a fictional universe.
    """
    id: str
    name: str
    universe_id: str
    
    # Calendar structure
    days_per_week: int = 7
    months_per_year: int = 12
    days_per_year: int = 365
    
    # Month definitions (name -> days)
    month_definitions: Dict[str, int] = field(default_factory=dict)
    
    # Week day names
    weekday_names: List[str] = field(default_factory=list)
    
    # Era/epoch settings
    epoch_name: str = "Common Era"
    epoch_abbreviation: str = "CE"
    before_epoch_abbreviation: str = "BCE"
    allow_negative_years: bool = True
    
    # Current date marker (for "now" in timeline)
    current_date_year: Optional[int] = None
    current_date_month: Optional[int] = None
    current_date_day: Optional[int] = None
    
    def __post_init__(self):
        """Initialize default month and weekday names if not provided."""
        if not self.month_definitions:
            # Default Gregorian-like months
            self.month_definitions = {
                "January": 31, "February": 28, "March": 31, "April": 30,
                "May": 31, "June": 30, "July": 31, "August": 31,
                "September": 30, "October": 31, "November": 30, "December": 31
            }
        
        if not self.weekday_names:
            # Default weekday names
            self.weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                                 "Friday", "Saturday", "Sunday"]
    
    def get_month_name(self, month_number: int) -> str:
        """Get month name by number (1-indexed)."""
        month_names = list(self.month_definitions.keys())
        if 1 <= month_number <= len(month_names):
            return month_names[month_number - 1]
        return f"Month {month_number}"
    
    def get_days_in_month(self, month_number: int, year: Optional[int] = None) -> int:
        """Get number of days in a given month."""
        month_names = list(self.month_definitions.keys())
        if 1 <= month_number <= len(month_names):
            month_name = month_names[month_number - 1]
            return self.month_definitions[month_name]
        return 30  # Default
    
    def format_date(self, year: int, month: Optional[int] = None, 
                   day: Optional[int] = None) -> str:
        """Format a date according to this calendar system."""
        parts = []
        
        if day and month:
            parts.append(f"{day}")
            parts.append(self.get_month_name(month))
        elif month:
            parts.append(self.get_month_name(month))
        
        # Year with era
        if year < 0 and self.allow_negative_years:
            parts.append(f"{abs(year)} {self.before_epoch_abbreviation}")
        else:
            parts.append(f"{year} {self.epoch_abbreviation}")
        
        return " ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert calendar to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'universe_id': self.universe_id,
            'days_per_week': self.days_per_week,
            'months_per_year': self.months_per_year,
            'days_per_year': self.days_per_year,
            'month_definitions': self.month_definitions,
            'weekday_names': self.weekday_names,
            'epoch_name': self.epoch_name,
            'epoch_abbreviation': self.epoch_abbreviation,
            'before_epoch_abbreviation': self.before_epoch_abbreviation,
            'allow_negative_years': self.allow_negative_years,
            'current_date_year': self.current_date_year,
            'current_date_month': self.current_date_month,
            'current_date_day': self.current_date_day,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CustomCalendar':
        """Create calendar from dictionary."""
        return cls(**data)


class DateCalculator:
    """
    Utility class for date calculations in custom calendar systems.
    """
    
    @staticmethod
    def days_between(date1: datetime, date2: datetime) -> int:
        """Calculate days between two standard dates."""
        delta = abs(date2 - date1)
        return delta.days
    
    @staticmethod
    def years_between(date1: datetime, date2: datetime) -> float:
        """Calculate years between two standard dates."""
        days = DateCalculator.days_between(date1, date2)
        return days / 365.25
    
    @staticmethod
    def calculate_age(birth_date: datetime, current_date: Optional[datetime] = None) -> int:
        """Calculate age in years from birth date to current date."""
        if current_date is None:
            current_date = datetime.now()
        
        age = current_date.year - birth_date.year
        
        # Adjust if birthday hasn't occurred yet this year
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return max(0, age)
    
    @staticmethod
    def custom_days_between(year1: int, month1: int, day1: int,
                           year2: int, month2: int, day2: int,
                           calendar: CustomCalendar) -> int:
        """
        Calculate days between two dates in a custom calendar system.
        Simplified calculation assuming uniform year lengths.
        """
        # Convert both dates to "days from epoch"
        days1 = DateCalculator._to_days_from_epoch(year1, month1, day1, calendar)
        days2 = DateCalculator._to_days_from_epoch(year2, month2, day2, calendar)
        
        return abs(days2 - days1)
    
    @staticmethod
    def _to_days_from_epoch(year: int, month: int, day: int, 
                           calendar: CustomCalendar) -> int:
        """Convert a custom calendar date to days from epoch."""
        # Years to days
        days = year * calendar.days_per_year
        
        # Add days for complete months
        month_names = list(calendar.month_definitions.keys())
        for i in range(min(month - 1, len(month_names))):
            month_name = month_names[i]
            days += calendar.month_definitions[month_name]
        
        # Add remaining days
        days += day
        
        return days
    
    @staticmethod
    def custom_calculate_age(birth_year: int, birth_month: int, birth_day: int,
                           current_year: int, current_month: int, current_day: int,
                           calendar: CustomCalendar) -> int:
        """Calculate age in years using custom calendar."""
        age = current_year - birth_year
        
        # Adjust if birthday hasn't occurred yet this year
        if (current_month, current_day) < (birth_month, birth_day):
            age -= 1
        
        return max(0, age)
    
    @staticmethod
    def format_duration(days: int) -> str:
        """Format duration in days to human-readable string."""
        if days < 7:
            return f"{days} day{'s' if days != 1 else ''}"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''}"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months != 1 else ''}"
        else:
            years = days // 365
            remaining_days = days % 365
            if remaining_days > 30:
                months = remaining_days // 30
                return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"
            else:
                return f"{years} year{'s' if years != 1 else ''}"


class CalendarConverter:
    """
    Converts dates between different calendar systems.
    """
    
    @staticmethod
    def standard_to_custom(standard_date: datetime, 
                          calendar: CustomCalendar) -> tuple[int, int, int]:
        """
        Convert standard Gregorian date to custom calendar.
        Simple conversion based on day offsets.
        """
        # Calculate days since reference point (e.g., year 1)
        reference = datetime(1, 1, 1)
        days_since_ref = (standard_date - reference).days
        
        # Convert to custom calendar
        year = days_since_ref // calendar.days_per_year + 1
        remaining_days = days_since_ref % calendar.days_per_year
        
        # Find month and day
        month = 1
        month_names = list(calendar.month_definitions.keys())
        
        for i, month_name in enumerate(month_names, 1):
            days_in_month = calendar.month_definitions[month_name]
            if remaining_days < days_in_month:
                month = i
                day = remaining_days + 1
                break
            remaining_days -= days_in_month
        else:
            # Fallback to last month
            month = len(month_names)
            day = 1
        
        return (year, month, day)
    
    @staticmethod
    def custom_to_standard(year: int, month: int, day: int,
                          calendar: CustomCalendar) -> datetime:
        """
        Convert custom calendar date to standard Gregorian.
        Approximate conversion.
        """
        # Calculate total days
        total_days = DateCalculator._to_days_from_epoch(year, month, day, calendar)
        
        # Convert to standard date
        reference = datetime(1, 1, 1)
        try:
            standard_date = reference + timedelta(days=total_days)
            return standard_date
        except OverflowError:
            # Date is too far in future/past
            return reference


# Preset calendar templates
PRESET_CALENDARS = {
    "gregorian": {
        "name": "Gregorian Calendar",
        "days_per_week": 7,
        "months_per_year": 12,
        "days_per_year": 365,
        "month_definitions": {
            "January": 31, "February": 28, "March": 31, "April": 30,
            "May": 31, "June": 30, "July": 31, "August": 31,
            "September": 30, "October": 31, "November": 30, "December": 31
        },
        "weekday_names": ["Monday", "Tuesday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"],
        "epoch_name": "Common Era",
        "epoch_abbreviation": "CE",
        "before_epoch_abbreviation": "BCE",
        "allow_negative_years": True
    },
    "tolkien": {
        "name": "Shire Calendar",
        "days_per_week": 7,
        "months_per_year": 12,
        "days_per_year": 365,
        "month_definitions": {
            "Afteryule": 30, "Solmath": 30, "Rethe": 30, "Astron": 30,
            "Thrimidge": 30, "Forelithe": 30, "Afterlithe": 30, "Wedmath": 30,
            "Halimath": 30, "Winterfilth": 30, "Blotmath": 30, "Foreyule": 30
        },
        "weekday_names": ["Sterday", "Sunday", "Monday", "Trewsday", 
                         "Hevensday", "Mersday", "Highday"],
        "epoch_name": "Shire Reckoning",
        "epoch_abbreviation": "SR",
        "before_epoch_abbreviation": "BSR",
        "allow_negative_years": True
    },
    "fantasy_13": {
        "name": "13-Month Calendar",
        "days_per_week": 7,
        "months_per_year": 13,
        "days_per_year": 364,
        "month_definitions": {
            "Primus": 28, "Secundus": 28, "Tertius": 28, "Quartus": 28,
            "Quintus": 28, "Sextus": 28, "Septimus": 28, "Octavus": 28,
            "Nonus": 28, "Decimus": 28, "Undecimus": 28, "Duodecimus": 28,
            "Ultimus": 28
        },
        "weekday_names": ["Firstday", "Seconday", "Thirday", "Fourthday",
                         "Fifthday", "Sixthday", "Restday"],
        "epoch_name": "Age of Heroes",
        "epoch_abbreviation": "AH",
        "before_epoch_abbreviation": "BAH",
        "allow_negative_years": True
    }
}


def create_calendar_from_preset(preset_name: str, universe_id: str, 
                                calendar_id: str) -> CustomCalendar:
    """Create a custom calendar from a preset template."""
    if preset_name not in PRESET_CALENDARS:
        preset_name = "gregorian"
    
    preset = PRESET_CALENDARS[preset_name].copy()
    preset['id'] = calendar_id
    preset['universe_id'] = universe_id
    
    return CustomCalendar.from_dict(preset)
