# Purpose: Pydantic models for PODVOX API requests and responses

from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

# Request Models
class PodcastAnalysisRequest(BaseModel):
    """Request model for podcast analysis with Sieve APIs"""
    prospect_name: str
    podcast_url: HttpUrl
    query_topic: str = "AI thoughts"  # Default based on example
    min_clip_length: Optional[float] = 10.0

class MomentsExtractionRequest(BaseModel):
    """Request model for Sieve Moments API"""
    podcast_url: HttpUrl
    queries: List[str]
    min_clip_length: Optional[float] = 10.0
    start_time: Optional[float] = 0
    end_time: Optional[float] = -1
    render: Optional[bool] = True

class AskAnalysisRequest(BaseModel):
    """Request model for Sieve Ask API"""
    podcast_url: HttpUrl
    prompt: str
    start_time: Optional[float] = 0
    end_time: Optional[float] = -1
    backend: Optional[str] = "sieve-fast"

class VoicenoteGenerationRequest(BaseModel):
    """Request model for full voicenote generation pipeline"""
    prospect_name: str
    podcast_name: str
    podcast_url: HttpUrl
    tone: Optional[str] = "casual"
    query_topic: Optional[str] = "AI thoughts"

class SimpleScriptRequest(BaseModel):
    """Request model for simple script generation matching OpenAI docs example"""
    name: str
    context: str

# ElevenLabs Models
class TextToSpeechRequest(BaseModel):
    """Request model for ElevenLabs text-to-speech conversion"""
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = "eleven_monolingual_v1"
    voice_settings: Optional[Dict[str, Any]] = None

class VoiceSettings(BaseModel):
    """ElevenLabs voice configuration settings"""
    stability: float = 0.5
    similarity_boost: float = 0.8
    style: float = 0.0
    use_speaker_boost: bool = True

class VoicenoteCreationRequest(BaseModel):
    """Request model for creating voicenote files"""
    text: str
    voice_id: Optional[str] = None
    output_format: Optional[str] = "mp3"
    voice_settings: Optional[VoiceSettings] = None

# Response Models
class MomentResult(BaseModel):
    """Individual moment extracted from podcast"""
    start_time: float
    end_time: float
    duration: float
    clip_url: Optional[str] = None
    description: Optional[str] = None

class MomentsResponse(BaseModel):
    """Response from Sieve Moments API"""
    moments: List[MomentResult]
    total_moments: int
    query: str
    processing_time: Optional[float] = None

class AskResponse(BaseModel):
    """Response from Sieve Ask API"""
    answer: str
    context_start_time: float
    context_end_time: float
    backend_used: str
    processing_time: Optional[float] = None

class GeneratedScript(BaseModel):
    """Generated voicenote script"""
    script: str
    target_length_seconds: int
    tone: str
    created_at: datetime

class SimpleScriptResponse(BaseModel):
    """Response model for simple script generation"""
    name: str
    script: str
    word_count: int
    success: bool = True

class VoicenoteResponse(BaseModel):
    """Complete voicenote generation response"""
    prospect_name: str
    podcast_name: str
    moments_found: List[MomentResult]
    context_analysis: str
    generated_script: GeneratedScript
    voicenote_url: Optional[str] = None
    processing_steps: List[str]
    success: bool = True

# ElevenLabs Response Models
class TextToSpeechResponse(BaseModel):
    """Response from ElevenLabs text-to-speech conversion"""
    audio_size_bytes: int
    generation_time_seconds: float
    success: bool = True
    message: Optional[str] = None

class VoicenoteFileResponse(BaseModel):
    """Response for voicenote file creation"""
    file_path: str
    file_size_bytes: int
    duration_estimate_seconds: Optional[float] = None
    voice_id: str
    success: bool = True

class VoiceInfo(BaseModel):
    """ElevenLabs voice information"""
    voice_id: str
    name: str
    category: str
    description: Optional[str] = None
    preview_url: Optional[str] = None

# Error Models
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime 