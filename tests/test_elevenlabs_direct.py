# Purpose: Direct ElevenLabs test - test TTS functionality without FastAPI

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.elevenlabs_service import elevenlabs_service

async def test_elevenlabs_direct():
    """Test ElevenLabs service directly"""
    print("🎵 Direct ElevenLabs TTS Test")
    print("=" * 40)
    
    steven_message = "Hey Steven! was just listening to your podcast with Sabba - you mentioned how you think AGI is only two years away. I have a few interesting takes, if you wanna to explore it more on the podcast, I can send over some more details about me! Thanks"
    
    try:
        # Test 1: Get voice info
        print("🔍 Testing voice info...")
        voice_info = await elevenlabs_service.get_voice_info()
        print(f"✅ Voice loaded: {voice_info.get('name', 'Unknown')}")
        print(f"   Voice ID: {voice_info.get('voice_id', 'Unknown')}")
        print(f"   Category: {voice_info.get('category', 'Unknown')}")
        
        # Test 2: Generate the Steven message
        print(f"\n🎵 Generating Steven's voicenote...")
        print(f"   Message: {steven_message[:60]}...")
        
        file_path = await elevenlabs_service.create_voicenote_file(
            text=steven_message,
            file_format="mp3"
        )
        
        # Check file
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ Voicenote created successfully!")
            print(f"   File: {file_path}")
            print(f"   Size: {file_size:,} bytes")
            
            # Estimate duration
            word_count = len(steven_message.split())
            duration_estimate = (word_count / 150) * 60  # ~150 words per minute
            print(f"   Estimated duration: {duration_estimate:.1f} seconds")
            
            return True
        else:
            print(f"❌ File was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def run_direct_elevenlabs_test():
    """Main test runner function"""
    print("📝 Direct ElevenLabs Test Suite")
    print("Testing TTS functionality without API layer")
    print("=" * 50)
    
    success = await test_elevenlabs_direct()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Direct ElevenLabs test passed!")
        print("🎵 Steven's voicenote is ready!")
    else:
        print("❌ Direct ElevenLabs test failed")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(run_direct_elevenlabs_test()) 