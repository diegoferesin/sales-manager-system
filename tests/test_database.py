"""
Unit tests for database operations and connection management.
"""
import pytest
from src.database.connection import DatabaseConnection

def test_singleton_pattern():
    """Test that DatabaseConnection follows singleton pattern."""
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2

def test_query_execution():
    """Test query execution."""
    db = DatabaseConnection()
    result = db.execute_query("SELECT 1")
    assert result is not None
    assert len(result) > 0
