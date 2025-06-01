# Purpose: OpenAI integration service for PODVOX - generates personalized voicenote scripts
# Enhanced to match specifications in OpenAI-ScriptWriterDocs.md

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
            # System prompt matching OpenAI-ScriptWriterDocs.md specifications
            system_prompt = """You are a personal outreach assistant that creates short, casual, conversational voicenote scripts for podcast outreach.

Your task is to:
- Write in natural, friendly spoken English — as if the user is recording a short, informal voice message.
- Mention the prospect's first name early in the script.
- Refer to a specific insight or moment from their podcast episode (provided as context).
- Keep it casual, slightly enthusiastic, suggesting a possible collaboration or follow-up.
- Make it sound personal, not scripted, and avoid formal email language.
- End with a light invitation to continue the conversation.

**Formatting Rules**:
- Write in first person.
- Avoid filler phrases like "I hope you're doing well" — get to the point quickly.
- Keep the voicenote under 60 words — concise and snappy."""
            
            # User message format matching the documentation
            user_message = f"Prospect Name: {prospect_name}\nPodcast Context: {context_analysis}"
            
            # Add podcast name if provided for more context
            if podcast_name:
                user_message += f"\nPodcast Name: {podcast_name}"
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                temperature=0.8,  # Higher creativity as specified in docs
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,  # Reduced since we want under 60 words
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Log word count for validation
            word_count = len(generated_text.split())
            logger.info(f"Generated script with {word_count} words")
            
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
    
    async def generate_simple_script(
        self,
        name: str,
        context: str
    ) -> GeneratedScript:
        """
        Simple script generation function matching the documentation example
        
        Args:
            name: Prospect's name
            context: Podcast context from Sieve analysis
            
        Returns:
            GeneratedScript object with the generated script
        """
        logger.info(f"Generating simple script for {name}")
        
        try:
            system_prompt = """You are a personal outreach assistant that creates short, casual, conversational voicenote scripts for podcast outreach.

Your task is to:
- Write in natural, friendly spoken English — as if the user is recording a short, informal voice message.
- Mention the prospect's first name early in the script.
- Refer to a specific insight or moment from their podcast episode (provided as context).
- Keep it casual, slightly enthusiastic, suggesting a possible collaboration or follow-up.
- Make it sound personal, not scripted, and avoid formal email language.
- End with a light invitation to continue the conversation.

**Formatting Rules**:
- Write in first person.
- Avoid filler phrases like "I hope you're doing well" — get to the point quickly.
- Keep the voicenote under 60 words — concise and snappy."""
            
            user_message = f"Prospect Name: {name}\nPodcast Context: {context}"
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                temperature=0.8,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            generated_text = response.choices[0].message.content.strip()
            word_count = len(generated_text.split())
            logger.info(f"Generated simple script: {word_count} words")
            
            # Return a proper GeneratedScript object
            script = GeneratedScript(
                script=generated_text,
                target_length_seconds=20,  # Default 20 seconds
                tone="casual",
                created_at=datetime.now()
            )
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating simple script: {str(e)}")
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
            Optimize this voicenote script for natural speech delivery while keeping it under 60 words:
            
            Original script:
            {script}
            
            Requirements:
            1. Should take approximately {target_length} seconds to speak naturally
            2. Use conversational language and contractions
            3. Add natural pauses where appropriate (indicate with commas)
            4. Remove any awkward phrasing
            5. Ensure smooth flow when spoken aloud
            6. Keep the core message and personalization intact
            7. Stay under 60 words maximum
            
            Return only the optimized script text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                temperature=0.3,  # Lower temperature for refinement
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            
            refined_script = response.choices[0].message.content.strip()
            logger.info("Successfully refined script for voice delivery")
            return refined_script
            
        except Exception as e:
            logger.error(f"Error refining script: {str(e)}")
            return script  # Return original if refinement fails

# Global service instance
script_generator = ScriptGeneratorService() 