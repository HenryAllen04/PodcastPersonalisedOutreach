# Purpose: Sieve API integration service for PODVOX - handles Moments and Ask endpoints

import sieve
import asyncio
import time
import os
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models import MomentResult, MomentsResponse, AskResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SieveService:
    """Service class for interacting with Sieve APIs"""
    
    def __init__(self):
        """Initialize Sieve service with environment variable authentication"""
        # Sieve now uses environment variable authentication
        # Make sure SIEVE_API_KEY is set in environment
        if not os.getenv('SIEVE_API_KEY'):
            os.environ['SIEVE_API_KEY'] = settings.sieve_api_key
        
        # Get function references
        self.moments_function = sieve.function.get("sieve/moments")
        self.ask_function = sieve.function.get("sieve/ask")
        
        logger.info("Sieve service initialized successfully with environment authentication")
    
    async def extract_moments(
        self,
        podcast_url: str,
        queries: List[str],
        min_clip_length: float = 10.0,
        start_time: float = 0,
        end_time: float = -1,
        render: bool = True
    ) -> MomentsResponse:
        """
        Extract moments from podcast using Sieve Moments API
        
        Args:
            podcast_url: URL of the podcast/video
            queries: List of search queries (e.g., ["AI thoughts", "artificial intelligence"])
            min_clip_length: Minimum clip length in seconds
            start_time: Start processing from this time
            end_time: End processing at this time (-1 for full video)
            render: Whether to render extracted clips
            
        Returns:
            MomentsResponse with extracted moments
        """
        start_process_time = time.time()
        logger.info(f"Starting moments extraction for: {podcast_url}")
        logger.info(f"Queries: {queries}")
        
        try:
            # Create Sieve File object
            video = sieve.File(url=podcast_url)
            
            all_moments = []
            
            # Process each query separately for better results
            for query in queries:
                logger.info(f"Processing query: '{query}'")
                
                # Use .push() for async processing as recommended by Sieve CTO
                job = self.moments_function.push(
                    video=video,
                    query=query,
                    min_clip_length=min_clip_length,
                    start_time=start_time,
                    end_time=end_time,
                    render=render
                )
                
                # Get results (this blocks until complete)
                results = job.result()
                
                # Convert generator to list
                results_list = list(results)
                
                # Process results into our format
                for result in results_list:
                    start_time = result.get('start_time', 0)
                    end_time = result.get('end_time', 0)
                    duration = end_time - start_time  # Calculate duration
                    
                    moment = MomentResult(
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        clip_url=result.get('clip_url'),  # Optional field
                        description=f"Query: {query}"
                    )
                    all_moments.append(moment)
                    
                logger.info(f"Found {len(results_list)} moments for query: '{query}'")
            
            processing_time = time.time() - start_process_time
            
            response = MomentsResponse(
                moments=all_moments,
                total_moments=len(all_moments),
                query=", ".join(queries),
                processing_time=processing_time
            )
            
            logger.info(f"Completed moments extraction. Total moments: {len(all_moments)}")
            return response
            
        except Exception as e:
            logger.error(f"Error in moments extraction: {str(e)}")
            raise Exception(f"Failed to extract moments: {str(e)}")
    
    async def ask_about_content(
        self,
        podcast_url: str,
        prompt: str,
        start_time: float = 0,
        end_time: float = -1,
        backend: str = "sieve-fast"
    ) -> AskResponse:
        """
        Ask questions about specific content using Sieve Ask API
        
        Args:
            podcast_url: URL of the podcast/video
            prompt: Question/instruction for content analysis
            start_time: Start analysis from this timestamp
            end_time: End analysis at this timestamp
            backend: Processing backend ("sieve-fast" or "sieve-contextual")
            
        Returns:
            AskResponse with analysis results
        """
        start_process_time = time.time()
        logger.info(f"Starting content analysis for: {podcast_url}")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Time range: {start_time}s to {end_time}s")
        
        try:
            # Create Sieve File object
            video = sieve.File(url=podcast_url)
            
            # Use .push() for async processing
            job = self.ask_function.push(
                video=video,
                prompt=prompt,
                start_time=start_time,
                end_time=end_time,
                backend=backend
            )
            
            # Get results
            result = job.result()
            
            processing_time = time.time() - start_process_time
            
            response = AskResponse(
                answer=result,
                context_start_time=start_time,
                context_end_time=end_time,
                backend_used=backend,
                processing_time=processing_time
            )
            
            logger.info("Completed content analysis")
            return response
            
        except Exception as e:
            logger.error(f"Error in content analysis: {str(e)}")
            raise Exception(f"Failed to analyze content: {str(e)}")
    
    async def analyze_moments_with_context(
        self,
        podcast_url: str,
        prospect_name: str,
        query_topic: str = "AI thoughts"
    ) -> Dict[str, Any]:
        """
        Complete workflow: Extract moments then analyze them for context
        Based on the example in SampleData/exampleInput.md
        
        Args:
            podcast_url: URL of the podcast
            prospect_name: Name of the person (e.g., "Steven Bartlett")  
            query_topic: What to search for (e.g., "AI thoughts")
            
        Returns:
            Dictionary with moments and context analysis
        """
        logger.info(f"Starting complete analysis for {prospect_name}")
        logger.info(f"Topic: {query_topic}")
        
        # Step 1: Extract moments where the topic is discussed
        moments_queries = [
            f"{query_topic}",
            f"artificial intelligence",
            f"AI technology",
            f"machine learning"
        ]
        
        moments_response = await self.extract_moments(
            podcast_url=podcast_url,
            queries=moments_queries,
            min_clip_length=15.0  # Longer clips for better context
        )
        
        if not moments_response.moments:
            logger.warning(f"No moments found for topic: {query_topic}")
            return {
                "moments": [],
                "context_analysis": "No relevant moments found",
                "success": False
            }
        
        # Step 2: Analyze the best moment for context
        best_moment = moments_response.moments[0]  # Take first/best result
        
        context_prompt = f"""
        Analyze this specific segment where {prospect_name} discusses {query_topic}. 
        Please provide:
        1. What specific points they made about {query_topic}
        2. Their opinion or stance on the topic
        3. Any personal experiences or insights they shared
        4. Key quotes or memorable phrases they used
        
        Format the response in a way that would help someone create a personalized outreach message.
        """
        
        context_response = await self.ask_about_content(
            podcast_url=podcast_url,
            prompt=context_prompt,
            start_time=best_moment.start_time,
            end_time=best_moment.end_time,
            backend=settings.sieve_backend
        )
        
        return {
            "moments": moments_response.moments,
            "context_analysis": context_response.answer,
            "best_moment": best_moment,
            "success": True,
            "processing_info": {
                "moments_found": len(moments_response.moments),
                "query_topic": query_topic,
                "prospect_name": prospect_name
            }
        }

# Global service instance
sieve_service = SieveService() 