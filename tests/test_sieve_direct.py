# Purpose: Direct Sieve API tests - testing Moments and Ask APIs without FastAPI layer

import sieve
import os
import sys
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up authentication
os.environ['SIEVE_API_KEY'] = 'Nb1Hg8W5xDrHsOYb50THDMHdr668tPLckUK7NblUAig'

class TestSieveDirect:
    """Direct tests for Sieve APIs without FastAPI layer"""
    
    @staticmethod
    def test_moments_api():
        """Test Sieve Moments API directly"""
        print("🔍 Testing Sieve Moments API directly...")
        
        try:
            # Get the moments function
            moments_fn = sieve.function.get("sieve/moments")
            print("✅ Got moments function reference")
            
            # Create input video
            video = sieve.File(url="https://www.youtube.com/watch?v=u0o3IlsEQbI")
            print("✅ Created video file object")
            
            # Test with render=False (metadata only)
            print("\n📡 Calling moments API with render=False...")
            job = moments_fn.push(
                video=video,
                query="AI thoughts",
                min_clip_length=15.0,
                start_time=0,
                end_time=-1,
                render=False
            )
            
            print("⏳ Waiting for results...")
            results = job.result()
            
            print("✅ Got results!")
            print(f"📊 Type of results: {type(results)}")
            
            # Convert generator to list
            results_list = list(results)
            print(f"📊 Length of results: {len(results_list)}")
            
            if results_list:
                print(f"📊 Type of first result: {type(results_list[0])}")
                print(f"📊 First result: {results_list[0]}")
                
                # Check if it's the expected format
                if isinstance(results_list[0], dict) and 'start_time' in results_list[0]:
                    print("✅ Results match expected format!")
                    for i, result in enumerate(results_list[:3]):  # Show first 3
                        start_time = result.get('start_time')
                        end_time = result.get('end_time')
                        duration = end_time - start_time if start_time and end_time else 0
                        print(f"   Moment {i+1}: {start_time}s - {end_time}s ({duration:.1f}s)")
                    
                    return results_list[0]  # Return first moment for chaining
                else:
                    print("❌ Unexpected result format")
                    return None
            else:
                print("❌ No results returned")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def test_ask_api(moment=None):
        """Test Ask API directly with known moment"""
        # Use provided moment or default to known working moment
        if moment is None:
            moment = {"start_time": 6330.04, "end_time": 6355.04}
            
        print(f"\n🔍 Testing Ask API directly with moment ({moment['start_time']}s - {moment['end_time']}s)...")
        
        try:
            # Get the ask function
            ask_fn = sieve.function.get("sieve/ask")
            print("✅ Got ask function reference")
            
            # Create input video
            video = sieve.File(url="https://www.youtube.com/watch?v=u0o3IlsEQbI")
            print("✅ Created video file object")
            
            # Create prompt
            prompt = "What does Steven Bartlett say about AI in this specific segment? Provide detailed analysis of his thoughts and opinions."
            
            print(f"\n📡 Calling Ask API...")
            print(f"   Prompt: {prompt[:50]}...")
            print(f"   Time range: {moment['start_time']}s - {moment['end_time']}s")
            print(f"   Backend: sieve-fast")
            
            job = ask_fn.push(
                video=video,
                prompt=prompt,
                start_time=moment['start_time'],
                end_time=moment['end_time'],
                backend="sieve-fast"
                # No output_schema - will return string
            )
            
            print("⏳ Waiting for results...")
            result = job.result()
            
            print("✅ Got result!")
            print(f"📊 Type of result: {type(result)}")
            print(f"📊 Result preview: {str(result)[:200]}...")
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def test_moments_to_ask_workflow():
        """Test complete Moments → Ask workflow"""
        print("🚀 Testing Complete Moments → Ask Workflow (Direct Sieve)")
        print("=" * 60)
        
        # Step 1: Get moments
        moment = TestSieveDirect.test_moments_api()
        
        if not moment:
            print("\n❌ Cannot proceed to Ask API without moments")
            return False
        
        # Step 2: Use moment in ask API
        analysis = TestSieveDirect.test_ask_api(moment)
        
        if analysis:
            print("\n🎉 Complete workflow successful!")
            print("\n📋 Summary:")
            print(f"   Prospect: Steven Bartlett")
            print(f"   Moment: {moment['start_time']}s - {moment['end_time']}s")
            duration = moment['end_time'] - moment['start_time']
            print(f"   Duration: {duration:.1f}s")
            print(f"   Analysis: {str(analysis)[:300]}...")
            return True
        else:
            print("\n❌ Workflow failed at Ask API step")
            return False

def run_all_direct_tests():
    """Run all direct Sieve API tests"""
    print("📝 Direct Sieve API Test Suite")
    print("Testing Sieve APIs without FastAPI layer")
    print("=" * 50)
    
    success = TestSieveDirect.test_moments_to_ask_workflow()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All direct tests passed!")
    else:
        print("❌ Some tests failed")
    
    return success

if __name__ == "__main__":
    run_all_direct_tests() 