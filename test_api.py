# Purpose: Test script for PODVOX API endpoints using sample data

import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
SAMPLE_DATA = {
    "prospect_name": "Steven Bartlett",
    "podcast_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
    "query_topic": "AI thoughts",
    "podcast_name": "The Diary of a CEO"
}

async def test_healthcheck():
    """Test the health check endpoint"""
    print("🔍 Testing healthcheck endpoint...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/healthcheck")
        
        if response.status_code == 200:
            print("✅ Healthcheck passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Healthcheck failed: {response.status_code}")
            print(f"   Error: {response.text}")

async def test_extract_moments():
    """Test the extract moments endpoint"""
    print("\n🔍 Testing extract moments endpoint...")
    
    payload = {
        "podcast_url": SAMPLE_DATA["podcast_url"],
        "queries": [SAMPLE_DATA["query_topic"], "artificial intelligence", "AI technology"],
        "min_clip_length": 15.0,
        "render": True
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(f"{BASE_URL}/extract-moments", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Extract moments successful!")
                print(f"   Found {data['total_moments']} moments")
                print(f"   Processing time: {data.get('processing_time', 'N/A')}s")
                
                if data['moments']:
                    first_moment = data['moments'][0]
                    print(f"   First moment: {first_moment['start_time']}s - {first_moment['end_time']}s")
                
                return data
            else:
                print(f"❌ Extract moments failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Extract moments error: {str(e)}")
            return None

async def test_ask_about_content():
    """Test the ask about content endpoint"""
    print("\n🔍 Testing ask about content endpoint...")
    
    payload = {
        "podcast_url": SAMPLE_DATA["podcast_url"],
        "prompt": f"What does {SAMPLE_DATA['prospect_name']} say about AI and artificial intelligence? Provide specific quotes and insights.",
        "start_time": 0,
        "end_time": -1,
        "backend": "sieve-fast"
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(f"{BASE_URL}/ask-about-content", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Ask about content successful!")
                print(f"   Processing time: {data.get('processing_time', 'N/A')}s")
                print(f"   Answer preview: {data['answer'][:200]}...")
                
                return data
            else:
                print(f"❌ Ask about content failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Ask about content error: {str(e)}")
            return None

async def test_analyze_podcast():
    """Test the complete podcast analysis endpoint"""
    print("\n🔍 Testing analyze podcast endpoint...")
    
    payload = {
        "prospect_name": SAMPLE_DATA["prospect_name"],
        "podcast_url": SAMPLE_DATA["podcast_url"],
        "query_topic": SAMPLE_DATA["query_topic"],
        "min_clip_length": 15.0
    }
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            response = await client.post(f"{BASE_URL}/analyze-podcast", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Analyze podcast successful!")
                print(f"   Prospect: {data['prospect_name']}")
                print(f"   Topic: {data['query_topic']}")
                print(f"   Moments found: {data['moments_found']}")
                print(f"   Context preview: {data['context_analysis'][:200]}...")
                
                return data
            else:
                print(f"❌ Analyze podcast failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Analyze podcast error: {str(e)}")
            return None

async def test_generate_script(context_analysis: str):
    """Test the script generation endpoint"""
    print("\n🔍 Testing generate script endpoint...")
    
    params = {
        "prospect_name": SAMPLE_DATA["prospect_name"],
        "context_analysis": context_analysis,
        "podcast_name": SAMPLE_DATA["podcast_name"],
        "tone": "casual",
        "target_length": 20
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(f"{BASE_URL}/generate-script", params=params)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Generate script successful!")
                print(f"   Prospect: {data['prospect_name']}")
                print(f"   Script: {data['generated_script']['script']}")
                print(f"   Length: {data['generated_script']['target_length_seconds']}s")
                
                return data
            else:
                print(f"❌ Generate script failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Generate script error: {str(e)}")
            return None

async def test_full_pipeline():
    """Test the complete end-to-end pipeline"""
    print("\n🔍 Testing full pipeline endpoint...")
    
    payload = {
        "prospect_name": SAMPLE_DATA["prospect_name"],
        "podcast_name": SAMPLE_DATA["podcast_name"],
        "podcast_url": SAMPLE_DATA["podcast_url"],
        "tone": "casual",
        "query_topic": SAMPLE_DATA["query_topic"]
    }
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(f"{BASE_URL}/generate", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Full pipeline successful!")
                print(f"   Prospect: {data['prospect_name']}")
                print(f"   Moments found: {len(data['moments_found'])}")
                print(f"   Generated script: {data['generated_script']['script']}")
                print("\n   Processing steps:")
                for step in data['processing_steps']:
                    print(f"   - {step}")
                
                return data
            else:
                print(f"❌ Full pipeline failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Full pipeline error: {str(e)}")
            return None

async def main():
    """Run all tests"""
    print("🚀 Starting PODVOX API Tests")
    print("=" * 50)
    
    # Test individual endpoints
    await test_healthcheck()
    
    # Test moments extraction
    moments_data = await test_extract_moments()
    
    # Test content analysis
    ask_data = await test_ask_about_content()
    
    # Test complete analysis
    analysis_data = await test_analyze_podcast()
    
    # Test script generation (if we have analysis data)
    if analysis_data and analysis_data.get('context_analysis'):
        script_data = await test_generate_script(analysis_data['context_analysis'])
    
    # Test full pipeline
    pipeline_data = await test_full_pipeline()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    print("Note: Make sure the FastAPI server is running on localhost:8000")
    print("Run: uvicorn app.main:app --reload --port 8000")
    print()
    
    asyncio.run(main()) 