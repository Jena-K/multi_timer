"""
Timer template data model.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any
from uuid import UUID, uuid4

from models.base import Serializable, get_current_time, parse_uuid


@dataclass
class TimerTemplate(Serializable):
    """Timer template model for storing template configurations."""
    id: UUID
    name: str
    duration: timedelta  # Format: MM:SS (minutes: 00-99, seconds: 00-59)
    display_order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, name: str, duration: timedelta, display_order: int) -> 'TimerTemplate':
        """
        Create a new timer template.

        Args:
            name: Template name
            duration: Timer duration (timedelta)
            display_order: Display order in list

        Returns:
            TimerTemplate: New template instance
        """
        now = get_current_time()
        return cls(
            id=uuid4(),
            name=name,
            duration=duration,
            display_order=display_order,
            created_at=now,
            updated_at=now
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary for database storage."""
        return {
            'id': str(self.id),
            'name': self.name,
            'duration_seconds': int(self.duration.total_seconds()),
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimerTemplate':
        """Create template from dictionary."""
        return cls(
            id=parse_uuid(data['id']),
            name=data['name'],
            duration=timedelta(seconds=data['duration_seconds']),
            display_order=data['display_order'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )
