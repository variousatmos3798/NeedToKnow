# YouTube Tutorial Generator & Refiner - Project Plan

## Overview
An intelligent app that converts YouTube video tutorials into actionable step-by-step guides, with the ability to refine and improve instructions by analyzing multiple videos on the same topic.

## Core Features

### 1. Video Import & Processing
- Accept YouTube video URLs
- Extract video transcripts automatically
- Parse and clean transcript data
- Extract video metadata (title, duration, creator)

### 2. AI-Powered Tutorial Generation
- Convert transcripts into clear, actionable steps
- Identify key concepts and procedures
- Format steps with proper structure (prerequisites, main steps, verification)
- Generate concise summaries

### 3. Multi-Source Refinement (Key Feature)
- Group videos by topic/concept
- Analyze multiple transcripts for the same topic
- Identify complementary information
- Merge and refine instructions
- Fill gaps with specific details from various sources
- Maintain version history of refinements

### 4. Topic Management
- Create and organize topics
- Associate multiple videos with a topic
- Track which videos contributed to the final tutorial
- Show confidence/completeness score

## Technical Architecture

### Frontend
**Technology**: React/Next.js or Vue.js

**Components**:
- URL Input Form
- Topic Creator/Selector
- Tutorial Viewer (step-by-step display)
- Video List (sources for each topic)
- Refinement History Viewer
- Export Options (PDF, Markdown)

**Features**:
- Real-time processing status
- Diff viewer for tutorial updates
- Search and filter topics
- Responsive design

### Backend
**Technology**: Python (FastAPI) or Node.js (Express)

**Modules**:

1. **Video Service**
   - YouTube transcript extraction (youtube-transcript-api)
   - Video metadata extraction
   - URL validation
   - Caching layer for transcripts

2. **AI Service**
   - Integration with OpenAI/Anthropic API
   - Prompt engineering for tutorial generation
   - Prompt engineering for tutorial refinement
   - Context window management for long transcripts

3. **Tutorial Service**
   - Tutorial CRUD operations
   - Version management
   - Refinement logic (merging multiple sources)
   - Quality scoring

4. **Topic Service**
   - Topic CRUD operations
   - Video-topic associations
   - Tutorial-topic associations

### Database
**Technology**: PostgreSQL or MongoDB

**Schema**:

```
Topics
- id
- name
- description
- created_at
- updated_at
- completeness_score

Videos
- id
- youtube_url
- video_id
- title
- duration
- channel_name
- transcript_text
- processed_at
- metadata (JSON)

Topics_Videos (Junction)
- topic_id
- video_id
- added_at
- contribution_notes

Tutorials
- id
- topic_id
- version
- content (JSON structured steps)
- created_at
- source_video_ids (array)
- refinement_notes

Tutorial_Versions (History)
- id
- tutorial_id
- version
- content
- changes_summary
- created_at
```

### AI Prompting Strategy

#### Initial Tutorial Generation
```
Given this YouTube video transcript about [TOPIC], create a clear, actionable 
step-by-step tutorial. Format as:

1. Overview (what will be accomplished)
2. Prerequisites (tools, knowledge needed)
3. Step-by-step instructions (numbered, clear, actionable)
4. Common pitfalls to avoid
5. Verification steps (how to know it worked)

Make each step specific and actionable. If timestamps are available, reference them.
```

#### Tutorial Refinement
```
You are refining an existing tutorial by incorporating new information from 
additional video sources.

Current Tutorial: [EXISTING_TUTORIAL]
New Video Transcript: [NEW_TRANSCRIPT]

Tasks:
1. Identify new information not in the current tutorial
2. Identify contradictions or alternative approaches
3. Fill gaps in the existing tutorial
4. Add missing prerequisites or steps
5. Improve clarity with specific examples
6. Merge duplicate information

Output: Enhanced tutorial with change notes
```

## Implementation Phases

### Phase 1: MVP (2-3 weeks)
- [ ] Basic URL input and transcript extraction
- [ ] Single video to tutorial conversion
- [ ] Simple frontend to display results
- [ ] PostgreSQL database setup
- [ ] Basic API with FastAPI

### Phase 2: Multi-Source Refinement (2-3 weeks)
- [ ] Topic creation and management
- [ ] Associate multiple videos with topics
- [ ] Implement refinement algorithm
- [ ] Version history tracking
- [ ] Improved UI with diff viewer

### Phase 3: Polish & Features (2-3 weeks)
- [ ] Export functionality (PDF, Markdown)
- [ ] Search and filtering
- [ ] Quality scoring system
- [ ] Error handling and edge cases
- [ ] Performance optimization
- [ ] User accounts and saved topics

### Phase 4: Advanced Features
- [ ] Collaborative refinement (multiple users)
- [ ] AI-suggested related videos
- [ ] Integration with note-taking apps
- [ ] Browser extension for quick capture
- [ ] Playlist processing (batch multiple videos)

## Technical Challenges & Solutions

### Challenge 1: Transcript Availability
**Problem**: Not all YouTube videos have transcripts
**Solutions**:
- Use youtube-transcript-api library (handles auto-generated captions)
- Fallback to Whisper API for audio transcription
- Clear error messaging when unavailable

### Challenge 2: Long Transcripts (Context Window Limits)
**Problem**: Hour-long videos exceed AI context windows
**Solutions**:
- Chunk transcripts intelligently (by topic/section)
- Use summarization in first pass
- Implement map-reduce pattern for processing
- Use Claude 3.5 Sonnet (200K context) or GPT-4 Turbo

### Challenge 3: Merging Conflicting Information
**Problem**: Different videos might have contradictory approaches
**Solutions**:
- Present multiple approaches when they exist
- Use confidence scoring based on frequency
- Allow user to choose preferred method
- Flag contradictions for manual review

### Challenge 4: Quality Control
**Problem**: Generated tutorials might miss important details
**Solutions**:
- Implement quality scoring based on:
  - Completeness of steps
  - Presence of prerequisites
  - Verification steps included
  - Number of source videos
- Allow user feedback and manual editing
- A/B test different prompts

### Challenge 5: Incremental Updates
**Problem**: Adding new videos should intelligently update existing tutorials
**Solutions**:
- Use structured format (JSON) for tutorials
- Implement diff algorithm for changes
- Highlight what changed and why
- Allow users to accept/reject refinements

## Tech Stack Recommendation

### Option 1: Python Stack (Recommended for AI-heavy app)
- **Backend**: FastAPI
- **Frontend**: React with Next.js
- **Database**: PostgreSQL with SQLAlchemy
- **AI**: OpenAI API (GPT-4) or Anthropic (Claude)
- **Transcript**: youtube-transcript-api
- **Deployment**: Docker, Railway/Render/Fly.io

### Option 2: JavaScript Stack
- **Backend**: Node.js with Express
- **Frontend**: React with Next.js
- **Database**: PostgreSQL with Prisma
- **AI**: OpenAI API
- **Transcript**: youtube-transcript npm package
- **Deployment**: Vercel (frontend) + Railway (backend)

## API Endpoints (FastAPI Example)

```
POST   /api/videos/extract          # Extract transcript from URL
POST   /api/topics                   # Create new topic
GET    /api/topics                   # List all topics
GET    /api/topics/{id}              # Get topic with tutorial
POST   /api/topics/{id}/videos       # Add video to topic
POST   /api/topics/{id}/refine       # Trigger refinement
GET    /api/tutorials/{id}/versions  # Get version history
POST   /api/tutorials/{id}/export    # Export tutorial
```

## Environment Variables Needed

```
# AI Service
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Database
DATABASE_URL=

# Optional
YOUTUBE_API_KEY=  # For metadata if needed
REDIS_URL=        # For caching
```

## File Structure

```
youtube-tutorial-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── topic.py
│   │   │   ├── video.py
│   │   │   └── tutorial.py
│   │   ├── services/
│   │   │   ├── youtube_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── tutorial_service.py
│   │   │   └── refinement_service.py
│   │   ├── routes/
│   │   │   ├── videos.py
│   │   │   ├── topics.py
│   │   │   └── tutorials.py
│   │   └── utils/
│   │       ├── prompts.py
│   │       └── transcript_parser.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── URLInput.tsx
│   │   │   ├── TopicManager.tsx
│   │   │   ├── TutorialViewer.tsx
│   │   │   └── VersionHistory.tsx
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Next Steps to Start Implementation

1. **Set up development environment**
   - Install Python/Node.js
   - Set up virtual environment
   - Install dependencies

2. **Database setup**
   - Install PostgreSQL
   - Create database schema
   - Set up migrations

3. **Test YouTube transcript extraction**
   - Write script to test youtube-transcript-api
   - Handle edge cases

4. **Create initial AI prompts**
   - Test with sample transcripts
   - Iterate on prompt quality

5. **Build basic API**
   - Set up FastAPI project
   - Create video extraction endpoint
   - Create tutorial generation endpoint

6. **Build simple frontend**
   - URL input form
   - Display generated tutorial
   - Basic styling

Would you like me to start implementing any specific part of this plan?
