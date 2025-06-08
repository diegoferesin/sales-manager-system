"""
Database connection module implementing the Singleton pattern.
"""
from typing import Optional, Dict, Any, List
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import pandas as pd

class DatabaseConnection:
    """
    Singleton class for managing database connections.
    This class ensures only one database connection exists throughout the application.
    """
    _instance: Optional['DatabaseConnection'] = None
    _engine: Optional[Engine] = None
    _Session: Optional[sessionmaker] = None

    def __new__(cls) -> 'DatabaseConnection':
        """
        Create a new instance only if one doesn't exist.
        Returns:
            DatabaseConnection: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        Initialize the database connection.
        Loads environment variables and creates the SQLAlchemy engine.
        """
        load_dotenv()
        
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_name = os.getenv('DB_NAME')

        if not all([db_user, db_password, db_name]):
            raise ValueError("Missing required database configuration in .env file")

        connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        self._engine = create_engine(connection_string)
        self._Session = sessionmaker(bind=self._engine)

    def get_session(self) -> Session:
        """
        Get a new database session.
        Returns:
            Session: A new SQLAlchemy session.
        """
        if not self._Session:
            raise RuntimeError("Database connection not initialized")
        return self._Session()

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.
        Args:
            query (str): SQL query to execute.
            params (Dict[str, Any], optional): Parameters for the query.
        Returns:
            pd.DataFrame: Query results as a DataFrame.
        """
        if not self._engine:
            raise RuntimeError("Database connection not initialized")
        
        try:
            return pd.read_sql(text(query), self._engine, params=params)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {str(e)}")

    def execute_select(self, table: str, columns: List[str] = None, 
                      where_clause: str = None, order_by: str = None, 
                      limit: int = None) -> pd.DataFrame:
        """
        Execute a SELECT query with convenience parameters.
        Args:
            table (str): Table name to select from.
            columns (List[str], optional): Columns to select. If None, selects all.
            where_clause (str, optional): WHERE clause without the WHERE keyword.
            order_by (str, optional): ORDER BY clause without the ORDER BY keyword.
            limit (int, optional): Number of rows to limit.
        Returns:
            pd.DataFrame: Query results as a DataFrame.
        """
        # Build the query
        cols = "*" if not columns else ", ".join(columns)
        query = f"SELECT {cols} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query)

    def execute_aggregation(self, table: str, aggregations: Dict[str, str], 
                          group_by: List[str] = None, where_clause: str = None,
                          having_clause: str = None, order_by: str = None) -> pd.DataFrame:
        """
        Execute an aggregation query with convenience parameters.
        Args:
            table (str): Table name to query.
            aggregations (Dict[str, str]): Dictionary with alias: aggregation_function pairs.
            group_by (List[str], optional): Columns to group by.
            where_clause (str, optional): WHERE clause without the WHERE keyword.
            having_clause (str, optional): HAVING clause without the HAVING keyword.
            order_by (str, optional): ORDER BY clause without the ORDER BY keyword.
        Returns:
            pd.DataFrame: Query results as a DataFrame.
        """
        # Build aggregation part
        agg_parts = [f"{func} AS {alias}" for alias, func in aggregations.items()]
        
        # Build GROUP BY columns if provided
        if group_by:
            select_cols = ", ".join(group_by) + ", " + ", ".join(agg_parts)
        else:
            select_cols = ", ".join(agg_parts)
        
        query = f"SELECT {select_cols} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if group_by:
            query += f" GROUP BY {', '.join(group_by)}"
        
        if having_clause:
            query += f" HAVING {having_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        return self.execute_query(query)

    def execute_join_query(self, main_table: str, joins: List[Dict[str, str]], 
                          columns: List[str] = None, where_clause: str = None,
                          order_by: str = None, limit: int = None) -> pd.DataFrame:
        """
        Execute a JOIN query with convenience parameters.
        Args:
            main_table (str): Main table name.
            joins (List[Dict]): List of join specifications with keys: 'table', 'on', 'type'.
            columns (List[str], optional): Columns to select. If None, selects all.
            where_clause (str, optional): WHERE clause without the WHERE keyword.
            order_by (str, optional): ORDER BY clause without the ORDER BY keyword.
            limit (int, optional): Number of rows to limit.
        Returns:
            pd.DataFrame: Query results as a DataFrame.
        """
        cols = "*" if not columns else ", ".join(columns)
        query = f"SELECT {cols} FROM {main_table}"
        
        # Add joins
        for join in joins:
            join_type = join.get('type', 'INNER').upper()
            query += f" {join_type} JOIN {join['table']} ON {join['on']}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query)

    def execute_insert(self, table: str, data: Dict[str, Any]) -> bool:
        """
        Execute an INSERT query.
        Args:
            table (str): Table name to insert into.
            data (Dict[str, Any]): Dictionary with column: value pairs.
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with self._engine.connect() as conn:
                columns = ", ".join(data.keys())
                placeholders = ", ".join([f":{key}" for key in data.keys()])
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                conn.execute(text(query), data)
                conn.commit()
                return True
        except Exception as e:
            raise RuntimeError(f"Error executing insert: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test the database connection.
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            result = self.execute_query("SELECT 1 as test")
            return len(result) > 0 and result.iloc[0]['test'] == 1
        except Exception:
            return False

    def get_table_info(self, table: str) -> pd.DataFrame:
        """
        Get information about a table's structure.
        Args:
            table (str): Table name.
        Returns:
            pd.DataFrame: Table structure information.
        """
        query = f"DESCRIBE {table}"
        return self.execute_query(query)

    def close(self) -> None:
        """
        Close the database connection.
        """
        if self._engine:
            self._engine.dispose()
            self._instance = None 