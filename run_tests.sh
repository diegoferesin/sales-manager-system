#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Add src to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Generate coverage report
python -m coverage html

echo "Tests completed. Coverage report generated in htmlcov/index.html" 