import os
from typing import Dict, Any
from dotenv import load_dotenv


class DatabaseConfig:
    """
    DatabaseConfig handles the configuration and connection settings for the database.
    It uses environment variables for sensitive information and provides a centralized
    way to manage database settings.
    """

    def __init__(self):
        """
        Initialize the database configuration by loading environment variables.
        """
        load_dotenv()
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load database configuration from environment variables.
        
        Returns:
            Dict[str, Any]: Dictionary containing database configuration.
        """
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'database': os.getenv('DB_NAME', 'sales_manager'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '12345678'),
        }

    @property
    def connection_string(self) -> str:
        """
        Get the database connection string.
        
        Returns:
            str: PostgreSQL connection string.
        """
        config = self._config
        return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the database configuration dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing database configuration.
        """
        return self._config.copy()

    def __str__(self) -> str:
        """
        String representation of the database configuration.
        
        Returns:
            str: String representation of the configuration.
        """
        config = self._config.copy()
        config['password'] = '****'  # Hide password in string representation
        return f"DatabaseConfig({config})" 