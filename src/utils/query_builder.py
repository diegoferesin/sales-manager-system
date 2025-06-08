"""
Builder pattern implementation for constructing SQL queries.
"""
from typing import List, Dict, Any, Optional


class SQLQueryBuilder:
    """
    Builder class for constructing SQL queries in a fluent manner.
    This pattern solves the problem of complex query construction and makes
    the code more readable and maintainable.
    """
    
    def __init__(self):
        """
        Initialize the query builder.
        """
        self.reset()
    
    def reset(self) -> 'SQLQueryBuilder':
        """
        Reset the builder to initial state.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._select_fields: List[str] = []
        self._from_table: str = ""
        self._joins: List[str] = []
        self._where_conditions: List[str] = []
        self._group_by_fields: List[str] = []
        self._having_conditions: List[str] = []
        self._order_by_fields: List[str] = []
        self._limit_value: Optional[int] = None
        return self
    
    def select(self, fields: List[str]) -> 'SQLQueryBuilder':
        """
        Add SELECT fields to the query.
        Args:
            fields (List[str]): List of field names or expressions.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._select_fields.extend(fields)
        return self
    
    def select_field(self, field: str) -> 'SQLQueryBuilder':
        """
        Add a single SELECT field to the query.
        Args:
            field (str): Field name or expression.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._select_fields.append(field)
        return self
    
    def from_table(self, table: str) -> 'SQLQueryBuilder':
        """
        Set the FROM table.
        Args:
            table (str): Table name.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._from_table = table
        return self
    
    def inner_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        """
        Add an INNER JOIN to the query.
        Args:
            table (str): Table to join.
            on_condition (str): JOIN condition.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._joins.append(f"INNER JOIN {table} ON {on_condition}")
        return self
    
    def left_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        """
        Add a LEFT JOIN to the query.
        Args:
            table (str): Table to join.
            on_condition (str): JOIN condition.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._joins.append(f"LEFT JOIN {table} ON {on_condition}")
        return self
    
    def right_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        """
        Add a RIGHT JOIN to the query.
        Args:
            table (str): Table to join.
            on_condition (str): JOIN condition.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._joins.append(f"RIGHT JOIN {table} ON {on_condition}")
        return self
    
    def where(self, condition: str) -> 'SQLQueryBuilder':
        """
        Add a WHERE condition.
        Args:
            condition (str): WHERE condition.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._where_conditions.append(condition)
        return self
    
    def where_equals(self, field: str, value: Any) -> 'SQLQueryBuilder':
        """
        Add a WHERE equals condition.
        Args:
            field (str): Field name.
            value (Any): Value to compare.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        if isinstance(value, str):
            self._where_conditions.append(f"{field} = '{value}'")
        else:
            self._where_conditions.append(f"{field} = {value}")
        return self
    
    def where_in(self, field: str, values: List[Any]) -> 'SQLQueryBuilder':
        """
        Add a WHERE IN condition.
        Args:
            field (str): Field name.
            values (List[Any]): List of values.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        value_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in values])
        self._where_conditions.append(f"{field} IN ({value_str})")
        return self
    
    def where_between(self, field: str, start: Any, end: Any) -> 'SQLQueryBuilder':
        """
        Add a WHERE BETWEEN condition.
        Args:
            field (str): Field name.
            start (Any): Start value.
            end (Any): End value.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        if isinstance(start, str):
            start_str = f"'{start}'"
            end_str = f"'{end}'"
        else:
            start_str = str(start)
            end_str = str(end)
        self._where_conditions.append(f"{field} BETWEEN {start_str} AND {end_str}")
        return self
    
    def group_by(self, fields: List[str]) -> 'SQLQueryBuilder':
        """
        Add GROUP BY fields.
        Args:
            fields (List[str]): List of field names.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._group_by_fields.extend(fields)
        return self
    
    def having(self, condition: str) -> 'SQLQueryBuilder':
        """
        Add a HAVING condition.
        Args:
            condition (str): HAVING condition.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._having_conditions.append(condition)
        return self
    
    def order_by(self, field: str, direction: str = "ASC") -> 'SQLQueryBuilder':
        """
        Add ORDER BY field.
        Args:
            field (str): Field name.
            direction (str): Sort direction (ASC or DESC).
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._order_by_fields.append(f"{field} {direction.upper()}")
        return self
    
    def limit(self, count: int) -> 'SQLQueryBuilder':
        """
        Add LIMIT clause.
        Args:
            count (int): Number of rows to limit.
        Returns:
            SQLQueryBuilder: Self for method chaining.
        """
        self._limit_value = count
        return self
    
    def build(self) -> str:
        """
        Build the final SQL query string.
        Returns:
            str: Complete SQL query.
        Raises:
            ValueError: If required parts are missing.
        """
        if not self._select_fields:
            raise ValueError("SELECT fields are required")
        if not self._from_table:
            raise ValueError("FROM table is required")
        
        # Build SELECT clause
        select_clause = "SELECT " + ", ".join(self._select_fields)
        
        # Build FROM clause
        from_clause = f"FROM {self._from_table}"
        
        # Build query parts
        query_parts = [select_clause, from_clause]
        
        # Add JOINs
        if self._joins:
            query_parts.extend(self._joins)
        
        # Add WHERE
        if self._where_conditions:
            where_clause = "WHERE " + " AND ".join(self._where_conditions)
            query_parts.append(where_clause)
        
        # Add GROUP BY
        if self._group_by_fields:
            group_by_clause = "GROUP BY " + ", ".join(self._group_by_fields)
            query_parts.append(group_by_clause)
        
        # Add HAVING
        if self._having_conditions:
            having_clause = "HAVING " + " AND ".join(self._having_conditions)
            query_parts.append(having_clause)
        
        # Add ORDER BY
        if self._order_by_fields:
            order_by_clause = "ORDER BY " + ", ".join(self._order_by_fields)
            query_parts.append(order_by_clause)
        
        # Add LIMIT
        if self._limit_value:
            limit_clause = f"LIMIT {self._limit_value}"
            query_parts.append(limit_clause)
        
        return "\n".join(query_parts)


class QueryBuilderDirector:
    """
    Director class that provides preset query patterns.
    This provides common query patterns that can be reused.
    """
    
    def __init__(self, builder: SQLQueryBuilder):
        """
        Initialize the director with a builder.
        Args:
            builder (SQLQueryBuilder): The query builder to use.
        """
        self.builder = builder
    
    def build_sales_summary_by_category(self) -> str:
        """
        Build a sales summary by category query.
        Returns:
            str: SQL query for sales summary by category.
        """
        return (self.builder
                .reset()
                .select([
                    "c.category_name",
                    "COUNT(s.sale_id) as total_sales",
                    "SUM(s.total_price) as total_revenue",
                    "AVG(s.total_price) as avg_sale_amount"
                ])
                .from_table("sales s")
                .inner_join("products p", "s.product_id = p.product_id")
                .inner_join("categories c", "p.category_id = c.category_id")
                .group_by(["c.category_name"])
                .order_by("total_revenue", "DESC")
                .build())
    
    def build_top_customers(self, limit: int = 10) -> str:
        """
        Build a top customers query.
        Args:
            limit (int): Number of top customers to return.
        Returns:
            str: SQL query for top customers.
        """
        return (self.builder
                .reset()
                .select([
                    "CONCAT(c.first_name, ' ', c.last_name) as customer_name",
                    "COUNT(s.sale_id) as total_purchases",
                    "SUM(s.total_price) as total_spent"
                ])
                .from_table("sales s")
                .inner_join("customers c", "s.customer_id = c.customer_id")
                .group_by(["c.customer_id", "c.first_name", "c.last_name"])
                .order_by("total_spent", "DESC")
                .limit(limit)
                .build())
    
    def build_monthly_sales_trend(self, year: int) -> str:
        """
        Build a monthly sales trend query.
        Args:
            year (int): Year to analyze.
        Returns:
            str: SQL query for monthly sales trend.
        """
        return (self.builder
                .reset()
                .select([
                    "MONTH(sale_date) as month",
                    "MONTHNAME(sale_date) as month_name",
                    "COUNT(sale_id) as total_sales",
                    "SUM(total_price) as total_revenue"
                ])
                .from_table("sales")
                .where(f"YEAR(sale_date) = {year}")
                .group_by(["MONTH(sale_date)", "MONTHNAME(sale_date)"])
                .order_by("month", "ASC")
                .build()) 