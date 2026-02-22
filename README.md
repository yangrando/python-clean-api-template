# Python Clean API Template (FastAPI + Clean Architecture + AI Ready)

![CI](https://github.com/yangrando/python-clean-api-template/actions/workflows/python_ci.yml/badge.svg)

A production-grade FastAPI backend template following Clean Architecture principles, including authentication, LLM integration, structured logging, testing, and Docker support.

This project demonstrates backend engineering maturity, security best practices, and AI-ready architecture.

---

## 🎯 Purpose

This repository was created to showcase:

- Clean Architecture applied to backend systems
- FastAPI with proper dependency injection
- JWT authentication with secure password hashing
- LLM-ready abstraction layer
- Production-ready project structure
- Pytest-based testing strategy
- Environment-based configuration
- Dockerized deployment setup

This is not a tutorial-level project — it reflects real-world backend design decisions.

---

## 🏗 Architecture Overview

The project follows strict layer separation:

```
app/
  core/
  domain/
  usecases/
  infrastructure/
  api/
main.py
tests/
Dockerfile
requirements.txt
```

---

### 🔹 Core Layer
- Application configuration via Pydantic Settings
- Security utilities (JWT, hashing)
- Structured logging configuration

---

### 🔹 Domain Layer
- Pure Python entities
- Abstract repository interfaces
- No FastAPI or framework dependencies

---

### 🔹 Use Cases Layer
- Register user
- Login user
- Generate AI response
- Depends only on domain contracts

---

### 🔹 Infrastructure Layer
- In-memory repository implementation
- JWT token generation
- LLM service abstraction
- Simulated LLM implementation (AI-ready structure)

---

### 🔹 API Layer
- FastAPI routes
- Dependency injection
- Authentication guards
- Proper HTTP status handling
- Exception mapping

---

## 🔐 Authentication Flow

Endpoints:

- `POST /register`
- `POST /login`
- `GET /me` (protected)
- `POST /generate` (AI endpoint)

Security includes:

- JWT token with expiration
- Password hashing using passlib
- Dependency-based authentication guard

---

## 🤖 AI / LLM Integration

The project includes an abstraction layer for AI generation.

- `/generate` endpoint receives a prompt
- Calls LLM service abstraction
- Returns structured JSON response
- Simulated delay mimics real-world LLM latency
- Easily replaceable with OpenAI or other provider

This design keeps AI integration decoupled from business logic.

---

## 🧪 Testing Strategy

Testing is implemented using pytest.

Test coverage includes:

- User registration success
- Login success
- Login failure
- Protected route without token
- AI generation success

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Tests are independent of a running server and use dependency overrides where required.

---

## ⚙️ Configuration

Environment variables are loaded via Pydantic BaseSettings.

Example `.env`:

```
SECRET_KEY=supersecretkeythatisverystrong123
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

`.env.example` is included as a template.

---

## 🐳 Running with Docker

Build image:

```bash
docker build -t python-clean-api .
```

Run container:

```bash
docker run -p 8000:8000 python-clean-api
```

Application runs with Uvicorn on port 8000.

---

## 🚀 Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start server:

```bash
uvicorn main:app --reload
```

API documentation available at:

```
http://localhost:8000/docs
```

---

## 🛠 Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Pytest
- JWT (python-jose)
- Passlib
- Uvicorn
- Docker

---

## 🧠 Engineering Principles Applied

- Clean Architecture separation
- Dependency inversion
- Security-first configuration
- Explicit error modeling
- Structured logging
- Testability without server runtime
- AI-ready extensibility

---

## 📌 Why This Project Matters

Many backend templates online are simplistic or tightly coupled.

This repository demonstrates:

- Production-ready organization
- Real authentication handling
- AI abstraction layer
- Secure configuration management
- Scalable backend design

It reflects how I structure backend systems that support mobile applications and AI-driven products.

---

## 📫 Author

Yan Felipe Grando  
Senior Mobile Engineer | Fullstack Capable | AI-Oriented  
Flutter • iOS • FastAPI • Clean Architecture
