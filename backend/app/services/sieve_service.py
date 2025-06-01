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
        logger.info(f"SIEVE_API_KEY present: {bool(os.getenv('SIEVE_API_KEY'))}")
    
    async def extract_moments(
        self,
        podcast_url: str,
        queries: List[str],
        min_clip_length: float = 10.0,
        start_time: float = 0,
        end_time: float = -1,
        render: bool = False  # Keep False for better performance as requested
    ) -> MomentsResponse:
        """
        Extract moments from podcast using Sieve Moments API
        
        Args:
            podcast_url: URL of the podcast/video
            queries: List of search queries (e.g., ["AI thoughts", "artificial intelligence"])
            min_clip_length: Minimum clip length in seconds
            start_time: Start processing from this time
            end_time: End processing at this time (-1 for full video)
            render: Whether to render extracted clips (False = metadata only, faster)
            
        Returns:
            MomentsResponse with extracted moments
        """
        start_process_time = time.time()
        logger.info("="*80)
        logger.info(f"🎯 STARTING SIEVE MOMENTS EXTRACTION")
        logger.info(f"📺 Podcast URL: {podcast_url}")
        logger.info(f"🔍 Queries: {queries}")
        logger.info(f"⏱️  Min clip length: {min_clip_length}s")
        logger.info(f"🎬 Render clips: {render}")
        logger.info(f"📊 Time range: {start_time}s to {end_time}s")
        logger.info("="*80)
        
        try:
            # Create Sieve File object
            logger.info(f"📁 Creating Sieve File object...")
            video = sieve.File(url=podcast_url)
            logger.info(f"✅ Sieve File created successfully")
            
            all_moments = []
            
            # Process each query separately for better results
            for i, query in enumerate(queries, 1):
                logger.info(f"\n🔍 Processing query {i}/{len(queries)}: '{query}'")
                logger.info(f"⏳ Pushing job to Sieve...")
                
                # Use .push() for async processing as recommended by Sieve CTO
                job = self.moments_function.push(
                    video=video,
                    query=query,
                    min_clip_length=min_clip_length,
                    start_time=start_time,
                    end_time=end_time,
                    render=render
                )
                
                logger.info(f"🚀 Job pushed! Job running in background...")
                logger.info(f"⏳ Waiting for results (this may take 2-5 minutes)...")
                
                # Get results (this blocks until complete)
                query_start_time = time.time()
                results = job.result()
                query_processing_time = time.time() - query_start_time
                
                logger.info(f"✅ Query '{query}' completed in {query_processing_time:.1f}s")
                
                # Convert generator to list
                results_list = list(results)
                logger.info(f"📋 Raw results count: {len(results_list)}")
                
                # Log each result for debugging
                for j, result in enumerate(results_list):
                    logger.info(f"📄 Result {j+1}: {result}")
                    logger.info(f"📄 Result type: {type(result)}")
                
                # Process results into our format
                for j, result in enumerate(results_list):
                    try:
                        if render:
                            # When render=True: result is tuple of (clip, metadata)
                            logger.info(f"🎬 Processing rendered result {j+1} (tuple format)")
                            clip, metadata = result
                            logger.info(f"🎬 Clip: {clip}")
                            logger.info(f"📊 Metadata: {metadata}")
                            start_time_val = metadata.get('start_time', 0)
                            end_time_val = metadata.get('end_time', 0)
                            clip_url = clip.url if hasattr(clip, 'url') else None
                        else:
                            # When render=False: result is just metadata dict
                            logger.info(f"📊 Processing metadata-only result {j+1}")
                            metadata = result
                            logger.info(f"📊 Metadata: {metadata}")
                            logger.info(f"📊 Metadata type: {type(metadata)}")
                            
                            # Handle different possible formats
                            if hasattr(metadata, 'get'):
                                # Dictionary-like object
                                start_time_val = metadata.get('start_time', 0)
                                end_time_val = metadata.get('end_time', 0)
                            elif hasattr(metadata, 'start_time'):
                                # Object with attributes
                                start_time_val = metadata.start_time
                                end_time_val = metadata.end_time
                            else:
                                logger.error(f"❌ Unknown metadata format: {type(metadata)}")
                                continue
                                
                            clip_url = None
                        
                        duration = end_time_val - start_time_val
                        
                        logger.info(f"⏱️  Moment: {start_time_val:.2f}s - {end_time_val:.2f}s ({duration:.2f}s)")
                        
                        moment = MomentResult(
                            start_time=start_time_val,
                            end_time=end_time_val,
                            duration=duration,
                            clip_url=clip_url,
                            description=f"Query: {query}"
                        )
                        all_moments.append(moment)
                        
                        logger.info(f"✅ Moment {j+1} processed successfully")
                        
                    except Exception as e:
                        logger.error(f"❌ Error processing result {j+1}: {str(e)}")
                        logger.error(f"❌ Result content: {result}")
                        continue
                
                logger.info(f"✅ Query '{query}' processed: {len(results_list)} moments found")
            
            processing_time = time.time() - start_process_time
            
            response = MomentsResponse(
                moments=all_moments,
                total_moments=len(all_moments),
                query=", ".join(queries),
                processing_time=processing_time
            )
            
            logger.info("="*80)
            logger.info(f"🎉 MOMENTS EXTRACTION COMPLETED")
            logger.info(f"📊 Total moments found: {len(all_moments)}")
            logger.info(f"⏱️  Total processing time: {processing_time:.1f}s")
            for i, moment in enumerate(all_moments):
                logger.info(f"   Moment {i+1}: {moment.start_time:.1f}s - {moment.end_time:.1f}s ({moment.duration:.1f}s)")
            logger.info("="*80)
            
            return response
            
        except Exception as e:
            logger.error("="*80)
            logger.error(f"❌ SIEVE MOMENTS EXTRACTION FAILED")
            logger.error(f"❌ Error: {str(e)}")
            logger.error(f"❌ Error type: {type(e)}")
            logger.error("="*80)
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
        logger.info("="*80)
        logger.info(f"🚀 STARTING COMPLETE ANALYSIS WORKFLOW")
        logger.info(f"👤 Prospect: {prospect_name}")
        logger.info(f"🎯 Topic: {query_topic}")
        logger.info("="*80)
        
        # Step 1: Extract moments where the topic is discussed
        moments_queries = [query_topic]
        
        logger.info(f"🔍 Step 1: Extracting moments for query: {query_topic}")
        
        moments_response = await self.extract_moments(
            podcast_url=podcast_url,
            queries=moments_queries,
            min_clip_length=15.0  # Longer clips for better context
        )
        
        if not moments_response.moments:
            logger.warning(f"⚠️  No moments found for topic: {query_topic}")
            return {
                "moments": [],
                "context_analysis": "No relevant moments found",
                "success": False
            }
        
        logger.info(f"✅ Step 1 completed: Found {len(moments_response.moments)} moments")
        
        # Step 2: Analyze the best moment for context
        best_moment = moments_response.moments[0]  # Take first/best result
        
        logger.info(f"🎯 Step 2: Analyzing best moment")
        logger.info(f"⏱️  Best moment: {best_moment.start_time:.1f}s - {best_moment.end_time:.1f}s")
        
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
        
        logger.info(f"✅ Step 2 completed: Context analysis generated")
        logger.info(f"📝 Context length: {len(context_response.answer)} characters")
        
        result = {
            "moments": moments_response.moments,
            "context_analysis": context_response.answer,
            "best_moment": {
                "start_time": best_moment.start_time,
                "end_time": best_moment.end_time,
                "duration": best_moment.duration
            },
            "success": True,
            "processing_info": {
                "moments_found": len(moments_response.moments),
                "query_topic": query_topic,
                "prospect_name": prospect_name
            }
        }
        
        logger.info("="*80)
        logger.info(f"🎉 COMPLETE ANALYSIS WORKFLOW FINISHED")
        logger.info(f"✅ Success: {result['success']}")
        logger.info("="*80)
        
        return result

# Global service instance
sieve_service = SieveService() 