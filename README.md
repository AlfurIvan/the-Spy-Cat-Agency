# Spy Cat Agency - Mission Management System

This is a Django-based application designed for the Spy Cat Agency (SCA) to manage spy cats, their missions, and targets. The application allows for CRUD operations on spy cats, missions, and targets, and ensures that the agency can effectively assign, update, and track their operations.

## Features

- **Spy Cats**:
  - Create, update, list, and delete spy cats.
  - Validate spy cat breeds using TheCatAPI.
  
- **Missions**:
  - Create, update, list, and delete missions.
  - Assign cats to missions (one cat can only have one mission at a time).
  - Automatically mark missions as complete when all targets are completed.

- **Targets**:
  - Create and manage targets within missions.
  - Mark targets as completed.
  - Prevent notes from being updated once a target is marked as completed.
  - Enforce uniqueness of target names.
  
## Requirements

- Python 3.x
- Django 3.x or above
- Django REST Framework
- TheCatAPI for breed validation
- PostgreSQL (or any other database you prefer)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/spy-cat-agency.git
cd spy-cat-agency

```
### 2. Install dependencies
Make sure you have Poetry installed, then run:
```bash
poetry install
```


### 3. Set up environment variables
Create a .env file in the root of the project and copy here containment of .env.example

### 4. Run the application

```bash
docker compose up -d --build
```
The app should now be running at http://127.0.0.1:8000.

### 5. Documentation
Navigate to http://127.0.0.1:8000/api/docs/ for exploration of this app.

### 6. Postman Collection
    link will be here soon