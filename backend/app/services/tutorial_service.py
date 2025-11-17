from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .. import models, schemas
from .youtube_service import YouTubeService
from .ai_service import AIService

class TutorialService:
    def __init__(self, db: Session):
        self.db = db
        self.youtube_service = YouTubeService()
        self.ai_service = AIService()

    def create_topic(self, topic_data: schemas.TopicCreate) -> models.Topic:
        """Create a new topic"""
        topic = models.Topic(
            name=topic_data.name,
            description=topic_data.description
        )
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def get_topic(self, topic_id: int) -> Optional[models.Topic]:
        """Get a topic by ID"""
        return self.db.query(models.Topic).filter(models.Topic.id == topic_id).first()

    def get_all_topics(self) -> List[models.Topic]:
        """Get all topics"""
        return self.db.query(models.Topic).all()

    def update_topic(self, topic_id: int, topic_data: schemas.TopicUpdate) -> Optional[models.Topic]:
        """Update a topic"""
        topic = self.get_topic(topic_id)
        if not topic:
            return None
        
        if topic_data.name is not None:
            topic.name = topic_data.name
        if topic_data.description is not None:
            topic.description = topic_data.description
        
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic"""
        topic = self.get_topic(topic_id)
        if not topic:
            return False
        
        self.db.delete(topic)
        self.db.commit()
        return True

    def add_video_to_topic(self, topic_id: int, youtube_url: str) -> Dict[str, Any]:
        """Add a video to a topic and generate/refine tutorial"""
        topic = self.get_topic(topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")

        # Process video
        video_data = self.youtube_service.process_video(youtube_url)
        
        # Check if video already exists
        existing_video = self.db.query(models.Video).filter(
            models.Video.video_id == video_data["video_id"]
        ).first()

        if existing_video:
            # Check if already associated with this topic
            if existing_video in topic.videos:
                raise ValueError("Video already added to this topic")
            video = existing_video
        else:
            # Create new video record
            video = models.Video(
                youtube_url=video_data["youtube_url"],
                video_id=video_data["video_id"],
                transcript_text=video_data["transcript"],
                title=video_data["metadata"].get("title"),
                channel_name=video_data["metadata"].get("channel_name"),
                duration=video_data["metadata"].get("duration"),
                metadata=video_data["metadata"]
            )
            self.db.add(video)
            self.db.commit()
            self.db.refresh(video)

        # Associate video with topic
        topic.videos.append(video)
        self.db.commit()

        # Generate or refine tutorial
        tutorial = self._generate_or_refine_tutorial(topic, video)

        return {
            "video": video,
            "tutorial": tutorial,
            "action": "refined" if len(topic.videos) > 1 else "created"
        }

    def _generate_or_refine_tutorial(self, topic: models.Topic, new_video: models.Video) -> models.Tutorial:
        """Generate new tutorial or refine existing one"""
        # Get existing tutorial for this topic
        existing_tutorial = self.db.query(models.Tutorial).filter(
            models.Tutorial.topic_id == topic.id
        ).order_by(models.Tutorial.version.desc()).first()

        if not existing_tutorial:
            # Generate initial tutorial
            tutorial_content = self.ai_service.generate_tutorial(
                transcript=new_video.transcript_text,
                topic_name=topic.name,
                video_title=new_video.title
            )

            tutorial = models.Tutorial(
                topic_id=topic.id,
                version=1,
                content=tutorial_content,
                source_video_ids=[new_video.id],
                refinement_notes="Initial tutorial generated"
            )
            self.db.add(tutorial)
            self.db.commit()
            self.db.refresh(tutorial)

            # Update topic completeness
            topic.completeness_score = self._calculate_completeness(tutorial_content)
            self.db.commit()

            return tutorial
        else:
            # Refine existing tutorial
            result = self.ai_service.refine_tutorial(
                existing_tutorial=existing_tutorial.content,
                new_transcript=new_video.transcript_text,
                topic_name=topic.name,
                video_title=new_video.title
            )

            # Save old version to history
            old_version = models.TutorialVersion(
                tutorial_id=existing_tutorial.id,
                version=existing_tutorial.version,
                content=existing_tutorial.content,
                changes_summary=f"Version before adding video: {new_video.title or new_video.video_id}"
            )
            self.db.add(old_version)

            # Update tutorial with refined content
            existing_tutorial.version += 1
            existing_tutorial.content = result["tutorial"]
            existing_tutorial.refinement_notes = result["changes_summary"]
            
            # Add new video ID to sources
            source_ids = existing_tutorial.source_video_ids or []
            if new_video.id not in source_ids:
                source_ids.append(new_video.id)
            existing_tutorial.source_video_ids = source_ids

            self.db.commit()
            self.db.refresh(existing_tutorial)

            # Update topic completeness
            topic.completeness_score = self._calculate_completeness(existing_tutorial.content)
            self.db.commit()

            return existing_tutorial

    def _calculate_completeness(self, tutorial_content: Dict[str, Any]) -> float:
        """Calculate completeness score based on tutorial content"""
        score = 0.0
        
        # Check for overview
        if tutorial_content.get("overview"):
            score += 0.2
        
        # Check for prerequisites
        if tutorial_content.get("prerequisites") and len(tutorial_content["prerequisites"]) > 0:
            score += 0.15
        
        # Check for steps (most important)
        steps = tutorial_content.get("steps", [])
        if len(steps) > 0:
            score += 0.4
            # Bonus for detailed steps
            if len(steps) >= 5:
                score += 0.1
        
        # Check for common pitfalls
        if tutorial_content.get("common_pitfalls") and len(tutorial_content["common_pitfalls"]) > 0:
            score += 0.1
        
        # Check for verification
        if tutorial_content.get("verification") and len(tutorial_content["verification"]) > 0:
            score += 0.15
        
        return min(score, 1.0)

    def get_tutorial_versions(self, tutorial_id: int) -> List[models.TutorialVersion]:
        """Get all versions of a tutorial"""
        return self.db.query(models.TutorialVersion).filter(
            models.TutorialVersion.tutorial_id == tutorial_id
        ).order_by(models.TutorialVersion.version.desc()).all()
