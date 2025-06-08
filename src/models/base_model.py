from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd


class BaseModel(ABC):
    """
    BaseModel is an abstract base class that defines the interface for all data models in the system.
    It provides common functionality for data validation, transformation, and database operations.
    """

    def __init__(self):
        """
        Initialize the base model with default values.
        """
        self._data: Dict[str, Any] = {}

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the model's data according to business rules.
        
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model instance to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary containing the model's data.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """
        Create a model instance from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing the model's data.
            
        Returns:
            BaseModel: A new instance of the model.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'BaseModel':
        """
        Create a model instance from a pandas DataFrame row.
        
        Args:
            df (pd.DataFrame): DataFrame containing the model's data.
            
        Returns:
            BaseModel: A new instance of the model.
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the model.
        
        Returns:
            str: String representation of the model.
        """
        return f"{self.__class__.__name__}({self._data})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the model.
        
        Returns:
            str: Detailed string representation of the model.
        """
        return self.__str__() 