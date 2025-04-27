# 🏥 Hospital Management System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-brightgreen)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue)
![Deployed](https://img.shields.io/badge/Deployment-Render.com-orange)

> Fullstack Dockerized Hospital Management System — FastAPI backend + Static Frontend (HTML/CSS/JS) 🚀

---

## 📚 Table of Contents

- [Project Description](#-project-description)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Local Deployment](#-local-deployment-docker-compose)
- [Render Deployment](#-render-deployment)
- [API Endpoints Overview](#-api-endpoints-overview)
- [Environment Variables](#-environment-variables)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Support](#-support)

---

## 📋 Project Description

The **Hospital Management System** streamlines hospital operations by managing Patients, Doctors, and Appointments.  
Built with **FastAPI** backend, **SQLite** database, and a simple static **frontend with nginx**, all fully containerized with Docker.

---

## ✅ Features

- Manage Patients, Doctors, Appointments
- Secure Authentication (JWT)
- Admin, Doctor, Patient roles
- Search & filter functionality
- REST API-first approach
- Full API Documentation (`/api/docs`)
- Production-ready Docker deployment

---

## 📋 Tech Stack

| Layer            | Technology |
|------------------|-------------|
| Backend          | FastAPI, SQLAlchemy |
| Frontend         | HTML5, CSS3, JavaScript |
| Database         | SQLite |
| Web Server       | nginx |
| Containerization | Docker, Docker Compose |
| Deployment       | Render.com |

---

## 📂 Project Structure

```
dvhms/
├── backend/                # FastAPI backend
├── database/                # Database config
├── models/                  # SQLAlchemy models
├── routers/                 # API endpoints
├── frontend/                # Static frontend (HTML/CSS/JS)
├── auth.py                  # Auth helpers
├── main.py                  # App entrypoint
├── Dockerfile               # Combined Dockerfile (Backend + Frontend)
├── Dockerfile.backend       # Backend-only Dockerfile
├── Dockerfile.frontend      # Frontend-only Dockerfile
├── docker-compose.yml       # For local development
├── nginx.conf               # nginx configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # Documentation
```

---

## 🖼️ Screenshots

> _Coming soon..._ (Add frontend screenshots here)

---

## 🐳 Local Deployment (Docker Compose)

```bash
git clone https://github.com/Adityaminz18/dvhms.git
cd dvhms
cp .env.example .env
docker-compose up --build
```

- Frontend: http://localhost
- Backend API: http://localhost:8000/api
- Swagger Docs: http://localhost/api/docs

---

## 🚀 Render Deployment

> Deploy easily on [Render.com](https://render.com/)

1. Connect your GitHub repo to Render.
2. Create a **New Web Service**.
3. Environment: **Docker**.
4. Set environment variables: `ENV`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
5. Expose **Port 80**.
6. Deploy and enjoy 🚀.

---

## 📢 API Endpoints Overview

| Entity        | Endpoint |
|---------------|----------|
| Auth          | `/api/auth/login`, `/api/auth/signup` |
| Users         | `/api/users` |
| Doctors       | `/api/doctors` |
| Patients      | `/api/patients` |
| Appointments  | `/api/appointments` |
| API Docs      | `/api/docs` |

---

## ⚙️ Environment Variables

| Variable | Description |
|:---------|:------------|
| ENV | `development` or `production` |
| SECRET_KEY | Secret key for JWT tokens |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time in minutes |

> Set these manually in Render dashboard or `.env` file locally.

---

## 🔮 Future Enhancements

- Password reset & email verification
- Advanced dashboard & analytics
- Move to PostgreSQL (production database)
- Real-time notifications system

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## ⭐ Support

If you find this project useful, please consider giving a ⭐ on [GitHub](https://github.com/Adityaminz18/dvhms)!
