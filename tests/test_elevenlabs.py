# Purpose: ElevenLabs TTS tests - testing text-to-speech conversion and voicenote generation

import asyncio
import httpx
import os
import sys
import tempfile

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
BASE_URL = "http://localhost:8000"
STEVEN_TEST_MESSAGE = "Hey Steven! was just listening to your podcast with Sabba - you mentioned how you think AGI is only two years away. I have a few interesting takes, if you wanna to explore it more on the podcast, I can send over some more details about me! Thanks"

class TestElevenLabs:
    """Test suite for ElevenLabs TTS functionality"""
    
    @staticmethod
    async def test_voice_info():
        """Test getting voice information"""
        print("🔍 Testing voice info endpoint...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{BASE_URL}/voice-info")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Voice info retrieved successfully!")
                    print(f"   Voice ID: {data['voice_id']}")
                    print(f"   Name: {data['name']}")
                    print(f"   Category: {data['category']}")
                    return True
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available (API keys not configured)")
                    return False
                else:
                    print(f"❌ Voice info failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Voice info error: {str(e)}")
                return False

    @staticmethod
    async def test_list_voices():
        """Test listing available voices"""
        print("\n🔍 Testing list voices endpoint...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{BASE_URL}/list-voices")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Voices listed successfully!")
                    voices = data.get('voices', [])
                    print(f"   Found {len(voices)} voices")
                    
                    # Show first few voices
                    for i, voice in enumerate(voices[:3]):
                        print(f"   Voice {i+1}: {voice.get('name', 'Unknown')} ({voice.get('voice_id', 'No ID')})")
                    
                    return True
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available")
                    return False
                else:
                    print(f"❌ List voices failed: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ List voices error: {str(e)}")
                return False

    @staticmethod
    async def test_text_to_speech():
        """Test basic text-to-speech conversion"""
        print("\n🔍 Testing text-to-speech endpoint...")
        
        payload = {
            "text": "Hello, this is a test of the ElevenLabs text-to-speech integration.",
            "model_id": "eleven_monolingual_v1"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{BASE_URL}/text-to-speech", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Text-to-speech successful!")
                    print(f"   Audio size: {data['audio_size_bytes']} bytes")
                    print(f"   Generation time: {data['generation_time_seconds']:.2f}s")
                    return True
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available")
                    return False
                else:
                    print(f"❌ Text-to-speech failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Text-to-speech error: {str(e)}")
                return False

    @staticmethod
    async def test_create_voicenote():
        """Test creating a voicenote file"""
        print("\n🔍 Testing create voicenote endpoint...")
        
        payload = {
            "text": "This is a test voicenote file creation using ElevenLabs TTS.",
            "output_format": "mp3"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{BASE_URL}/create-voicenote", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Voicenote file created successfully!")
                    print(f"   File path: {data['file_path']}")
                    print(f"   File size: {data['file_size_bytes']} bytes")
                    print(f"   Duration estimate: {data['duration_estimate_seconds']:.1f}s")
                    print(f"   Voice ID: {data['voice_id']}")
                    return data['file_path']
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available")
                    return False
                else:
                    print(f"❌ Create voicenote failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Create voicenote error: {str(e)}")
                return False

    @staticmethod
    async def test_steven_message():
        """Test the specific Steven Bartlett message"""
        print(f"\n🔍 Testing Steven message: '{STEVEN_TEST_MESSAGE[:50]}...'")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{BASE_URL}/test-steven-message")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Steven message voicenote generated successfully!")
                    print(f"   Message: {data['message']}")
                    print(f"   File: {data['filename']}")
                    print(f"   Size: {data['file_size_bytes']} bytes")
                    print(f"   Download URL: {data['download_url']}")
                    
                    # Test download functionality
                    print("\n🔍 Testing download functionality...")
                    download_response = await client.get(f"{BASE_URL}{data['download_url']}")
                    
                    if download_response.status_code == 200:
                        print(f"✅ Download successful! Downloaded {len(download_response.content)} bytes")
                        return True
                    else:
                        print(f"❌ Download failed: {download_response.status_code}")
                        return False
                        
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available")
                    return False
                else:
                    print(f"❌ Steven message failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Steven message error: {str(e)}")
                return False

    @staticmethod
    async def test_custom_voice_settings():
        """Test voicenote creation with custom voice settings"""
        print("\n🔍 Testing custom voice settings...")
        
        payload = {
            "text": "This test uses custom voice settings for more expressive speech.",
            "output_format": "mp3",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.9,
                "style": 0.2,
                "use_speaker_boost": True
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{BASE_URL}/create-voicenote", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Custom voice settings worked!")
                    print(f"   File size: {data['file_size_bytes']} bytes")
                    print(f"   Duration: {data['duration_estimate_seconds']:.1f}s")
                    return True
                elif response.status_code == 503:
                    print("⚠️ ElevenLabs service not available")
                    return False
                else:
                    print(f"❌ Custom voice settings failed: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Custom voice settings error: {str(e)}")
                return False

async def run_elevenlabs_tests():
    """Run all ElevenLabs tests"""
    print("📝 ElevenLabs TTS Test Suite")
    print("Testing text-to-speech functionality")
    print("=" * 50)
    
    # Test voice info first to check if service is available
    voice_info_ok = await TestElevenLabs.test_voice_info()
    
    if not voice_info_ok:
        print("\n⚠️ ElevenLabs tests skipped - service not available")
        print("   Make sure ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID are configured")
        return False
    
    # Run all tests
    list_voices_ok = await TestElevenLabs.test_list_voices()
    tts_ok = await TestElevenLabs.test_text_to_speech()
    voicenote_ok = await TestElevenLabs.test_create_voicenote()
    steven_ok = await TestElevenLabs.test_steven_message()
    custom_ok = await TestElevenLabs.test_custom_voice_settings()
    
    print("\n" + "=" * 50)
    
    # Count successes
    tests = [voice_info_ok, list_voices_ok, tts_ok, voicenote_ok, steven_ok, custom_ok]
    passed = sum(1 for test in tests if test)
    total = len(tests)
    
    if passed == total:
        print("🎉 All ElevenLabs tests passed!")
        print(f"\n🎵 Steven's voicenote has been generated!")
        print(f"   Text: '{STEVEN_TEST_MESSAGE}'")
    else:
        print(f"❌ {total - passed} ElevenLabs tests failed")
        print("   Make sure FastAPI server is running and ElevenLabs is configured")
    
    return passed == total

if __name__ == "__main__":
    print("Note: Make sure FastAPI server is running on localhost:8000")
    print("Run: uvicorn app.main:app --reload --port 8000")
    print()
    
    asyncio.run(run_elevenlabs_tests()) 