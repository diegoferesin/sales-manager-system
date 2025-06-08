"""
Advanced SQL Queries Module

This module contains complex SQL queries using CTEs (Common Table Expressions) 
and Window Functions for advanced business analytics and reporting.

Author: Sales Manager System
Date: 2024
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date
import pandas as pd
from .connection import DatabaseConnection


class AdvancedSQLQueries:
    """
    Advanced SQL query executor with CTE and Window Functions support.
    
    This class provides methods to execute complex analytical queries
    that help in business decision making and performance optimization.
    """
    
    def __init__(self):
        """Initialize with database connection."""
        self.db = DatabaseConnection()
    
    def sales_performance_analysis_with_cte(self, 
                                          start_date: Optional[str] = None, 
                                          end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Advanced sales performance analysis using CTEs and window functions.
        
        This query uses:
        - CTE to aggregate sales data by salesperson and product category
        - Window functions to rank salespeople by performance
        - ROW_NUMBER() and RANK() for detailed ranking analysis
        
        Args:
            start_date (str, optional): Start date for analysis (YYYY-MM-DD)
            end_date (str, optional): End date for analysis (YYYY-MM-DD)
            
        Returns:
            List[Dict[str, Any]]: Query results with performance metrics
        """
        
        query = """
        WITH sales_summary AS (
            -- CTE 1: Aggregate sales data by salesperson and category
            SELECT 
                e.employee_id,
                CONCAT(e.first_name, ' ', e.last_name) as salesperson_name,
                c.category_name,
                COUNT(s.sale_id) as total_transactions,
                SUM(s.quantity) as total_quantity_sold,
                SUM(s.total_price) as total_revenue,
                AVG(s.total_price) as avg_transaction_value,
                SUM(s.discount) as total_discounts_given
            FROM sales s
            INNER JOIN employees e ON s.sales_person_id = e.employee_id
            INNER JOIN products p ON s.product_id = p.product_id
            INNER JOIN categories c ON p.category_id = c.category_id
            WHERE s.sale_date >= COALESCE(:start_date, DATE_SUB(CURDATE(), INTERVAL 1 YEAR))
              AND s.sale_date <= COALESCE(:end_date, CURDATE())
            GROUP BY e.employee_id, e.first_name, e.last_name, c.category_id, c.category_name
        ),
        performance_metrics AS (
            -- CTE 2: Calculate performance metrics and rankings
            SELECT 
                employee_id,
                salesperson_name,
                category_name,
                total_transactions,
                total_quantity_sold,
                total_revenue,
                avg_transaction_value,
                total_discounts_given,
                -- Window functions for ranking
                ROW_NUMBER() OVER (
                    PARTITION BY category_name 
                    ORDER BY total_revenue DESC
                ) as revenue_rank_in_category,
                RANK() OVER (
                    ORDER BY total_revenue DESC
                ) as overall_revenue_rank,
                DENSE_RANK() OVER (
                    PARTITION BY category_name 
                    ORDER BY total_transactions DESC
                ) as transactions_rank_in_category,
                -- Performance percentiles
                PERCENT_RANK() OVER (
                    ORDER BY total_revenue
                ) as revenue_percentile,
                -- Running totals
                SUM(total_revenue) OVER (
                    PARTITION BY employee_id 
                    ORDER BY total_revenue DESC 
                    ROWS UNBOUNDED PRECEDING
                ) as cumulative_revenue,
                -- Performance compared to category average
                AVG(total_revenue) OVER (
                    PARTITION BY category_name
                ) as category_avg_revenue
            FROM sales_summary
        )
        SELECT 
            pm.*,
            CASE 
                WHEN pm.total_revenue > pm.category_avg_revenue THEN 'Above Average'
                WHEN pm.total_revenue = pm.category_avg_revenue THEN 'Average'
                ELSE 'Below Average'
            END as performance_category,
            -- Calculate efficiency metrics
            ROUND(pm.total_revenue / NULLIF(pm.total_transactions, 0), 2) as revenue_per_transaction,
            ROUND(pm.total_quantity_sold / NULLIF(pm.total_transactions, 0), 2) as avg_items_per_transaction,
            ROUND((pm.total_discounts_given / NULLIF(pm.total_revenue, 0)) * 100, 2) as discount_percentage
        FROM performance_metrics pm
        ORDER BY pm.overall_revenue_rank, pm.category_name;
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        return self.db.execute_query(query, params)
    
    def customer_segmentation_with_window_functions(self, 
                                                  analysis_months: int = 12) -> List[Dict[str, Any]]:
        """
        Customer segmentation analysis using CTEs and advanced window functions.
        
        This query performs RFM (Recency, Frequency, Monetary) analysis using:
        - CTE for customer purchase behavior aggregation
        - Window functions for quartile calculations
        - LAG() function for trend analysis
        - NTILE() for customer segmentation
        
        Args:
            analysis_months (int): Number of months to analyze (default: 12)
            
        Returns:
            List[Dict[str, Any]]: Customer segmentation results
        """
        
        query = """
        WITH customer_metrics AS (
            -- CTE 1: Calculate RFM metrics for each customer
            SELECT 
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                c.gender,
                ci.city_name,
                co.country_name,
                -- Recency: Days since last purchase
                DATEDIFF(CURDATE(), MAX(s.sale_date)) as days_since_last_purchase,
                -- Frequency: Number of purchases
                COUNT(DISTINCT s.sale_id) as total_purchases,
                COUNT(DISTINCT s.product_id) as unique_products_bought,
                COUNT(DISTINCT DATE(s.sale_date)) as shopping_days,
                -- Monetary: Total spent
                SUM(s.total_price) as total_spent,
                AVG(s.total_price) as avg_purchase_value,
                SUM(s.quantity) as total_items_bought,
                -- Time-based metrics
                MIN(s.sale_date) as first_purchase_date,
                MAX(s.sale_date) as last_purchase_date,
                DATEDIFF(MAX(s.sale_date), MIN(s.sale_date)) as customer_lifetime_days
            FROM customers c
            INNER JOIN sales s ON c.customer_id = s.customer_id
            INNER JOIN cities ci ON c.city_id = ci.city_id
            INNER JOIN countries co ON ci.country_id = co.country_id
            WHERE s.sale_date >= DATE_SUB(CURDATE(), INTERVAL :analysis_months MONTH)
            GROUP BY c.customer_id, c.first_name, c.last_name, c.gender, 
                     ci.city_name, co.country_name
        ),
        customer_scores AS (
            -- CTE 2: Calculate RFM scores using window functions
            SELECT 
                cm.*,
                -- RFM Scoring using NTILE (quintiles)
                NTILE(5) OVER (ORDER BY days_since_last_purchase) as recency_score,
                NTILE(5) OVER (ORDER BY total_purchases DESC) as frequency_score,
                NTILE(5) OVER (ORDER BY total_spent DESC) as monetary_score,
                
                -- Percentile rankings
                PERCENT_RANK() OVER (ORDER BY total_spent DESC) as spending_percentile,
                PERCENT_RANK() OVER (ORDER BY total_purchases DESC) as frequency_percentile,
                
                -- Comparative metrics using window functions
                AVG(total_spent) OVER () as overall_avg_spent,
                AVG(total_purchases) OVER () as overall_avg_purchases,
                
                -- Customer lifetime value calculation
                CASE 
                    WHEN customer_lifetime_days > 0 
                    THEN ROUND(total_spent / (customer_lifetime_days / 30.44), 2)
                    ELSE total_spent
                END as monthly_value,
                
                -- Ranking within geographic segments
                ROW_NUMBER() OVER (
                    PARTITION BY country_name 
                    ORDER BY total_spent DESC
                ) as country_spending_rank,
                
                ROW_NUMBER() OVER (
                    PARTITION BY city_name 
                    ORDER BY total_spent DESC
                ) as city_spending_rank
            FROM customer_metrics cm
        ),
        segmented_customers AS (
            -- CTE 3: Create customer segments
            SELECT 
                cs.*,
                -- Create RFM segment
                CONCAT(
                    CAST(6 - recency_score AS CHAR), 
                    CAST(frequency_score AS CHAR), 
                    CAST(monetary_score AS CHAR)
                ) as rfm_segment,
                
                -- Business segment classification
                CASE 
                    WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 
                        THEN 'Champions'
                    WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 4 
                        THEN 'Loyal Customers'
                    WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score >= 3 
                        THEN 'Potential Loyalists'
                    WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score <= 2 
                        THEN 'New Customers'
                    WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 
                        THEN 'At Risk'
                    WHEN recency_score <= 2 AND frequency_score >= 4 AND monetary_score >= 4 
                        THEN 'Cannot Lose Them'
                    WHEN recency_score <= 3 AND frequency_score <= 2 AND monetary_score <= 2 
                        THEN 'Hibernating'
                    ELSE 'Others'
                END as customer_segment,
                
                -- Calculate customer value index
                ROUND(
                    (frequency_score * 0.3 + monetary_score * 0.5 + (6 - recency_score) * 0.2) 
                    / 5 * 100, 2
                ) as customer_value_index
            FROM customer_scores cs
        )
        SELECT 
            sc.*,
            -- Add segment statistics
            COUNT(*) OVER (PARTITION BY customer_segment) as segment_size,
            AVG(total_spent) OVER (PARTITION BY customer_segment) as segment_avg_spent,
            AVG(customer_value_index) OVER (PARTITION BY customer_segment) as segment_avg_value_index
        FROM segmented_customers sc
        ORDER BY customer_value_index DESC, total_spent DESC;
        """
        
        params = {'analysis_months': analysis_months}
        
        return self.db.execute_query(query, params)
    
    def product_performance_trends_with_cte(self, 
                                          category_id: Optional[int] = None,
                                          time_period: str = 'monthly') -> List[Dict[str, Any]]:
        """
        Product performance trend analysis using CTEs and window functions.
        
        This query analyzes product performance trends over time using:
        - CTEs for time-based aggregations  
        - LAG() and LEAD() for trend comparison
        - Moving averages using window functions
        - Growth rate calculations
        
        Args:
            category_id (int, optional): Filter by specific category
            time_period (str): Aggregation period ('daily', 'weekly', 'monthly')
            
        Returns:
            List[Dict[str, Any]]: Product performance trends
        """
        
        # Define date truncation based on time period
        date_trunc_map = {
            'daily': "DATE(s.sale_date)",
            'weekly': "DATE_FORMAT(s.sale_date, '%Y-%u')",
            'monthly': "DATE_FORMAT(s.sale_date, '%Y-%m')"
        }
        
        date_trunc = date_trunc_map.get(time_period, "DATE_FORMAT(s.sale_date, '%Y-%m')")
        
        query = f"""
        WITH time_series_sales AS (
            -- CTE 1: Aggregate sales by product and time period
            SELECT 
                p.product_id,
                p.product_name,
                c.category_name,
                p.price as current_price,
                {date_trunc} as time_period,
                COUNT(s.sale_id) as transactions,
                SUM(s.quantity) as units_sold,
                SUM(s.total_price) as revenue,
                AVG(s.total_price) as avg_transaction_value,
                COUNT(DISTINCT s.customer_id) as unique_customers,
                SUM(s.discount) as total_discounts
            FROM products p
            INNER JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN sales s ON p.product_id = s.product_id
            WHERE s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 18 MONTH)
              AND (:category_id IS NULL OR c.category_id = :category_id)
            GROUP BY p.product_id, p.product_name, c.category_name, p.price, time_period
        ),
        performance_trends AS (
            -- CTE 2: Calculate trends and moving averages
            SELECT 
                tss.*,
                -- Previous period comparisons using LAG
                LAG(revenue, 1) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period
                ) as previous_period_revenue,
                
                LAG(units_sold, 1) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period
                ) as previous_period_units,
                
                -- Next period using LEAD for forecasting validation
                LEAD(revenue, 1) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period
                ) as next_period_revenue,
                
                -- Moving averages (3-period)
                AVG(revenue) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period 
                    ROWS 2 PRECEDING
                ) as revenue_3period_ma,
                
                AVG(units_sold) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period 
                    ROWS 2 PRECEDING
                ) as units_3period_ma,
                
                -- Cumulative metrics
                SUM(revenue) OVER (
                    PARTITION BY product_id 
                    ORDER BY time_period 
                    ROWS UNBOUNDED PRECEDING
                ) as cumulative_revenue,
                
                -- Performance ranking within category
                ROW_NUMBER() OVER (
                    PARTITION BY category_name, time_period 
                    ORDER BY revenue DESC
                ) as category_revenue_rank,
                
                -- Overall ranking
                RANK() OVER (
                    PARTITION BY time_period 
                    ORDER BY revenue DESC
                ) as overall_revenue_rank,
                
                -- Performance percentile
                PERCENT_RANK() OVER (
                    PARTITION BY category_name, time_period 
                    ORDER BY revenue
                ) as category_performance_percentile
            FROM time_series_sales tss
        )
        SELECT 
            pt.*,
            -- Calculate growth rates
            CASE 
                WHEN previous_period_revenue IS NOT NULL AND previous_period_revenue > 0
                THEN ROUND(((revenue - previous_period_revenue) / previous_period_revenue) * 100, 2)
                ELSE NULL
            END as revenue_growth_rate,
            
            CASE 
                WHEN previous_period_units IS NOT NULL AND previous_period_units > 0
                THEN ROUND(((units_sold - previous_period_units) / CAST(previous_period_units AS DECIMAL)) * 100, 2)
                ELSE NULL
            END as units_growth_rate,
            
            -- Trend indicators
            CASE 
                WHEN revenue > revenue_3period_ma THEN 'Above Trend'
                WHEN revenue < revenue_3period_ma THEN 'Below Trend'
                ELSE 'On Trend'
            END as revenue_trend_indicator,
            
            -- Performance classification
            CASE 
                WHEN category_performance_percentile >= 0.8 THEN 'Top Performer'
                WHEN category_performance_percentile >= 0.6 THEN 'Good Performer'
                WHEN category_performance_percentile >= 0.4 THEN 'Average Performer'
                WHEN category_performance_percentile >= 0.2 THEN 'Poor Performer'
                ELSE 'Bottom Performer'
            END as performance_class,
            
            -- Calculate revenue per customer
            ROUND(revenue / NULLIF(unique_customers, 0), 2) as revenue_per_customer,
            
            -- Discount impact analysis
            ROUND((total_discounts / NULLIF(revenue, 0)) * 100, 2) as discount_rate_percent
        FROM performance_trends pt
        ORDER BY pt.product_id, pt.time_period;
        """
        
        params = {'category_id': category_id}
        
        return self.db.execute_query(query, params)
    
    def advanced_sales_analytics_dashboard(self, 
                                         date_range_days: int = 90) -> Dict[str, List[Dict[str, Any]]]:
        """
        Comprehensive analytics dashboard with multiple CTE-based queries.
        
        Returns a complete dashboard dataset combining multiple analyses:
        - Sales trends with moving averages
        - Top performers identification
        - Geographic performance analysis
        - Seasonal patterns analysis
        
        Args:
            date_range_days (int): Number of days to analyze
            
        Returns:
            Dict containing multiple analysis results
        """
        
        # Query 1: Sales Trends with Moving Averages
        trends_query = """
        WITH daily_sales AS (
            SELECT 
                DATE(s.sale_date) as sale_date,
                COUNT(s.sale_id) as daily_transactions,
                SUM(s.total_price) as daily_revenue,
                SUM(s.quantity) as daily_units,
                COUNT(DISTINCT s.customer_id) as daily_customers,
                AVG(s.total_price) as daily_avg_transaction
            FROM sales s
            WHERE s.sale_date >= DATE_SUB(CURDATE(), INTERVAL :date_range_days DAY)
            GROUP BY DATE(s.sale_date)
        )
        SELECT 
            ds.*,
            AVG(daily_revenue) OVER (
                ORDER BY sale_date 
                ROWS 6 PRECEDING
            ) as revenue_7day_ma,
            AVG(daily_transactions) OVER (
                ORDER BY sale_date 
                ROWS 6 PRECEDING
            ) as transactions_7day_ma,
            LAG(daily_revenue, 7) OVER (ORDER BY sale_date) as revenue_7days_ago,
            ROW_NUMBER() OVER (ORDER BY daily_revenue DESC) as revenue_rank
        FROM daily_sales ds
        ORDER BY sale_date;
        """
        
        # Query 2: Geographic Performance
        geographic_query = """
        WITH geo_performance AS (
            SELECT 
                co.country_name,
                ci.city_name,
                COUNT(s.sale_id) as total_sales,
                SUM(s.total_price) as total_revenue,
                COUNT(DISTINCT s.customer_id) as unique_customers,
                AVG(s.total_price) as avg_transaction_value
            FROM sales s
            INNER JOIN customers c ON s.customer_id = c.customer_id
            INNER JOIN cities ci ON c.city_id = ci.city_id
            INNER JOIN countries co ON ci.country_id = co.country_id
            WHERE s.sale_date >= DATE_SUB(CURDATE(), INTERVAL :date_range_days DAY)
            GROUP BY co.country_name, ci.city_name
        )
        SELECT 
            gp.*,
            RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank,
            PERCENT_RANK() OVER (ORDER BY total_revenue) as revenue_percentile,
            ROUND(total_revenue / NULLIF(unique_customers, 0), 2) as revenue_per_customer
        FROM geo_performance gp
        ORDER BY total_revenue DESC;
        """
        
        params = {'date_range_days': date_range_days}
        
        # Execute all queries
        results = {
            'sales_trends': self.db.execute_query(trends_query, params),
            'geographic_performance': self.db.execute_query(geographic_query, params)
        }
        
        return results
    
    def export_results_to_dataframe(self, 
                                   query_results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert query results to pandas DataFrame for further analysis.
        
        Args:
            query_results: Results from any of the advanced queries
            
        Returns:
            pd.DataFrame: Formatted DataFrame with proper data types
        """
        if not query_results:
            return pd.DataFrame()
        
        df = pd.DataFrame(query_results)
        
        # Convert date columns
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = [col for col in df.columns if any(keyword in col.lower() 
                          for keyword in ['price', 'revenue', 'total', 'avg', 'rate', 'score', 'rank'])]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df


def main():
    """
    Demonstration of advanced SQL queries execution.
    """
    print("=== Advanced SQL Queries Demo ===")
    
    # Initialize advanced queries
    advanced_queries = AdvancedSQLQueries()
    
    try:
        # Demo 1: Sales Performance Analysis
        print("\n1. Sales Performance Analysis with CTEs...")
        performance_results = advanced_queries.sales_performance_analysis_with_cte()
        print(f"   Retrieved {len(performance_results)} performance records")
        
        # Demo 2: Customer Segmentation
        print("\n2. Customer Segmentation Analysis...")
        segmentation_results = advanced_queries.customer_segmentation_with_window_functions()
        print(f"   Analyzed {len(segmentation_results)} customers")
        
        # Demo 3: Product Trends
        print("\n3. Product Performance Trends...")
        trends_results = advanced_queries.product_performance_trends_with_cte()
        print(f"   Analyzed {len(trends_results)} product-period combinations")
        
        # Demo 4: Dashboard Analytics
        print("\n4. Advanced Analytics Dashboard...")
        dashboard_results = advanced_queries.advanced_sales_analytics_dashboard()
        for key, results in dashboard_results.items():
            print(f"   {key}: {len(results)} records")
        
        print("\n=== All Advanced Queries Executed Successfully! ===")
        
    except Exception as e:
        print(f"Error executing advanced queries: {e}")


if __name__ == "__main__":
    main() 