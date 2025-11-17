import os
from typing import Dict, Any, Optional
import json
from anthropic import Anthropic

class AIService:
    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if self.anthropic_key:
            self.client = Anthropic(api_key=self.anthropic_key)
            self.provider = "anthropic"
        elif self.openai_key:
            # OpenAI implementation would go here
            self.provider = "openai"
        else:
            raise ValueError("No AI API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")

    def generate_tutorial(self, transcript: str, topic_name: str, video_title: Optional[str] = None) -> Dict[str, Any]:
        """Generate initial tutorial from a single video transcript"""
        
        prompt = f"""You are an expert technical writer. Convert this YouTube video transcript into a clear, actionable step-by-step tutorial.

Topic: {topic_name}
{f'Video Title: {video_title}' if video_title else ''}

Transcript:
{transcript[:50000]}  # Limit to ~50k chars to stay within context

Create a structured tutorial with:
1. Overview (what will be accomplished)
2. Prerequisites (tools, knowledge, setup needed)
3. Step-by-step instructions (numbered, clear, actionable)
4. Common pitfalls to avoid
5. Verification steps (how to confirm success)

Make each step specific and actionable. Focus on the actual procedures demonstrated, not commentary.

Return your response as a JSON object with this exact structure:
{{
    "overview": "Brief description of what this tutorial accomplishes",
    "prerequisites": ["prerequisite 1", "prerequisite 2"],
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "What this step accomplishes",
            "details": ["specific action 1", "specific action 2"]
        }}
    ],
    "common_pitfalls": ["pitfall 1", "pitfall 2"],
    "verification": ["how to verify step 1 worked", "how to verify step 2 worked"]
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

        if self.provider == "anthropic":
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        else:
            # OpenAI implementation
            raise NotImplementedError("OpenAI implementation pending")

        # Parse JSON response
        try:
            tutorial_content = json.loads(content)
            return tutorial_content
        except json.JSONDecodeError:
            # If AI doesn't return pure JSON, try to extract it
            json_match = content.find('{')
            if json_match != -1:
                json_end = content.rfind('}') + 1
                tutorial_content = json.loads(content[json_match:json_end])
                return tutorial_content
            raise ValueError("Failed to parse AI response as JSON")

    def refine_tutorial(self, existing_tutorial: Dict[str, Any], new_transcript: str, 
                       topic_name: str, video_title: Optional[str] = None) -> Dict[str, Any]:
        """Refine existing tutorial by incorporating new video insights"""
        
        prompt = f"""You are an expert technical writer refining an existing tutorial with new information.

Topic: {topic_name}
{f'New Video Title: {video_title}' if video_title else ''}

EXISTING TUTORIAL:
{json.dumps(existing_tutorial, indent=2)}

NEW VIDEO TRANSCRIPT:
{new_transcript[:50000]}

Your task:
1. Identify NEW information not in the existing tutorial
2. Identify contradictions or alternative approaches
3. Fill gaps in the existing tutorial
4. Add missing prerequisites or steps
5. Improve clarity with specific examples from the new video
6. Merge duplicate or redundant information
7. Maintain the structure but enhance content

Return an IMPROVED tutorial with the same JSON structure:
{{
    "overview": "Enhanced overview",
    "prerequisites": ["enhanced prerequisites"],
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "Enhanced description",
            "details": ["more specific actions"]
        }}
    ],
    "common_pitfalls": ["enhanced pitfalls"],
    "verification": ["enhanced verification steps"]
}}

Also provide a summary of changes made.

Return as JSON with this structure:
{{
    "tutorial": {{ ... the enhanced tutorial ... }},
    "changes_summary": "Bullet list of what was added, improved, or changed"
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

        if self.provider == "anthropic":
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        else:
            raise NotImplementedError("OpenAI implementation pending")

        # Parse JSON response
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError:
            # Try to extract JSON
            json_match = content.find('{')
            if json_match != -1:
                json_end = content.rfind('}') + 1
                result = json.loads(content[json_match:json_end])
                return result
            raise ValueError("Failed to parse AI response as JSON")
