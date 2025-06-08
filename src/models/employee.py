from typing import Any, Dict
import pandas as pd
from .base_model import BaseModel

class Employee(BaseModel):
    """
    Employee represents an employee entity in the system, containing personal and employment information.
    """
    def __init__(self, employee_id: int = None, first_name: str = None, middle_initial: str = None, 
                 last_name: str = None, birth_date: str = None, gender: str = None, 
                 city_id: int = None, hire_date: str = None):
        """
        Initialize an Employee instance.
        Args:
            employee_id (int, optional): Unique identifier for the employee.
            first_name (str, optional): First name of the employee.
            middle_initial (str, optional): Middle initial of the employee.
            last_name (str, optional): Last name of the employee.
            birth_date (str, optional): Date of birth of the employee.
            gender (str, optional): Gender of the employee (M/F).
            city_id (int, optional): Identifier for the city where the employee resides.
            hire_date (str, optional): Date when the employee was hired.
        """
        super().__init__()
        self._data = {
            'employee_id': employee_id,
            'first_name': first_name,
            'middle_initial': middle_initial,
            'last_name': last_name,
            'birth_date': birth_date,
            'gender': gender,
            'city_id': city_id,
            'hire_date': hire_date
        }

    def validate(self) -> bool:
        """
        Validate the employee data.
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if not self._data['first_name'] or not self._data['last_name']:
            return False
        if self._data['city_id'] is not None and not isinstance(self._data['city_id'], int):
            return False
        if self._data['middle_initial'] is not None and len(self._data['middle_initial']) > 5:
            return False
        if self._data['gender'] is not None and self._data['gender'] not in ['M', 'F']:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the employee instance to a dictionary.
        Returns:
            Dict[str, Any]: Dictionary containing the employee's data.
        """
        return self._data.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """
        Create an Employee instance from a dictionary.
        Args:
            data (Dict[str, Any]): Dictionary containing the employee's data.
        Returns:
            Employee: A new Employee instance.
        """
        return cls(
            employee_id=data.get('employee_id'),
            first_name=data.get('first_name'),
            middle_initial=data.get('middle_initial'),
            last_name=data.get('last_name'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            city_id=data.get('city_id'),
            hire_date=data.get('hire_date')
        )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'Employee':
        """
        Create an Employee instance from a pandas DataFrame row.
        Args:
            df (pd.DataFrame): DataFrame containing the employee's data.
        Returns:
            Employee: A new Employee instance.
        """
        if df.empty:
            return cls()
        
        # Handle both column naming conventions (from CSV and DB)
        employee_id = df.get('EmployeeID', df.get('employee_id', [None]))[0]
        first_name = df.get('FirstName', df.get('first_name', [None]))[0]
        middle_initial = df.get('MiddleInitial', df.get('middle_initial', [None]))[0]
        last_name = df.get('LastName', df.get('last_name', [None]))[0]
        birth_date = df.get('BirthDate', df.get('birth_date', [None]))[0]
        gender = df.get('Gender', df.get('gender', [None]))[0]
        city_id = df.get('CityID', df.get('city_id', [None]))[0]
        hire_date = df.get('HireDate', df.get('hire_date', [None]))[0]
        
        return cls(
            employee_id=employee_id,
            first_name=first_name,
            middle_initial=middle_initial,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            city_id=city_id,
            hire_date=hire_date
        )

    @property
    def employee_id(self) -> int:
        """
        Get the employee ID.
        Returns:
            int: The employee ID.
        """
        return self._data['employee_id']

    @property
    def first_name(self) -> str:
        """
        Get the employee's first name.
        Returns:
            str: The first name.
        """
        return self._data['first_name']

    @property
    def middle_initial(self) -> str:
        """
        Get the employee's middle initial.
        Returns:
            str: The middle initial.
        """
        return self._data['middle_initial']

    @property
    def last_name(self) -> str:
        """
        Get the employee's last name.
        Returns:
            str: The last name.
        """
        return self._data['last_name']

    @property
    def birth_date(self) -> str:
        """
        Get the employee's birth date.
        Returns:
            str: The birth date.
        """
        return self._data['birth_date']

    @property
    def gender(self) -> str:
        """
        Get the employee's gender.
        Returns:
            str: The gender (M/F).
        """
        return self._data['gender']

    @property
    def city_id(self) -> int:
        """
        Get the city ID where the employee resides.
        Returns:
            int: The city ID.
        """
        return self._data['city_id']

    @property
    def hire_date(self) -> str:
        """
        Get the employee's hire date.
        Returns:
            str: The hire date.
        """
        return self._data['hire_date'] 