# Api_django_email_loginsystem

This project is login by email instead of username. It uses token-based authentication, and there are three key entities: **User**, **Client**, and **Project**. We will be using a relational database like MySQL for data storage, and Django as the framework.

Example: This project is a task management system where users can be assigned to projects by clients. Clients can create and manage multiple projects, assign users to those projects, and track progress.

## Features

- **User Management**: Users can register, log in, and be assigned to projects.
- **Client Management**: Clients can create, update, and delete projects. Each client can manage multiple projects.
- **Project Assignment**: Projects can be assigned to multiple users.
- **Project Overview**: Users can view their assigned projects and project details.

## Database Entities

- **User**: Represents an individual in the system, who can be assigned to multiple projects.
- **Client**: Represents a client who can have multiple projects.
- **Project**: Represents the work assigned to a client. A project can have many users working on it.

## Project Mechanism

### 1. User Registration & Authentication:
Users can register using their email and password. Once registered, users can log in to view or manage the projects they are assigned to.

### 2. Client Creation and Management:
Clients can create new projects by providing details like project name, description, and client association. Clients can update or delete projects as needed. Each client can have multiple projects, and these projects are linked to them in the database.

### 3. Project Creation:
Projects are created under a specific client, and users can be assigned to the project. The project will have a many-to-many relationship with users, meaning multiple users can work on the same project.

### 4. Viewing Assigned Projects:
Logged-in users can view all the projects they are assigned to. This is done by querying the projects related to the user in the database.

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**
- **Django 3.x** (or 4.x)
- **PostgreSQL** or **MySQL**

PostgreSQL or MySQL (as the database backend)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/bkbimal250/Api_django_email_loginsystem.git



### 2.Create a virtual environment:

```base
python -m venv myenv


3. Activate the virtual environment:
Windows:

```bash
myenv\Scripts\activate


```bash
source myenv/bin/activate

### 4. Install the dependencies:

```bash
pip install -r requirements.txt

5. Set up the database:
Make sure your database is set up (PostgreSQL/MySQL).

For example, configure the database settings in settings.py:

bash```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Use MySQL backend
        'NAME': 'your_database_name',  # The name of your MySQL database
        'USER': 'your_mysql_username',  # Your MySQL username
        'PASSWORD': 'your_mysql_password',  # Your MySQL password
        'HOST': 'localhost',  # Set to 'localhost' if MySQL is running locally
        'PORT': '3306',  # Default MySQL port (use the correct port if it's different)
    }
}
Update DATABASES settings in settings.py for your database connection.


### 6.Run database migrations:

```bash
python manage.py makemigrations

```bash
python manage.py migrate

### 7. Create a superuser (if using Django Admin):

```bash
python manage.py createsuperuser

### 8. Run the development server:
```bash
python manage.py runserver


You can now access the app at http://127.0.0.1:8000/.
Test the API using Postman, first create an account and use it:
Go to this URL:

Postman

The API URLs:
plaintext
```bash
http://localhost:8000/api/accounts/register/,
http://localhost:8000/api/accounts/login/,
http://localhost:8000/api/accounts/projects/,
http://localhost:8000/api/accounts/clients/
http://localhost:8000/api/accounts/users/
http://localhost:8000/api/accounts/Login/
