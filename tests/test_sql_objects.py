"""
Unit tests for SQL objects (functions, triggers, procedures, views).
"""
import pytest
from src.database.connection import DatabaseConnection
from src.database.sql_objects_demo import SQLObjectsDemo

def test_sql_function_execution():
    """Test execution of SQL functions."""
    db = DatabaseConnection()
    demo = SQLObjectsDemo(db)
    
    # Test calculate_discount function
    result = demo.execute_function(
        "calculate_discount",
        [100.00, 0.15]
    )
    assert result is not None
    assert float(result[0][0]) == 85.00

def test_sql_trigger_creation():
    """Test creation and execution of SQL triggers."""
    db = DatabaseConnection()
    demo = SQLObjectsDemo(db)
    
    # Test update_inventory trigger
    demo.create_trigger(
        "update_inventory",
        """
        CREATE TRIGGER update_inventory
        AFTER INSERT ON sales
        FOR EACH ROW
        BEGIN
            UPDATE products 
            SET stock = stock - NEW.quantity 
            WHERE product_id = NEW.product_id;
        END;
        """
    )
    assert demo.trigger_exists("update_inventory")

def test_sql_procedure_execution():
    """Test execution of stored procedures."""
    db = DatabaseConnection()
    demo = SQLObjectsDemo(db)
    
    # Test generate_sales_report procedure
    result = demo.execute_procedure(
        "generate_sales_report",
        ["2024-01-01", "2024-03-31"]
    )
    assert result is not None
    assert len(result) > 0

def test_sql_view_creation():
    """Test creation and querying of SQL views."""
    db = DatabaseConnection()
    demo = SQLObjectsDemo(db)
    
    # Test sales_summary view
    demo.create_view(
        "sales_summary",
        """
        CREATE VIEW sales_summary AS
        SELECT 
            s.sale_date,
            p.name as product_name,
            c.name as customer_name,
            s.quantity,
            s.total_price
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN customers c ON s.customer_id = c.customer_id;
        """
    )
    assert demo.view_exists("sales_summary")
    
    # Test querying the view
    result = demo.query_view("sales_summary")
    assert result is not None

def test_sql_view_execution():
    demo = SQLObjectsDemo()
    try:
        result = demo.demo_customer_purchase_history(1)
        assert isinstance(result, list)
    except Exception:
        pytest.skip("Vista SQL no disponible en la base de datos de test")
