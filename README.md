# FastAPI CRUD API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-grade RESTful API built with **FastAPI**, featuring CRUD operations for managing users, MySQL integration, middleware, logging, and robust error handling.

---

## ✨ Features

- **CRUD Operations**: Create, Read, Update, and Delete users with a clean API.
- **FastAPI**: High-performance, async-ready framework with automatic Swagger docs.
- **MySQL Database**: Persistent storage using SQLAlchemy ORM.
- **Dependency Injection**: Efficient database session management.
- **Middleware**: CORS support and custom request logging.
- **Logging**: Production-ready with console and rotating file output (5MB, 3 backups).
- **Error Handling**: Graceful, minimal error responses for a polished user experience.

---

## 🛠️ Project Structure
```
fastapi-crud-api/
├── app/
│   ├── init.py
│   ├── main.py              # App entry point
│   ├── api/
│   │   └── endpoints/
│   │       └── user.py      # User CRUD endpoints
│   ├── core/
│   │   └── middleware.py    # Custom middleware (logging)
│   ├── db/
│   │   └── database.py      # Database setup
│   ├── models/
│   │   └── user.py          # SQLAlchemy models
│   └── schemas/
│       └── user.py          # Pydantic schemas
├── logs/
│   └── app.log              # Log files (auto-generated)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.12+**: [Download](https://www.python.org/downloads/)
- **Docker**: [Install](https://www.docker.com/get-started) (for MySQL)
- **Git**: [Install](https://git-scm.com/)

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/inzemam21/fastapi-crud-api.git
   cd fastapi-crud-api

2. **Create a Virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**

4. **Run MySQL with Docker**
docker run -d -p 3306:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=fastapi_db mysql:latest

5. **Start the APP**
uvicorn app.main:app --reload

6. **Access the API**
URL: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs

📖 API Endpoints
Method	Endpoint	 Description	Request Body Example
POST	/users/	Create a new user	{"name": "Alice", "email": "alice@example.com"}
GET	/users/	List all users	-
GET	/users/{id}	Get a user by ID	-
PUT	/users/{id}	Update a user	{"name": "Alice Updated", "email": "alice.updated@example.com"}
DELETE	/users/{id}	Delete a user	-