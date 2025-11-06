# Pharma REST API

A sample REST API for a fictional pharmaceutical company, built with **FastAPI** and **SQLModel**.  
This project demonstrates user authentication, drug and clinical trial management, and order processing.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Demo Data](#demo-data)
- [Docker](#docker)
- [License](#license)

---

## Features

- User authentication with **JWT tokens**
- Admin-only endpoints for managing users, drugs, and clinical trials
- Public endpoints for browsing drugs and clinical trials
- Order creation and automatic stock adjustment
- Database seeding with demo users and sample drugs
- Health check endpoint

---

## Tech Stack

- **Python 3.11+**
- **FastAPI** – web framework
- **SQLModel** – ORM and database models
- **SQLite** – default database
- **Passlib** – password hashing
- **Python-JOSE** – JWT authentication
- **Uvicorn** – ASGI server
- **Docker** – optional containerized deployment

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/pharma-api.git
cd pharma-api
```

### Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Initialize the database and seed demo data

```bash
python -m app.initial_data
```

### Run the API

```bash
uvicorn app.main:app --reload
```

Open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive API documentation.

---

## Usage

### 1. Authenticate

Obtain a JWT token using the demo admin credentials:

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=admin
password=adminpass
```

**Response:**

```json
{
  "access_token": "<your_token_here>",
  "token_type": "bearer"
}
```

Use this token to access **admin-only endpoints**.

### 2. Admin actions

- Create new users
- Add drugs and clinical trials

### 3. User actions

- List drugs and trials
- Place orders (authenticated)

---

## API Endpoints

| Endpoint          | Method | Auth          | Description                     |
|-----------------|--------|---------------|---------------------------------|
| `/auth/token`    | POST   | No            | Login and get JWT token          |
| `/users`         | POST   | Admin only    | Create new user                  |
| `/drugs`         | GET    | No            | List all drugs                   |
| `/drugs`         | POST   | Admin only    | Add a new drug                   |
| `/drugs/{id}`    | GET    | No            | Retrieve details of a drug       |
| `/trials`        | GET    | No            | List clinical trials             |
| `/trials`        | POST   | Admin only    | Add a clinical trial             |
| `/orders`        | POST   | Authenticated | Place an order                   |
| `/health`        | GET    | No            | Health check                     |

---

## Demo Data

**Users:**

- Admin: `admin / adminpass`
- Normal user: `Joe / pass123`

**Drugs:**

1. Small Molecule 01 – Cardiac support agent
2. Vaccine 01 – Antiviral for COVID19
3. Monoclonal Antibody 01 – Targeted therapeutic for oncology

---

## Docker

Build and run using Docker:

```bash
docker build -t pharma-api .
docker run -p 8000:8000 pharma-api
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## License

This project is provided for educational purposes and is open source.  
Feel free to use and modify as needed.

