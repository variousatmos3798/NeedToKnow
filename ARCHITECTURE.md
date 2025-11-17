# NeedToKnow - System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ URL Input    │  │ Topic View   │  │ Tutorial     │     │
│  │ Component    │  │ Dashboard    │  │ Viewer       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                      Backend Services                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Video Processing Service                      │  │
│  │  • YouTube Transcript Extraction                      │  │
│  │  • Transcript Cleaning                                │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI Processing Pipeline                       │  │
│  │  • Content Analysis                                   │  │
│  │  • Step Extraction                                    │  │
│  │  • Tutorial Generation                                │  │
│  │  • Tutorial Refinement                                │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Topic Management Service                     │  │
│  │  • Topic CRUD                                         │  │
│  │  • Video Association                                  │  │
│  │  • Version Control                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ PostgreSQL   │  │ Vector DB    │  │ Redis Cache  │     │
│  │ (Structured) │  │ (Semantic)   │  │ (Transcripts)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ YouTube API  │  │ OpenAI API   │  │ Embeddings   │     │
│  │ / yt-dlp     │  │ / Claude     │  │ Service      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Video Import Flow

```
User submits URL
    ↓
Backend validates URL
    ↓
Extract transcript (YouTube API / yt-dlp)
    ↓
Store transcript in cache (Redis)
    ↓
Store video metadata in DB
    ↓
Return video ID to frontend
```

### 2. Tutorial Generation Flow

```
Video transcript available
    ↓
Check if video belongs to existing topic
    ├─→ New Topic: Generate tutorial
    └─→ Existing Topic: Refine tutorial
    ↓
AI Processing:
  • Clean transcript
  • Extract key concepts
  • Identify steps
  • Structure tutorial
    ↓
Store tutorial version
    ↓
Update topic with new tutorial
```

### 3. Tutorial Refinement Flow

```
New video added to existing topic
    ↓
Load existing tutorial
    ↓
Process new video transcript
    ↓
Compare with existing steps (semantic similarity)
    ↓
AI Refinement:
  • Merge duplicate steps
  • Add missing steps
  • Resolve conflicts
  • Improve clarity
    ↓
Create new tutorial version
    ↓
Store version history
```

## Component Details

### Frontend Components

#### URLInput Component
- Input field for YouTube URL
- Validation (URL format, YouTube domain)
- Submit button
- Loading state during processing

#### TopicDashboard Component
- List of all topics
- Create new topic button
- Search/filter topics
- Topic cards with video count

#### TopicDetail Component
- Topic information
- Associated videos list
- Add video button
- Current tutorial display
- Version history

#### TutorialViewer Component
- Step-by-step display
- Prerequisites section
- Estimated time
- Export options
- Print-friendly view

### Backend Services

#### VideoService
```typescript
class VideoService {
  async importVideo(url: string): Promise<Video>
  async extractTranscript(videoId: string): Promise<string>
  async getVideoMetadata(videoId: string): Promise<VideoMetadata>
  async cleanTranscript(transcript: string): Promise<string>
}
```

#### TutorialService
```typescript
class TutorialService {
  async generateTutorial(transcript: string, topic: string): Promise<Tutorial>
  async refineTutorial(
    existingTutorial: Tutorial,
    newTranscript: string
  ): Promise<Tutorial>
  async mergeSteps(steps: Step[]): Promise<Step[]>
  async detectDuplicates(steps: Step[]): Promise<DuplicateGroup[]>
}
```

#### TopicService
```typescript
class TopicService {
  async createTopic(data: CreateTopicDto): Promise<Topic>
  async addVideoToTopic(topicId: string, videoId: string): Promise<Topic>
  async getTopicTutorial(topicId: string): Promise<Tutorial>
  async getTopicHistory(topicId: string): Promise<TutorialVersion[]>
}
```

### AI Processing Pipeline

#### Step 1: Transcript Cleaning
- Remove timestamps
- Remove filler words ("um", "uh", "like")
- Remove repeated phrases
- Normalize punctuation

#### Step 2: Content Analysis
- Extract key concepts
- Identify prerequisites
- Detect tutorial structure
- Find step indicators ("first", "then", "next")

#### Step 3: Step Extraction
- Parse natural language into steps
- Group related actions
- Order steps logically
- Extract details and tips

#### Step 4: Tutorial Generation/Refinement
- Structure steps with titles and descriptions
- Add prerequisites section
- Estimate completion time
- Generate tips and warnings

## Database Schema

### Topics Table
```sql
CREATE TABLE topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  tutorial_version INTEGER DEFAULT 1
);
```

### Videos Table
```sql
CREATE TABLE videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_id VARCHAR(20) UNIQUE NOT NULL,
  title VARCHAR(255),
  channel VARCHAR(255),
  duration INTEGER,
  transcript TEXT,
  processed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### TopicVideos Junction Table
```sql
CREATE TABLE topic_videos (
  topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
  video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
  added_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (topic_id, video_id)
);
```

### Tutorials Table
```sql
CREATE TABLE tutorials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  steps JSONB NOT NULL,
  prerequisites TEXT[],
  estimated_time VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(topic_id, version)
);
```

## API Design

### RESTful Endpoints

#### Videos
- `POST /api/videos/import` - Import YouTube URL
- `GET /api/videos/:id` - Get video details
- `GET /api/videos/:id/transcript` - Get transcript

#### Topics
- `GET /api/topics` - List all topics
- `POST /api/topics` - Create new topic
- `GET /api/topics/:id` - Get topic details
- `PUT /api/topics/:id` - Update topic
- `DELETE /api/topics/:id` - Delete topic

#### Topic Videos
- `POST /api/topics/:id/videos` - Add video to topic
- `DELETE /api/topics/:id/videos/:videoId` - Remove video from topic

#### Tutorials
- `GET /api/topics/:id/tutorial` - Get current tutorial
- `GET /api/topics/:id/tutorial/history` - Get version history
- `POST /api/topics/:id/refine` - Trigger manual refinement

## Security Considerations

1. **Input Validation**: Validate YouTube URLs, sanitize inputs
2. **Rate Limiting**: Prevent abuse of API endpoints
3. **API Keys**: Secure storage of external API keys
4. **CORS**: Configure properly for frontend access
5. **Error Handling**: Don't expose sensitive information in errors

## Performance Optimizations

1. **Caching**: Cache transcripts in Redis
2. **Queue System**: Process videos asynchronously
3. **Batch Processing**: Process multiple videos efficiently
4. **Lazy Loading**: Load tutorial versions on demand
5. **CDN**: Serve static assets via CDN

## Monitoring & Logging

- Track video processing times
- Monitor AI API usage and costs
- Log errors and failures
- Track user engagement metrics
- Alert on system failures
