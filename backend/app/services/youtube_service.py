from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from typing import Optional, Dict, Any

class YouTubeService:
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def get_transcript(video_id: str) -> Optional[str]:
        """Fetch transcript for a YouTube video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine all transcript segments
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            return full_transcript
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            raise Exception(f"Transcript not available for video {video_id}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")

    @staticmethod
    def get_video_metadata(video_id: str) -> Dict[str, Any]:
        """Get basic video metadata (without API key)"""
        # Note: For full metadata, you'd need YouTube Data API
        # This is a placeholder that returns basic info
        return {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }

    @classmethod
    def process_video(cls, youtube_url: str) -> Dict[str, Any]:
        """Complete video processing: extract ID, get transcript and metadata"""
        video_id = cls.extract_video_id(youtube_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        transcript = cls.get_transcript(video_id)
        metadata = cls.get_video_metadata(video_id)

        return {
            "video_id": video_id,
            "youtube_url": youtube_url,
            "transcript": transcript,
            "metadata": metadata
        }
