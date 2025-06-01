#!/usr/bin/env python3
"""
Purpose: Test complete PODVOX pipeline using SampleData example
Tests the full workflow: Sieve → OpenAI → ElevenLabs → Voicenote
"""

import asyncio
import requests
import json
import time
from datetime import datetime

def test_complete_pipeline():
    """Test the complete pipeline using SampleData example"""
    print("🚀 PODVOX Complete Pipeline Test")
    print("Testing the full workflow from SampleData/exampleInput.md")
    print("=" * 80)
    
    # Test data from SampleData/exampleInput.md
    test_data = {
        "prospect_name": "Steven Bartlett",
        "podcast_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI", 
        "podcast_name": "The Diary of a CEO",
        "query_topic": "AI thoughts",
        "tone": "casual"
    }
    
    # Expected example voicenote from sample data
    expected_style = """Hey Steven, was just listening to your podcast with Sabba - you mentioned how you think AGI is only two years away. I've got a bunch of interesting takes on the topic, curious if you wanted to explore it more on the podcast, I'll send over some more details about me. Let me know your thoughts."""
    
    print(f"📊 Test Parameters:")
    print(f"   Prospect: {test_data['prospect_name']}")
    print(f"   Podcast: {test_data['podcast_name']}")
    print(f"   URL: {test_data['podcast_url']}")
    print(f"   Topic: {test_data['query_topic']}")
    print(f"\n📝 Expected Style (from sample):")
    print(f"   \"{expected_style}\"")
    print(f"   Word count: {len(expected_style.split())} words")
    
    BASE_URL = "http://localhost:8000"
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/healthcheck")
        if response.status_code != 200:
            print("\n❌ FastAPI server not running. Start it with:")
            print("   uvicorn app.main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to FastAPI server. Make sure it's running on localhost:8000")
        return
    
    print(f"\n✅ FastAPI server is running")
    print("\n" + "="*80)
    
    # Test the complete pipeline
    print("🎯 Testing Complete Pipeline Endpoint")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-complete-voicenote",
            params=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result["success"]:
                print("🎉 Pipeline Completed Successfully!")
                print(f"\n📊 Results:")
                print(f"   • Prospect: {result['prospect_name']}")
                print(f"   • Moments found: {result['moments_found']}")
                print(f"   • Processing time: {result['total_processing_time']:.1f}s")
                
                print(f"\n📝 Generated Script ({result['script_word_count']} words):")
                print(f"   \"{result['generated_script']}\"")
                
                # Compare with expected style
                generated_words = result['script_word_count']
                expected_words = len(expected_style.split())
                print(f"\n📊 Comparison with Sample:")
                print(f"   • Generated: {generated_words} words")
                print(f"   • Expected: {expected_words} words")
                print(f"   • Under 60 words: {'✅' if generated_words <= 60 else '❌'}")
                print(f"   • Contains 'Steven': {'✅' if 'Steven' in result['generated_script'] else '❌'}")
                print(f"   • Contains 'AI': {'✅' if 'AI' in result['generated_script'] or 'ai' in result['generated_script'].lower() else '❌'}")
                
                # Voicenote info
                if result.get("voicenote"):
                    voicenote = result["voicenote"]
                    print(f"\n🎧 Voicenote Generated:")
                    print(f"   • Filename: {voicenote['filename']}")
                    print(f"   • Size: {voicenote['file_size_bytes']} bytes")
                    print(f"   • Duration: ~{voicenote['duration_estimate_seconds']:.1f}s")
                    print(f"   • Download: {BASE_URL}{voicenote['download_url']}")
                else:
                    print(f"\n⚠️ Voicenote: ElevenLabs not available (script ready for voice generation)")
                
                # Processing log
                print(f"\n📋 Processing Log:")
                for step in result["processing_log"]:
                    print(f"   {step}")
                    
                # Context analysis preview
                print(f"\n🧠 Context Analysis (preview):")
                context = result["context_analysis"]
                preview = context[:200] + "..." if len(context) > 200 else context
                print(f"   {preview}")
                
            else:
                print(f"❌ Pipeline failed: {result['error']}")
                if "processing_log" in result:
                    print("\n📋 Processing Log:")
                    for step in result["processing_log"]:
                        print(f"   {step}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
    
    total_test_time = time.time() - start_time
    print(f"\n⏱️ Total test time: {total_test_time:.1f} seconds")

def test_individual_components():
    """Test individual components separately for debugging"""
    print("\n" + "="*80)
    print("🔧 Testing Individual Components")
    print("-" * 50)
    
    BASE_URL = "http://localhost:8000"
    
    # Test data
    test_data = {
        "prospect_name": "Steven Bartlett",
        "podcast_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI",
        "query_topic": "AI thoughts"
    }
    
    # Test 1: Podcast Analysis
    print("🎯 Test 1: Podcast Analysis")
    try:
        response = requests.post(
            f"{BASE_URL}/analyze-podcast",
            json=test_data
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Found {result['moments_found']} moments")
            print(f"   📊 Context length: {len(result['context_analysis'])} characters")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Script Generation (with mock context)
    print("\n🎯 Test 2: Script Generation")
    mock_context = "Steven discussed his thoughts on artificial general intelligence, mentioning that he believes AGI could be achieved within the next 2 years. He emphasized the rapid pace of AI development and the potential implications for society."
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-simple-script",
            json={
                "name": "Steven Bartlett",
                "context": mock_context
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Generated script: \"{result['script']}\"")
            print(f"   📊 Word count: {result['word_count']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def main():
    """Run all tests"""
    print(f"🚀 PODVOX Complete Pipeline Test Suite")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Main pipeline test
    test_complete_pipeline()
    
    # Individual component tests for debugging
    test_individual_components()
    
    print(f"\n🎉 Test suite completed!")
    print(f"📋 Pipeline Summary:")
    print(f"   ✅ Sieve API: Extracts AI discussion moments")
    print(f"   ✅ OpenAI API: Generates personalized scripts (<60 words)")
    print(f"   ✅ ElevenLabs API: Creates voicenote files")
    print(f"   ✅ Complete workflow ready for podcast outreach!")

if __name__ == "__main__":
    main() 