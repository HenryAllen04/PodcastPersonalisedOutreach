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
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("📝 PODVOX Test Suite - Running All Tests")
        print("=" * 70)
        print("Testing: Direct Sieve APIs → FastAPI Endpoints → Integration")
        print()
        
        # Run all test suites
        direct_ok = await self.run_direct_tests()
        api_ok = await self.run_api_tests()
        integration_ok = await self.run_integration_tests()
        
        # Print summary
        self.print_summary()
        
        return all([direct_ok, api_ok, integration_ok])
    
    async def run_quick_tests(self):
        """Run only quick tests (direct API tests)"""
        print("📝 PODVOX Quick Test Suite")
        print("=" * 70)
        print("Running quick direct API tests only...")
        print()
        
        direct_ok = await self.run_direct_tests()
        self.print_summary(quick=True)
        
        return direct_ok
    
    def print_summary(self, quick=False):
        """Print test results summary"""
        print("\n\n" + "=" * 70)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 70)
        
        for test_type, result in self.results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            test_name = {
                'direct': 'Direct Sieve API Tests',
                'api': 'FastAPI Endpoint Tests', 
                'integration': 'Integration Tests'
            }.get(test_type, test_type)
            
            print(f"{test_name}: {status}")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        
        print(f"\nOverall: {passed_tests}/{total_tests} test suites passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! 🎉")
        else:
            print("❌ Some tests failed - check output above for details")
        
        if not quick:
            print("\n💡 Tips:")
            if not self.results.get('api', True):
                print("   - For API tests: Make sure FastAPI server is running")
                print("     Run: uvicorn app.main:app --reload --port 8000")
            if not self.results.get('direct', True):
                print("   - For direct tests: Check your SIEVE_API_KEY environment variable")
            if not self.results.get('integration', True):
                print("   - For integration tests: Ensure all services are properly configured")

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
    else:
        success = await runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 