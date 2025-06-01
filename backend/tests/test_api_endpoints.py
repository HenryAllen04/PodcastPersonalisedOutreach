# Purpose: FastAPI endpoint tests - testing our API endpoints with Sieve integration

import asyncio
import httpx
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
BASE_URL = "http://localhost:8000"
TEST_DATA = {
    "podcast_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
    "prospect_name": "Steven Bartlett",
    "query_topic": "AI thoughts",
    "podcast_name": "The Diary of a CEO"
}

class TestAPIEndpoints:
    """Test suite for FastAPI endpoints"""
    
    @staticmethod
    async def test_healthcheck():
        """Test the health check endpoint"""
        print("🔍 Testing healthcheck endpoint...")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/healthcheck")
            
            if response.status_code == 200:
                print("✅ Healthcheck passed!")
                data = response.json()
                print(f"   Status: {data['status']}")
                print(f"   Version: {data['version']}")
                return True
            else:
                print(f"❌ Healthcheck failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False

    @staticmethod
    async def test_moments_endpoint():
        """Test the moments extraction endpoint"""
        print("\n🔍 Testing /extract-moments endpoint...")
        
        payload = {
            "podcast_url": TEST_DATA["podcast_url"],
            "queries": [TEST_DATA["query_topic"], "artificial intelligence"],
            "min_clip_length": 15.0,
            "render": False
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                print("   Sending request...")
                response = await client.post(f"{BASE_URL}/extract-moments", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Moments endpoint successful!")
                    print(f"   Found {data['total_moments']} moments")
                    print(f"   Processing time: {data.get('processing_time', 'N/A')}s")
                    
                    if data['moments']:
                        first_moment = data['moments'][0]
                        print(f"   First moment: {first_moment['start_time']}s - {first_moment['end_time']}s")
                        return first_moment
                    
                    return True
                else:
                    print(f"❌ Moments endpoint failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Moments endpoint error: {str(e)}")
                return False

    @staticmethod
    async def test_ask_endpoint(moment=None):
        """Test the ask about content endpoint"""
        if moment is None:
            moment = {"start_time": 6330.04, "end_time": 6355.04}
            
        print(f"\n🔍 Testing /ask-about-content endpoint...")
        print(f"   Using moment: {moment['start_time']}s - {moment['end_time']}s")
        
        payload = {
            "podcast_url": TEST_DATA["podcast_url"],
            "prompt": f"What does {TEST_DATA['prospect_name']} say about AI in this segment? Provide specific insights.",
            "start_time": moment['start_time'],
            "end_time": moment['end_time'],
            "backend": "sieve-fast"
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                print("   Sending request...")
                response = await client.post(f"{BASE_URL}/ask-about-content", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Ask endpoint successful!")
                    print(f"   Processing time: {data.get('processing_time', 'N/A')}s")
                    print(f"   Answer preview: {data['answer'][:150]}...")
                    return data['answer']
                else:
                    print(f"❌ Ask endpoint failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Ask endpoint error: {str(e)}")
                return False

    @staticmethod
    async def test_analyze_podcast_endpoint():
        """Test the complete podcast analysis endpoint"""
        print("\n🔍 Testing /analyze-podcast endpoint...")
        
        payload = {
            "prospect_name": TEST_DATA["prospect_name"],
            "podcast_url": TEST_DATA["podcast_url"],
            "query_topic": TEST_DATA["query_topic"],
            "min_clip_length": 15.0
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                print("   Sending request...")
                response = await client.post(f"{BASE_URL}/analyze-podcast", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Analyze podcast endpoint successful!")
                    print(f"   Prospect: {data['prospect_name']}")
                    print(f"   Topic: {data['query_topic']}")
                    print(f"   Moments found: {data['moments_found']}")
                    print(f"   Context preview: {data['context_analysis'][:150]}...")
                    return data
                else:
                    print(f"❌ Analyze podcast failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Analyze podcast error: {str(e)}")
                return False

    @staticmethod
    async def test_complete_workflow():
        """Test the complete end-to-end workflow"""
        print("\n🔍 Testing complete API workflow...")
        
        # Step 1: Test moments
        moment = await TestAPIEndpoints.test_moments_endpoint()
        if not moment or moment is True:
            print("   Using default moment for Ask API test")
            moment = {"start_time": 6330.04, "end_time": 6355.04}
        
        # Step 2: Test ask with the moment
        analysis = await TestAPIEndpoints.test_ask_endpoint(moment)
        
        if analysis:
            print("\n🎉 Complete API workflow successful!")
            return True
        else:
            print("\n❌ API workflow failed")
            return False

async def run_all_api_tests():
    """Run all FastAPI endpoint tests"""
    print("📝 FastAPI Endpoint Test Suite")
    print("Testing API endpoints with Sieve integration")
    print("=" * 50)
    
    # Test basic health
    health_ok = await TestAPIEndpoints.test_healthcheck()
    
    if not health_ok:
        print("❌ API server not responding - check if server is running")
        return False
    
    # Test complete workflow
    workflow_ok = await TestAPIEndpoints.test_complete_workflow()
    
    # Test analyze endpoint
    analysis_ok = await TestAPIEndpoints.test_analyze_podcast_endpoint()
    
    print("\n" + "=" * 50)
    all_passed = health_ok and workflow_ok and analysis_ok
    
    if all_passed:
        print("🎉 All API tests passed!")
    else:
        print("❌ Some API tests failed")
        print("   Make sure FastAPI server is running: uvicorn app.main:app --reload --port 8000")
    
    return all_passed

if __name__ == "__main__":
    print("Note: Make sure FastAPI server is running on localhost:8000")
    print("Run: uvicorn app.main:app --reload --port 8000")
    print()
    
    asyncio.run(run_all_api_tests()) 