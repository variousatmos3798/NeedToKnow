from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import get_db
from ..services.tutorial_service import TutorialService

router = APIRouter(prefix="/api/topics", tags=["topics"])

@router.post("", response_model=schemas.TopicResponse, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """Create a new topic"""
    service = TutorialService(db)
    new_topic = service.create_topic(topic)
    return new_topic

@router.get("", response_model=List[schemas.TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    """Get all topics"""
    service = TutorialService(db)
    topics = service.get_all_topics()
    return topics

@router.get("/{topic_id}", response_model=schemas.TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get a specific topic"""
    service = TutorialService(db)
    topic = service.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.put("/{topic_id}", response_model=schemas.TopicResponse)
def update_topic(topic_id: int, topic_data: schemas.TopicUpdate, db: Session = Depends(get_db)):
    """Update a topic"""
    service = TutorialService(db)
    topic = service.update_topic(topic_id, topic_data)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """Delete a topic"""
    service = TutorialService(db)
    success = service.delete_topic(topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return None

@router.post("/{topic_id}/videos", status_code=201)
def add_video_to_topic(
    topic_id: int, 
    request: schemas.AddVideoToTopicRequest, 
    db: Session = Depends(get_db)
):
    """Add a video to a topic and generate/refine tutorial"""
    service = TutorialService(db)
    try:
        result = service.add_video_to_topic(topic_id, request.youtube_url)
        return {
            "message": f"Video {result['action']} successfully",
            "video_id": result["video"].id,
            "tutorial_id": result["tutorial"].id,
            "tutorial_version": result["tutorial"].version,
            "action": result["action"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@router.get("/{topic_id}/tutorial", response_model=schemas.TutorialResponse)
def get_topic_tutorial(topic_id: int, db: Session = Depends(get_db)):
    """Get the latest tutorial for a topic"""
    from ..models import Tutorial
    tutorial = db.query(Tutorial).filter(
        Tutorial.topic_id == topic_id
    ).order_by(Tutorial.version.desc()).first()
    
    if not tutorial:
        raise HTTPException(status_code=404, detail="No tutorial found for this topic")
    return tutorial

@router.get("/{topic_id}/tutorial/versions", response_model=List[schemas.TutorialVersionResponse])
def get_tutorial_versions(topic_id: int, db: Session = Depends(get_db)):
    """Get all versions of a topic's tutorial"""
    from ..models import Tutorial
    tutorial = db.query(Tutorial).filter(
        Tutorial.topic_id == topic_id
    ).order_by(Tutorial.version.desc()).first()
    
    if not tutorial:
        raise HTTPException(status_code=404, detail="No tutorial found for this topic")
    
    service = TutorialService(db)
    versions = service.get_tutorial_versions(tutorial.id)
    return versions
