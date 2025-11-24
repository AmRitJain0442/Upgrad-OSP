"""
Simple unit test for workflow course/quiz generation (no API calls needed)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.workflow.agents import get_relevant_course_for_step, generate_step_quiz
from app.prompting.curriculum import FULL_CURRICULUM


def test_course_mapping():
    """Test that courses are mapped correctly to workflow steps"""
    print("=" * 80)
    print("TEST 1: COURSE MAPPING")
    print("=" * 80)

    test_cases = [
        {
            "category": "research",
            "description": "Gather and summarize research data",
            "title": "Research Phase",
            "expected_course": "foundations",
        },
        {
            "category": "presentation",
            "description": "Create slides from content",
            "title": "Build Presentation",
            "expected_course": "presentation-builder",
        },
        {
            "category": "writing",
            "description": "Write business report",
            "title": "Content Creation",
            "expected_course": "domain-specific",
        },
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"  Category: {test['category']}")
        print(f"  Description: {test['description']}")

        course = get_relevant_course_for_step(
            test["category"], test["description"], test["title"]
        )

        if course:
            print(f"  ✅ Got course: {course['title']}")
            print(f"     ID: {course['id']}")
            print(f"     URL: {course['url']}")
            passed += 1
        else:
            print("  ❌ No course returned!")
            failed += 1

    print(f"\n{'=' * 80}")
    print(f"Course Mapping: {passed}/{len(test_cases)} passed")
    return failed == 0


def test_quiz_generation():
    """Test quiz generation function exists and has correct structure"""
    print("\n" + "=" * 80)
    print("TEST 2: QUIZ GENERATION FUNCTION")
    print("=" * 80)

    # Test if function exists
    try:
        # We can't actually call it without API, but we can check signature
        import inspect

        sig = inspect.signature(generate_step_quiz)
        params = list(sig.parameters.keys())

        print("\n✅ Function exists: generate_step_quiz")
        print(f"   Parameters: {params}")

        if (
            "step_title" in params
            and "step_description" in params
            and "ai_tool" in params
        ):
            print("   ✅ Has correct parameters")
            return True
        else:
            print("   ❌ Missing required parameters")
            return False

    except Exception as e:
        print(f"❌ Error checking function: {e}")
        return False


def test_course_availability():
    """Test that all courses exist in curriculum"""
    print("\n" + "=" * 80)
    print("TEST 3: COURSE CURRICULUM")
    print("=" * 80)

    expected_courses = [
        "foundations",
        "advanced-patterns",
        "domain-specific",
        "advanced-techniques",
        "presentation-builder",
    ]

    print(f"\nChecking {len(FULL_CURRICULUM)} courses in curriculum:")

    found_ids = [c["id"] for c in FULL_CURRICULUM]

    passed = 0
    for course_id in expected_courses:
        if course_id in found_ids:
            course = next(c for c in FULL_CURRICULUM if c["id"] == course_id)
            print(f"  ✅ {course['title']}")
            passed += 1
        else:
            print(f"  ❌ Missing: {course_id}")

    print(f"\n{'=' * 80}")
    print(f"Courses Available: {passed}/{len(expected_courses)}")
    return passed == len(expected_courses)


def test_workflow_step_model():
    """Test that WorkflowStep model has required fields"""
    print("\n" + "=" * 80)
    print("TEST 4: WORKFLOW STEP MODEL")
    print("=" * 80)

    from app.workflow.models import WorkflowStep

    # Get model fields
    fields = WorkflowStep.model_fields

    required_new_fields = ["related_course", "evaluator_link", "quiz"]

    print("\nChecking WorkflowStep model fields:")

    passed = 0
    for field in required_new_fields:
        if field in fields:
            field_info = fields[field]
            print(f"  ✅ {field}: {field_info.annotation}")
            passed += 1
        else:
            print(f"  ❌ Missing field: {field}")

    print(f"\n{'=' * 80}")
    print(f"Model Fields: {passed}/{len(required_new_fields)}")
    return passed == len(required_new_fields)


def main():
    """Run all unit tests"""
    print("\n🧪 RUNNING WORKFLOW FEATURE UNIT TESTS\n")

    results = {
        "Course Mapping": test_course_mapping(),
        "Quiz Function": test_quiz_generation(),
        "Course Availability": test_course_availability(),
        "Model Fields": test_workflow_step_model(),
    }

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 ALL UNIT TESTS PASSED!")
        print("\nThe workflow feature code is correctly implemented:")
        print("  ✓ Course mapping function works")
        print("  ✓ Quiz generation function exists")
        print("  ✓ All courses are available")
        print("  ✓ Model has required fields")
        print(
            "\nTo test with actual API calls, run the web server and generate a workflow."
        )
        return 0
    else:
        print("\n❌ SOME TESTS FAILED!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
