"""
Factory Method pattern implementation for creating model instances.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Type
import pandas as pd

from ..models.category import Category
from ..models.city import City
from ..models.country import Country
from ..models.customer import Customer
from ..models.employee import Employee
from ..models.product import Product
from ..models.sale import Sale
from ..models.base_model import BaseModel


class ModelFactory(ABC):
    """
    Abstract factory class for creating model instances.
    This pattern solves the problem of object creation complexity and allows
    for easy extension when new model types are added.
    """
    
    @abstractmethod
    def create_model(self, data: Dict[str, Any]) -> BaseModel:
        """
        Create a model instance from data.
        Args:
            data (Dict[str, Any]): Data dictionary to create model from.
        Returns:
            BaseModel: Created model instance.
        """
        pass

    @abstractmethod
    def create_from_dataframe(self, df: pd.DataFrame) -> BaseModel:
        """
        Create a model instance from a DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing model data.
        Returns:
            BaseModel: Created model instance.
        """
        pass


class CategoryFactory(ModelFactory):
    """
    Factory for creating Category model instances.
    """
    
    def create_model(self, data: Dict[str, Any]) -> Category:
        """
        Create a Category instance from data.
        Args:
            data (Dict[str, Any]): Category data dictionary.
        Returns:
            Category: Created Category instance.
        """
        return Category.from_dict(data)
    
    def create_from_dataframe(self, df: pd.DataFrame) -> Category:
        """
        Create a Category instance from a DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing category data.
        Returns:
            Category: Created Category instance.
        """
        return Category.from_dataframe(df)


class ProductFactory(ModelFactory):
    """
    Factory for creating Product model instances.
    """
    
    def create_model(self, data: Dict[str, Any]) -> Product:
        """
        Create a Product instance from data.
        Args:
            data (Dict[str, Any]): Product data dictionary.
        Returns:
            Product: Created Product instance.
        """
        return Product.from_dict(data)
    
    def create_from_dataframe(self, df: pd.DataFrame) -> Product:
        """
        Create a Product instance from a DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing product data.
        Returns:
            Product: Created Product instance.
        """
        return Product.from_dataframe(df)


class SaleFactory(ModelFactory):
    """
    Factory for creating Sale model instances.
    """
    
    def create_model(self, data: Dict[str, Any]) -> Sale:
        """
        Create a Sale instance from data.
        Args:
            data (Dict[str, Any]): Sale data dictionary.
        Returns:
            Sale: Created Sale instance.
        """
        return Sale.from_dict(data)
    
    def create_from_dataframe(self, df: pd.DataFrame) -> Sale:
        """
        Create a Sale instance from a DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing sale data.
        Returns:
            Sale: Created Sale instance.
        """
        return Sale.from_dataframe(df)


class ModelFactoryRegistry:
    """
    Registry that manages different model factories.
    This solves the problem of having to know which specific factory to use
    and provides a unified interface for model creation.
    """
    
    _factories: Dict[str, Type[ModelFactory]] = {
        'category': CategoryFactory,
        'product': ProductFactory,
        'sale': SaleFactory,
        'city': ModelFactory,  # Could be expanded with specific factories
        'country': ModelFactory,
        'customer': ModelFactory,
        'employee': ModelFactory,
    }
    
    @classmethod
    def get_factory(cls, model_type: str) -> ModelFactory:
        """
        Get the appropriate factory for a model type.
        Args:
            model_type (str): Type of model ('category', 'product', 'sale', etc.)
        Returns:
            ModelFactory: Factory instance for the model type.
        Raises:
            ValueError: If model type is not supported.
        """
        if model_type not in cls._factories:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        factory_class = cls._factories[model_type]
        return factory_class()
    
    @classmethod
    def create_model(cls, model_type: str, data: Dict[str, Any]) -> BaseModel:
        """
        Create a model instance using the appropriate factory.
        Args:
            model_type (str): Type of model to create.
            data (Dict[str, Any]): Data for the model.
        Returns:
            BaseModel: Created model instance.
        """
        factory = cls.get_factory(model_type)
        return factory.create_model(data)
    
    @classmethod
    def register_factory(cls, model_type: str, factory_class: Type[ModelFactory]) -> None:
        """
        Register a new factory for a model type.
        Args:
            model_type (str): Model type identifier.
            factory_class (Type[ModelFactory]): Factory class to register.
        """
        cls._factories[model_type] = factory_class 