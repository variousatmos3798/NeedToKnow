# Implementation Guide

## Getting Started

This guide provides step-by-step instructions to begin building NeedToKnow.

## Prerequisites

- Node.js 18+ or Python 3.10+
- PostgreSQL (or SQLite for development)
- API keys:
  - OpenAI API key (or Anthropic Claude)
  - YouTube API key (optional, for metadata)

## Phase 1: MVP Setup

### Step 1: Choose Your Stack

**Option A: Node.js/TypeScript Stack**
```bash
# Backend: Node.js + Express + TypeScript
# Frontend: Next.js + React + TypeScript
# Database: PostgreSQL + Prisma ORM
```

**Option B: Python Stack**
```bash
# Backend: FastAPI + Python
# Frontend: Next.js + React + TypeScript (or separate)
# Database: PostgreSQL + SQLAlchemy
```

### Step 2: Initialize Backend

#### Node.js Approach
```bash
mkdir needtoknow-backend
cd needtoknow-backend
npm init -y
npm install express cors dotenv
npm install -D typescript @types/node @types/express ts-node nodemon
npm install prisma @prisma/client
npm install axios
npm install openai  # or @anthropic-ai/sdk
```

#### Python Approach
```bash
mkdir needtoknow-backend
cd needtoknow-backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install fastapi uvicorn python-dotenv
pip install sqlalchemy psycopg2-binary
pip install openai  # or anthropic
pip install yt-dlp youtube-transcript-api
```

### Step 3: Initialize Frontend

```bash
npx create-next-app@latest needtoknow-frontend --typescript --tailwind --app
cd needtoknow-frontend
npm install axios
npm install @radix-ui/react-dialog @radix-ui/react-select
```

### Step 4: Set Up Database

#### With Prisma (Node.js)
```bash
npx prisma init
# Edit prisma/schema.prisma with models from PLAN.md
npx prisma migrate dev --name init
```

#### With SQLAlchemy (Python)
```python
# Create database.py with models
# Run migrations with Alembic
```

### Step 5: Create Core Services

#### Transcript Extraction Service

**Node.js:**
```typescript
// services/youtubeService.ts
import axios from 'axios';

export async function extractTranscript(videoId: string): Promise<string> {
  // Use youtube-transcript-api npm package
  // or yt-dlp via child_process
}
```

**Python:**
```python
# services/youtube_service.py
from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ' '.join([item['text'] for item in transcript])
```

#### AI Processing Service

**Node.js:**
```typescript
// services/aiService.ts
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function generateTutorial(
  transcript: string,
  topic: string
): Promise<Tutorial> {
  const prompt = `
    Convert this YouTube tutorial transcript into a step-by-step guide.
    Topic: ${topic}
    Transcript: ${transcript}
    
    Return a JSON object with:
    - steps: array of {number, title, description, details[]}
    - prerequisites: array of strings
    - estimatedTime: string
  `;
  
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    response_format: { type: 'json_object' }
  });
  
  return JSON.parse(response.choices[0].message.content);
}
```

**Python:**
```python
# services/ai_service.py
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tutorial(transcript: str, topic: str) -> dict:
    prompt = f"""
    Convert this YouTube tutorial transcript into a step-by-step guide.
    Topic: {topic}
    Transcript: {transcript}
    
    Return a JSON object with:
    - steps: array of {{number, title, description, details[]}}
    - prerequisites: array of strings
    - estimatedTime: string
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)
```

### Step 6: Create API Endpoints

#### Node.js (Express)
```typescript
// routes/videos.ts
import express from 'express';
import { extractTranscript } from '../services/youtubeService';

const router = express.Router();

router.post('/import', async (req, res) => {
  const { url } = req.body;
  const videoId = extractVideoId(url);
  const transcript = await extractTranscript(videoId);
  // Save to database
  res.json({ videoId, transcript });
});
```

#### Python (FastAPI)
```python
# routes/videos.py
from fastapi import APIRouter, HTTPException
from services.youtube_service import extract_transcript

router = APIRouter()

@router.post("/import")
async def import_video(url: str):
    video_id = extract_video_id(url)
    transcript = extract_transcript(video_id)
    # Save to database
    return {"video_id": video_id, "transcript": transcript}
```

### Step 7: Create Frontend Components

#### URL Input Component
```tsx
// components/URLInput.tsx
'use client';

import { useState } from 'react';
import axios from 'axios';

export default function URLInput() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('/api/videos/import', { url });
      // Handle success
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste YouTube URL here"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : 'Import'}
      </button>
    </form>
  );
}
```

## Phase 2: Topic Management

### Add Topic Model
- Create topics table
- Add topic creation endpoint
- Add UI for topic management

### Associate Videos with Topics
- Create junction table (topic_videos)
- Add endpoint to add video to topic
- Update UI to show topic selection

## Phase 3: Tutorial Refinement

### Implement Refinement Logic

```typescript
async function refineTutorial(
  existingTutorial: Tutorial,
  newTranscript: string
): Promise<Tutorial> {
  // 1. Generate tutorial from new transcript
  const newTutorial = await generateTutorial(newTranscript, topic);
  
  // 2. Compare steps semantically
  const mergedSteps = await mergeSteps(
    existingTutorial.steps,
    newTutorial.steps
  );
  
  // 3. Remove duplicates
  const deduplicatedSteps = await removeDuplicates(mergedSteps);
  
  // 4. Reorder logically
  const orderedSteps = await reorderSteps(deduplicatedSteps);
  
  return {
    ...existingTutorial,
    steps: orderedSteps,
    version: existingTutorial.version + 1
  };
}
```

### Semantic Similarity

Use embeddings to detect similar steps:

```typescript
import OpenAI from 'openai';

async function findSimilarSteps(
  step1: Step,
  step2: Step
): Promise<number> {
  const embedding1 = await getEmbedding(step1.description);
  const embedding2 = await getEmbedding(step2.description);
  return cosineSimilarity(embedding1, embedding2);
}
```

## Testing Strategy

### Unit Tests
- Test transcript extraction
- Test AI prompt generation
- Test step merging logic

### Integration Tests
- Test full video import flow
- Test tutorial generation
- Test refinement process

### E2E Tests
- Test user journey: import → create topic → refine

## Environment Variables

Create `.env` file:

```env
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/needtoknow
OPENAI_API_KEY=sk-...
YOUTUBE_API_KEY=... (optional)

# Frontend (if separate)
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## Deployment Checklist

- [ ] Set up production database
- [ ] Configure environment variables
- [ ] Set up CI/CD pipeline
- [ ] Configure rate limiting
- [ ] Set up monitoring/logging
- [ ] Test error handling
- [ ] Set up backup strategy

## Next Steps After MVP

1. Add user authentication (optional)
2. Implement export functionality
3. Add search capabilities
4. Improve AI prompts based on feedback
5. Add progress tracking
6. Implement sharing features

## Resources

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Prisma Documentation](https://www.prisma.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
