# NeedToKnow - YouTube Tutorial Generator & Refiner

## Project Overview

An AI-powered application that extracts YouTube video transcripts, synthesizes them into actionable step-by-step tutorials, and continuously refines tutorials as users add more related videos to the same topic.

## Core Features

### 1. YouTube Transcript Extraction
- Import YouTube video URLs
- Extract transcripts using YouTube API or web scraping
- Handle videos with/without captions
- Support multiple languages

### 2. AI-Powered Tutorial Generation
- Convert transcripts into structured, actionable steps
- Remove filler content, pauses, and conversational elements
- Organize steps logically
- Extract key concepts and prerequisites

### 3. Multi-Video Topic Aggregation
- Group videos by topic/concept
- Merge and synthesize information from multiple sources
- Identify overlapping and unique content
- Resolve conflicts between different approaches

### 4. Continuous Refinement
- Update existing tutorials when new videos are added
- Improve clarity and completeness
- Fill gaps in previous tutorials
- Maintain version history

### 5. User Interface
- Simple URL input
- Topic management (create, view, update topics)
- Step-by-step tutorial display
- Export capabilities (markdown, PDF, etc.)

## Architecture

### High-Level Flow

```
User Input (YouTube URL)
    ↓
Transcript Extraction Service
    ↓
Topic Matching/Grouping
    ↓
AI Processing Pipeline
    ├─→ New Topic → Generate Tutorial
    └─→ Existing Topic → Refine Tutorial
    ↓
Tutorial Storage & Display
```

### Component Breakdown

#### 1. **Frontend** (Web Application)
- **URL Input Component**: Paste YouTube URLs
- **Topic Dashboard**: View all topics and their associated videos
- **Tutorial Viewer**: Display step-by-step instructions
- **Video Management**: Add/remove videos from topics

#### 2. **Backend API**
- **Video Processing Service**: Handle transcript extraction
- **AI Service**: Process transcripts and generate/refine tutorials
- **Topic Management**: CRUD operations for topics
- **Storage Layer**: Database for topics, videos, and tutorials

#### 3. **AI Processing Pipeline**
- **Transcript Cleaner**: Remove filler words, timestamps, etc.
- **Content Analyzer**: Extract key concepts and steps
- **Tutorial Generator**: Create structured step-by-step guides
- **Tutorial Refiner**: Merge and improve existing tutorials

#### 4. **Data Storage**
- **Topics**: Topic metadata, associated video IDs
- **Videos**: Video metadata, transcripts, processing status
- **Tutorials**: Generated/refined tutorial content, version history

## Technical Stack Recommendations

### Frontend
- **Framework**: React/Next.js or Vue.js
- **UI Library**: Tailwind CSS + shadcn/ui or Material-UI
- **State Management**: Zustand or Redux Toolkit

### Backend
- **Runtime**: Node.js (Express/Fastify) or Python (FastAPI)
- **API**: RESTful API or GraphQL
- **Database**: PostgreSQL (for structured data) + Vector DB (for semantic search)

### AI/ML
- **LLM**: OpenAI GPT-4, Anthropic Claude, or local models (Llama 3)
- **Embeddings**: For semantic similarity (OpenAI embeddings or sentence-transformers)
- **Transcript Processing**: youtube-transcript-api or yt-dlp

### Infrastructure
- **Hosting**: Vercel/Netlify (frontend), Railway/Render (backend)
- **Queue System**: BullMQ or Celery (for async processing)
- **Caching**: Redis (for transcripts and API responses)

## Data Models

### Topic
```typescript
{
  id: string
  title: string
  description: string
  createdAt: Date
  updatedAt: Date
  videoIds: string[]
  tutorialVersion: number
}
```

### Video
```typescript
{
  id: string
  youtubeId: string
  title: string
  channel: string
  duration: number
  transcript: string
  processedAt: Date
  topicId: string
}
```

### Tutorial
```typescript
{
  id: string
  topicId: string
  version: number
  steps: Step[]
  prerequisites: string[]
  estimatedTime: string
  lastRefinedAt: Date
}

Step {
  number: number
  title: string
  description: string
  details: string[]
  tips?: string[]
  warnings?: string[]
}
```

## Implementation Phases

### Phase 1: MVP - Single Video Processing
- [ ] Set up project structure (frontend + backend)
- [ ] YouTube transcript extraction
- [ ] Basic AI prompt to convert transcript to steps
- [ ] Simple UI to input URL and display steps
- [ ] Basic storage (SQLite or PostgreSQL)

### Phase 2: Topic Management
- [ ] Topic creation and management
- [ ] Associate videos with topics
- [ ] Display all videos in a topic
- [ ] Basic tutorial merging (concatenate steps)

### Phase 3: Intelligent Refinement
- [ ] Semantic similarity detection
- [ ] Duplicate step detection and merging
- [ ] Conflict resolution between different approaches
- [ ] Gap identification and filling
- [ ] Version history tracking

### Phase 4: Enhanced Features
- [ ] Export tutorials (Markdown, PDF)
- [ ] Search functionality
- [ ] User authentication (optional)
- [ ] Sharing capabilities
- [ ] Progress tracking

### Phase 5: Advanced AI Features
- [ ] Better context understanding
- [ ] Prerequisite detection
- [ ] Difficulty estimation
- [ ] Time estimation
- [ ] Visual aids extraction (screenshots/timestamps)

## Key Challenges & Solutions

### Challenge 1: Transcript Quality
- **Problem**: Some videos have poor/no transcripts
- **Solution**: Fallback to speech-to-text APIs, allow manual transcript upload

### Challenge 2: Multiple Approaches Conflict
- **Problem**: Different videos show different ways to do the same thing
- **Solution**: Present alternatives, let user choose, or merge common steps

### Challenge 3: Context Loss
- **Problem**: Transcripts lack visual context
- **Solution**: Extract timestamps for key steps, link back to video moments

### Challenge 4: Cost Management
- **Problem**: LLM API calls can be expensive
- **Solution**: Cache results, batch processing, use cheaper models for simple tasks

### Challenge 5: Scalability
- **Problem**: Processing multiple videos simultaneously
- **Solution**: Queue system, background workers, rate limiting

## API Endpoints (Proposed)

```
POST   /api/videos/import          - Import YouTube URL
GET    /api/videos/:id             - Get video details
GET    /api/videos/:id/transcript  - Get transcript

POST   /api/topics                 - Create topic
GET    /api/topics                 - List all topics
GET    /api/topics/:id             - Get topic details
PUT    /api/topics/:id             - Update topic
DELETE /api/topics/:id             - Delete topic
POST   /api/topics/:id/videos      - Add video to topic

GET    /api/topics/:id/tutorial    - Get current tutorial
GET    /api/topics/:id/tutorial/history - Get version history
POST   /api/topics/:id/refine      - Trigger manual refinement
```

## Environment Variables

```env
# YouTube API (optional, for metadata)
YOUTUBE_API_KEY=

# AI Provider
OPENAI_API_KEY=
# OR
ANTHROPIC_API_KEY=

# Database
DATABASE_URL=

# Redis (optional, for caching)
REDIS_URL=

# App
NODE_ENV=development
PORT=3000
```

## Next Steps

1. **Choose Tech Stack**: Decide on frontend/backend frameworks
2. **Set Up Project**: Initialize repositories, install dependencies
3. **Build MVP**: Start with Phase 1 - single video processing
4. **Test with Real Videos**: Use actual YouTube tutorials
5. **Iterate**: Refine based on results

## Example Use Case

**User Journey:**
1. User wants to learn "How to use Cursor 2.0"
2. Finds 3 YouTube videos:
   - Video 1: "Cursor 2.0 Overview" (30 min)
   - Video 2: "Advanced Cursor Features" (45 min)
   - Video 3: "Cursor Setup Guide" (15 min)
3. User creates topic "Cursor 2.0 Tutorial"
4. Imports all 3 URLs
5. App processes each video:
   - Extracts transcripts
   - Generates steps from Video 1
   - Adds/refines steps from Video 2
   - Merges and improves with Video 3
6. User gets comprehensive step-by-step guide covering all aspects

## Success Metrics

- Accuracy of extracted steps
- Time saved vs watching videos
- User satisfaction with tutorial quality
- Number of videos successfully processed
- Tutorial refinement improvement over time
