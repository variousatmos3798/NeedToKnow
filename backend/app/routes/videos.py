from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/api/videos", tags=["videos"])

@router.get("", response_model=List[schemas.VideoResponse])
def get_videos(db: Session = Depends(get_db)):
    """Get all processed videos"""
    videos = db.query(models.Video).all()
    return videos

@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get a specific video"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
