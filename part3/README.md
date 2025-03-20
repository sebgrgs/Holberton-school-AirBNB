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

### Tables and Relationships

#### User Table
- Stores user account information and authentication details
- Primary key: id (UUID)
- Unique constraint: email
- Password is stored as a bcrypt hash for security
- is_admin flag determines administrative privileges

#### Place Table
- Stores rental property listings
- Primary key: id (UUID)
- Foreign key: owner_id references User.id
- Geographic coordinates stored as latitude/longitude
- Price stored as float for monetary values

#### Review Table
- Stores user reviews for properties
- Primary key: id (UUID)
- Foreign keys:
  - user_id references User.id (the reviewer)
  - place_id references Place.id (the reviewed property)
- Rating constrained between 1-5

#### Amenity Table
- Stores available property features
- Primary key: id (UUID)
- Unique constraint: name

#### Place_Amenity (Junction Table)
- Implements many-to-many relationship between Place and Amenity
- Composite primary key: (place_id, amenity_id)
- Foreign keys:
  - place_id references Place.id
  - amenity_id references Amenity.id

#### Key Relationships
- One User can own many Places (one-to-many)
- One User can write many Reviews (one-to-many)
- One Place can have many Reviews (one-to-many)
- Many Places can have many Amenities (many-to-many via Place_Amenity)

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

## Technologies Used

- **Flask**: Web framework for building the API
- **Flask-RESTx**: Extension for building REST APIs with Swagger documentation
- **SQLAlchemy/Flask-SQLAlchemy**: ORM for database access and management
- **Flask-Migrate**: Database migration management
- **Flask-JWT-Extended**: Authentication with JSON Web Tokens
- **Flask-Bcrypt**: Password hashing and security
- **Python-dotenv**: Environment variable management
- **SQLite/MySQL**: Database engines
- **Unit Testing**: Python's unittest framework for testing

## Authors
- [Mathieu ZUCALLI](github.com/matzuc2)
- [Sebastien GEORGESCU](github.com/sebgrgs)