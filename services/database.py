"""
SQLite database service for Timer For Ryu.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19

Usage:
    from services.database import DatabaseService
    from pathlib import Path

    db = DatabaseService(Path("data/timer_data.db"))
    templates = db.get_all_templates()
"""
import sqlite3
import os
import logging
from pathlib import Path
from typing import List, Optional, Callable, TypeVar, Any
from contextlib import contextmanager
from datetime import timedelta
from models.template import TimerTemplate
from models.timer import TimerInstance

logger = logging.getLogger(__name__)

T = TypeVar('T')


def get_data_dir() -> Path:
    """
    Get application data directory.

    Returns:
        Path: Application data directory path
    """
    if os.name == 'nt':  # Windows
        base_dir = Path(os.environ['APPDATA']) / 'TimerForRyu'
    else:  # macOS/Linux
        base_dir = Path.home() / '.timer_for_ryu'

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_db_path() -> Path:
    """
    Get database file path.

    Returns:
        Path: Database file path
    """
    return get_data_dir() / 'timer_data.db'


class DatabaseService:
    """SQLite database service for templates and timers."""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database service.

        Args:
            db_path: Optional custom database path (defaults to %APPDATA%/TimerForRyu/timer_data.db)
        """
        self.db_path = db_path or get_db_path()
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _execute_query(
        self,
        operation: Callable[[sqlite3.Cursor], T],
        error_message: str
    ) -> T:
        """
        Execute database operation with error handling.

        Args:
            operation: Function that takes cursor and returns result
            error_message: Error message prefix for logging

        Returns:
            T: Result from operation function
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                return operation(cursor)
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            raise

    def _init_database(self) -> None:
        """Create database and tables if they don't exist."""
        def _create_tables(cursor: sqlite3.Cursor) -> None:
            # Create templates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS templates (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    display_order INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create timers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timers (
                    id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    template_id TEXT NOT NULL,
                    display_order INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE
                )
            """)

        self._execute_query(_create_tables, "Database initialization error")

    # Template CRUD operations

    def create_template(self, template: TimerTemplate) -> None:
        """
        Create a new template in database.

        Args:
            template: TimerTemplate instance to save
        """
        def _insert(cursor: sqlite3.Cursor) -> None:
            data = template.to_dict()
            cursor.execute("""
                INSERT INTO templates (id, name, duration_seconds, display_order, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['id'],
                data['name'],
                data['duration_seconds'],
                data['display_order'],
                data['created_at'],
                data['updated_at']
            ))

        self._execute_query(_insert, "Error creating template")

    def get_all_templates(self) -> List[TimerTemplate]:
        """
        Get all templates ordered by display_order.

        Returns:
            List[TimerTemplate]: List of all templates
        """
        def _select(cursor: sqlite3.Cursor) -> List[TimerTemplate]:
            cursor.row_factory = sqlite3.Row
            cursor.execute("""
                SELECT id, name, duration_seconds, display_order, created_at, updated_at
                FROM templates
                ORDER BY display_order ASC
            """)
            return [TimerTemplate.from_dict(dict(row)) for row in cursor.fetchall()]

        try:
            return self._execute_query(_select, "Error getting templates")
        except Exception:
            return []

    def update_template(self, template: TimerTemplate) -> None:
        """
        Update existing template.

        Args:
            template: TimerTemplate instance with updated values
        """
        def _update(cursor: sqlite3.Cursor) -> None:
            data = template.to_dict()
            cursor.execute("""
                UPDATE templates
                SET name = ?, duration_seconds = ?, display_order = ?, updated_at = ?
                WHERE id = ?
            """, (
                data['name'],
                data['duration_seconds'],
                data['display_order'],
                data['updated_at'],
                data['id']
            ))

        self._execute_query(_update, "Error updating template")

    def delete_template(self, template_id: str) -> None:
        """
        Delete template and cascade delete associated timers.

        Args:
            template_id: UUID string of template to delete
        """
        def _delete(cursor: sqlite3.Cursor) -> None:
            # SQLite CASCADE DELETE automatically deletes associated timers
            cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))

        self._execute_query(_delete, "Error deleting template")

    # Timer CRUD operations

    def create_timer(self, timer: TimerInstance) -> None:
        """
        Create a new timer in database.

        Args:
            timer: TimerInstance to save
        """
        def _insert(cursor: sqlite3.Cursor) -> None:
            data = timer.to_dict()
            cursor.execute("""
                INSERT INTO timers (id, customer_name, template_id, display_order, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['id'],
                data['customer_name'],
                data['template_id'],
                data['display_order'],
                data['created_at']
            ))

        self._execute_query(_insert, "Error creating timer")

    def _fetch_timers_with_templates(
        self,
        cursor: sqlite3.Cursor,
        where_clause: str = "",
        params: tuple = ()
    ) -> List[tuple[TimerInstance, TimerTemplate]]:
        """
        Common method to fetch timers with their templates.

        Args:
            cursor: Database cursor
            where_clause: Optional WHERE clause (e.g., "WHERE t.template_id = ?")
            params: Parameters for WHERE clause

        Returns:
            List[tuple[TimerInstance, TimerTemplate]]: List of (timer, template) tuples
        """
        query = f"""
            SELECT
                t.id, t.customer_name, t.template_id, t.display_order, t.created_at,
                tp.id as template_id_full, tp.name, tp.duration_seconds,
                tp.display_order as template_display_order, tp.created_at as template_created_at,
                tp.updated_at as template_updated_at
            FROM timers t
            JOIN templates tp ON t.template_id = tp.id
            {where_clause}
            ORDER BY t.display_order ASC
        """
        cursor.row_factory = sqlite3.Row
        cursor.execute(query, params)

        timers = []
        for row in cursor.fetchall():
            row_dict = dict(row)

            # Extract template data
            template_data = {
                'id': row_dict['template_id_full'],
                'name': row_dict['name'],
                'duration_seconds': row_dict['duration_seconds'],
                'display_order': row_dict['template_display_order'],
                'created_at': row_dict['template_created_at'],
                'updated_at': row_dict['template_updated_at']
            }
            template = TimerTemplate.from_dict(template_data)

            # Extract timer data
            timer_data = {
                'id': row_dict['id'],
                'customer_name': row_dict['customer_name'],
                'template_id': row_dict['template_id'],
                'display_order': row_dict['display_order'],
                'created_at': row_dict['created_at']
            }
            timer = TimerInstance.from_dict(timer_data, template.duration)

            timers.append((timer, template))

        return timers

    def get_all_timers(self) -> List[tuple[TimerInstance, TimerTemplate]]:
        """
        Get all timers with their associated templates.

        Returns:
            List[tuple[TimerInstance, TimerTemplate]]: List of (timer, template) tuples
        """
        def _select(cursor: sqlite3.Cursor) -> List[tuple[TimerInstance, TimerTemplate]]:
            return self._fetch_timers_with_templates(cursor)

        try:
            return self._execute_query(_select, "Error getting timers")
        except Exception:
            return []

    def update_timer(self, timer: TimerInstance) -> None:
        """
        Update existing timer.

        Args:
            timer: TimerInstance with updated values
        """
        def _update(cursor: sqlite3.Cursor) -> None:
            data = timer.to_dict()
            cursor.execute("""
                UPDATE timers
                SET customer_name = ?, display_order = ?
                WHERE id = ?
            """, (
                data['customer_name'],
                data['display_order'],
                data['id']
            ))

        self._execute_query(_update, "Error updating timer")

    def delete_timer(self, timer_id: str) -> None:
        """
        Delete timer instance.

        Args:
            timer_id: UUID string of timer to delete
        """
        def _delete(cursor: sqlite3.Cursor) -> None:
            cursor.execute("DELETE FROM timers WHERE id = ?", (timer_id,))

        self._execute_query(_delete, "Error deleting timer")

    def get_timers_by_template(self, template_id: str) -> List[TimerInstance]:
        """
        Get all timers associated with a specific template.

        Args:
            template_id: UUID string of template

        Returns:
            List[TimerInstance]: List of timers using this template
        """
        def _select(cursor: sqlite3.Cursor) -> List[TimerInstance]:
            results = self._fetch_timers_with_templates(
                cursor,
                where_clause="WHERE t.template_id = ?",
                params=(template_id,)
            )
            # Return only timer instances, not templates
            return [timer for timer, _ in results]

        try:
            return self._execute_query(_select, "Error getting timers by template")
        except Exception:
            return []
