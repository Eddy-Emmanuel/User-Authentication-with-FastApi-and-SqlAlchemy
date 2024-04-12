# My API Documentation

## Overview
This API provides functionality for user registration, authentication, and user management.

## Features
### User Management
- **Register User**: Register a new user.
- **Get User**: Retrieve user details.
- **Delete User**: Delete a user from the system.

### Authentication
- **Authenticate User**: Obtain an access token for authentication.

### Default
- **Homepage**: Display the homepage with API documentation.

## Endpoints

### User Management

#### Register User
- **Method**: `POST`
- **Endpoint**: `/register_user`
- **Description**: Registers a new user with the system.

#### Get User
- **Method**: `GET`
- **Endpoint**: `/get_user`
- **Description**: Retrieves user details.

#### Delete User
- **Method**: `DELETE`
- **Endpoint**: `/delete_user`
- **Description**: Deletes a user from the system.

### Authentication

#### Authenticate User
- **Method**: `POST`
- **Endpoint**: `/authenticate_user`
- **Description**: Obtains an access token for user authentication.

### Default

#### Homepage
- **Method**: `GET`
- **Endpoint**: `/`
- **Description**: Displays the homepage with API documentation.

## Usage
- Clone the repository: `git clone https://github.com/Eddy-Emmanuel/User-Authentication-with-FastApi-and-SqlAlchemy`
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `uvicorn main:app --reload`
- Access the API documentation and test the endpoints.

## Technologies Used
- FastAPI
- SQLAlchemy
- JWT for authentication
- Uvicorn

## Contributing
Contributions are welcome! Please follow the contribution guidelines in CONTRIBUTING.md.
