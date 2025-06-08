-- =============================================
-- Advanced SQL Objects for Sales Manager System
-- =============================================

-- =============================================
-- 1. Function: Calculate Customer Lifetime Value
-- =============================================
DELIMITER //

CREATE FUNCTION calculate_customer_lifetime_value(
    customer_id INT,
    months_analysis INT
) RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
COMMENT 'Calculates the customer lifetime value based on purchase history'
BEGIN
    DECLARE total_spent DECIMAL(10,2);
    DECLARE avg_monthly_value DECIMAL(10,2);
    DECLARE first_purchase_date DATE;
    DECLARE last_purchase_date DATE;
    DECLARE months_active INT;
    
    -- Get customer purchase metrics
    SELECT 
        SUM(total_price) as total_spent,
        MIN(sale_date) as first_purchase,
        MAX(sale_date) as last_purchase
    INTO 
        total_spent,
        first_purchase_date,
        last_purchase_date
    FROM sales
    WHERE customer_id = customer_id
    AND sale_date >= DATE_SUB(CURDATE(), INTERVAL months_analysis MONTH);
    
    -- Calculate months active
    SET months_active = TIMESTAMPDIFF(MONTH, first_purchase_date, last_purchase_date);
    IF months_active = 0 THEN SET months_active = 1; END IF;
    
    -- Calculate average monthly value
    SET avg_monthly_value = total_spent / months_active;
    
    RETURN avg_monthly_value;
END //

DELIMITER ;

-- =============================================
-- 2. Trigger: Update Product Stock and Sales Stats
-- =============================================
DELIMITER //

CREATE TRIGGER after_sale_insert
AFTER INSERT ON sales
FOR EACH ROW
BEGIN
    -- Update product statistics
    UPDATE products 
    SET 
        total_sales = total_sales + NEW.quantity,
        last_sale_date = NEW.sale_date,
        total_revenue = total_revenue + NEW.total_price
    WHERE product_id = NEW.product_id;
    
    -- Update category statistics
    UPDATE categories c
    INNER JOIN products p ON c.category_id = p.category_id
    SET 
        c.total_sales = c.total_sales + NEW.quantity,
        c.total_revenue = c.total_revenue + NEW.total_price,
        c.last_sale_date = NEW.sale_date
    WHERE p.product_id = NEW.product_id;
    
    -- Log the sale for audit
    INSERT INTO sales_audit_log (
        sale_id,
        product_id,
        customer_id,
        sales_person_id,
        quantity,
        total_price,
        sale_date,
        action_type
    ) VALUES (
        NEW.sale_id,
        NEW.product_id,
        NEW.customer_id,
        NEW.sales_person_id,
        NEW.quantity,
        NEW.total_price,
        NEW.sale_date,
        'INSERT'
    );
END //

DELIMITER ;

-- =============================================
-- 3. Stored Procedure: Generate Sales Report
-- =============================================
DELIMITER //

CREATE PROCEDURE generate_sales_report(
    IN start_date DATE,
    IN end_date DATE,
    IN category_id INT,
    IN include_details BOOLEAN
)
BEGIN
    -- Declare variables for report
    DECLARE total_revenue DECIMAL(10,2);
    DECLARE total_transactions INT;
    DECLARE avg_transaction_value DECIMAL(10,2);
    
    -- Calculate summary metrics
    SELECT 
        SUM(total_price),
        COUNT(sale_id),
        AVG(total_price)
    INTO 
        total_revenue,
        total_transactions,
        avg_transaction_value
    FROM sales s
    INNER JOIN products p ON s.product_id = p.product_id
    WHERE s.sale_date BETWEEN start_date AND end_date
    AND (category_id IS NULL OR p.category_id = category_id);
    
    -- Return summary results
    SELECT 
        total_revenue,
        total_transactions,
        avg_transaction_value,
        start_date as report_start_date,
        end_date as report_end_date;
    
    -- Return detailed results if requested
    IF include_details THEN
        SELECT 
            s.sale_date,
            p.product_name,
            c.category_name,
            CONCAT(e.first_name, ' ', e.last_name) as salesperson,
            s.quantity,
            s.total_price,
            s.discount
        FROM sales s
        INNER JOIN products p ON s.product_id = p.product_id
        INNER JOIN categories c ON p.category_id = c.category_id
        INNER JOIN employees e ON s.sales_person_id = e.employee_id
        WHERE s.sale_date BETWEEN start_date AND end_date
        AND (category_id IS NULL OR p.category_id = category_id)
        ORDER BY s.sale_date, s.total_price DESC;
    END IF;
END //

DELIMITER ;

-- =============================================
-- 4. View: Customer Purchase History
-- =============================================
CREATE VIEW customer_purchase_history AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.gender,
    ci.city_name,
    co.country_name,
    COUNT(DISTINCT s.sale_id) as total_purchases,
    SUM(s.total_price) as total_spent,
    AVG(s.total_price) as avg_purchase_value,
    MIN(s.sale_date) as first_purchase_date,
    MAX(s.sale_date) as last_purchase_date,
    COUNT(DISTINCT s.product_id) as unique_products_bought,
    SUM(s.quantity) as total_items_bought,
    SUM(s.discount) as total_discounts_received,
    ROUND(SUM(s.discount) / NULLIF(SUM(s.total_price), 0) * 100, 2) as discount_percentage
FROM customers c
INNER JOIN sales s ON c.customer_id = s.customer_id
INNER JOIN cities ci ON c.city_id = ci.city_id
INNER JOIN countries co ON ci.country_id = co.country_id
GROUP BY 
    c.customer_id, 
    c.first_name, 
    c.last_name, 
    c.gender, 
    ci.city_name, 
    co.country_name;

-- =============================================
-- 5. Indexes for Performance Optimization
-- =============================================

-- Composite index for sales queries
CREATE INDEX idx_sales_date_product ON sales(sale_date, product_id);

-- Composite index for customer analysis
CREATE INDEX idx_customer_city_country ON customers(city_id, customer_id);

-- Index for product category lookups
CREATE INDEX idx_product_category ON products(category_id);

-- Index for employee performance analysis
CREATE INDEX idx_sales_employee ON sales(sales_person_id, sale_date);

-- Full-text index for product search
CREATE FULLTEXT INDEX idx_product_search ON products(product_name, class_type);

-- =============================================
-- 6. Additional Tables for Audit and Statistics
-- =============================================

-- Sales audit log table
CREATE TABLE IF NOT EXISTS sales_audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    product_id INT,
    customer_id INT,
    sales_person_id INT,
    quantity INT,
    total_price DECIMAL(10,2),
    sale_date DATE,
    action_type VARCHAR(10),
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (sales_person_id) REFERENCES employees(employee_id)
);

-- Add statistics columns to products table
ALTER TABLE products
ADD COLUMN total_sales INT DEFAULT 0,
ADD COLUMN total_revenue DECIMAL(10,2) DEFAULT 0,
ADD COLUMN last_sale_date DATE;

-- Add statistics columns to categories table
ALTER TABLE categories
ADD COLUMN total_sales INT DEFAULT 0,
ADD COLUMN total_revenue DECIMAL(10,2) DEFAULT 0,
ADD COLUMN last_sale_date DATE; 