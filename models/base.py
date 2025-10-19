"""
Base models and utilities for Timer For Ryu application.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict
from uuid import UUID


class Serializable(ABC):
    """Base class for models that can be serialized to/from dictionaries."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for database storage."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        """Create model from dictionary loaded from database."""
        pass


def get_current_time() -> datetime:
    """Get current datetime. Centralized for easier testing and consistency."""
    return datetime.now()


def parse_uuid(value: str | UUID) -> UUID:
    """Parse UUID from string or UUID object."""
    return value if isinstance(value, UUID) else UUID(value)