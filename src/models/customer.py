from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class Customer(BaseModel):
    """
    Customer represents a customer entity in the system, containing personal and contact information.
    """
    def __init__(self, customer_id: int = None, first_name: str = None, middle_initial: str = None, 
                 last_name: str = None, city_id: int = None, address: str = None):
        """
        Initialize a Customer instance.
        Args:
            customer_id (int, optional): Unique identifier for the customer.
            first_name (str, optional): First name of the customer.
            middle_initial (str, optional): Middle initial of the customer.
            last_name (str, optional): Last name of the customer.
            city_id (int, optional): Identifier for the city where the customer resides.
            address (str, optional): Customer's address.
        """
        super().__init__()
        self._data = {
            'customer_id': customer_id,
            'first_name': first_name,
            'middle_initial': middle_initial,
            'last_name': last_name,
            'city_id': city_id,
            'address': address
        }

    def validate(self) -> bool:
        """
        Validate the customer data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['first_name'] or not self._data['last_name']:
            return False
        if self._data['city_id'] is not None and not isinstance(self._data['city_id'], int):
            return False
        if self._data['middle_initial'] is not None and len(self._data['middle_initial']) > 5:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the customer instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the customer's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """
        Create a Customer instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the customer's data.
        Returns:
            Customer: A new Customer instance.
        """
        return cls(
            customer_id=data.get('customer_id'),
            first_name=data.get('first_name'),
            middle_initial=data.get('middle_initial'),
            last_name=data.get('last_name'),
            city_id=data.get('city_id'),
            address=data.get('address')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Customer':
        """
        Create a Customer instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the customer's data.
        Returns:
            Customer: A new Customer instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        customer_id = df.get('CustomerID', df.get('customer_id', [None]))[0]
        first_name = df.get('FirstName', df.get('first_name', [None]))[0]
        middle_initial = df.get('MiddleInitial', df.get('middle_initial', [None]))[0]
        last_name = df.get('LastName', df.get('last_name', [None]))[0]
        city_id = df.get('CityID', df.get('city_id', [None]))[0]
        address = df.get('Address', df.get('address', [None]))[0]
        
        return cls(
            customer_id=customer_id,
            first_name=first_name,
            middle_initial=middle_initial,
            last_name=last_name,
            city_id=city_id,
            address=address
        )

    @property
    def customer_id(self) -> int:
        """
        Get the customer ID.
        Returns:
            int: The customer ID.
        """
        return self._data['customer_id']

    @property
    def first_name(self) -> str:
        """
        Get the customer's first name.
        Returns:
            str: The first name.
        """
        return self._data['first_name']

    @property
    def middle_initial(self) -> str:
        """
        Get the customer's middle initial.
        Returns:
            str: The middle initial.
        """
        return self._data['middle_initial']

    @property
    def last_name(self) -> str:
        """
        Get the customer's last name.
        Returns:
            str: The last name.
        """
        return self._data['last_name']

    @property
    def city_id(self) -> int:
        """
        Get the city ID where the customer resides.
        Returns:
            int: The city ID.
        """
        return self._data['city_id']

    @property
    def address(self) -> str:
        """
        Get the customer's address.
        Returns:
            str: The address.
        """
        return self._data['address'] 