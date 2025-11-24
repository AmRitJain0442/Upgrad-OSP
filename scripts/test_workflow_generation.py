"""
Test script to validate workflow generation with courses, quizzes, and evaluator links
Uses actual Gemini API to generate real workflows
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.workflow.agents import generate_workflow_roadmap, search_with_gemini_web
from app.workflow.models import AIToolSearchResult

# Verify API key is loaded
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    print("❌ ERROR: No Gemini API key found!")
    print("   Please set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file")
    sys.exit(1)
else:
    print(f"✅ API Key loaded: {GEMINI_API_KEY[:10]}...")

# Configure Gemini
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)


async def test_workflow_generation():
    """Test complete workflow generation with all features"""

    print("=" * 80)
    print("TESTING WORKFLOW GENERATION WITH COURSES, QUIZZES & EVALUATOR")
    print("=" * 80)

    # Test input
    task_description = "Create a presentation from my research data"
    answers = {
        "What format is your input data?": "PDF research papers",
        "What output format do you need?": "PowerPoint presentation",
        "How much time do you have?": "2-3 hours",
    }

    print(f"\n📋 Task: {task_description}")
    print(f"📝 User Answers: {answers}")

    # Search for tools using Gemini API
    print("\n🔍 Searching for AI tools using Gemini API...")
    try:
        ai_tools = await search_with_gemini_web(task_description, answers)
        print(f"✅ Found {len(ai_tools)} tools via API")
        for tool in ai_tools[:3]:
            print(f"   - {tool.tool_name}: {tool.use_case}")
    except Exception as e:
        print(f"⚠️  API search failed: {e}")
        print("   Using fallback tools for testing...")
        ai_tools = [
            AIToolSearchResult(
                tool_name="ChatGPT",
                description="AI assistant for research and analysis",
                url="https://chat.openai.com",
                use_case="Summarize research papers",
                pricing="Free/Paid",
            ),
            AIToolSearchResult(
                tool_name="Gamma.app",
                description="AI presentation builder",
                url="https://gamma.app",
                use_case="Create presentation from content",
                pricing="Free/Paid",
            ),
        ]

    if not ai_tools or len(ai_tools) == 0:
        print("❌ No tools found, adding fallback tools")
        ai_tools = [
            AIToolSearchResult(
                tool_name="ChatGPT",
                description="AI assistant",
                url="https://chat.openai.com",
                use_case="Analysis",
                pricing="Free",
            )
        ]

    # Generate roadmap
    print("\n🗺️  Generating workflow roadmap...")
    roadmap = await generate_workflow_roadmap(task_description, answers, ai_tools)

    print(f"\n✅ Roadmap Generated: {roadmap.task_title}")
    print(f"   Difficulty: {roadmap.difficulty_level}")
    print(f"   Total Time: {roadmap.total_estimated_time}")
    print(f"   Steps: {len(roadmap.steps)}")

    # Validate each step
    print("\n" + "=" * 80)
    print("VALIDATING STEPS")
    print("=" * 80)

    all_valid = True

    for i, step in enumerate(roadmap.steps, 1):
        print(f"\n📍 Step {i}: {step.title}")
        print(f"   Tool: {step.ai_tool}")
        print(f"   Time: {step.estimated_time}")

        # Check course recommendation
        if step.related_course:
            print(f"   📚 Course: {step.related_course['title']}")
            print(f"      URL: {step.related_course['url']}")
            print("   ✅ Course recommendation present")
        else:
            print("   ❌ MISSING: Course recommendation")
            all_valid = False

        # Check evaluator link
        if step.evaluator_link:
            print(f"   ⚡ Evaluator: {step.evaluator_link}")
            print("   ✅ Evaluator link present")
        else:
            print("   ❌ MISSING: Evaluator link")
            all_valid = False

        # Check quiz
        if step.quiz:
            print(f"   📝 Quiz: {step.quiz['question'][:60]}...")
            print(f"      Options: {len(step.quiz['options'])}")
            print(f"      Correct: Option {step.quiz['correct_index'] + 1}")
            print("   ✅ Quiz present")
        else:
            print("   ❌ MISSING: Quiz")
            all_valid = False

        # Check other required fields
        if not step.prompts or len(step.prompts) < 3:
            print(f"   ⚠️  WARNING: Only {len(step.prompts)} prompts (expected 3+)")
        else:
            print(f"   ✅ {len(step.prompts)} prompts present")

        if not step.alternatives:
            print("   ⚠️  WARNING: No alternative tools")
        else:
            print(f"   ✅ {len(step.alternatives)} alternative tools")

    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)

    if all_valid:
        print("✅ ALL VALIDATIONS PASSED!")
        print("   - All steps have course recommendations")
        print("   - All steps have evaluator links")
        print("   - All steps have quizzes")
        return True
    else:
        print("❌ SOME VALIDATIONS FAILED!")
        print("   Check the output above for missing fields")
        return False


async def test_json_export():
    """Test that roadmap can be serialized to JSON"""
    print("\n" + "=" * 80)
    print("TESTING JSON SERIALIZATION WITH API")
    print("=" * 80)

    task_description = "Write a blog post about AI trends"
    answers = {
        "What's your target audience?": "Tech professionals",
        "Desired length?": "1500-2000 words",
    }

    print("🔍 Getting AI tools...")
    try:
        ai_tools = await search_with_gemini_web(task_description, answers)
        if not ai_tools:
            raise Exception("No tools found")
    except:
        ai_tools = [
            AIToolSearchResult(
                tool_name="ChatGPT",
                description="AI writing assistant",
                url="https://chat.openai.com",
                use_case="Generate blog content",
                pricing="Free",
            )
        ]

    print("🗺️  Generating roadmap with API...")
    roadmap = await generate_workflow_roadmap(task_description, answers, ai_tools)

    try:
        import json

        roadmap_dict = roadmap.model_dump()
        json_str = json.dumps(roadmap_dict, indent=2)
        print(f"✅ Successfully serialized to JSON ({len(json_str)} bytes)")

        # Check if all fields are present
        parsed = json.loads(json_str)
        first_step = parsed["steps"][0]

        required_fields = ["related_course", "evaluator_link", "quiz"]
        missing = [f for f in required_fields if f not in first_step]

        if missing:
            print(f"❌ Missing fields in JSON: {missing}")
            return False
        else:
            print("✅ All required fields present in JSON")
            return True

    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False


async def main():
    """Run all tests"""
    try:
        test1_passed = await test_workflow_generation()
        test2_passed = await test_json_export()

        print("\n" + "=" * 80)
        print("FINAL SUMMARY")
        print("=" * 80)
        print(
            f"Workflow Generation Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}"
        )
        print(
            f"JSON Serialization Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}"
        )

        if test1_passed and test2_passed:
            print("\n🎉 ALL TESTS PASSED! The workflow feature is working correctly.")
            sys.exit(0)
        else:
            print("\n❌ SOME TESTS FAILED! Please fix the issues above.")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
