# Purpose: OpenAI integration service for PODVOX - generates personalized voicenote scripts

import openai
from typing import Dict, Any
from app.config import settings
from app.models import GeneratedScript
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ScriptGeneratorService:
    """Service class for generating voicenote scripts using OpenAI"""
    
    def __init__(self):
        """Initialize OpenAI service with API key"""
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        logger.info("Script generator service initialized successfully")
    
    async def generate_voicenote_script(
        self,
        prospect_name: str,
        context_analysis: str,
        podcast_name: str = "",
        tone: str = "casual",
        target_length: int = 20
    ) -> GeneratedScript:
        """
        Generate a personalized voicenote script based on podcast analysis
        
        Args:
            prospect_name: Name of the prospect (e.g., "Steven Bartlett")
            context_analysis: Analysis from Sieve Ask API
            podcast_name: Name of the podcast (optional)
            tone: Tone of the script ("casual", "professional", "friendly")
            target_length: Target length in seconds (default 20)
            
        Returns:
            GeneratedScript with the generated voicenote content
        """
        logger.info(f"Generating script for {prospect_name}")
        logger.info(f"Tone: {tone}, Target length: {target_length}s")
        
        try:
            # Create the prompt based on the example voicenote style
            system_prompt = f"""
            You are an expert at creating personalized voicenote scripts for podcast outreach.
            
            Your task is to create a {target_length}-second voicenote script that:
            1. References specific content from their podcast episode
            2. Shows genuine interest and insight
            3. Offers value or connection
            4. Maintains a {tone} tone
            5. Ends with a clear call-to-action
            
            The script should sound natural when spoken aloud and feel personal, not generic.
            Target speaking pace: ~150 words per minute.
            """
            
            user_prompt = f"""
            Create a personalized voicenote script for {prospect_name}.
            
            Context from their podcast:
            {context_analysis}
            
            Podcast: {podcast_name if podcast_name else "their recent episode"}
            
            Style examples:
            - "Hey [Name], was just listening to your podcast where you mentioned [specific point]. It really resonated with me because [personal connection]. I'd love to [value proposition]. Let me know your thoughts."
            
            Make it sound authentic and conversational, like you're genuinely reaching out because their content inspired you.
            
            Target length: {target_length} seconds (approximately {target_length * 2.5:.0f} words)
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            script = GeneratedScript(
                script=generated_text,
                target_length_seconds=target_length,
                tone=tone,
                created_at=datetime.now()
            )
            
            logger.info("Successfully generated voicenote script")
            return script
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            raise Exception(f"Failed to generate script: {str(e)}")
    
    async def refine_script_for_voice(
        self,
        script: str,
        target_length: int = 20
    ) -> str:
        """
        Refine a script to be optimized for voice delivery
        
        Args:
            script: Original script text
            target_length: Target length in seconds
            
        Returns:
            Refined script optimized for speaking
        """
        logger.info("Refining script for voice delivery")
        
        try:
            prompt = f"""
            Optimize this voicenote script for natural speech delivery:
            
            Original script:
            {script}
            
            Requirements:
            1. Should take approximately {target_length} seconds to speak naturally
            2. Use conversational language and contractions
            3. Add natural pauses where appropriate (indicate with commas)
            4. Remove any awkward phrasing
            5. Ensure smooth flow when spoken aloud
            6. Keep the core message and personalization intact
            
            Return only the optimized script text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            refined_script = response.choices[0].message.content.strip()
            logger.info("Successfully refined script for voice delivery")
            return refined_script
            
        except Exception as e:
            logger.error(f"Error refining script: {str(e)}")
            return script  # Return original if refinement fails

# Global service instance
script_generator = ScriptGeneratorService() 