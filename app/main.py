# Purpose: Main FastAPI application for PODVOX - Personalized Podcast Outreach Engine

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Dict, Any
import time
import os
from datetime import datetime

from app.config import settings
from app.models import (
    PodcastAnalysisRequest,
    MomentsExtractionRequest, 
    AskAnalysisRequest,
    VoicenoteGenerationRequest,
    SimpleScriptRequest,
    TextToSpeechRequest,
    VoicenoteCreationRequest,
    MomentsResponse,
    AskResponse,
    VoicenoteResponse,
    SimpleScriptResponse,
    TextToSpeechResponse,
    VoicenoteFileResponse,
    VoiceInfo,
    ErrorResponse
)
from app.services.sieve_service import sieve_service
from app.services.script_generator import script_generator

# Initialize ElevenLabs service conditionally
try:
    from app.services.elevenlabs_service import elevenlabs_service
    ELEVENLABS_AVAILABLE = True
except Exception as e:
    print(f"ElevenLabs service not available: {e}")
    ELEVENLABS_AVAILABLE = False

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Personalized Podcast Outreach Engine - Generate AI-powered voicenotes based on podcast content",
    debug=settings.debug
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "PODVOX: Personalized Podcast Outreach Engine",
        "docs_url": "/docs",
        "status": "active"
    }

@app.get("/healthcheck")
async def healthcheck():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version
    }

@app.post("/extract-moments", response_model=MomentsResponse)
async def extract_moments(request: MomentsExtractionRequest):
    """
    Extract key moments from a podcast using Sieve Moments API
    
    Based on documentation in SieveIntergrationHelp/momentsEndpoint.md
    """
    try:
        response = await sieve_service.extract_moments(
            podcast_url=str(request.podcast_url),
            queries=request.queries,
            min_clip_length=request.min_clip_length,
            start_time=request.start_time,
            end_time=request.end_time,
            render=request.render
        )
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract moments: {str(e)}"
        )

@app.post("/ask-about-content", response_model=AskResponse)
async def ask_about_content(request: AskAnalysisRequest):
    """
    Ask questions about podcast content using Sieve Ask API
    
    Based on documentation in SieveIntergrationHelp/askEndpoint.md
    """
    try:
        response = await sieve_service.ask_about_content(
            podcast_url=str(request.podcast_url),
            prompt=request.prompt,
            start_time=request.start_time,
            end_time=request.end_time,
            backend=request.backend
        )
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze content: {str(e)}"
        )

@app.post("/analyze-podcast")
async def analyze_podcast(request: PodcastAnalysisRequest):
    """
    Complete podcast analysis workflow: Extract moments + Get context
    
    This implements the workflow described in SampleData/exampleInput.md:
    1. Extract moments where the topic is discussed
    2. Use Ask API to get detailed context about those moments
    """
    try:
        result = await sieve_service.analyze_moments_with_context(
            podcast_url=str(request.podcast_url),
            prospect_name=request.prospect_name,
            query_topic=request.query_topic
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=404,
                detail=f"No relevant content found for topic: {request.query_topic}"
            )
        
        return {
            "prospect_name": request.prospect_name,
            "query_topic": request.query_topic,
            "moments_found": len(result["moments"]),
            "moments": result["moments"],
            "context_analysis": result["context_analysis"],
            "best_moment": result["best_moment"],
            "processing_info": result["processing_info"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze podcast: {str(e)}"
        )

@app.post("/generate-script")
async def generate_script(
    prospect_name: str,
    context_analysis: str,
    podcast_name: str = "",
    tone: str = "casual",
    target_length: int = 20
):
    """
    Generate a personalized voicenote script using OpenAI
    
    This is step 3 in the workflow: Send context to OpenAI to create a 20-second script
    """
    try:
        script = await script_generator.generate_voicenote_script(
            prospect_name=prospect_name,
            context_analysis=context_analysis,
            podcast_name=podcast_name,
            tone=tone,
            target_length=target_length
        )
        
        return {
            "prospect_name": prospect_name,
            "generated_script": script,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate script: {str(e)}"
        )

@app.post("/generate-simple-script", response_model=SimpleScriptResponse)
async def generate_simple_script(request: SimpleScriptRequest):
    """
    Simple script generation endpoint matching OpenAI-ScriptWriterDocs.md example
    
    This endpoint provides a direct implementation of the generate_script function
    shown in the documentation for creating concise, casual voicenote scripts.
    """
    try:
        script_text = await script_generator.generate_simple_script(
            name=request.name,
            context=request.context
        )
        
        return SimpleScriptResponse(
            name=request.name,
            script=script_text,
            word_count=len(script_text.split()),
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate simple script: {str(e)}"
        )

@app.post("/generate", response_model=VoicenoteResponse)
async def generate_voicenote(request: VoicenoteGenerationRequest):
    """
    Complete end-to-end voicenote generation pipeline
    
    Implements the full workflow from SampleData/exampleInput.md:
    1. Extract moments via Sieve where prospect talks about the topic
    2. Use Ask endpoint to get context around those moments  
    3. Send to OpenAI to make a 20-second script for voicenote
    4. Send script to ElevenLabs to make voicenote
    """
    processing_steps = []
    start_time = time.time()
    
    try:
        # Step 1: Analyze podcast content
        processing_steps.append("Starting podcast analysis...")
        
        analysis_result = await sieve_service.analyze_moments_with_context(
            podcast_url=str(request.podcast_url),
            prospect_name=request.prospect_name,
            query_topic=request.query_topic or "AI thoughts"
        )
        
        if not analysis_result["success"]:
            raise HTTPException(
                status_code=404,
                detail=f"No relevant content found for topic: {request.query_topic}"
            )
        
        processing_steps.append(f"Found {len(analysis_result['moments'])} relevant moments")
        
        # Step 2: Generate personalized script
        processing_steps.append("Generating personalized script...")
        
        script = await script_generator.generate_voicenote_script(
            prospect_name=request.prospect_name,
            context_analysis=analysis_result["context_analysis"],
            podcast_name=request.podcast_name,
            tone=request.tone,
            target_length=20
        )
        
        processing_steps.append("Script generated successfully")
        
        # Step 3: Generate voicenote with ElevenLabs
        voicenote_url = None
        if ELEVENLABS_AVAILABLE:
            processing_steps.append("Generating voicenote with ElevenLabs...")
            try:
                file_path = await elevenlabs_service.create_voicenote_file(
                    text=script.script,
                    output_path=None,  # Auto-generate temp file
                    file_format="mp3"
                )
                
                # Create download URL
                filename = os.path.basename(file_path)
                voicenote_url = f"/download-voicenote/{filename}"
                processing_steps.append(f"Voicenote generated: {filename}")
                
            except Exception as e:
                processing_steps.append(f"Voicenote generation failed: {str(e)}")
        else:
            processing_steps.append("ElevenLabs not available - script ready for voice generation")
        
        # Create response
        response = VoicenoteResponse(
            prospect_name=request.prospect_name,
            podcast_name=request.podcast_name,
            moments_found=analysis_result["moments"],
            context_analysis=analysis_result["context_analysis"],
            generated_script=script,
            voicenote_url=voicenote_url,
            processing_steps=processing_steps,
            success=True
        )
        
        processing_time = time.time() - start_time
        processing_steps.append(f"Total processing time: {processing_time:.2f} seconds")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate voicenote: {str(e)}"
        )

@app.post("/generate-complete-voicenote")
async def generate_complete_voicenote(
    prospect_name: str,
    podcast_url: str,
    podcast_name: str = "",
    query_topic: str = "AI thoughts",
    tone: str = "casual"
):
    """
    Complete pipeline endpoint matching SampleData/exampleInput.md workflow
    
    This endpoint demonstrates the exact workflow described in the sample data:
    1. Extract moments via Sieve where prospect talks about AI
    2. Use Ask endpoint to get context around those moments
    3. Send to OpenAI to make a 20-second script for voicenote
    4. Send script to ElevenLabs to make voicenote
    
    Returns: Complete voicenote ready for podcast outreach
    """
    processing_log = []
    start_time = time.time()
    
    try:
        processing_log.append("🎯 Step 1: Extracting AI discussion moments from podcast...")
        
        # Step 1 & 2: Sieve analysis (combined moments + ask)
        analysis_result = await sieve_service.analyze_moments_with_context(
            podcast_url=podcast_url,
            prospect_name=prospect_name,
            query_topic=query_topic
        )
        
        if not analysis_result["success"]:
            return {
                "success": False,
                "error": f"No {query_topic} discussion found in podcast",
                "processing_log": processing_log
            }
        
        processing_log.append(f"✅ Found {len(analysis_result['moments'])} relevant moments")
        processing_log.append(f"🧠 Best moment: {analysis_result['best_moment']['start_time']:.1f}s - {analysis_result['best_moment']['end_time']:.1f}s")
        
        processing_log.append("🎯 Step 2: Generating personalized 20-second script...")
        
        # Step 3: OpenAI script generation
        script = await script_generator.generate_simple_script(
            name=prospect_name,
            context=analysis_result["context_analysis"]
        )
        
        word_count = len(script.split())
        processing_log.append(f"✅ Generated {word_count}-word script")
        
        # Step 4: ElevenLabs voicenote generation
        voicenote_info = None
        if ELEVENLABS_AVAILABLE:
            processing_log.append("🎯 Step 3: Creating voicenote with ElevenLabs...")
            
            try:
                file_path = await elevenlabs_service.create_voicenote_file(
                    text=script,
                    output_path=None,
                    file_format="mp3"
                )
                
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                voicenote_info = {
                    "filename": filename,
                    "file_path": file_path,
                    "file_size_bytes": file_size,
                    "download_url": f"/download-voicenote/{filename}",
                    "duration_estimate_seconds": (word_count / 150) * 60  # ~150 words/min
                }
                
                processing_log.append(f"✅ Voicenote created: {filename} ({file_size} bytes)")
                
            except Exception as e:
                processing_log.append(f"❌ Voicenote generation failed: {str(e)}")
        else:
            processing_log.append("⚠️ ElevenLabs not available - script ready for manual voice generation")
        
        total_time = time.time() - start_time
        processing_log.append(f"🎉 Pipeline completed in {total_time:.1f} seconds")
        
        return {
            "success": True,
            "prospect_name": prospect_name,
            "podcast_name": podcast_name,
            "query_topic": query_topic,
            "moments_found": len(analysis_result['moments']),
            "context_analysis": analysis_result["context_analysis"],
            "generated_script": script,
            "script_word_count": word_count,
            "voicenote": voicenote_info,
            "processing_log": processing_log,
            "total_processing_time": total_time
        }
        
    except Exception as e:
        processing_log.append(f"❌ Pipeline failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "processing_log": processing_log
        }

# ElevenLabs Endpoints
@app.post("/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech using ElevenLabs API
    
    Returns audio data as bytes for immediate use
    """
    if not ELEVENLABS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs service not available. Check API keys and configuration."
        )
    
    start_time = time.time()
    
    try:
        audio_data = await elevenlabs_service.text_to_speech(
            text=request.text,
            voice_id=request.voice_id,
            model_id=request.model_id,
            voice_settings=request.voice_settings
        )
        
        generation_time = time.time() - start_time
        
        return TextToSpeechResponse(
            audio_size_bytes=len(audio_data),
            generation_time_seconds=generation_time,
            success=True,
            message="Audio generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate speech: {str(e)}"
        )

@app.post("/create-voicenote", response_model=VoicenoteFileResponse)
async def create_voicenote(request: VoicenoteCreationRequest):
    """
    Create a voicenote file from text using ElevenLabs
    
    Returns file path to the generated audio file
    """
    if not ELEVENLABS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs service not available. Check API keys and configuration."
        )
    
    try:
        # Use VoiceSettings model if provided, otherwise use defaults
        voice_settings_dict = None
        if request.voice_settings:
            voice_settings_dict = {
                "stability": request.voice_settings.stability,
                "similarity_boost": request.voice_settings.similarity_boost,
                "style": request.voice_settings.style,
                "use_speaker_boost": request.voice_settings.use_speaker_boost
            }
        
        file_path = await elevenlabs_service.create_voicenote_file(
            text=request.text,
            output_path=None,  # Auto-generate temp file
            file_format=request.output_format
        )
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Estimate duration (rough calculation: ~150 words per minute)
        word_count = len(request.text.split())
        duration_estimate = (word_count / 150) * 60  # Convert to seconds
        
        return VoicenoteFileResponse(
            file_path=file_path,
            file_size_bytes=file_size,
            duration_estimate_seconds=duration_estimate,
            voice_id=request.voice_id or settings.elevenlabs_voice_id,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create voicenote file: {str(e)}"
        )

@app.get("/download-voicenote/{filename}")
async def download_voicenote(filename: str):
    """
    Download a generated voicenote file
    
    This endpoint allows downloading voicenote files created by the /create-voicenote endpoint
    """
    import tempfile
    
    # Security: only allow files from temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    # Validate file exists and is safe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Voicenote file not found")
    
    if not file_path.startswith(temp_dir):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )

@app.get("/voice-info", response_model=VoiceInfo)
async def get_voice_info(voice_id: str = None):
    """
    Get information about the configured or specified voice
    """
    if not ELEVENLABS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs service not available. Check API keys and configuration."
        )
    
    try:
        voice_info = await elevenlabs_service.get_voice_info(voice_id)
        
        return VoiceInfo(
            voice_id=voice_info["voice_id"],
            name=voice_info["name"],
            category=voice_info.get("category", "unknown"),
            description=voice_info.get("description"),
            preview_url=voice_info.get("preview_url")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get voice info: {str(e)}"
        )

@app.get("/list-voices")
async def list_voices():
    """
    List all available ElevenLabs voices
    """
    if not ELEVENLABS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs service not available. Check API keys and configuration."
        )
    
    try:
        voices = await elevenlabs_service.list_voices()
        return voices
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list voices: {str(e)}"
        )

# Test endpoint for the specific message
@app.post("/test-steven-message")
async def test_steven_message():
    """
    Test endpoint to generate the specific Steven Bartlett voicenote
    
    Uses the exact text provided by the user for testing
    """
    if not ELEVENLABS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs service not available. Check API keys and configuration."
        )
    
    test_text = "Hey Steven! was just listening to your podcast with Sabba - you mentioned how you think AGI is only two years away. I have a few interesting takes, if you wanna to explore it more on the podcast, I can send over some more details about me! Thanks"
    
    try:
        file_path = await elevenlabs_service.create_voicenote_file(
            text=test_text,
            output_path=None,
            file_format="mp3"
        )
        
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        return {
            "message": "Test voicenote generated successfully!",
            "text": test_text,
            "file_path": file_path,
            "filename": filename,
            "file_size_bytes": file_size,
            "download_url": f"/download-voicenote/{filename}",
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test voicenote: {str(e)}"
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    ) 