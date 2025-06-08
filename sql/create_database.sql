-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS sales_manager;

-- Use the database
USE sales_manager;

-- Create tables
-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- Countries table
CREATE TABLE IF NOT EXISTS countries (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL,
    country_code VARCHAR(2) NOT NULL
);

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    city_id INT PRIMARY KEY,
    city_name VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10),
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);


-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(5) NULL,
    last_name VARCHAR(50) NOT NULL,
    city_id INT,
    address VARCHAR(100),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(1),
    last_name VARCHAR(50) NOT NULL,
    birth_date DATETIME NOT NULL,
    gender CHAR(1) NOT NULL,
    city_id INT,
    hire_date DATETIME NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,4) NOT NULL,
    category_id INT,
    class VARCHAR(20),
    modify_date VARCHAR(20),
    resistant VARCHAR(20),
    is_allergic VARCHAR(10),
    vitality_days INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    employee_id INT,
    customer_id INT,
    product_id INT,
    quantity INT NOT NULL,
    discount DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    transaction_number VARCHAR(50) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sale Details table
CREATE TABLE IF NOT EXISTS sale_details (
    sale_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(5, 2) DEFAULT 0.00,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create indexes for better performance
CREATE INDEX idx_customers_city ON customers(city_id);
CREATE INDEX idx_customers_last_name ON customers(last_name);
CREATE INDEX idx_customers_first_name ON customers(first_name);
CREATE INDEX idx_customers_full_name ON customers(last_name, first_name);
CREATE INDEX idx_employees_city ON employees(city_id);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_sales_customer ON sales(customer_id);
CREATE INDEX idx_sales_employee ON sales(employee_id);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sale_details_sale ON sale_details(sale_id);
CREATE INDEX idx_sale_details_product ON sale_details(product_id); 