"""
Timer instance data model.

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
from models.enums import TimerStatus


@dataclass
class TimerInstance(Serializable):
    """Timer instance model for active customer timers."""
    id: UUID
    customer_name: str
    template_id: UUID
    remaining_time: timedelta  # Runtime only - NOT saved to DB
    status: TimerStatus  # Runtime only - NOT saved to DB
    display_order: int  # Saved to DB
    created_at: datetime  # Saved to DB

    @classmethod
    def create(
        cls,
        customer_name: str,
        template_id: UUID,
        initial_duration: timedelta,
        display_order: int
    ) -> 'TimerInstance':
        """
        Create a new timer instance.

        Args:
            customer_name: Customer name
            template_id: Associated template ID
            initial_duration: Initial timer duration
            display_order: Display order in list

        Returns:
            TimerInstance: New timer instance
        """
        return cls(
            id=uuid4(),
            customer_name=customer_name,
            template_id=template_id,
            remaining_time=initial_duration,
            status=TimerStatus.STOPPED,
            display_order=display_order,
            created_at=get_current_time()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert timer to dictionary for database storage."""
        return {
            'id': str(self.id),
            'customer_name': self.customer_name,
            'template_id': str(self.template_id),
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], template_duration: timedelta) -> 'TimerInstance':
        """
        Create timer from dictionary loaded from database.

        Args:
            data: Dictionary from database
            template_duration: Duration from associated template

        Returns:
            TimerInstance: Timer instance with STOPPED status
        """
        return cls(
            id=parse_uuid(data['id']),
            customer_name=data['customer_name'],
            template_id=parse_uuid(data['template_id']),
            remaining_time=template_duration,  # Reset to template duration
            status=TimerStatus.STOPPED,  # Always start as STOPPED
            display_order=data['display_order'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
