# Purpose: Main FastAPI application for PODVOX - Personalized Podcast Outreach Engine

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import time
from datetime import datetime

from app.config import settings
from app.models import (
    PodcastAnalysisRequest,
    MomentsExtractionRequest, 
    AskAnalysisRequest,
    VoicenoteGenerationRequest,
    MomentsResponse,
    AskResponse,
    VoicenoteResponse,
    ErrorResponse
)
from app.services.sieve_service import sieve_service
from app.services.script_generator import script_generator

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

@app.post("/generate", response_model=VoicenoteResponse)
async def generate_voicenote(request: VoicenoteGenerationRequest):
    """
    Complete end-to-end voicenote generation pipeline
    
    Implements the full workflow from SampleData/exampleInput.md:
    1. Extract moments via Sieve where prospect talks about the topic
    2. Use Ask endpoint to get context around those moments  
    3. Send to OpenAI to make a 20-second script for voicenote
    4. (Future) Send script to ElevenLabs to make voicenote
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
        
        # Step 3: Future - Generate voicenote with ElevenLabs
        processing_steps.append("Voicenote generation ready (ElevenLabs integration coming soon)")
        
        # Create response
        response = VoicenoteResponse(
            prospect_name=request.prospect_name,
            podcast_name=request.podcast_name,
            moments_found=analysis_result["moments"],
            context_analysis=analysis_result["context_analysis"],
            generated_script=script,
            voicenote_url=None,  # Will be populated when ElevenLabs is integrated
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

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            timestamp=datetime.now()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.now()
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    ) 