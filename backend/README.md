# YouTube Tutorial Generator - Backend

FastAPI backend for processing YouTube videos and generating tutorials using AI.

## Setup

1. **Install Python 3.9+**

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
- Get Anthropic API key from: https://console.anthropic.com/
- OR get OpenAI API key from: https://platform.openai.com/

```
ANTHROPIC_API_KEY=your_key_here
```

5. **Run the server**
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Endpoints

### Topics
- `POST /api/topics` - Create a new topic
- `GET /api/topics` - List all topics
- `GET /api/topics/{id}` - Get topic details
- `PUT /api/topics/{id}` - Update topic
- `DELETE /api/topics/{id}` - Delete topic

### Videos & Tutorials
- `POST /api/topics/{id}/videos` - Add video to topic (generates/refines tutorial)
- `GET /api/topics/{id}/tutorial` - Get latest tutorial for topic
- `GET /api/topics/{id}/tutorial/versions` - Get tutorial version history

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/              # API endpoints
│   │   ├── topics.py
│   │   └── videos.py
│   └── services/            # Business logic
│       ├── youtube_service.py    # YouTube transcript extraction
│       ├── ai_service.py         # AI tutorial generation
│       └── tutorial_service.py   # Tutorial management
└── run.py                   # Server startup script
```

## Technologies

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **youtube-transcript-api** - YouTube transcript extraction
- **Anthropic Claude** - AI for tutorial generation
- **SQLite** - Default database (easily switchable to PostgreSQL)

## Database

By default, uses SQLite (`tutorial_app.db`). To use PostgreSQL:

1. Install PostgreSQL
2. Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## AI Service

The app uses Claude 3.5 Sonnet by default for superior reasoning and long context support (200K tokens). You can also configure OpenAI GPT-4 by setting `OPENAI_API_KEY`.

## Development

Run with auto-reload:
```bash
python run.py
```

Run tests (coming soon):
```bash
pytest
```
