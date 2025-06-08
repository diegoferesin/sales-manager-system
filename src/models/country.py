from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class Country(BaseModel):
    """
    Country represents a country entity in the system, containing metadata and reference information.
    """
    def __init__(self, country_id: int = None, country_name: str = None, country_code: str = None):
        """
        Initialize a Country instance.
        Args:
            country_id (int, optional): Unique identifier for the country.
            country_name (str, optional): Name of the country.
            country_code (str, optional): Country code (e.g., ISO code).
        """
        super().__init__()
        self._data = {
            'country_id': country_id,
            'country_name': country_name,
            'country_code': country_code
        }

    def validate(self) -> bool:
        """
        Validate the country data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['country_name'] or not self._data['country_code']:
            return False
        if len(self._data['country_code']) != 2:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the country instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the country's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Country':
        """
        Create a Country instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the country's data.
        Returns:
            Country: A new Country instance.
        """
        return cls(
            country_id=data.get('country_id'),
            country_name=data.get('country_name'),
            country_code=data.get('country_code')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Country':
        """
        Create a Country instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the country's data.
        Returns:
            Country: A new Country instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        country_id = df.get('CountryID', df.get('country_id', [None]))[0]
        country_name = df.get('CountryName', df.get('country_name', [None]))[0]
        country_code = df.get('CountryCode', df.get('country_code', [None]))[0]
        
        return cls(
            country_id=country_id,
            country_name=country_name,
            country_code=country_code
        )

    @property
    def country_id(self) -> int:
        """
        Get the country ID.
        Returns:
            int: The country ID.
        """
        return self._data['country_id']

    @property
    def country_name(self) -> str:
        """
        Get the country name.
        Returns:
            str: The country name.
        """
        return self._data['country_name']

    @property
    def country_code(self) -> str:
        """
        Get the country code.
        Returns:
            str: The country code.
        """
        return self._data['country_code'] 