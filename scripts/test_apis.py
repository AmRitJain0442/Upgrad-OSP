"""
API Testing Script - Tests all configured APIs
Run this to verify all API keys are working correctly
"""
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import httpx
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_status(api_name: str, status: str, message: str = ""):
    """Print formatted API status"""
    if status == "SUCCESS":
        symbol = "✓"
        color = Colors.GREEN
    elif status == "FAILED":
        symbol = "✗"
        color = Colors.RED
    else:
        symbol = "⚠"
        color = Colors.YELLOW
    
    print(f"{color}{symbol} {api_name:<20}{Colors.RESET} {message}")


async def test_gemini_api():
    """Test Google Gemini API"""
    try:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print_status("Gemini API", "FAILED", "No API key found (GEMINI_API_KEY or GOOGLE_API_KEY)")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(
            "Count from 1 to 3",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        # Check if response has valid content
        if response.parts:
            print_status("Gemini API", "SUCCESS", f"Response: {response.text[:50]}")
            return True
        else:
            # Check finish reason
            finish_reason = response.candidates[0].finish_reason if response.candidates else None
            print_status("Gemini API", "FAILED", f"No response received. Finish reason: {finish_reason}")
            return False
            
    except Exception as e:
        print_status("Gemini API", "FAILED", f"Error: {str(e)[:80]}")
        return False


async def test_perplexity_api():
    """Test Perplexity API"""
    try:
        api_key = os.getenv('PERPLEXITY_API_KEY')
        
        if not api_key:
            print_status("Perplexity API", "FAILED", "No API key found (PERPLEXITY_API_KEY)")
            return False
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "user",
                            "content": "Say 'API test successful' in 3 words"
                        }
                    ],
                    "temperature": 0.2,
                    "max_tokens": 50
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                print_status("Perplexity API", "SUCCESS", f"Response: {content[:50]}")
                return True
            else:
                print_status("Perplexity API", "FAILED", f"Status: {response.status_code}, Body: {response.text[:80]}")
                return False
                
    except Exception as e:
        print_status("Perplexity API", "FAILED", f"Error: {str(e)[:80]}")
        return False


async def test_tavily_api():
    """Test Tavily API"""
    try:
        api_key = os.getenv('TAVILY_API_KEY')
        
        if not api_key:
            print_status("Tavily API", "FAILED", "No API key found (TAVILY_API_KEY)")
            return False
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "api_key": api_key,
                    "query": "AI tools",
                    "search_depth": "basic",
                    "max_results": 1
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print_status("Tavily API", "SUCCESS", f"Found {len(results)} result(s)")
                return True
            else:
                print_status("Tavily API", "FAILED", f"Status: {response.status_code}, Body: {response.text[:80]}")
                return False
                
    except Exception as e:
        print_status("Tavily API", "FAILED", f"Error: {str(e)[:80]}")
        return False


async def test_all_apis():
    """Run all API tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}API Configuration Test{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    # Test each API
    results = {}
    
    print(f"{Colors.BOLD}Testing APIs...{Colors.RESET}\n")
    
    results['gemini'] = await test_gemini_api()
    results['perplexity'] = await test_perplexity_api()
    results['tavily'] = await test_tavily_api()
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"Total APIs tested: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All APIs are working correctly!{Colors.RESET}\n")
    elif passed > 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some APIs are not working. Check the errors above.{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ All APIs failed. Please check your .env file and API keys.{Colors.RESET}\n")
    
    # Environment check
    print(f"{Colors.BOLD}Environment Variables:{Colors.RESET}")
    env_vars = ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'PERPLEXITY_API_KEY', 'TAVILY_API_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  {var}: {masked}")
        else:
            print(f"  {var}: {Colors.RED}Not set{Colors.RESET}")
    
    print()


if __name__ == "__main__":
    print(f"\n{Colors.BOLD}Starting API tests...{Colors.RESET}")
    asyncio.run(test_all_apis())
