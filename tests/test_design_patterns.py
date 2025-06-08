"""
Unit tests for design patterns implementation.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch

from src.database.connection import DatabaseConnection
from src.utils.model_factory import ModelFactoryRegistry, CategoryFactory, ProductFactory
from src.utils.query_builder import SQLQueryBuilder, QueryBuilderDirector
from src.utils.analysis_strategies import (
    RevenueAnalysisStrategy, 
    QuantityAnalysisStrategy, 
    SalesAnalysisContext,
    AnalysisStrategyFactory
)
from src.utils.decorators import timing_decorator, logging_decorator, caching_decorator


class TestSingletonPattern:
    """
    Test cases for Singleton pattern implementation.
    """
    
    def test_singleton_same_instance(self):
        """
        Test that DatabaseConnection returns the same instance.
        """
        # Mock the environment variables to avoid actual database connection
        with patch.dict('os.environ', {
            'DB_USER': 'test_user',
            'DB_PASSWORD': 'test_password', 
            'DB_HOST': 'localhost',
            'DB_PORT': '3306',
            'DB_NAME': 'test_db'
        }):
            with patch('src.database.connection.create_engine'):
                db1 = DatabaseConnection()
                db2 = DatabaseConnection()
                
                assert db1 is db2, "DatabaseConnection should return the same instance"
    
    def test_singleton_reset_after_close(self):
        """
        Test that singleton resets after close.
        """
        with patch.dict('os.environ', {
            'DB_USER': 'test_user',
            'DB_PASSWORD': 'test_password',
            'DB_HOST': 'localhost', 
            'DB_PORT': '3306',
            'DB_NAME': 'test_db'
        }):
            with patch('src.database.connection.create_engine'):
                db1 = DatabaseConnection()
                db1.close()
                db2 = DatabaseConnection()
                
                # After close, we should get a new instance
                assert db1 is not db2, "New instance should be created after close"


class TestFactoryPattern:
    """
    Test cases for Factory pattern implementation.
    """
    
    def test_category_factory_creation(self):
        """
        Test CategoryFactory creates Category instances.
        """
        factory = CategoryFactory()
        category_data = {'category_id': 1, 'category_name': 'Electronics'}
        
        category = factory.create_model(category_data)
        
        assert category.category_id == 1
        assert category.category_name == 'Electronics'
    
    def test_product_factory_creation(self):
        """
        Test ProductFactory creates Product instances.
        """
        factory = ProductFactory()
        product_data = {
            'product_id': 1,
            'product_name': 'Laptop',
            'price': 999.99,
            'category_id': 1
        }
        
        product = factory.create_model(product_data)
        
        assert product.product_id == 1
        assert product.product_name == 'Laptop'
        assert product.price == 999.99
    
    def test_model_factory_registry(self):
        """
        Test ModelFactoryRegistry creates correct models.
        """
        category_data = {'category_id': 1, 'category_name': 'Electronics'}
        
        category = ModelFactoryRegistry.create_model('category', category_data)
        
        assert category.category_id == 1
        assert category.category_name == 'Electronics'
    
    def test_factory_registry_invalid_type(self):
        """
        Test that invalid model type raises ValueError.
        """
        with pytest.raises(ValueError, match="Unsupported model type"):
            ModelFactoryRegistry.create_model('invalid_type', {})


class TestBuilderPattern:
    """
    Test cases for Builder pattern implementation.
    """
    
    def test_simple_query_builder(self):
        """
        Test basic SQL query building.
        """
        builder = SQLQueryBuilder()
        
        query = (builder
                .select(['name', 'age'])
                .from_table('users')
                .where('age > 18')
                .order_by('name')
                .build())
        
        expected = "SELECT name, age\nFROM users\nWHERE age > 18\nORDER BY name ASC"
        assert query == expected
    
    def test_complex_query_builder(self):
        """
        Test complex SQL query building with joins.
        """
        builder = SQLQueryBuilder()
        
        query = (builder
                .select(['u.name', 'p.title'])
                .from_table('users u')
                .inner_join('posts p', 'u.id = p.user_id')
                .where('u.active = 1')
                .group_by(['u.id'])
                .order_by('u.name')
                .limit(10)
                .build())
        
        expected_parts = [
            "SELECT u.name, p.title",
            "FROM users u",
            "INNER JOIN posts p ON u.id = p.user_id",
            "WHERE u.active = 1",
            "GROUP BY u.id",
            "ORDER BY u.name ASC",
            "LIMIT 10"
        ]
        expected = "\n".join(expected_parts)
        assert query == expected
    
    def test_query_builder_director(self):
        """
        Test QueryBuilderDirector preset patterns.
        """
        builder = SQLQueryBuilder()
        director = QueryBuilderDirector(builder)
        
        query = director.build_sales_summary_by_category()
        
        assert "SELECT c.category_name" in query
        assert "FROM sales s" in query
        assert "INNER JOIN products p" in query
        assert "INNER JOIN categories c" in query
        assert "GROUP BY c.category_name" in query
    
    def test_builder_validation(self):
        """
        Test that builder validates required fields.
        """
        builder = SQLQueryBuilder()
        
        with pytest.raises(ValueError, match="SELECT fields are required"):
            builder.from_table('users').build()
        
        with pytest.raises(ValueError, match="FROM table is required"):
            builder.select(['name']).build()


class TestStrategyPattern:
    """
    Test cases for Strategy pattern implementation.
    """
    
    def test_revenue_analysis_strategy(self):
        """
        Test RevenueAnalysisStrategy.
        """
        strategy = RevenueAnalysisStrategy()
        
        # Create sample data
        data = pd.DataFrame({
            'total_price': [100.0, 200.0, 150.0, 300.0],
            'sale_id': [1, 2, 3, 4]
        })
        
        results = strategy.analyze(data)
        
        assert results['strategy'] == "Revenue Analysis Strategy"
        assert results['total_revenue'] == 750.0
        assert results['average_sale_amount'] == 187.5
        assert results['total_transactions'] == 4
        assert 'revenue_quartiles' in results
    
    def test_quantity_analysis_strategy(self):
        """
        Test QuantityAnalysisStrategy.
        """
        strategy = QuantityAnalysisStrategy()
        
        # Create sample data
        data = pd.DataFrame({
            'quantity': [1, 5, 3, 10, 2],
            'sale_id': [1, 2, 3, 4, 5]
        })
        
        results = strategy.analyze(data)
        
        assert results['strategy'] == "Quantity Analysis Strategy"
        assert results['total_items_sold'] == 21
        assert results['average_quantity_per_sale'] == 4.2
        assert results['total_transactions'] == 5
        assert 'quantity_distribution' in results
    
    def test_analysis_strategy_factory(self):
        """
        Test AnalysisStrategyFactory.
        """
        revenue_strategy = AnalysisStrategyFactory.create_strategy('revenue')
        quantity_strategy = AnalysisStrategyFactory.create_strategy('quantity')
        
        assert isinstance(revenue_strategy, RevenueAnalysisStrategy)
        assert isinstance(quantity_strategy, QuantityAnalysisStrategy)
        
        available_strategies = AnalysisStrategyFactory.get_available_strategies()
        assert 'revenue' in available_strategies
        assert 'quantity' in available_strategies
    
    def test_analysis_context(self):
        """
        Test SalesAnalysisContext strategy switching.
        """
        revenue_strategy = RevenueAnalysisStrategy()
        context = SalesAnalysisContext(revenue_strategy)
        
        # Test strategy switching
        quantity_strategy = QuantityAnalysisStrategy()
        context.set_strategy(quantity_strategy)
        
        assert context._strategy is quantity_strategy
    
    def test_strategy_with_missing_columns(self):
        """
        Test strategy behavior with missing required columns.
        """
        strategy = RevenueAnalysisStrategy()
        
        # Data without required 'total_price' column
        data = pd.DataFrame({'sale_id': [1, 2, 3]})
        
        with pytest.raises(ValueError, match="Data must contain 'total_price' column"):
            strategy.analyze(data)


class TestDecoratorPattern:
    """
    Test cases for Decorator pattern implementation.
    """
    
    def test_timing_decorator(self):
        """
        Test timing decorator functionality.
        """
        @timing_decorator
        def sample_function():
            return "test_result"
        
        result = sample_function()
        assert result == "test_result"
    
    def test_logging_decorator(self):
        """
        Test logging decorator functionality.
        """
        @logging_decorator
        def sample_function(arg1, arg2=None):
            return f"result_{arg1}_{arg2}"
        
        result = sample_function("test", arg2="value")
        assert result == "result_test_value"
    
    def test_caching_decorator(self):
        """
        Test caching decorator functionality.
        """
        call_count = 0
        
        @caching_decorator(cache_ttl=300)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increment
        
        # Different parameter should not use cache
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2
    
    def test_decorator_with_dataframe_result(self):
        """
        Test decorator with DataFrame result.
        """
        @timing_decorator
        def function_returning_dataframe():
            return pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        
        result = function_returning_dataframe()
        assert isinstance(result, pd.DataFrame)
        assert 'execution_time' in result.attrs


class TestIntegration:
    """
    Integration tests combining multiple patterns.
    """
    
    def test_factory_with_builder(self):
        """
        Test Factory pattern combined with Builder pattern.
        """
        # Use factory to create model
        category_data = {'category_id': 1, 'category_name': 'Electronics'}
        category = ModelFactoryRegistry.create_model('category', category_data)
        
        # Use builder to create query
        builder = SQLQueryBuilder()
        query = (builder
                .select(['*'])
                .from_table('categories')
                .where_equals('category_id', category.category_id)
                .build())
        
        assert "SELECT *" in query
        assert "FROM categories" in query
        assert "WHERE category_id = 1" in query
    
    def test_strategy_with_decorator(self):
        """
        Test Strategy pattern combined with Decorator pattern.
        """
        @timing_decorator
        @logging_decorator
        def decorated_analysis(strategy, data):
            return strategy.analyze(data)
        
        strategy = RevenueAnalysisStrategy()
        data = pd.DataFrame({'total_price': [100.0, 200.0]})
        
        result = decorated_analysis(strategy, data)
        
        assert result['strategy'] == "Revenue Analysis Strategy"
        assert result['total_revenue'] == 300.0 