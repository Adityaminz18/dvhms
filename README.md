# Hospital Management System

## Description
The **Hospital Management System** is a web-based application designed to streamline hospital operations. It provides an efficient way to manage patients, doctors, and appointments. The backend is powered by **FastAPI** with **SQLite** as the database, while the frontend is built using **Bolt.new**, a no-code website builder that communicates with the backend via REST APIs.

## Features
- **Patient Management**: Add, update, and view patient records.
- **Doctor Management**: Manage doctor profiles and specialties.
- **Appointment Booking**: Schedule, update, and cancel appointments.
- **Search Functionality**: Search for patients, doctors, or appointments.
- **Secure API Communication**: REST APIs for seamless frontend-backend interaction.

## Tech Stack
- **Backend**: FastAPI, SQLite
- **Frontend**: Bolt.new (No-code website builder)
- **API Communication**: REST APIs

## Installation Instructions
### Backend Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/hospital-management-system.git
    cd hospital-management-system
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
5. Access the API documentation at `http://127.0.0.1:8000/docs`.

### Frontend Setup
1. Use **Bolt.new** to design the frontend.
2. Configure the frontend to make REST API calls to the backend server.

## API Usage
- Ensure **CORS** is enabled in the FastAPI backend:
  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update with specific origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
  )
  ```
- Example API call using `fetch()` in JavaScript:
  ```javascript
  fetch('http://127.0.0.1:8000/patients', {
        method: 'GET',
        headers: {
             'Content-Type': 'application/json'
        }
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
  ```

## Directory Structure
```
Hospital Management System/
├── main.py                # Entry point for the FastAPI application
├── models/                # Database models
├── routers/               # API route definitions
├── database.py            # SQLite database connection
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Future Improvements
- Add user authentication and role-based access control.
- Implement advanced reporting and analytics.
- Integrate payment gateway for billing.
- Enhance UI/UX of the frontend.

## License
This project is licensed under the [MIT License](LICENSE).  
