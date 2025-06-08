# Sales Manager System

A robust data engineering project for analyzing sales data across multiple store locations, implementing advanced design patterns and SQL analysis capabilities.

## Project Overview

This system is designed to process daily sales data, organize information in a database, and enable complex analysis through SQL queries. It implements object-oriented programming principles, design patterns, and advanced data analysis strategies to create a scalable, maintainable, and extensible solution.

## Project Structure

```
sales-manager-system/
├── data/               # Directory for CSV data files
│   ├── raw/           # Original CSV files
│   └── processed/     # Processed data files
├── src/               # Source code
│   ├── models/        # Data models (Category, Product, Sale, etc.)
│   ├── database/      # Database connection and query management
│   │   ├── connection.py       # Singleton database connection
│   │   └── query_examples.py   # Example queries
│   ├── utils/         # Utility functions and design patterns
│   │   ├── model_factory.py    # Factory Method pattern
│   │   ├── query_builder.py    # Builder pattern for SQL
│   │   ├── decorators.py       # Decorator pattern implementations
│   │   └── analysis_strategies.py # Strategy pattern for analysis
│   ├── config/        # Configuration files
│   └── services/      # Business logic services
├── sql/              # SQL scripts and queries
├── tests/            # Test files
│   └── test_design_patterns.py # Unit tests for design patterns
├── notebooks/        # Jupyter notebooks
│   └── demo_integracion.ipynb  # Integration demonstration
├── requirements.txt   # Project dependencies
├── setup.sh          # Setup script
├── .env.example       # Environment variables template
└── README.md         # Project documentation
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
./setup.sh
```

### 2. Database Configuration

Create a `.env` file in the project root with your database credentials:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sales_manager_db
```

**Important**: Add `.env` to your `.gitignore` file to avoid exposing credentials.

### 3. Run Tests

```bash
# Run all tests
pytest

# Run design pattern tests specifically
pytest tests/test_design_patterns.py -v

# Run with coverage
pytest --cov=src tests/
```

### 4. Launch Jupyter Notebook

```bash
# Start Jupyter and open the integration demo
jupyter notebook notebooks/demo_integracion.ipynb
```

## Architecture & Design Patterns

The system implements several design patterns to ensure scalability, maintainability, and extensibility:

### 1. Singleton Pattern (`DatabaseConnection`)
**Purpose**: Ensures only one database connection instance exists throughout the application.

**Implementation**: `src/database/connection.py`

**Benefits**:
- Resource optimization
- Consistent connection management
- Centralized configuration

```python
# Usage example
db = DatabaseConnection()  # Always returns the same instance
```

### 2. Factory Method Pattern (`ModelFactory`)
**Purpose**: Simplifies and standardizes the creation of data model instances.

**Implementation**: `src/utils/model_factory.py`

**Benefits**:
- Flexible object creation
- Easy extensibility for new models
- Consistent validation and initialization

```python
# Usage example
category = ModelFactoryRegistry.create_model('category', data)
product = ModelFactoryRegistry.create_model('product', data)
```

### 3. Builder Pattern (`SQLQueryBuilder`)
**Purpose**: Enables fluent, step-by-step construction of complex SQL queries.

**Implementation**: `src/utils/query_builder.py`

**Benefits**:
- Readable and maintainable query construction
- Reusable query components
- Built-in validation

```python
# Usage example
query = (SQLQueryBuilder()
    .select(['name', 'price'])
    .from_table('products')
    .where('price > 100')
    .order_by('price', 'DESC')
    .limit(10)
    .build())
```

### 4. Decorator Pattern (Multiple Decorators)
**Purpose**: Adds cross-cutting functionality like logging, timing, caching, and error handling.

**Implementation**: `src/utils/decorators.py`

**Benefits**:
- Separation of concerns
- Flexible composition of features
- Enhanced debugging and monitoring

```python
# Usage example
@database_operation(cache_ttl=300, max_retries=3)
def complex_query():
    return db.execute_query("SELECT * FROM sales")
```

### 5. Strategy Pattern (`AnalysisStrategy`)
**Purpose**: Enables interchangeable analysis algorithms for different business needs.

**Implementation**: `src/utils/analysis_strategies.py`

**Benefits**:
- Flexible analysis approaches
- Easy addition of new analysis types
- Independent testing of algorithms

```python
# Usage example
strategy = AnalysisStrategyFactory.create_strategy('revenue')
context = SalesAnalysisContext(strategy)
results = context.perform_analysis(sales_data)
```

## Data Model

The system implements a comprehensive data model with robust validation and flexible data handling:

### Base Model
- Abstract base class providing common functionality
- Data validation and type checking
- Dictionary and DataFrame conversion methods
- Consistent error handling and documentation

### Entity Models
1. **Category**
   - category_id (INT PRIMARY KEY)
   - category_name (VARCHAR(50) NOT NULL)

2. **City**
   - city_id (INT PRIMARY KEY)
   - city_name (VARCHAR(50) NOT NULL)
   - zip_code (VARCHAR(10))
   - country_id (INT FOREIGN KEY)

3. **Country**
   - country_id (INT PRIMARY KEY)
   - country_name (VARCHAR(50) NOT NULL)
   - country_code (VARCHAR(2) NOT NULL)

4. **Customer**
   - customer_id (INT PRIMARY KEY)
   - first_name (VARCHAR(50) NOT NULL)
   - middle_initial (VARCHAR(1))
   - last_name (VARCHAR(50) NOT NULL)
   - birth_date (DATE)
   - gender (VARCHAR(1))
   - city_id (INT FOREIGN KEY)
   - address (VARCHAR(255))

5. **Employee**
   - employee_id (INT PRIMARY KEY)
   - first_name (VARCHAR(50) NOT NULL)
   - middle_initial (VARCHAR(1))
   - last_name (VARCHAR(50) NOT NULL)
   - birth_date (DATE)
   - gender (VARCHAR(1))
   - city_id (INT FOREIGN KEY)
   - hire_date (DATE)

6. **Product**
   - product_id (INT PRIMARY KEY)
   - product_name (VARCHAR(100) NOT NULL)
   - price (DECIMAL(10,4) NOT NULL)
   - category_id (INT FOREIGN KEY)
   - class_type (VARCHAR(20))
   - modify_date (VARCHAR(20))
   - resistant (VARCHAR(20))
   - is_allergic (VARCHAR(10))
   - vitality_days (INT)

7. **Sale**
   - sale_id (INT PRIMARY KEY)
   - sales_person_id (INT FOREIGN KEY)
   - customer_id (INT FOREIGN KEY)
   - product_id (INT FOREIGN KEY)
   - quantity (INT NOT NULL)
   - discount (DECIMAL(10,2) DEFAULT 0)
   - total_price (DECIMAL(10,2) NOT NULL)
   - sale_date (DATE NOT NULL)
   - transaction_number (VARCHAR(50) NOT NULL)

## SQL Objects

The system implements various SQL objects to enhance database functionality and performance:

### 1. Functions
- **calculate_discount**: Calculates final price after applying discounts
- **get_customer_lifetime_value**: Computes total customer spending
- **calculate_product_profit**: Determines product profitability
- **get_sales_trend**: Analyzes sales trends over time

### 2. Triggers
- **update_inventory**: Automatically updates inventory after sales
- **log_price_changes**: Tracks product price modifications
- **validate_sale_date**: Ensures sales dates are valid
- **update_customer_stats**: Maintains customer statistics

### 3. Stored Procedures
- **generate_sales_report**: Creates comprehensive sales reports
- **process_daily_sales**: Handles daily sales processing
- **update_product_categories**: Manages product categorization
- **calculate_monthly_metrics**: Computes monthly performance metrics

### 4. Views
- **sales_summary**: Aggregated sales data
- **customer_purchase_history**: Customer buying patterns
- **product_performance**: Product sales metrics
- **employee_sales_stats**: Sales performance by employee

### 5. Indexes
- **idx_sales_date**: Optimizes date-based queries
- **idx_product_category**: Improves category filtering
- **idx_customer_name**: Enhances customer name searches
- **idx_sales_amount**: Speeds up amount-based queries

### Usage Examples

```sql
-- Function Example
SELECT calculate_discount(100.00, 0.15) as final_price;

-- Trigger Example
CREATE TRIGGER update_inventory
AFTER INSERT ON sales
FOR EACH ROW
BEGIN
    UPDATE products 
    SET stock = stock - NEW.quantity 
    WHERE product_id = NEW.product_id;
END;

-- Stored Procedure Example
CALL generate_sales_report('2024-01-01', '2024-03-31');

-- View Example
SELECT * FROM sales_summary 
WHERE sale_date >= '2024-01-01';

-- Index Example
CREATE INDEX idx_sales_date ON sales(sale_date);
```

These SQL objects are demonstrated in the Python module through the `SQLObjectsDemo` class, which provides methods to:
- Create and manage all SQL objects
- Execute and test their functionality
- Monitor performance and usage
- Maintain and update as needed

## Advanced Features

### SQL Query Builder with Advanced Capabilities

The system includes a sophisticated query builder supporting:

- **Complex Joins**: INNER, LEFT, RIGHT joins with multiple tables
- **Aggregations**: GROUP BY, HAVING clauses with statistical functions
- **Window Functions**: RANK(), PERCENT_RANK(), ROW_NUMBER()
- **Subqueries**: Nested queries and CTEs
- **Parameter Binding**: Safe parameterized queries
- **Query Validation**: Built-in syntax and logic validation

### Analysis Strategies

Multiple analysis algorithms are available:

1. **Revenue Analysis**: Total revenue, averages, quartiles, distribution analysis
2. **Quantity Analysis**: Item counts, bulk sale analysis, quantity distributions
3. **Customer Behavior**: Lifetime value, segmentation, purchase patterns
4. **Product Performance**: Sales ranking, category performance, trend analysis

### Enhanced Database Operations

- **Connection Pooling**: Efficient resource management
- **Query Caching**: LRU cache for expensive queries
- **Retry Logic**: Automatic retry for transient failures
- **Performance Monitoring**: Execution time tracking and logging
- **Error Handling**: Graceful error recovery and user-friendly messages

## Development Process

### Phase 1: System Foundation ✅
- [x] Project setup and environment configuration
- [x] Data model implementation
  - [x] Base model with common functionality
  - [x] Entity models with validation
  - [x] CSV and database field mapping
- [x] Database schema design
  - [x] Table creation scripts
  - [x] Foreign key relationships
  - [x] Data type definitions

### Phase 2: Design Patterns & Advanced Features ✅
- [x] Design pattern implementation
  - [x] Singleton pattern for database connection
  - [x] Factory method for model creation
  - [x] Builder pattern for SQL query construction
  - [x] Decorator pattern for cross-cutting concerns
  - [x] Strategy pattern for analysis algorithms
- [x] Advanced SQL capabilities
  - [x] Complex query builder with fluent API
  - [x] Query optimization and caching
  - [x] Parameter binding and validation
- [x] Comprehensive testing
  - [x] Unit tests for all design patterns
  - [x] Integration tests
  - [x] Mock testing for database operations
- [x] Documentation and demonstration
  - [x] Interactive Jupyter notebook
  - [x] Code documentation and examples
  - [x] Pattern justification and benefits

### Phase 3: Advanced Analytics & Production Features
- [ ] Advanced data processing pipelines
- [ ] Real-time data streaming capabilities
- [ ] Machine learning integration
- [ ] Performance optimization and indexing
- [ ] API development for external integrations
- [ ] Advanced visualization and reporting
- [ ] Monitoring and alerting systems

## Testing

The project includes a comprehensive test suite using pytest and coverage reporting:

### Running Tests

```bash
# Run all tests with coverage
./run_tests.sh

# Or run tests manually
python -m pytest tests/
```

### Test Coverage

The test suite aims to maintain at least 80% code coverage. Coverage reports are generated in:
- Terminal output (missing lines)
- HTML report (htmlcov/index.html)

### Test Categories

1. **Database Tests**
   - Connection management
   - Query execution
   - Transaction handling
   - Singleton pattern verification

2. **Model Tests**
   - Product creation and validation
   - Customer creation and validation
   - Sale creation and validation
   - Store creation and validation

3. **SQL Object Tests**
   - Function execution
   - Trigger creation and execution
   - Stored procedure execution
   - View creation and querying

## Security & Best Practices

### Data Security
- **Environment Variables**: Sensitive data stored in `.env` files
- **Parameter Binding**: SQL injection prevention
- **Input Validation**: Comprehensive data sanitization
- **Access Control**: Role-based permissions (future implementation)

### Code Quality
- **Type Hints**: Full type annotation for better IDE support
- **Documentation**: Comprehensive docstrings and examples
- **Code Standards**: PEP 8 compliance with automated formatting
- **Error Handling**: Graceful failure handling and user feedback

### Performance Optimization
- **Query Optimization**: Efficient SQL generation and execution
- **Connection Pooling**: Resource management optimization
- **Caching Strategies**: Multiple cache levels for different data types
- **Lazy Loading**: On-demand data loading for large datasets

## Usage Examples

### Basic Query Execution

```python
from src.database.connection import DatabaseConnection

# Get database connection (Singleton)
db = DatabaseConnection()

# Execute simple query
results = db.execute_query("SELECT * FROM products LIMIT 10")

# Execute parameterized query
sales = db.execute_query(
    "SELECT * FROM sales WHERE sale_date >= :start_date", 
    {'start_date': '2023-01-01'}
)
```

### Advanced Query Building

```python
from src.utils.query_builder import SQLQueryBuilder, QueryBuilderDirector

# Build complex query
builder = SQLQueryBuilder()
query = (builder
    .select(['p.product_name', 'SUM(s.total_price) as revenue'])
    .from_table('products p')
    .inner_join('sales s', 'p.product_id = s.product_id')
    .where('s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)')
    .group_by(['p.product_id'])
    .order_by('revenue', 'DESC')
    .limit(20)
    .build())

# Use predefined query patterns
director = QueryBuilderDirector(builder)
category_analysis = director.build_sales_summary_by_category()
```

### Analysis Strategy Usage

```python
from src.utils.analysis_strategies import AnalysisStrategyFactory, SalesAnalysisContext

# Create analysis strategy
revenue_strategy = AnalysisStrategyFactory.create_strategy('revenue')
context = SalesAnalysisContext(revenue_strategy)

# Perform analysis
results = context.perform_analysis()

# Switch strategies dynamically
quantity_strategy = AnalysisStrategyFactory.create_strategy('quantity')
context.set_strategy(quantity_strategy)
quantity_results = context.perform_analysis()
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Code Style**: Follow PEP 8 and use type hints
2. **Testing**: Add tests for new features and patterns
3. **Documentation**: Update docstrings and README for changes
4. **Design Patterns**: Justify any new patterns with clear use cases

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Run the full test suite
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using modern Python best practices
- Incorporates proven design patterns for enterprise-scale applications
- Designed for educational and production use in data engineering contexts
