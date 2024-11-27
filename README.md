# Getting started

```bash
# create python virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies in requirements.txt and requirements-dev.txt
pip install -r requirements.txt
pip install -r requirements-dev.txt

# create a copy of the .env.example file and rename it to .env
# update the .env file with the correct values
cp .env.example .env

# run the web application for development
python -m phone_books_web
```

# Tests

## Running tests
```bash
# run all tests
python -m pytest

# run an individual module test
python -m pytest tests/test_module.py

# run all test marked with
python -m pytest -m "asyncio"
python -m pytest -m "slow"

# run specific test function
python -m pytest tests/test_module.py::test_function

# run specific test class
python -m pytest tests/test_module.py::TestClass

# run specific test method
python -m pytest tests/test_module.py::TestClass::test_method

# run all tests matching a pattern
python -m pytest -k "test_prefix"
```