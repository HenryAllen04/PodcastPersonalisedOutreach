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

# Error Models
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime 