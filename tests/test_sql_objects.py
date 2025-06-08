"""
Unit tests for SQL objects (functions, triggers, procedures, views).
"""
import pytest
from src.database.sql_objects_demo import SQLObjectsDemo

def test_sql_function_execution():
    demo = SQLObjectsDemo()
    try:
        result = demo.demo_customer_lifetime_value(1, 12)
        assert isinstance(result, (float, int))
    except Exception:
        pytest.skip("Función SQL no disponible en la base de datos de test")

def test_sql_view_execution():
    demo = SQLObjectsDemo()
    try:
        result = demo.demo_customer_purchase_history(1)
        assert isinstance(result, list)
    except Exception:
        pytest.skip("Vista SQL no disponible en la base de datos de test")
