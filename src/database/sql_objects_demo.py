"""
SQL Objects Demo Module

This module demonstrates the usage of advanced SQL objects:
- Functions
- Triggers
- Stored Procedures
- Views
- Indexes

Author: Sales Manager System
Date: 2024
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
import pandas as pd
from .connection import DatabaseConnection


class SQLObjectsDemo:
    """
    Demonstrates the usage of advanced SQL objects in the system.
    
    This class provides methods to execute and showcase the functionality
    of various SQL objects created for performance optimization and
    business process automation.
    """
    
    def __init__(self):
        """Initialize with database connection."""
        self.db = DatabaseConnection()
    
    def demo_customer_lifetime_value(self, customer_id: int, months: int = 12) -> float:
        """
        Demonstrate the customer lifetime value calculation function.
        
        Args:
            customer_id: ID of the customer to analyze
            months: Number of months to analyze
            
        Returns:
            float: Calculated customer lifetime value
        """
        query = """
        SELECT calculate_customer_lifetime_value(:customer_id, :months) as lifetime_value;
        """
        
        params = {
            'customer_id': customer_id,
            'months': months
        }
        
        result = self.db.execute_query(query, params)
        if isinstance(result, pd.DataFrame):
            return result['lifetime_value'].iloc[0] if not result.empty else 0.0
        return result[0]['lifetime_value'] if result else 0.0
    
    def demo_sales_report_procedure(self, 
                                  start_date: Optional[str] = None,
                                  end_date: Optional[str] = None,
                                  category_id: Optional[int] = None,
                                  include_details: bool = True) -> Dict[str, Any]:
        """
        Demonstrate the sales report stored procedure.
        
        Args:
            start_date: Start date for the report
            end_date: End date for the report
            category_id: Optional category filter
            include_details: Whether to include detailed results
            
        Returns:
            Dict containing summary and detailed results
        """
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Call the stored procedure
        query = """
        CALL generate_sales_report(:start_date, :end_date, :category_id, :include_details);
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'category_id': category_id,
            'include_details': include_details
        }
        
        # Execute the procedure
        results = self.db.execute_query(query, params)
        
        # Process results
        if isinstance(results, pd.DataFrame):
            if not results.empty:
                summary = results.iloc[0].to_dict()
                details = results.iloc[1:].to_dict('records') if len(results) > 1 else []
                return {'summary': summary, 'details': details}
        elif results:
            summary = results[0]
            details = results[1] if len(results) > 1 else []
            return {'summary': summary, 'details': details}
        
        return {'summary': {}, 'details': []}
    
    def demo_customer_purchase_history(self, 
                                     customer_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Demonstrate the customer purchase history view.
        
        Args:
            customer_id: Optional customer ID filter
            
        Returns:
            List of customer purchase history records
        """
        query = """
        SELECT * FROM customer_purchase_history
        WHERE (:customer_id IS NULL OR customer_id = :customer_id)
        ORDER BY total_spent DESC;
        """
        
        params = {'customer_id': customer_id}
        
        results = self.db.execute_query(query, params)
        if isinstance(results, pd.DataFrame):
            return results.to_dict('records')
        return results
    
    def demo_trigger_with_new_sale(self, 
                                 product_id: int,
                                 customer_id: int,
                                 sales_person_id: int,
                                 quantity: int,
                                 total_price: float,
                                 discount: float = 0.0) -> Dict[str, Any]:
        """
        Demonstrate the after_sale_insert trigger by inserting a new sale.
        
        Args:
            product_id: ID of the product sold
            customer_id: ID of the customer
            sales_person_id: ID of the sales person
            quantity: Number of items sold
            total_price: Total price of the sale
            discount: Discount amount
            
        Returns:
            Dict containing the inserted sale and triggered updates
        """
        # Insert new sale
        insert_query = """
        INSERT INTO sales (
            product_id, customer_id, sales_person_id,
            quantity, total_price, discount, sale_date,
            transaction_number
        ) VALUES (
            :product_id, :customer_id, :sales_person_id,
            :quantity, :total_price, :discount, CURDATE(),
            CONCAT('TRX', DATE_FORMAT(CURDATE(), '%Y%m%d'), LPAD(LAST_INSERT_ID(), 4, '0'))
        );
        """
        
        params = {
            'product_id': product_id,
            'customer_id': customer_id,
            'sales_person_id': sales_person_id,
            'quantity': quantity,
            'total_price': total_price,
            'discount': discount
        }
        
        # Execute insert
        self.db.execute_query(insert_query, params)
        
        # Get the inserted sale
        sale_query = """
        SELECT * FROM sales WHERE sale_id = LAST_INSERT_ID();
        """
        sale_result = self.db.execute_query(sale_query)
        sale = sale_result.iloc[0].to_dict() if isinstance(sale_result, pd.DataFrame) else sale_result[0]
        
        # Get the triggered updates
        product_query = """
        SELECT total_sales, total_revenue, last_sale_date 
        FROM products WHERE product_id = :product_id;
        """
        product_result = self.db.execute_query(product_query, {'product_id': product_id})
        product = product_result.iloc[0].to_dict() if isinstance(product_result, pd.DataFrame) else product_result[0]
        
        category_query = """
        SELECT c.total_sales, c.total_revenue, c.last_sale_date
        FROM categories c
        INNER JOIN products p ON c.category_id = p.category_id
        WHERE p.product_id = :product_id;
        """
        category_result = self.db.execute_query(category_query, {'product_id': product_id})
        category = category_result.iloc[0].to_dict() if isinstance(category_result, pd.DataFrame) else category_result[0]
        
        audit_query = """
        SELECT * FROM sales_audit_log 
        WHERE sale_id = :sale_id
        ORDER BY action_timestamp DESC
        LIMIT 1;
        """
        audit_result = self.db.execute_query(audit_query, {'sale_id': sale['sale_id']})
        audit = audit_result.iloc[0].to_dict() if isinstance(audit_result, pd.DataFrame) else audit_result[0]
        
        return {
            'sale': sale,
            'product_updates': product,
            'category_updates': category,
            'audit_log': audit
        }
    
    def demo_index_usage(self) -> Dict[str, Any]:
        """
        Demonstrate the usage of created indexes.
        
        Returns:
            Dict containing query execution plans
        """
        # Test sales date-product index
        sales_query = """
        EXPLAIN SELECT * FROM sales 
        WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        AND product_id IN (1, 2, 3);
        """
        sales_plan = self.db.execute_query(sales_query)
        if isinstance(sales_plan, pd.DataFrame):
            sales_plan = sales_plan.to_dict('records')
        
        # Test customer-city-country index
        customer_query = """
        EXPLAIN SELECT * FROM customers 
        WHERE city_id = 1
        ORDER BY customer_id;
        """
        customer_plan = self.db.execute_query(customer_query)
        if isinstance(customer_plan, pd.DataFrame):
            customer_plan = customer_plan.to_dict('records')
        
        # Test product category index
        product_query = """
        EXPLAIN SELECT * FROM products 
        WHERE category_id = 1;
        """
        product_plan = self.db.execute_query(product_query)
        if isinstance(product_plan, pd.DataFrame):
            product_plan = product_plan.to_dict('records')
        
        # Test full-text search index
        search_query = """
        EXPLAIN SELECT * FROM products 
        WHERE MATCH(product_name, class_type) 
        AGAINST('organic' IN BOOLEAN MODE);
        """
        search_plan = self.db.execute_query(search_query)
        if isinstance(search_plan, pd.DataFrame):
            search_plan = search_plan.to_dict('records')
        
        return {
            'sales_index_plan': sales_plan,
            'customer_index_plan': customer_plan,
            'product_index_plan': product_plan,
            'search_index_plan': search_plan
        }


def main():
    """
    Demonstrate the usage of all SQL objects.
    """
    print("=== SQL Objects Demo ===")
    
    demo = SQLObjectsDemo()
    
    try:
        # 1. Demo Customer Lifetime Value Function
        print("\n1. Customer Lifetime Value Function Demo...")
        customer_id = 1  # Example customer
        lifetime_value = demo.demo_customer_lifetime_value(customer_id)
        print(f"   Customer {customer_id} Lifetime Value: ${lifetime_value:.2f}")
        
        # 2. Demo Sales Report Procedure
        print("\n2. Sales Report Procedure Demo...")
        report = demo.demo_sales_report_procedure(
            start_date='2024-01-01',
            end_date='2024-03-31',
            include_details=True
        )
        print(f"   Total Revenue: ${report['summary']['total_revenue']:.2f}")
        print(f"   Total Transactions: {report['summary']['total_transactions']}")
        print(f"   Average Transaction Value: ${report['summary']['avg_transaction_value']:.2f}")
        
        # 3. Demo Customer Purchase History View
        print("\n3. Customer Purchase History View Demo...")
        history = demo.demo_customer_purchase_history()
        print(f"   Retrieved {len(history)} customer records")
        if history:
            print(f"   Top Customer: {history[0]['customer_name']}")
            print(f"   Total Spent: ${history[0]['total_spent']:.2f}")
        
        # 4. Demo Trigger with New Sale
        print("\n4. Trigger Demo with New Sale...")
        trigger_result = demo.demo_trigger_with_new_sale(
            product_id=1,
            customer_id=1,
            sales_person_id=1,
            quantity=2,
            total_price=100.00,
            discount=10.00
        )
        print("   Sale inserted successfully")
        print(f"   Product total sales updated to: {trigger_result['product_updates']['total_sales']}")
        print(f"   Audit log created with ID: {trigger_result['audit_log']['log_id']}")
        
        # 5. Demo Index Usage
        print("\n5. Index Usage Demo...")
        index_plans = demo.demo_index_usage()
        print("   Index execution plans retrieved successfully")
        for name, plan in index_plans.items():
            print(f"   {name}: {len(plan)} rows in plan")
        
        print("\n=== All SQL Objects Demo Completed Successfully! ===")
        
    except Exception as e:
        print(f"Error during SQL objects demo: {e}")


if __name__ == "__main__":
    main() 