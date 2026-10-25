# AI Campus Helpdesk API

A REST API built with FastAPI and SQLAlchemy to help college students find FAQs and manage support tickets.

## Features

- FAQ CRUD operations
- Search FAQs by keyword
- Filter FAQs by category
- FAQ pagination
- Create and retrieve support tickets
- Filter tickets by status and category
- Search tickets by student name, title, or description
- Update ticket status
- Dashboard statistics
- Input validation
- Automated API tests using Pytest

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- HTTPX

## Project Structure

```text
AI-Campus-Helpdesk/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── faqs.py
│   ├── tickets.py
│   └── chatbot.py
├── tests/
│   └── test_api.py
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. Clone or download this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
python -m pip install fastapi "uvicorn[standard]" sqlalchemy python-dotenv openai pytest httpx
```

4. Start the API:

```bash
python -m uvicorn main:app --reload
```

5. Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## Run Automated Tests

```bash
python -m pytest tests/test_api.py -v
```

## Database

The project uses SQLite. The database file is created locally when the application initializes its tables.

## AI Chatbot

The chatbot endpoint is included. Live OpenAI-powered responses require a valid API key and available API credits. Without those, the chatbot may return an API configuration or billing error.

## Future Improvements

- Authentication and role-based access
- Admin dashboard
- More comprehensive automated tests
- Deployment to a cloud platform

## Author

Manik Chand
