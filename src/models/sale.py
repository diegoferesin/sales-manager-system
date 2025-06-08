from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class Sale(BaseModel):
    """
    Sale represents a sales transaction in the system, containing information about products sold and transaction details.
    """
    def __init__(self, sale_id: int = None, sales_person_id: int = None, customer_id: int = None, 
                 product_id: int = None, quantity: int = None, discount: float = None, 
                 total_price: float = None, sale_date: str = None, transaction_number: str = None):
        """
        Initialize a Sale instance.
        Args:
            sale_id (int, optional): Unique identifier for the sale.
            sales_person_id (int, optional): Identifier for the employee who processed the sale.
            customer_id (int, optional): Identifier for the customer who made the purchase.
            product_id (int, optional): Identifier for the product sold.
            quantity (int, optional): Number of units sold.
            discount (float, optional): Discount applied to the sale.
            total_price (float, optional): Total price after discount.
            sale_date (str, optional): Date when the sale occurred.
            transaction_number (str, optional): Unique transaction identifier.
        """
        super().__init__()
        self._data = {
            'sale_id': sale_id,
            'sales_person_id': sales_person_id,
            'customer_id': customer_id,
            'product_id': product_id,
            'quantity': quantity,
            'discount': discount,
            'total_price': total_price,
            'sale_date': sale_date,
            'transaction_number': transaction_number
        }

    def validate(self) -> bool:
        """
        Validate the sale data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if self._data['quantity'] is not None and not isinstance(self._data['quantity'], int):
            return False
        if self._data['discount'] is not None and not isinstance(self._data['discount'], (int, float)):
            return False
        if self._data['total_price'] is not None and not isinstance(self._data['total_price'], (int, float)):
            return False
        if self._data['sales_person_id'] is not None and not isinstance(self._data['sales_person_id'], int):
            return False
        if self._data['customer_id'] is not None and not isinstance(self._data['customer_id'], int):
            return False
        if self._data['product_id'] is not None and not isinstance(self._data['product_id'], int):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the sale instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the sale's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sale':
        """
        Create a Sale instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the sale's data.
        Returns:
            Sale: A new Sale instance.
        """
        return cls(
            sale_id=data.get('sale_id'),
            sales_person_id=data.get('sales_person_id'),
            customer_id=data.get('customer_id'),
            product_id=data.get('product_id'),
            quantity=data.get('quantity'),
            discount=data.get('discount'),
            total_price=data.get('total_price'),
            sale_date=data.get('sale_date'),
            transaction_number=data.get('transaction_number')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Sale':
        """
        Create a Sale instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the sale's data.
        Returns:
            Sale: A new Sale instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        sale_id = df.get('SalesID', df.get('sale_id', [None]))[0]
        sales_person_id = df.get('SalesPersonID', df.get('sales_person_id', [None]))[0]
        customer_id = df.get('CustomerID', df.get('customer_id', [None]))[0]
        product_id = df.get('ProductID', df.get('product_id', [None]))[0]
        quantity = df.get('Quantity', df.get('quantity', [None]))[0]
        discount = df.get('Discount', df.get('discount', [None]))[0]
        total_price = df.get('TotalPrice', df.get('total_price', [None]))[0]
        sale_date = df.get('SalesDate', df.get('sale_date', [None]))[0]
        transaction_number = df.get('TransactionNumber', df.get('transaction_number', [None]))[0]
        
        return cls(
            sale_id=sale_id,
            sales_person_id=sales_person_id,
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            discount=discount,
            total_price=total_price,
            sale_date=sale_date,
            transaction_number=transaction_number
        )

    @property
    def sale_id(self) -> int:
        """
        Get the sale ID.
        Returns:
            int: The sale ID.
        """
        return self._data['sale_id']

    @property
    def sales_person_id(self) -> int:
        """
        Get the sales person ID.
        Returns:
            int: The sales person ID.
        """
        return self._data['sales_person_id']

    @property
    def customer_id(self) -> int:
        """
        Get the customer ID.
        Returns:
            int: The customer ID.
        """
        return self._data['customer_id']

    @property
    def product_id(self) -> int:
        """
        Get the product ID.
        Returns:
            int: The product ID.
        """
        return self._data['product_id']

    @property
    def quantity(self) -> int:
        """
        Get the quantity sold.
        Returns:
            int: The quantity sold.
        """
        return self._data['quantity']

    @property
    def discount(self) -> float:
        """
        Get the discount applied.
        Returns:
            float: The discount amount.
        """
        return self._data['discount']

    @property
    def total_price(self) -> float:
        """
        Get the total price after discount.
        Returns:
            float: The total price.
        """
        return self._data['total_price']

    @property
    def sale_date(self) -> str:
        """
        Get the sale date.
        Returns:
            str: The sale date.
        """
        return self._data['sale_date']

    @property
    def transaction_number(self) -> str:
        """
        Get the transaction number.
        Returns:
            str: The transaction number.
        """
        return self._data['transaction_number'] 