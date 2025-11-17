# Setup Guide - YouTube Tutorial Generator & Refiner

Complete step-by-step guide to get the app running on your machine.

## Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 18 or higher** - [Download](https://nodejs.org/)
- ✅ **Anthropic API Key** - [Get one here](https://console.anthropic.com/)

## Step 1: Clone or Download

If you haven't already, get the code:

```bash
git clone <your-repo-url>
cd youtube-tutorial-app
```

## Step 2: Backend Setup

### 2.1 Navigate to backend directory

```bash
cd backend
```

### 2.2 Create and activate virtual environment

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Python dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- SQLAlchemy - Database ORM
- youtube-transcript-api - Video transcript extraction
- anthropic - AI API client
- And other dependencies

### 2.4 Configure environment variables

```bash
cp .env.example .env
```

Open `.env` in a text editor and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
DATABASE_URL=sqlite:///./tutorial_app.db
HOST=0.0.0.0
PORT=8000
```

**Getting an Anthropic API Key:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy and paste into `.env`

### 2.5 Test the backend

```bash
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Visit http://localhost:8000 - you should see:
```json
{
  "message": "YouTube Tutorial Generator & Refiner API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

Visit http://localhost:8000/docs for interactive API documentation!

**Keep this terminal open** - the backend needs to stay running.

## Step 3: Frontend Setup

Open a **NEW terminal window** (keep backend running in the first one).

### 3.1 Navigate to frontend directory

```bash
cd frontend  # If starting from project root
```

### 3.2 Install Node.js dependencies

```bash
npm install
```

This will install:
- React - UI library
- Vite - Build tool
- Axios - HTTP client
- And other dependencies

This might take a minute or two.

### 3.3 Start the development server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

## Step 4: Open the App

1. Open your web browser
2. Go to: **http://localhost:3000**
3. You should see the YouTube Tutorial Generator interface!

## Step 5: Test It Out

1. **Create a Topic**
   - Click on the form in the sidebar
   - Enter a name like "Test Tutorial"
   - Click "Create Topic"

2. **Add a Video**
   - With your topic selected, find the "Add YouTube Video" section
   - Paste a YouTube URL (try a short tutorial video)
   - Click "Add Video"
   - Wait 30-60 seconds for processing

3. **View Your Tutorial**
   - Once processed, you'll see a structured tutorial
   - Overview, prerequisites, step-by-step instructions, etc.

4. **Add Another Video**
   - Add a second video on the same topic
   - Watch the tutorial get refined!
   - Check the "Version History" tab to see changes

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**"API key not found" error:**
- Check that `.env` file exists in `backend/` directory
- Verify `ANTHROPIC_API_KEY` is set correctly
- No spaces around the `=` sign

**Port 8000 already in use:**
```bash
# Change port in backend/.env
PORT=8001
```

### Frontend Issues

**"Cannot find module" errors:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**Port 3000 already in use:**
```bash
# Vite will automatically suggest 3001
# Or specify in vite.config.js
```

**"Failed to fetch" errors:**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify `src/services/api.js` has correct backend URL

### Video Processing Issues

**"Transcript not available":**
- Not all YouTube videos have transcripts/captions
- Try a different video that has captions
- Look for the CC icon on YouTube player

**Processing takes too long:**
- First request is always slower (AI model cold start)
- Hour-long videos take longer to process
- Check backend terminal for error messages

## Optional: Docker Setup

If you prefer Docker:

```bash
# From project root
docker-compose up
```

This will start both backend and frontend in containers.

## Next Steps

- Read the main [README.md](README.md) for usage tips
- Check [PROJECT_PLAN.md](PROJECT_PLAN.md) for technical details
- Explore the API docs at http://localhost:8000/docs

## Need Help?

- Check the logs in both terminal windows
- Look for error messages in browser console (F12)
- Verify all prerequisites are installed correctly
- Make sure API key has credits (Anthropic Console)

Happy tutorial generating! 🚀
