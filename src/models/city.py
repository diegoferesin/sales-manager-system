from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class City(BaseModel):
    """
    City represents a city entity in the system, containing geographic and reference information.
    """
    def __init__(self, city_id: int = None, city_name: str = None, zip_code: str = None, country_id: int = None):
        """
        Initialize a City instance.
        Args:
            city_id (int, optional): Unique identifier for the city.
            city_name (str, optional): Name of the city.
            zip_code (str, optional): ZIP code of the city.
            country_id (int, optional): Identifier for the country this city belongs to.
        """
        super().__init__()
        self._data = {
            'city_id': city_id,
            'city_name': city_name,
            'zip_code': zip_code,
            'country_id': country_id
        }

    def validate(self) -> bool:
        """
        Validate the city data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['city_name'] or not isinstance(self._data['country_id'], int):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the city instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the city's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'City':
        """
        Create a City instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the city's data.
        Returns:
            City: A new City instance.
        """
        return cls(
            city_id=data.get('city_id'),
            city_name=data.get('city_name'),
            zip_code=data.get('zip_code'),
            country_id=data.get('country_id')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'City':
        """
        Create a City instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the city's data.
        Returns:
            City: A new City instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        city_id = df.get('CityID', df.get('city_id', [None]))[0]
        city_name = df.get('CityName', df.get('city_name', [None]))[0]
        zip_code = df.get('Zipcode', df.get('zip_code', [None]))[0]
        country_id = df.get('CountryID', df.get('country_id', [None]))[0]
        
        return cls(
            city_id=city_id,
            city_name=city_name,
            zip_code=zip_code,
            country_id=country_id
        )

    @property
    def city_id(self) -> int:
        """
        Get the city ID.
        Returns:
            int: The city ID.
        """
        return self._data['city_id']

    @property
    def city_name(self) -> str:
        """
        Get the city name.
        Returns:
            str: The city name.
        """
        return self._data['city_name']

    @property
    def zip_code(self) -> str:
        """
        Get the city's ZIP code.
        Returns:
            str: The ZIP code.
        """
        return self._data['zip_code']

    @property
    def country_id(self) -> int:
        """
        Get the country ID.
        Returns:
            int: The country ID.
        """
        return self._data['country_id'] 