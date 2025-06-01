# Purpose: End-to-end integration tests - testing complete workflows from user input to final output

import asyncio
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sieve_service import SieveService
from app.services.script_generator import ScriptGenerator

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def __init__(self):
        self.sieve_service = SieveService()
        self.script_generator = ScriptGenerator()
    
    async def test_moments_to_script_workflow(self):
        """Test complete Moments → Ask → Script generation workflow"""
        print("🚀 Testing Complete Integration Workflow")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test data
        podcast_url = "https://www.youtube.com/watch?v=u0o3IlsEQbI"
        prospect_name = "Steven Bartlett"
        topic = "AI thoughts"
        
        print(f"   Prospect: {prospect_name}")
        print(f"   Topic: {topic}")
        print(f"   Podcast: {podcast_url}")
        print()
        
        try:
            # Step 1: Extract moments
            print("📍 Step 1: Extracting key moments...")
            moments = await self.sieve_service.extract_key_moments(
                podcast_url=podcast_url,
                queries=[topic, "artificial intelligence"],
                min_clip_length=15.0
            )
            
            if not moments:
                print("❌ No moments found")
                return False
            
            print(f"✅ Found {len(moments)} moments")
            first_moment = moments[0]
            duration = first_moment['end_time'] - first_moment['start_time']
            print(f"   Best moment: {first_moment['start_time']}s - {first_moment['end_time']}s ({duration:.1f}s)")
            
            # Step 2: Get detailed insights
            print("\n📍 Step 2: Analyzing moment content...")
            context = await self.sieve_service.ask_about_content(
                podcast_url=podcast_url,
                prompt=f"What does {prospect_name} say about {topic} in this segment? Provide detailed insights and specific quotes.",
                start_time=first_moment['start_time'],
                end_time=first_moment['end_time']
            )
            
            if not context:
                print("❌ Failed to get context")
                return False
            
            print(f"✅ Got detailed analysis ({len(context)} characters)")
            print(f"   Preview: {context[:200]}...")
            
            # Step 3: Generate personalized script
            print("\n📍 Step 3: Generating personalized script...")
            script = await self.script_generator.generate_outreach_script(
                prospect_name=prospect_name,
                context=context,
                tone="casual"
            )
            
            if not script:
                print("❌ Failed to generate script")
                return False
            
            print(f"✅ Generated script ({len(script)} characters)")
            print(f"   Script preview: {script[:300]}...")
            
            # Step 4: Summary
            total_time = time.time() - start_time
            print(f"\n🎉 Complete workflow successful!")
            print(f"   Total processing time: {total_time:.1f}s")
            print(f"   Moment used: {first_moment['start_time']}s - {first_moment['end_time']}s")
            print(f"   Context length: {len(context)} chars")
            print(f"   Script length: {len(script)} chars")
            
            return True
            
        except Exception as e:
            print(f"❌ Integration test failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    async def test_multiple_topics_workflow(self):
        """Test workflow with multiple topics to find the best moments"""
        print("\n🚀 Testing Multi-Topic Analysis")
        print("=" * 60)
        
        podcast_url = "https://www.youtube.com/watch?v=u0o3IlsEQbI"
        prospect_name = "Steven Bartlett"
        
        topics = [
            "AI and artificial intelligence",
            "business insights",
            "personal stories",
            "childhood experiences"
        ]
        
        print(f"   Testing {len(topics)} different topics...")
        
        try:
            all_moments = []
            
            for i, topic in enumerate(topics, 1):
                print(f"\n📍 Topic {i}: {topic}")
                
                moments = await self.sieve_service.extract_key_moments(
                    podcast_url=podcast_url,
                    queries=[topic],
                    min_clip_length=10.0
                )
                
                if moments:
                    print(f"   ✅ Found {len(moments)} moments for '{topic}'")
                    all_moments.extend([(topic, moment) for moment in moments])
                else:
                    print(f"   ❌ No moments found for '{topic}'")
            
            if all_moments:
                print(f"\n📊 Total moments found: {len(all_moments)}")
                
                # Show best moments for each topic
                for topic, moment in all_moments[:5]:  # Show top 5
                    duration = moment['end_time'] - moment['start_time']
                    print(f"   {topic}: {moment['start_time']}s - {moment['end_time']}s ({duration:.1f}s)")
                
                return True
            else:
                print("\n❌ No moments found across any topics")
                return False
                
        except Exception as e:
            print(f"❌ Multi-topic test failed: {str(e)}")
            return False

    async def test_error_handling(self):
        """Test error handling with invalid inputs"""
        print("\n🚀 Testing Error Handling")
        print("=" * 60)
        
        try:
            # Test with invalid URL
            print("📍 Testing invalid podcast URL...")
            moments = await self.sieve_service.extract_key_moments(
                podcast_url="https://invalid-url.com/nonexistent",
                queries=["test"]
            )
            
            if moments is None or len(moments) == 0:
                print("✅ Correctly handled invalid URL")
            else:
                print("❌ Should have failed with invalid URL")
                return False
            
            # Test with empty query
            print("\n📍 Testing empty query...")
            moments = await self.sieve_service.extract_key_moments(
                podcast_url="https://www.youtube.com/watch?v=u0o3IlsEQbI",
                queries=[]
            )
            
            if moments is None or len(moments) == 0:
                print("✅ Correctly handled empty query")
            else:
                print("❌ Should have failed with empty query")
                return False
            
            print("\n✅ Error handling tests passed!")
            return True
            
        except Exception as e:
            print(f"✅ Expected error occurred: {type(e).__name__}")
            return True

async def run_integration_tests():
    """Run all integration tests"""
    print("📝 Integration Test Suite")
    print("Testing complete end-to-end workflows")
    print("=" * 50)
    
    integration_tester = TestIntegration()
    
    # Run main workflow test
    workflow_ok = await integration_tester.test_moments_to_script_workflow()
    
    # Run multi-topic test
    multi_topic_ok = await integration_tester.test_multiple_topics_workflow()
    
    # Run error handling test
    error_handling_ok = await integration_tester.test_error_handling()
    
    print("\n" + "=" * 50)
    all_passed = workflow_ok and multi_topic_ok and error_handling_ok
    
    if all_passed:
        print("🎉 All integration tests passed!")
    else:
        print("❌ Some integration tests failed")
    
    return all_passed

if __name__ == "__main__":
    asyncio.run(run_integration_tests()) 