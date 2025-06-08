-- Load categories
LOAD DATA INFILE '../raw/categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(category_id, category_name);

-- Load countries
LOAD DATA INFILE '../raw/countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(country_id, country_name, country_code);

-- Load cities
LOAD DATA INFILE '../raw/cities.csv'
INTO TABLE cities
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(city_id, city_name, zip_code, country_id);

-- Load customers
LOAD DATA INFILE '../raw/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(customer_id, first_name, middle_initial, last_name, city_id, address);

-- Load employees
LOAD DATA INFILE '../raw/employees.csv'
INTO TABLE employees
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(employee_id, first_name, middle_initial, last_name, @birth_date, gender, city_id, @hire_date)
SET birth_date = STR_TO_DATE(@birth_date, '%Y-%m-%d %H:%i:%s.%f'),
    hire_date = STR_TO_DATE(@hire_date, '%Y-%m-%d %H:%i:%s.%f');

-- Load products
LOAD DATA INFILE '../raw/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(product_id, product_name, unit_price, category_id, class, modify_date, resistant, is_allergic, vitality_days);

-- Load sales
LOAD DATA INFILE '../raw/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(sale_id, employee_id, customer_id, product_id, quantity, discount, total_price, @sale_date, transaction_number)
SET sale_date = CASE 
    WHEN @sale_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}' THEN 
        DATE_ADD(
            STR_TO_DATE(SUBSTRING_INDEX(@sale_date, ' ', 1), '%Y-%m-%d'),
            INTERVAL CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(@sale_date, ' ', -1), ':', 1) AS UNSIGNED) HOUR
        )
    ELSE CURDATE()
END;