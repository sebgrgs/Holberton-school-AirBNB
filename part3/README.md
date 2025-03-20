# hBnB - Part 3: Database Integration

This folder contains the implementation of the database layer for the AirBnB clone project, migrating from in-memory storage to a relational database using SQLAlchemy.

## Overview

Part 3 builds upon the REST API foundation established in Part 2, implementing a persistent storage layer with proper database models, relationships, and queries.

## Project Structure

### Models (`app/models/`)
- `base.py`: Base model with common attributes (id, created_at, updated_at)
- `user.py`: User model with authentication attributes and password hashing
- `place.py`: Place model with property details and relationships to users, reviews and amenities
- `review.py`: Review model with rating system and validation
- `amenity.py`: Amenity model for property features

### API Endpoints (`app/api/v1/`)
- `users.py`: User CRUD operations with authentication requirements
- `places.py`: Property listing endpoints with owner validation
- `reviews.py`: Review creation and retrieval with rating validations
- `amenities.py`: Amenity management with admin authorization
- `auth.py`: JWT authentication endpoints for login
- `protected.py`: Protected routes for testing authentication

### Database (`database/`)
- `schema.sql`: Database schema with tables, relationships and constraints
- `initial_data.sql`: Seed data with admin user, sample places, reviews and amenities
- `erdiagram.txt`: Text representation of the ER diagram
- `ERdiagramHbnb.png`: Visual diagram of database structure
- `setup_db.py`: Database initialization script with SQLAlchemy
- `test_queries.sql`: Example SQL queries for manual testing

### Configuration
- `config.py`: Environment-specific configurations (development, testing, production)
- `.env`: Environment variables for database connection (not in git)

### Authentication
- JWT-based authentication system
- Role-based access control (admin vs. regular users)
- Protected routes requiring authentication

### Configuration
- `config.py`: Application configuration with database connection settings

### Testing
- `test_sql.py`: Tests for SQLAlchemy configuration and repository implementation
- `test.py`: Test for the API endpoints

## Database Models

The application uses the following core models:
- Users: Account information and authentication
- Places: Rental properties with location and pricing information
- Amenities: Features available at rental properties
- Reviews: User feedback for properties

## Database ER Diagram

![AirBnB Database ER Diagram](/part3/database/ERdiagramHbnb.png)

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

5. Test the API endpoints:
```bash
python -m unittest test.py
```

## Authors
- [Mathieu ZUCALLI](github.com/matzuc2)
- [Sebastien GEORGESCU](github.com/sebgrgs)