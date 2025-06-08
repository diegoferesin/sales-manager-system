"""
Unit tests for model classes.
"""
import pytest
from src.models.product import Product
from src.models.category import Category
from src.models.customer import Customer
from src.models.sale import Sale

def test_product_creation():
    product = Product(product_id=1, product_name="Test Product", price=100.00, category_id=1)
    assert product.product_id == 1
    assert product.product_name == "Test Product"
    assert product.price == 100.00
    assert product.category_id == 1

def test_category_creation():
    category = Category(category_id=1, category_name="Test Category")
    assert category.category_id == 1
    assert category.category_name == "Test Category"

def test_customer_creation():
    customer = Customer(customer_id=1, first_name="Test", last_name="Customer")
    assert customer.customer_id == 1
    assert customer.first_name == "Test"
    assert customer.last_name == "Customer"

def test_sale_creation():
    sale = Sale(sale_id=1, sales_person_id=2, customer_id=3, product_id=4, quantity=5, discount=0.1, total_price=450.0, sale_date="2024-01-01", transaction_number="TXN001")
    assert sale.sale_id == 1
    assert sale.sales_person_id == 2
    assert sale.customer_id == 3
    assert sale.product_id == 4
    assert sale.quantity == 5
    assert sale.discount == 0.1
    assert sale.total_price == 450.0
    assert sale.sale_date == "2024-01-01"
    assert sale.transaction_number == "TXN001"
