"""
Enums for Timer For Ryu application.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from enum import Enum


class TimerStatus(Enum):
    """Timer state enumeration."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
