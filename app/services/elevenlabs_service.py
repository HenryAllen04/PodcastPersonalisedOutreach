# Purpose: ElevenLabs TTS integration service for PODVOX - converts text to voicenotes

import requests
import os
import tempfile
import time
from typing import Optional, Dict, Any
from pathlib import Path
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class ElevenLabsService:
    """Service class for ElevenLabs Text-to-Speech API integration"""
    
    def __init__(self):
        """Initialize ElevenLabs service with API credentials"""
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")
        if not self.voice_id:
            raise ValueError("ELEVENLABS_VOICE_ID environment variable is required")
            
        logger.info(f"ElevenLabs service initialized with voice ID: {self.voice_id}")
    
    async def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: str = "eleven_monolingual_v1",
        voice_settings: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Convert text to speech using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use (defaults to configured voice)
            model_id: ElevenLabs model to use
            voice_settings: Voice configuration settings
            
        Returns:
            Audio data as bytes
        """
        logger.info(f"Converting text to speech: {text[:100]}...")
        
        # Use provided voice_id or fall back to configured one
        voice_id = voice_id or self.voice_id
        
        # Default voice settings for natural speech
        if voice_settings is None:
            voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings
        }
        
        try:
            logger.info(f"Making request to ElevenLabs API...")
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                logger.info(f"Successfully generated {len(response.content)} bytes of audio")
                return response.content
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error calling ElevenLabs API: {str(e)}")
            raise Exception(f"Network error: {str(e)}")
    
    async def create_voicenote_file(
        self,
        text: str,
        output_path: Optional[str] = None,
        file_format: str = "mp3"
    ) -> str:
        """
        Create a voicenote file from text
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the file (if None, creates temp file)
            file_format: Audio format ('mp3', 'wav', etc.)
            
        Returns:
            Path to the created audio file
        """
        logger.info(f"Creating voicenote file for text: {text[:50]}...")
        
        # Generate audio data
        audio_data = await self.text_to_speech(text)
        
        # Determine output path
        if output_path is None:
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            timestamp = int(time.time())
            filename = f"voicenote_{timestamp}.{file_format}"
            output_path = os.path.join(temp_dir, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write audio data to file
        with open(output_path, 'wb') as audio_file:
            audio_file.write(audio_data)
        
        logger.info(f"Voicenote saved to: {output_path}")
        return output_path
    
    async def get_voice_info(self, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a voice
        
        Args:
            voice_id: Voice ID to get info for (defaults to configured voice)
            
        Returns:
            Voice information dictionary
        """
        voice_id = voice_id or self.voice_id
        url = f"{self.base_url}/voices/{voice_id}"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get voice info: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def list_voices(self) -> Dict[str, Any]:
        """
        List all available voices
        
        Returns:
            List of available voices
        """
        url = f"{self.base_url}/voices"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list voices: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")

# Create global service instance
elevenlabs_service = ElevenLabsService() 