# Purpose: Master test runner - runs all test suites for the PODVOX application

import asyncio
import sys
import os
import argparse

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_sieve_direct import run_all_direct_tests
from test_api_endpoints import run_all_api_tests
from test_integration import run_integration_tests
from test_elevenlabs import run_elevenlabs_tests
from test_elevenlabs_direct import run_direct_elevenlabs_test

class TestRunner:
    """Orchestrates all test suites"""
    
    def __init__(self):
        self.results = {}
    
    async def run_direct_tests(self):
        """Run direct Sieve API tests"""
        print("🚀 Running Direct Sieve API Tests")
        print("=" * 60)
        
        try:
            result = run_all_direct_tests()
            self.results['direct'] = result
            return result
        except Exception as e:
            print(f"❌ Direct tests failed with error: {e}")
            self.results['direct'] = False
            return False
    
    async def run_api_tests(self):
        """Run FastAPI endpoint tests"""
        print("\n\n🚀 Running FastAPI Endpoint Tests")
        print("=" * 60)
        
        try:
            result = await run_all_api_tests()
            self.results['api'] = result
            return result
        except Exception as e:
            print(f"❌ API tests failed with error: {e}")
            self.results['api'] = False
            return False
    
    async def run_integration_tests(self):
        """Run integration tests"""
        print("\n\n🚀 Running Integration Tests")
        print("=" * 60)
        
        try:
            result = await run_integration_tests()
            self.results['integration'] = result
            return result
        except Exception as e:
            print(f"❌ Integration tests failed with error: {e}")
            self.results['integration'] = False
            return False
    
    async def run_elevenlabs_tests(self):
        """Run ElevenLabs TTS tests (API endpoints)"""
        print("\n\n🚀 Running ElevenLabs API Tests")
        print("=" * 60)
        
        try:
            result = await run_elevenlabs_tests()
            self.results['elevenlabs_api'] = result
            return result
        except Exception as e:
            print(f"❌ ElevenLabs API tests failed with error: {e}")
            self.results['elevenlabs_api'] = False
            return False
    
    async def run_elevenlabs_direct_tests(self):
        """Run ElevenLabs direct tests (no API layer)"""
        print("\n\n🚀 Running ElevenLabs Direct Tests")
        print("=" * 60)
        
        try:
            result = await run_direct_elevenlabs_test()
            self.results['elevenlabs_direct'] = result
            return result
        except Exception as e:
            print(f"❌ ElevenLabs direct tests failed with error: {e}")
            self.results['elevenlabs_direct'] = False
            return False
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("📝 PODVOX Test Suite - Running All Tests")
        print("=" * 70)
        print("Testing: Direct Sieve APIs → FastAPI Endpoints → Integration → ElevenLabs")
        print()
        
        # Run all test suites
        direct_ok = await self.run_direct_tests()
        api_ok = await self.run_api_tests()
        integration_ok = await self.run_integration_tests()
        elevenlabs_direct_ok = await self.run_elevenlabs_direct_tests()
        elevenlabs_api_ok = await self.run_elevenlabs_tests()
        
        # Print summary
        self.print_summary()
        
        return all([direct_ok, api_ok, integration_ok, elevenlabs_direct_ok, elevenlabs_api_ok])
    
    async def run_quick_tests(self):
        """Run only quick tests (direct API tests)"""
        print("📝 PODVOX Quick Test Suite")
        print("=" * 70)
        print("Running quick direct API tests only...")
        print()
        
        direct_ok = await self.run_direct_tests()
        self.print_summary(quick=True)
        
        return direct_ok
    
    async def run_tts_only(self):
        """Run only ElevenLabs TTS tests"""
        print("📝 PODVOX TTS Test Suite")
        print("=" * 70)
        print("Running ElevenLabs text-to-speech tests...")
        print()
        
        # Run both direct and API TTS tests
        elevenlabs_direct_ok = await self.run_elevenlabs_direct_tests()
        elevenlabs_api_ok = await self.run_elevenlabs_tests()
        
        self.print_summary(tts_only=True)
        
        return elevenlabs_direct_ok or elevenlabs_api_ok  # Pass if either works
    
    def print_summary(self, quick=False, tts_only=False):
        """Print test results summary"""
        print("\n\n" + "=" * 70)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 70)
        
        for test_type, result in self.results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            test_name = {
                'direct': 'Direct Sieve API Tests',
                'api': 'FastAPI Endpoint Tests', 
                'integration': 'Integration Tests',
                'elevenlabs_api': 'ElevenLabs API Tests',
                'elevenlabs_direct': 'ElevenLabs Direct Tests'
            }.get(test_type, test_type)
            
            print(f"{test_name}: {status}")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        
        print(f"\nOverall: {passed_tests}/{total_tests} test suites passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! 🎉")
        else:
            print("❌ Some tests failed - check output above for details")
        
        if not quick and not tts_only:
            print("\n💡 Tips:")
            if not self.results.get('api', True):
                print("   - For API tests: Make sure FastAPI server is running")
                print("     Run: uvicorn app.main:app --reload --port 8000")
            if not self.results.get('direct', True):
                print("   - For direct tests: Check your SIEVE_API_KEY environment variable")
            if not self.results.get('integration', True):
                print("   - For integration tests: Ensure all services are properly configured")
            if not self.results.get('elevenlabs_direct', True) and not self.results.get('elevenlabs_api', True):
                print("   - For ElevenLabs tests: Check ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID")
                print("     ElevenLabs tests are optional - they'll be skipped if not configured")

async def main():
    """Main test runner with CLI options"""
    parser = argparse.ArgumentParser(description='PODVOX Test Suite Runner')
    parser.add_argument('--quick', action='store_true', 
                       help='Run only quick direct API tests')
    parser.add_argument('--direct', action='store_true',
                       help='Run only direct Sieve API tests')
    parser.add_argument('--api', action='store_true',
                       help='Run only FastAPI endpoint tests')
    parser.add_argument('--integration', action='store_true',
                       help='Run only integration tests')
    parser.add_argument('--tts', action='store_true',
                       help='Run only ElevenLabs TTS tests')
    parser.add_argument('--elevenlabs', action='store_true',
                       help='Run only ElevenLabs TTS tests (alias for --tts)')
    parser.add_argument('--tts-direct', action='store_true',
                       help='Run only direct ElevenLabs tests (no API layer)')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.quick:
        success = await runner.run_quick_tests()
    elif args.direct:
        success = await runner.run_direct_tests()
        runner.print_summary()
    elif args.api:
        success = await runner.run_api_tests()
        runner.print_summary()
    elif args.integration:
        success = await runner.run_integration_tests()
        runner.print_summary()
    elif args.tts or args.elevenlabs:
        success = await runner.run_tts_only()
    elif args.tts_direct:
        success = await runner.run_elevenlabs_direct_tests()
        runner.print_summary()
    else:
        success = await runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 