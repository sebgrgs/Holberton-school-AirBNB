# AirBnB Clone - Part 3: Database Integration

This folder contains the implementation of the database layer for the AirBnB clone project, migrating from in-memory storage to a relational database using SQLAlchemy.

## Overview

Part 3 builds upon the REST API foundation established in Part 2, implementing a persistent storage layer with proper database models, relationships, and queries.

## Components

### Database Structure
- `database/schema.sql`: SQL schema defining tables and relationships
- `database/initial_data.sql`: Initial seed data for the application
- `database/erdiagram.txt`: Entity relationship diagram documentation
- `database/test_queries.sql`: Sample SQL queries for testing
- `database/setup_db.py`: Script to initialize the database

### Configuration
- `config.py`: Application configuration with database connection settings

### Testing
- `test_sql.py`: Tests for SQLAlchemy configuration and repository implementation
- `test3.py`: API endpoint tests ensuring database persistence works

## Database Models

The application uses the following core models:
- Users: Account information and authentication
- Places: Rental properties with location and pricing information
- Amenities: Features available at rental properties
- Reviews: User feedback for properties

## Getting Started

1. Install required packages:
```bash
pip install flask flask-sqlalchemy
```

2. Initialize the database:
```bash
python database/setup_db.py
```

3. Run the application:
```bash
python api/v1/app.py
```

4. Run the test suite to verify the database integration:
```bash
python -m unittest test_sql.py
```

## Authors
- [Mathieu ZUCALLI](github.com/matzuc2)
- [Sebastien GEORGESCU](github.com/sebgrgs)