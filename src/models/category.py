from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel


class Category(BaseModel):
    """
    Category represents a product category in the system.
    It contains information about product categories and their relationships.
    """

    def __init__(self, category_id: int = None, category_name: str = None):
        """
        Initialize a Category instance.
        
        Args:
            category_id (int, optional): Unique identifier for the category.
            category_name (str, optional): Name of the category.
        """
        super().__init__()
        self._data = {
            'category_id': category_id,
            'category_name': category_name
        }

    def validate(self) -> bool:
        """
        Validate the category data.
        
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['category_name']:
            return False
        if self._data['category_id'] is not None and not isinstance(self._data['category_id'], int):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the category instance to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing the category's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Category':
        """
        Create a Category instance from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing the category's data.
            
        Returns:
            Category: A new Category instance.
        """
        return cls(
            category_id=data.get('category_id'),
            category_name=data.get('category_name')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Category':
        """
        Create a Category instance from a pandas DataFrame row.
        
        Args:
            df (pd.DataFrame): DataFrame containing the category's data.
            
        Returns:
            Category: A new Category instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        category_id = df.get('CategoryID', df.get('category_id', [None]))[0]
        category_name = df.get('CategoryName', df.get('category_name', [None]))[0]
        
        return cls(
            category_id=category_id,
            category_name=category_name
        )

    @property
    def category_id(self) -> int:
        """
        Get the category ID.
        
        Returns:
            int: The category ID.
        """
        return self._data['category_id']

    @property
    def category_name(self) -> str:
        """
        Get the category name.
        
        Returns:
            str: The category name.
        """
        return self._data['category_name'] 