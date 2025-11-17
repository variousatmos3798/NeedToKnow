from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Junction table for many-to-many relationship between topics and videos
topic_videos = Table(
    'topic_videos',
    Base.metadata,
    Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True),
    Column('video_id', Integer, ForeignKey('videos.id'), primary_key=True),
    Column('added_at', DateTime(timezone=True), server_default=func.now())
)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    completeness_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    videos = relationship("Video", secondary=topic_videos, back_populates="topics")
    tutorials = relationship("Tutorial", back_populates="topic", cascade="all, delete-orphan")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    youtube_url = Column(String(500), nullable=False)
    video_id = Column(String(50), nullable=False, unique=True)
    title = Column(String(500))
    duration = Column(Integer)  # in seconds
    channel_name = Column(String(255))
    transcript_text = Column(Text)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)

    # Relationships
    topics = relationship("Topic", secondary=topic_videos, back_populates="videos")

class Tutorial(Base):
    __tablename__ = "tutorials"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    version = Column(Integer, default=1)
    content = Column(JSON, nullable=False)  # Structured steps as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    source_video_ids = Column(JSON)  # Array of video IDs that contributed
    refinement_notes = Column(Text)

    # Relationships
    topic = relationship("Topic", back_populates="tutorials")
    versions = relationship("TutorialVersion", back_populates="tutorial", cascade="all, delete-orphan")

class TutorialVersion(Base):
    __tablename__ = "tutorial_versions"

    id = Column(Integer, primary_key=True, index=True)
    tutorial_id = Column(Integer, ForeignKey('tutorials.id'), nullable=False)
    version = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    changes_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tutorial = relationship("Tutorial", back_populates="versions")
