"""
Strategy pattern implementation for different sales analysis algorithms.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd
from ..database.connection import DatabaseConnection


class AnalysisStrategy(ABC):
    """
    Abstract strategy class for sales analysis.
    This pattern solves the problem of having multiple analysis algorithms
    and allows for easy switching between different analysis approaches.
    """
    
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform analysis on the provided data.
        Args:
            data (pd.DataFrame): Data to analyze.
        Returns:
            Dict[str, Any]: Analysis results.
        """
        pass
    
    @abstractmethod
    def get_analysis_name(self) -> str:
        """
        Get the name of this analysis strategy.
        Returns:
            str: Strategy name.
        """
        pass


class RevenueAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for revenue-focused analysis.
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform revenue analysis.
        Args:
            data (pd.DataFrame): Sales data.
        Returns:
            Dict[str, Any]: Revenue analysis results.
        """
        if 'total_price' not in data.columns:
            raise ValueError("Data must contain 'total_price' column for revenue analysis")
        
        results = {
            'strategy': self.get_analysis_name(),
            'total_revenue': float(data['total_price'].sum()),
            'average_sale_amount': float(data['total_price'].mean()),
            'median_sale_amount': float(data['total_price'].median()),
            'min_sale_amount': float(data['total_price'].min()),
            'max_sale_amount': float(data['total_price'].max()),
            'revenue_std': float(data['total_price'].std()),
            'total_transactions': len(data)
        }
        
        # Revenue distribution analysis
        if len(data) > 0:
            results['revenue_quartiles'] = {
                'q1': float(data['total_price'].quantile(0.25)),
                'q2': float(data['total_price'].quantile(0.5)),
                'q3': float(data['total_price'].quantile(0.75))
            }
        
        return results
    
    def get_analysis_name(self) -> str:
        """
        Get the strategy name.
        Returns:
            str: Strategy name.
        """
        return "Revenue Analysis Strategy"


class QuantityAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for quantity-focused analysis.
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform quantity analysis.
        Args:
            data (pd.DataFrame): Sales data.
        Returns:
            Dict[str, Any]: Quantity analysis results.
        """
        if 'quantity' not in data.columns:
            raise ValueError("Data must contain 'quantity' column for quantity analysis")
        
        results = {
            'strategy': self.get_analysis_name(),
            'total_items_sold': int(data['quantity'].sum()),
            'average_quantity_per_sale': float(data['quantity'].mean()),
            'median_quantity_per_sale': float(data['quantity'].median()),
            'min_quantity': int(data['quantity'].min()),
            'max_quantity': int(data['quantity'].max()),
            'quantity_std': float(data['quantity'].std()),
            'total_transactions': len(data)
        }
        
        # Quantity distribution analysis
        if len(data) > 0:
            results['quantity_distribution'] = {
                'single_item_sales': len(data[data['quantity'] == 1]),
                'bulk_sales_5_plus': len(data[data['quantity'] >= 5]),
                'bulk_sales_10_plus': len(data[data['quantity'] >= 10])
            }
        
        return results
    
    def get_analysis_name(self) -> str:
        """
        Get the strategy name.
        Returns:
            str: Strategy name.
        """
        return "Quantity Analysis Strategy"


class CustomerBehaviorAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for customer behavior analysis.
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform customer behavior analysis.
        Args:
            data (pd.DataFrame): Sales data.
        Returns:
            Dict[str, Any]: Customer behavior analysis results.
        """
        required_columns = ['customer_id', 'total_price']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Data must contain '{col}' column for customer behavior analysis")
        
        # Customer aggregations
        customer_stats = data.groupby('customer_id').agg({
            'total_price': ['sum', 'count', 'mean'],
            'sale_date': ['min', 'max'] if 'sale_date' in data.columns else []
        }).reset_index()
        
        # Flatten column names
        customer_stats.columns = [
            'customer_id', 'total_spent', 'purchase_count', 'avg_purchase_amount'
        ] + (['first_purchase', 'last_purchase'] if 'sale_date' in data.columns else [])
        
        results = {
            'strategy': self.get_analysis_name(),
            'unique_customers': len(customer_stats),
            'avg_customer_lifetime_value': float(customer_stats['total_spent'].mean()),
            'avg_purchases_per_customer': float(customer_stats['purchase_count'].mean()),
            'top_customers_count': len(customer_stats[customer_stats['total_spent'] > customer_stats['total_spent'].quantile(0.8)]),
            'one_time_customers': len(customer_stats[customer_stats['purchase_count'] == 1]),
            'repeat_customers': len(customer_stats[customer_stats['purchase_count'] > 1])
        }
        
        # Customer segmentation
        if len(customer_stats) > 0:
            high_value_threshold = customer_stats['total_spent'].quantile(0.8)
            high_frequency_threshold = customer_stats['purchase_count'].quantile(0.8)
            
            results['customer_segments'] = {
                'high_value_high_frequency': len(customer_stats[
                    (customer_stats['total_spent'] >= high_value_threshold) &
                    (customer_stats['purchase_count'] >= high_frequency_threshold)
                ]),
                'high_value_low_frequency': len(customer_stats[
                    (customer_stats['total_spent'] >= high_value_threshold) &
                    (customer_stats['purchase_count'] < high_frequency_threshold)
                ]),
                'low_value_high_frequency': len(customer_stats[
                    (customer_stats['total_spent'] < high_value_threshold) &
                    (customer_stats['purchase_count'] >= high_frequency_threshold)
                ]),
                'low_value_low_frequency': len(customer_stats[
                    (customer_stats['total_spent'] < high_value_threshold) &
                    (customer_stats['purchase_count'] < high_frequency_threshold)
                ])
            }
        
        return results
    
    def get_analysis_name(self) -> str:
        """
        Get the strategy name.
        Returns:
            str: Strategy name.
        """
        return "Customer Behavior Analysis Strategy"


class ProductPerformanceAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for product performance analysis.
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform product performance analysis.
        Args:
            data (pd.DataFrame): Sales data.
        Returns:
            Dict[str, Any]: Product performance analysis results.
        """
        required_columns = ['product_id', 'total_price', 'quantity']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Data must contain '{col}' column for product performance analysis")
        
        # Product aggregations
        product_stats = data.groupby('product_id').agg({
            'total_price': ['sum', 'count', 'mean'],
            'quantity': 'sum'
        }).reset_index()
        
        # Flatten column names
        product_stats.columns = ['product_id', 'total_revenue', 'sales_count', 'avg_sale_amount', 'total_quantity_sold']
        
        results = {
            'strategy': self.get_analysis_name(),
            'unique_products_sold': len(product_stats),
            'avg_revenue_per_product': float(product_stats['total_revenue'].mean()),
            'avg_quantity_per_product': float(product_stats['total_quantity_sold'].mean()),
            'top_performing_products_count': len(product_stats[product_stats['total_revenue'] > product_stats['total_revenue'].quantile(0.8)]),
            'underperforming_products_count': len(product_stats[product_stats['total_revenue'] < product_stats['total_revenue'].quantile(0.2)])
        }
        
        # Product performance tiers
        if len(product_stats) > 0:
            results['product_performance_tiers'] = {
                'top_tier': len(product_stats[product_stats['total_revenue'] >= product_stats['total_revenue'].quantile(0.8)]),
                'mid_tier': len(product_stats[
                    (product_stats['total_revenue'] >= product_stats['total_revenue'].quantile(0.4)) &
                    (product_stats['total_revenue'] < product_stats['total_revenue'].quantile(0.8))
                ]),
                'low_tier': len(product_stats[product_stats['total_revenue'] < product_stats['total_revenue'].quantile(0.4)])
            }
        
        return results
    
    def get_analysis_name(self) -> str:
        """
        Get the strategy name.
        Returns:
            str: Strategy name.
        """
        return "Product Performance Analysis Strategy"


class SalesAnalysisContext:
    """
    Context class that uses different analysis strategies.
    This provides a unified interface for performing different types of analysis.
    """
    
    def __init__(self, strategy: AnalysisStrategy):
        """
        Initialize with a specific analysis strategy.
        Args:
            strategy (AnalysisStrategy): The analysis strategy to use.
        """
        self._strategy = strategy
        self.db = DatabaseConnection()
    
    def set_strategy(self, strategy: AnalysisStrategy) -> None:
        """
        Change the analysis strategy.
        Args:
            strategy (AnalysisStrategy): New strategy to use.
        """
        self._strategy = strategy
    
    def perform_analysis(self, data: pd.DataFrame = None, table: str = None) -> Dict[str, Any]:
        """
        Perform analysis using the current strategy.
        Args:
            data (pd.DataFrame, optional): Data to analyze. If None, will query from table.
            table (str, optional): Table name to query data from.
        Returns:
            Dict[str, Any]: Analysis results.
        """
        if data is None:
            if table is None:
                # Default to sales table
                data = self.db.execute_query("SELECT * FROM sales")
            else:
                data = self.db.execute_query(f"SELECT * FROM {table}")
        
        return self._strategy.analyze(data)
    
    def compare_strategies(self, strategies: List[AnalysisStrategy], data: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Compare results from multiple analysis strategies.
        Args:
            strategies (List[AnalysisStrategy]): List of strategies to compare.
            data (pd.DataFrame, optional): Data to analyze.
        Returns:
            Dict[str, Any]: Comparison results.
        """
        if data is None:
            data = self.db.execute_query("SELECT * FROM sales")
        
        comparison_results = {}
        
        for strategy in strategies:
            try:
                results = strategy.analyze(data)
                comparison_results[strategy.get_analysis_name()] = results
            except Exception as e:
                comparison_results[strategy.get_analysis_name()] = {
                    'error': str(e)
                }
        
        return comparison_results


class AnalysisStrategyFactory:
    """
    Factory for creating analysis strategies.
    """
    
    _strategies = {
        'revenue': RevenueAnalysisStrategy,
        'quantity': QuantityAnalysisStrategy,
        'customer_behavior': CustomerBehaviorAnalysisStrategy,
        'product_performance': ProductPerformanceAnalysisStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_type: str) -> AnalysisStrategy:
        """
        Create an analysis strategy by type.
        Args:
            strategy_type (str): Type of strategy to create.
        Returns:
            AnalysisStrategy: Created strategy instance.
        Raises:
            ValueError: If strategy type is not supported.
        """
        if strategy_type not in cls._strategies:
            raise ValueError(f"Unsupported strategy type: {strategy_type}")
        
        strategy_class = cls._strategies[strategy_type]
        return strategy_class()
    
    @classmethod
    def get_available_strategies(cls) -> List[str]:
        """
        Get list of available strategy types.
        Returns:
            List[str]: Available strategy types.
        """
        return list(cls._strategies.keys()) 