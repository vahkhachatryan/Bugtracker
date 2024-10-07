# Bug Tracker Application

## Overview
This is a Bug Tracker application built with Flask and PostgreSQL. It allows users to register, create, assign, and update tasks (bugs or tasks), with different roles like manager, lead, developer, and tester.

## Features
- User registration with role assignment
- Task (bug) creation and assignment
- Task updates (status, assignee)
- Task deletion

## Installation

### Prerequisites
- Python 3.x
- PostgreSQL
- Pip (Python package installer)

### Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/bug-tracker.git
    cd bug-tracker
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up PostgreSQL and create a database:
    ```sql
    CREATE DATABASE Bugtracker;
    ```

5. Apply database migrations:
    ```bash
    flask db upgrade
    ```

6. Run the application:
    ```bash
    python app.py
    ```

7. Open the browser and go to:
    ```
    http://127.0.0.1:5004
    ```

## API Endpoints

### User Registration
- **POST /register**
- **Payload**:
    ```json
    {
        "username": "testuser",
        "password": "password123",
        "role": "developer"
    }
    ```

### Task Operations
- **GET /tasks** - Retrieve all tasks
- **POST /tasks** - Create a new task
- **PUT /tasks/<task_id>** - Update a task
- **DELETE /tasks/<task_id>** - Delete a task

## License
This project is licensed under the MIT License.

