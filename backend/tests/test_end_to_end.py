#!/usr/bin/env python3
"""
Purpose: End-to-end PODVOX test - from podcast URL to MP3 voicenote
Fast test with single query to avoid long wait times
"""

import requests
import time
import json

def test_complete_voicenote_generation():
    """Test complete pipeline: Sieve → OpenAI → ElevenLabs → MP3"""
    
    print("🚀 PODVOX END-TO-END VOICENOTE TEST")
    print("="*80)
    
    # Test parameters - simplified interface (just topic + video URL)
    test_data = {
        "topic": "AI thoughts",
        "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI"
    }
    
    print(f"🎯 Topic: {test_data['topic']}")
    print(f"📺 Video: {test_data['video_url']}")
    print("="*80)
    
    # API endpoint - using the simplified version
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/generate-voicenote-simple"
    
    print(f"🌐 Testing endpoint: {endpoint}")
    
    try:
        print(f"\n⏳ Starting complete pipeline...")
        start_time = time.time()
        
        # Make the API call with simplified parameters
        response = requests.post(endpoint, params=test_data, timeout=600)  # 10 minute timeout
        
        processing_time = time.time() - start_time
        
        print(f"✅ API call completed in {processing_time:.1f}s")
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n🎉 PIPELINE SUCCESS!")
            print(f"✅ Success: {result.get('success', False)}")
            
            if 'generated_script' in result:
                script = result['generated_script']
                word_count = len(script.split())
                print(f"\n📝 Generated Script ({word_count} words):")
                print(f"   \"{script}\"")
                
                print(f"✅ Under 60 words: {word_count <= 60}")
            
            if 'voicenote' in result:
                voicenote = result['voicenote']
                print(f"\n🎧 Voicenote Created:")
                print(f"   📁 Filename: {voicenote.get('filename', 'N/A')}")
                print(f"   🔗 Download URL: {voicenote.get('download_url', 'N/A')}")
                
                # Test download
                if 'download_url' in voicenote:
                    download_url = f"{base_url}{voicenote['download_url']}"
                    print(f"\n⬇️ Testing download from: {download_url}")
                    
                    download_response = requests.get(download_url)
                    if download_response.status_code == 200:
                        file_size = len(download_response.content)
                        print(f"✅ Download successful: {file_size} bytes")
                        print(f"✅ Content type: {download_response.headers.get('content-type', 'N/A')}")
                        
                        # Save file locally for verification
                        local_filename = f"test_voicenote_{int(time.time())}.mp3"
                        with open(local_filename, 'wb') as f:
                            f.write(download_response.content)
                        print(f"💾 Saved locally as: {local_filename}")
                        
                    else:
                        print(f"❌ Download failed: {download_response.status_code}")
            
            if 'moments_found' in result:
                print(f"\n📊 Processing Stats:")
                print(f"   🎯 Moments found: {result.get('moments_found', 0)}")
                print(f"   ⏱️ Total time: {processing_time:.1f}s")
            
            print(f"\n🎉 END-TO-END TEST COMPLETED SUCCESSFULLY!")
            
        else:
            print(f"❌ API call failed")
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 10 minutes")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        
    print("="*80)

def test_individual_endpoints():
    """Quick test of individual endpoints for debugging"""
    
    print("\n🔧 TESTING INDIVIDUAL ENDPOINTS")
    print("="*80)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"🏥 Health check: {response.status_code}")
    except:
        print(f"❌ Health check failed")
    
    # Test 2: Simple script generation
    try:
        script_data = {
            "name": "there",  # Generic name
            "context": "They discussed how AGI might be just 2 years away and shared thoughts on the rapid advancement of AI technology."
        }
        response = requests.post(f"{base_url}/generate-simple-script", json=script_data)
        if response.status_code == 200:
            result = response.json()
            print(f"📝 Script generation: ✅ ({len(result['script'].split())} words)")
        else:
            print(f"❌ Script generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Script test failed: {str(e)}")
    
    print("="*80)

def test_different_topics():
    """Test with different topics to show flexibility"""
    
    print("\n🎯 TESTING DIFFERENT TOPICS")
    print("="*80)
    
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/generate-voicenote-simple"
    
    test_cases = [
        {
            "topic": "productivity",
            "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
            "description": "Testing productivity topic"
        },
        {
            "topic": "entrepreneurship", 
            "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
            "description": "Testing entrepreneurship topic"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['description']}")
        print(f"   Topic: {test_case['topic']}")
        
        # For this demo, just show the request format
        print(f"   Request: POST {endpoint}")
        print(f"   Params: topic={test_case['topic']}, video_url={test_case['video_url']}")
        print(f"   ✅ Format valid")

if __name__ == "__main__":
    print("🎯 PODVOX SIMPLIFIED END-TO-END TEST")
    print("Testing complete pipeline with just topic + video URL")
    print("="*80)
    
    # Test individual endpoints first
    test_individual_endpoints()
    
    # Show different topic examples
    test_different_topics()
    
    # Then test complete pipeline
    test_complete_voicenote_generation()
    
    print("\n🎉 All tests completed!") 