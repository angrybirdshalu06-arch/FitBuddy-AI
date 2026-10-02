# FitBuddy

FitBuddy is an AI-powered fitness and wellness
plan generator.

The application uses:

- Python
- FastAPI
- Jinja2
- SQLite
- SQLAlchemy
- Pydantic
- Google Gemini
- HTML
- CSS
- JavaScript


## Features

1. User registration/details form

2. AI-generated 7-day workout plan

3. Nutrition/recovery recommendation

4. Feedback-based plan modification

5. REST API

6. SQLite database

7. Admin dashboard

8. Responsive UI

9. Gemini integration

10. Mock AI mode for development


## Installation

Create virtual environment:

python -m venv .venv


Activate:

Windows PowerShell:

.venv\Scripts\Activate.ps1


Install dependencies:

pip install -r requirements.txt


## Configuration

Create .env.

Example:

GEMINI_API_KEY=your_api_key

MOCK_AI=false

ADMIN_KEY=my-admin-key


## Development without Gemini

Set:

MOCK_AI=true


Then run:

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000


## API documentation

Open:

http://127.0.0.1:8000/docs


## Run tests

pytest -q


## Admin dashboard

Open:

http://127.0.0.1:8000/view-all-users?admin_key=my-admin-key


## Main API endpoints

POST /api/plans

GET /api/users/{user_id}

POST /api/plans/{user_id}/feedback

GET /health


## Database

SQLite database:

fitbuddy.db


The database is created automatically
when the application starts.