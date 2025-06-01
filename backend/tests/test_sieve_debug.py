#!/usr/bin/env python3
"""
Purpose: Debug Sieve API directly with comprehensive logging
Based on the example provided by the user
"""

import sieve
import os
import time
from app.config import settings

def test_sieve_direct():
    """Test Sieve API directly with the user's example format"""
    print("🧪 SIEVE API DIRECT TEST")
    print("="*80)
    
    # Set up authentication
    if not os.getenv('SIEVE_API_KEY'):
        os.environ['SIEVE_API_KEY'] = settings.sieve_api_key
    
    print(f"🔑 SIEVE_API_KEY present: {bool(os.getenv('SIEVE_API_KEY'))}")
    
    # Test parameters based on SampleData
    video_url = "https://www.youtube.com/watch?v=u0o3IlsEQbI"
    query = "AI thoughts"
    min_clip_length = 15.0
    start_time = 0
    end_time = -1
    render = False  # Turn off as requested
    
    print(f"\n📊 Test Parameters:")
    print(f"   Video URL: {video_url}")
    print(f"   Query: {query}")
    print(f"   Min clip length: {min_clip_length}s")
    print(f"   Start time: {start_time}s")
    print(f"   End time: {end_time}s")
    print(f"   Render: {render}")
    
    try:
        print(f"\n🎬 Creating Sieve File object...")
        video = sieve.File(url=video_url)
        print(f"✅ Video file created: {video}")
        
        print(f"\n🔍 Getting moments function...")
        moments = sieve.function.get("sieve/moments")
        print(f"✅ Moments function: {moments}")
        
        print(f"\n🚀 Pushing job to Sieve...")
        start_time_job = time.time()
        
        output = moments.push(video, query, min_clip_length, start_time, end_time, render)
        
        print(f"✅ Job pushed successfully!")
        print(f"📊 Job object: {output}")
        print(f"📊 Job type: {type(output)}")
        
        print('🔄 This is printing while a job is running in the background!')
        print('⏳ Waiting for results...')
        
        # Get results
        results_start_time = time.time()
        result_generator = output.result()
        results_time = time.time() - results_start_time
        
        print(f"✅ Results received in {results_time:.1f}s")
        print(f"📊 Result generator: {result_generator}")
        print(f"📊 Generator type: {type(result_generator)}")
        
        # Process results
        print(f"\n📋 Processing results...")
        results_list = []
        
        for i, output_object in enumerate(result_generator):
            print(f"\n📄 Result {i+1}:")
            print(f"   Content: {output_object}")
            print(f"   Type: {type(output_object)}")
            
            # Try to extract timing information
            if hasattr(output_object, 'get'):
                # Dictionary-like
                start_time_val = output_object.get('start_time', 'N/A')
                end_time_val = output_object.get('end_time', 'N/A')
                print(f"   Start time: {start_time_val}")
                print(f"   End time: {end_time_val}")
            elif hasattr(output_object, 'start_time'):
                # Object with attributes
                print(f"   Start time: {output_object.start_time}")
                print(f"   End time: {output_object.end_time}")
            else:
                print(f"   ⚠️ Unknown format - cannot extract timing")
            
            results_list.append(output_object)
        
        total_time = time.time() - start_time_job
        
        print(f"\n🎉 SIEVE TEST COMPLETED")
        print(f"📊 Total results: {len(results_list)}")
        print(f"⏱️ Total time: {total_time:.1f}s")
        print("="*80)
        
        return results_list
        
    except Exception as e:
        print(f"\n❌ SIEVE TEST FAILED")
        print(f"❌ Error: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        print("="*80)
        raise

def test_with_multiple_queries():
    """Test with multiple queries like in the main service"""
    print("\n🔍 TESTING MULTIPLE QUERIES")
    print("="*80)
    
    queries = ["AI thoughts", "artificial intelligence", "AGI", "machine learning"]
    video_url = "https://www.youtube.com/watch?v=u0o3IlsEQbI"
    
    for i, query in enumerate(queries, 1):
        print(f"\n🎯 Query {i}/{len(queries)}: '{query}'")
        try:
            video = sieve.File(url=video_url)
            moments = sieve.function.get("sieve/moments")
            
            start_time = time.time()
            output = moments.push(video, query, 15.0, 0, -1, False)
            
            print(f"⏳ Waiting for results...")
            results = list(output.result())
            processing_time = time.time() - start_time
            
            print(f"✅ Query '{query}': {len(results)} results in {processing_time:.1f}s")
            
            for j, result in enumerate(results[:2]):  # Show first 2 results
                print(f"   Result {j+1}: {result}")
                
        except Exception as e:
            print(f"❌ Query '{query}' failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 SIEVE API DEBUG SUITE")
    print("Testing Sieve API directly based on user examples")
    print("="*80)
    
    # Test 1: Direct API test
    try:
        results = test_sieve_direct()
        print(f"\n✅ Direct test passed: {len(results)} results")
    except Exception as e:
        print(f"\n❌ Direct test failed: {str(e)}")
    
    # Test 2: Multiple queries test
    try:
        test_with_multiple_queries()
        print(f"\n✅ Multiple queries test completed")
    except Exception as e:
        print(f"\n❌ Multiple queries test failed: {str(e)}")
    
    print(f"\n🎉 Debug suite completed!") 