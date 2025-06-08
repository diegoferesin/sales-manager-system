"""
Examples of how to use the DatabaseConnection class for SQL queries.
"""
from .connection import DatabaseConnection
import pandas as pd

class QueryExamples:
    """
    Class containing example queries using the DatabaseConnection methods.
    """
    
    def __init__(self):
        """
        Initialize with database connection.
        """
        self.db = DatabaseConnection()
    
    def get_sales_summary(self) -> pd.DataFrame:
        """
        Get a summary of sales by category.
        Returns:
            pd.DataFrame: Sales summary by category.
        """
        joins = [
            {'table': 'products p', 'on': 's.product_id = p.product_id'},
            {'table': 'categories c', 'on': 'p.category_id = c.category_id'}
        ]
        
        columns = [
            'c.category_name',
            'COUNT(s.sale_id) as total_sales',
            'SUM(s.total_price) as total_revenue',
            'AVG(s.total_price) as avg_sale_amount'
        ]
        
        return self.db.execute_join_query(
            main_table='sales s',
            joins=joins,
            columns=columns,
            order_by='total_revenue DESC'
        )
    
    def get_top_products(self, limit: int = 10) -> pd.DataFrame:
        """
        Get top selling products.
        Args:
            limit (int): Number of top products to return.
        Returns:
            pd.DataFrame: Top selling products.
        """
        aggregations = {
            'total_quantity': 'SUM(s.quantity)',
            'total_revenue': 'SUM(s.total_price)',
            'sales_count': 'COUNT(s.sale_id)'
        }
        
        joins = [
            {'table': 'products p', 'on': 's.product_id = p.product_id'}
        ]
        
        columns = [
            'p.product_name',
            'SUM(s.quantity) as total_quantity',
            'SUM(s.total_price) as total_revenue',
            'COUNT(s.sale_id) as sales_count'
        ]
        
        return self.db.execute_join_query(
            main_table='sales s',
            joins=joins,
            columns=columns,
            order_by='total_revenue DESC',
            limit=limit
        )
    
    def get_employee_performance(self) -> pd.DataFrame:
        """
        Get employee sales performance.
        Returns:
            pd.DataFrame: Employee performance data.
        """
        joins = [
            {'table': 'employees e', 'on': 's.sales_person_id = e.employee_id'}
        ]
        
        columns = [
            'CONCAT(e.first_name, " ", e.last_name) as employee_name',
            'COUNT(s.sale_id) as total_sales',
            'SUM(s.total_price) as total_revenue',
            'AVG(s.total_price) as avg_sale_amount'
        ]
        
        return self.db.execute_join_query(
            main_table='sales s',
            joins=joins,
            columns=columns,
            order_by='total_revenue DESC'
        )
    
    def get_monthly_sales_trend(self, year: int = 2023) -> pd.DataFrame:
        """
        Get monthly sales trend for a specific year.
        Args:
            year (int): Year to analyze.
        Returns:
            pd.DataFrame: Monthly sales trend.
        """
        query = """
        SELECT 
            MONTH(sale_date) as month,
            MONTHNAME(sale_date) as month_name,
            COUNT(sale_id) as total_sales,
            SUM(total_price) as total_revenue,
            AVG(total_price) as avg_sale_amount
        FROM sales 
        WHERE YEAR(sale_date) = :year
        GROUP BY MONTH(sale_date), MONTHNAME(sale_date)
        ORDER BY month
        """
        
        return self.db.execute_query(query, {'year': year})
    
    def get_customer_analysis(self) -> pd.DataFrame:
        """
        Get customer analysis with purchase behavior.
        Returns:
            pd.DataFrame: Customer analysis data.
        """
        joins = [
            {'table': 'customers c', 'on': 's.customer_id = c.customer_id'},
            {'table': 'cities ci', 'on': 'c.city_id = ci.city_id'}
        ]
        
        columns = [
            'CONCAT(c.first_name, " ", c.last_name) as customer_name',
            'ci.city_name',
            'COUNT(s.sale_id) as total_purchases',
            'SUM(s.total_price) as total_spent',
            'AVG(s.total_price) as avg_purchase_amount',
            'MAX(s.sale_date) as last_purchase_date'
        ]
        
        return self.db.execute_join_query(
            main_table='sales s',
            joins=joins,
            columns=columns,
            where_clause='s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)',
            order_by='total_spent DESC'
        )
    
    def get_product_category_performance(self) -> pd.DataFrame:
        """
        Get detailed product category performance.
        Returns:
            pd.DataFrame: Category performance with product details.
        """
        query = """
        SELECT 
            c.category_name,
            COUNT(DISTINCT p.product_id) as products_in_category,
            COUNT(s.sale_id) as total_sales,
            SUM(s.quantity) as total_quantity_sold,
            SUM(s.total_price) as total_revenue,
            AVG(s.total_price) as avg_sale_amount,
            MAX(s.sale_date) as last_sale_date
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        LEFT JOIN sales s ON p.product_id = s.product_id
        GROUP BY c.category_id, c.category_name
        ORDER BY total_revenue DESC
        """
        
        return self.db.execute_query(query)
    
    def test_all_methods(self) -> dict:
        """
        Test all query methods and return results.
        Returns:
            dict: Dictionary containing all query results.
        """
        results = {}
        
        try:
            results['connection_test'] = self.db.test_connection()
            results['sales_summary'] = self.get_sales_summary()
            results['top_products'] = self.get_top_products(5)
            results['employee_performance'] = self.get_employee_performance()
            results['monthly_trend'] = self.get_monthly_sales_trend()
            results['customer_analysis'] = self.get_customer_analysis()
            results['category_performance'] = self.get_product_category_performance()
            
        except Exception as e:
            results['error'] = str(e)
        
        return results 