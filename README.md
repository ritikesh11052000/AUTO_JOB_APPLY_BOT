# Auto Job Application Chatbot Backend

## Overview
This is the backend API for the Auto Job Application Chatbot. It provides core functionalities including user profile management, job listings, and application tracking.

## Tech Stack
- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Celery with Redis
- Async database support with databases package

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- PostgreSQL database
- Redis server for Celery

### Installation

1. Clone the repository

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup environment variables
Create a `.env` file in the root directory with the following:
```
DATABASE_URL=postgresql://user:password@localhost:5432/jobbot
REDIS_URL=redis://localhost:6379/0
```

5. Initialize the database
```bash
alembic upgrade head
```
(Or use the provided SQL schema to create tables manually)

6. Run the FastAPI server
```bash
uvicorn main:app --reload
```

7. Run Celery worker
```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

## API Endpoints

- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user details
- `POST /jobs/` - Add a new job listing
- `GET /jobs/` - List jobs
- `GET /jobs/{job_id}` - Get job details
- `POST /applications/` - Create a new application
- `GET /users/{user_id}/applications/` - List applications for a user

## Next Steps
- Implement job search module integration
- Implement resume generation and optimization
- Implement application auto-submission and tracking
- Add authentication and authorization
- Add unit and integration tests

## License
MIT License
