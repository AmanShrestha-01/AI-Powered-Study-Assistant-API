# AI-Powered Study Assistant API

An API that uses Claude AI to generate summaries, quiz questions, and study guides from user-uploaded notes. Includes usage tracking to limit AI requests per user.

## Tech Stack

- Python, Flask
- SQLAlchemy, SQLite
- Claude AI (Anthropic API)
- JWT Authentication, Bcrypt
- Swagger API Documentation

## Features

- User signup and login with hashed passwords
- JWT token-based authentication
- Upload and manage study notes
- AI-generated summaries from notes
- AI-generated multiple choice quizzes
- AI-generated study guides
- Usage tracking with per-user limits
- Auto-generated API docs at /apidocs

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /signup | Create account |
| POST | /login | Log in, get token |
| POST | /notes | Upload notes |
| GET | /notes | List your notes |
| POST | /notes/:id/summary | Generate AI summary |
| POST | /notes/:id/quiz | Generate AI quiz |
| POST | /notes/:id/study-guide | Generate AI study guide |
| GET | /usage | Check remaining AI requests |

## Run Locally

```bash
git clone https://github.com/AmanShrestha-01/AI-Powered-Study-Assistant-API.git
cd AI-Powered-Study-Assistant-API
pip install -r requirements.txt
python app.py
```

Visit API docs: http://127.0.0.1:8000/apidocs

## Run Tests

```bash
python test_app.py
```
