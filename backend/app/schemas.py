from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

# Video Schemas
class VideoCreate(BaseModel):
    youtube_url: str

class VideoResponse(BaseModel):
    id: int
    youtube_url: str
    video_id: str
    title: Optional[str]
    duration: Optional[int]
    channel_name: Optional[str]
    processed_at: datetime

    class Config:
        from_attributes = True

# Topic Schemas
class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    completeness_score: float
    created_at: datetime
    updated_at: Optional[datetime]
    videos: List[VideoResponse] = []

    class Config:
        from_attributes = True

# Tutorial Schemas
class TutorialStep(BaseModel):
    step_number: int
    title: str
    description: str
    details: List[str] = []

class TutorialContent(BaseModel):
    overview: str
    prerequisites: List[str] = []
    steps: List[TutorialStep] = []
    common_pitfalls: List[str] = []
    verification: List[str] = []

class TutorialResponse(BaseModel):
    id: int
    topic_id: int
    version: int
    content: Dict[Any, Any]
    created_at: datetime
    source_video_ids: Optional[List[int]]
    refinement_notes: Optional[str]

    class Config:
        from_attributes = True

class TutorialVersionResponse(BaseModel):
    id: int
    tutorial_id: int
    version: int
    content: Dict[Any, Any]
    changes_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Combined Response
class TopicWithTutorial(BaseModel):
    topic: TopicResponse
    tutorial: Optional[TutorialResponse]
    versions: List[TutorialVersionResponse] = []

# Request Schemas
class AddVideoToTopicRequest(BaseModel):
    youtube_url: str

class RefineRequest(BaseModel):
    force: bool = False
