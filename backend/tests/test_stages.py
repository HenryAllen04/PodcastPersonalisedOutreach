#!/usr/bin/env python3
"""
Purpose: Test the PODVOX simplified API with stage-by-stage logging
Shows clear progress through all 4 stages
"""

import requests
import time
import json

def test_podvox_stages():
    """Test the complete PODVOX pipeline with stage logging"""
    
    print("🎯 TESTING PODVOX WITH STAGE-BY-STAGE LOGGING")
    print("="*80)
    
    # Test parameters
    api_url = "http://localhost:8000/generate-voicenote-simple"
    params = {
        "topic": "AI thoughts",
        "video_url": "https://www.youtube.com/watch?v=u0o3IlsEQbI"
    }
    
    print(f"🌐 API URL: {api_url}")
    print(f"📊 Parameters:")
    print(f"   Topic: {params['topic']}")
    print(f"   Video: {params['video_url']}")
    print("="*80)
    
    try:
        print("⏳ Starting API call...")
        print("📋 Expected stages:")
        print("   🎯 Stage 1: Moments Extraction (Sieve) ~2 minutes")
        print("   🎯 Stage 2: Context Analysis (Sieve Ask) included in Stage 1") 
        print("   🎯 Stage 3: Script Generation (ChatGPT) ~5 seconds")
        print("   🎯 Stage 4: Voice Synthesis (ElevenLabs) ~10 seconds")
        print("="*80)
        
        start_time = time.time()
        
        # Make the API call
        response = requests.post(api_url, params=params, timeout=600)
        
        processing_time = time.time() - start_time
        
        print(f"\n✅ API CALL COMPLETED in {processing_time:.1f}s")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n🎉 PIPELINE RESULTS:")
            print("="*60)
            
            if result.get('success'):
                print(f"✅ Success: {result['success']}")
                print(f"🎯 Topic: {result.get('topic', 'N/A')}")
                print(f"👤 Prospect: {result.get('prospect_name', 'N/A')}")
                
                if 'generated_script' in result:
                    script = result['generated_script']
                    word_count = result.get('script_word_count', len(script.split()))
                    print(f"\n📝 Generated Script ({word_count} words):")
                    print(f"   \"{script}\"")
                
                if 'moments_found' in result:
                    print(f"\n📊 Processing Stats:")
                    print(f"   🎯 Moments found: {result['moments_found']}")
                
                if 'stage_times' in result:
                    print(f"\n⏱️ Stage Timing:")
                    stage_times = result['stage_times']
                    print(f"   Stage 1 (Moments): {stage_times.get('stage1_moments', 'N/A')}")
                    print(f"   Stage 2 (Ask): {stage_times.get('stage2_ask', 'N/A')}")
                    print(f"   Stage 3 (ChatGPT): {stage_times.get('stage3_chatgpt', 'N/A')}")
                    print(f"   Stage 4 (ElevenLabs): {stage_times.get('stage4_elevenlabs', 'N/A')}")
                    print(f"   Total: {stage_times.get('total', 'N/A')}")
                
                if 'voicenote' in result and result['voicenote']:
                    voicenote = result['voicenote']
                    print(f"\n🎧 Voicenote Created:")
                    print(f"   📁 Filename: {voicenote.get('filename', 'N/A')}")
                    print(f"   🔗 Download URL: {voicenote.get('download_url', 'N/A')}")
                    
                    # Test download availability
                    if 'download_url' in voicenote:
                        download_url = f"http://localhost:8000{voicenote['download_url']}"
                        try:
                            download_check = requests.head(download_url, timeout=5)
                            if download_check.status_code == 200:
                                print(f"   ✅ Download available: {download_url}")
                            else:
                                print(f"   ⚠️ Download status: {download_check.status_code}")
                        except:
                            print(f"   ❌ Download check failed")
                
                print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
                
            else:
                print(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")
                if 'stage_completed' in result:
                    print(f"📍 Failed at: {result['stage_completed']}")
        
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (>10 minutes)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the server running?")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    print("="*80)
    print("🎯 Test completed!")

if __name__ == "__main__":
    print("🚀 PODVOX STAGE TESTING SCRIPT")
    print("This script will test the complete pipeline and show stage-by-stage progress")
    print()
    
    test_podvox_stages() 