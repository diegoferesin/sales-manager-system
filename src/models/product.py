from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class Product(BaseModel):
    """
    Product represents a product entity in the system, containing information about items available for sale.
    """
    def __init__(self, product_id: int = None, product_name: str = None, price: float = None, 
                 category_id: int = None, class_type: str = None, modify_date: str = None,
                 resistant: str = None, is_allergic: str = None, vitality_days: int = None):
        """
        Initialize a Product instance.
        Args:
            product_id (int, optional): Unique identifier for the product.
            product_name (str, optional): Name of the product.
            price (float, optional): Price of the product.
            category_id (int, optional): Identifier for the product's category.
            class_type (str, optional): Classification of the product (Low/Medium/High).
            modify_date (str, optional): Date of last modification.
            resistant (str, optional): Durability classification (Durable/Weak/Unknown).
            is_allergic (str, optional): Allergy indicator (TRUE/FALSE/Unknown).
            vitality_days (int, optional): Number of days the product remains fresh.
        """
        super().__init__()
        self._data = {
            'product_id': product_id,
            'product_name': product_name,
            'price': price,
            'category_id': category_id,
            'class_type': class_type,
            'modify_date': modify_date,
            'resistant': resistant,
            'is_allergic': is_allergic,
            'vitality_days': vitality_days
        }

    def validate(self) -> bool:
        """
        Validate the product data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['product_name']:
            return False
        if self._data['price'] is not None and not isinstance(self._data['price'], (int, float)):
            return False
        if self._data['category_id'] is not None and not isinstance(self._data['category_id'], int):
            return False
        if self._data['class_type'] is not None and self._data['class_type'] not in ['Low', 'Medium', 'High']:
            return False
        if self._data['resistant'] is not None and self._data['resistant'] not in ['Durable', 'Weak', 'Unknown']:
            return False
        if self._data['is_allergic'] is not None and self._data['is_allergic'] not in ['TRUE', 'FALSE', 'Unknown']:
            return False
        if self._data['vitality_days'] is not None and not isinstance(self._data['vitality_days'], int):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the product's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """
        Create a Product instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the product's data.
        Returns:
            Product: A new Product instance.
        """
        return cls(
            product_id=data.get('product_id'),
            product_name=data.get('product_name'),
            price=data.get('price'),
            category_id=data.get('category_id'),
            class_type=data.get('class_type'),
            modify_date=data.get('modify_date'),
            resistant=data.get('resistant'),
            is_allergic=data.get('is_allergic'),
            vitality_days=data.get('vitality_days')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Product':
        """
        Create a Product instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the product's data.
        Returns:
            Product: A new Product instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        product_id = df.get('ProductID', df.get('product_id', [None]))[0]
        product_name = df.get('ProductName', df.get('product_name', [None]))[0]
        price = df.get('Price', df.get('price', [None]))[0]
        category_id = df.get('CategoryID', df.get('category_id', [None]))[0]
        class_type = df.get('Class', df.get('class_type', [None]))[0]
        modify_date = df.get('ModifyDate', df.get('modify_date', [None]))[0]
        resistant = df.get('Resistant', df.get('resistant', [None]))[0]
        is_allergic = df.get('IsAllergic', df.get('is_allergic', [None]))[0]
        vitality_days = df.get('VitalityDays', df.get('vitality_days', [None]))[0]
        
        return cls(
            product_id=product_id,
            product_name=product_name,
            price=price,
            category_id=category_id,
            class_type=class_type,
            modify_date=modify_date,
            resistant=resistant,
            is_allergic=is_allergic,
            vitality_days=vitality_days
        )

    @property
    def product_id(self) -> int:
        """
        Get the product ID.
        Returns:
            int: The product ID.
        """
        return self._data['product_id']

    @property
    def product_name(self) -> str:
        """
        Get the product name.
        Returns:
            str: The product name.
        """
        return self._data['product_name']

    @property
    def price(self) -> float:
        """
        Get the product price.
        Returns:
            float: The product price.
        """
        return self._data['price']

    @property
    def category_id(self) -> int:
        """
        Get the category ID.
        Returns:
            int: The category ID.
        """
        return self._data['category_id']

    @property
    def class_type(self) -> str:
        """
        Get the product class.
        Returns:
            str: The product class (Low/Medium/High).
        """
        return self._data['class_type']

    @property
    def modify_date(self) -> str:
        """
        Get the modification date.
        Returns:
            str: The modification date.
        """
        return self._data['modify_date']

    @property
    def resistant(self) -> str:
        """
        Get the resistance classification.
        Returns:
            str: The resistance classification (Durable/Weak/Unknown).
        """
        return self._data['resistant']

    @property
    def is_allergic(self) -> str:
        """
        Get the allergy indicator.
        Returns:
            str: The allergy indicator (TRUE/FALSE/Unknown).
        """
        return self._data['is_allergic']

    @property
    def vitality_days(self) -> int:
        """
        Get the vitality days.
        Returns:
            int: The number of days the product remains fresh.
        """
        return self._data['vitality_days'] 