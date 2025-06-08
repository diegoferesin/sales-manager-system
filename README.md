# Sales Manager System

A robust data engineering project for analyzing sales data across multiple store locations.

## Project Overview

This system is designed to process daily sales data, organize information in a database, and enable complex analysis through SQL queries. It implements object-oriented programming principles and design patterns to create a scalable and maintainable solution.

## Project Structure

```
sales-manager-system/
├── data/               # Directory for CSV data files
├── scripts/           # Python scripts for data processing
├── sql/              # SQL scripts and queries
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
.\venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Model

The system works with the following data entities:
- Categories (categories.csv)
- Cities (cities.csv)
- Countries (countries.csv)
- Customers (customers.csv)
- Employees (employees.csv)
- Products (products.csv)
- Sales (sales.csv)

## Development Process

### Phase 1: System Structure
- [x] Project setup and environment configuration
- [ ] Data model implementation
- [ ] Basic data processing pipeline
- [ ] Database schema design

### Phase 2: Data Processing
- [ ] Advanced data processing
- [ ] Data validation and cleaning
- [ ] Performance optimization

### Phase 3: Analysis and Reporting
- [ ] SQL query implementation
- [ ] Report generation
- [ ] Performance monitoring

## Technical Decisions

### Environment Setup
- Python virtual environment (venv) for dependency isolation
- Requirements.txt for dependency management
- Git for version control

### Data Processing
- Object-oriented design for entity modeling
- Design patterns for modular architecture
- SQL for data analysis and reporting

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
