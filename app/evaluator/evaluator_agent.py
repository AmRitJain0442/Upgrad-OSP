"""
Evaluator Agent
Uses Gemini to analyze prompts and AI outputs, providing constructive feedback
"""

import json
import os
import re
from typing import Optional

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from .models import EvaluationFeedback

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


EVALUATION_SYSTEM_PROMPT = """You are an expert prompt engineering evaluator and instructor. Your role is to analyze user prompts and AI outputs, providing constructive, educational feedback.

When evaluating, focus on:
1. **Prompt Quality**: Clarity, specificity, context, structure, constraints
2. **Output Analysis**: Relevance, completeness, accuracy, usefulness
3. **Gap Analysis**: Identify mismatches between prompt intent and output
4. **Root Cause**: Explain what in the prompt led to issues in the output
5. **Improvement Path**: Provide actionable, specific suggestions

Be encouraging but honest. Frame criticism constructively. Always provide a revised prompt example.

Return your analysis in the following JSON format:
{
    "overall_score": <0-100>,
    "prompt_quality": {
        "clarity_score": <0-100>,
        "specificity_score": <0-100>,
        "structure_score": <0-100>,
        "context_score": <0-100>,
        "summary": "<brief assessment>"
    },
    "output_analysis": {
        "relevance_score": <0-100>,
        "completeness_score": <0-100>,
        "quality_score": <0-100>,
        "summary": "<brief assessment>"
    },
    "what_went_wrong": [
        "<specific issue 1>",
        "<specific issue 2>"
    ],
    "what_went_right": [
        "<strength 1>",
        "<strength 2>"
    ],
    "improvement_suggestions": [
        "<actionable suggestion 1>",
        "<actionable suggestion 2>",
        "<actionable suggestion 3>"
    ],
    "revised_prompt": "<improved version of the user's prompt>"
}
"""


def create_evaluation_prompt(
    user_prompt: str,
    ai_output: str,
    output_type: str,
    expected_outcome: Optional[str] = None,
    ai_model_used: Optional[str] = None,
) -> str:
    """Create the evaluation prompt for Gemini"""

    prompt_parts = [
        "# Prompt Evaluation Request\n",
        "## User's Original Prompt:",
        f"```\n{user_prompt}\n```\n",
        "\n## AI Output Received:",
    ]

    if output_type == "text":
        prompt_parts.append(f"```\n{ai_output}\n```\n")
    elif output_type == "image_url":
        prompt_parts.append(f"[Image URL]: {ai_output}\n")
        prompt_parts.append(
            "Note: Evaluate based on the prompt's ability to generate images.\n"
        )
    elif output_type == "pdf_url":
        prompt_parts.append(f"[PDF URL]: {ai_output}\n")
        prompt_parts.append(
            "Note: Evaluate based on the prompt's ability to generate documents.\n"
        )

    if expected_outcome:
        prompt_parts.append(f"\n## User's Expected Outcome:\n{expected_outcome}\n")

    if ai_model_used:
        prompt_parts.append(f"\n## AI Model Used: {ai_model_used}\n")

    prompt_parts.append("\n## Your Task:")
    prompt_parts.append("""
Analyze this prompt-output pair and provide detailed, constructive feedback:

1. Evaluate the **prompt quality** across multiple dimensions
2. Analyze the **AI output** for relevance and quality
3. Identify **what went wrong** (if anything) and explain the root cause in the prompt
4. Highlight **what went right** to reinforce good practices
5. Provide **specific, actionable improvement suggestions**
6. Write a **revised prompt** that addresses the issues

Be educational, encouraging, and specific. Help the user understand the cause-effect relationship between prompt construction and output quality.

Return your analysis in the JSON format specified in the system prompt.
""")

    return "".join(prompt_parts)


def parse_gemini_response(response_text: str) -> dict:
    """Parse Gemini's response and extract JSON"""
    try:
        # First, try to parse directly as JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Remove markdown code blocks if present
        response_text = re.sub(r"```json\s*", "", response_text)
        response_text = re.sub(r"```\s*", "", response_text)

        # Try parsing again after cleanup
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass

        # Try to find JSON in the response using regex
        json_match = re.search(r"\{[\s\S]*\}", response_text)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)

        # If no JSON found, return a structured error
        raise ValueError("No valid JSON found in response")

    except Exception as e:
        # Return a structured fallback response
        return {
            "overall_score": 50,
            "prompt_quality": {
                "clarity_score": 50,
                "specificity_score": 50,
                "structure_score": 50,
                "context_score": 50,
                "summary": f"Unable to parse evaluation: {str(e)}",
            },
            "output_analysis": {
                "relevance_score": 50,
                "completeness_score": 50,
                "quality_score": 50,
                "summary": "Could not analyze output due to parsing error",
            },
            "what_went_wrong": [f"JSON parsing error: {str(e)}"],
            "what_went_right": [],
            "improvement_suggestions": ["Please try again"],
            "revised_prompt": "",
        }


async def evaluate_prompt_output(
    user_prompt: str,
    ai_output: str,
    output_type: str = "text",
    expected_outcome: Optional[str] = None,
    ai_model_used: Optional[str] = None,
) -> tuple[EvaluationFeedback, str]:
    """
    Evaluate a prompt-output pair using Gemini

    Returns:
        tuple: (EvaluationFeedback, raw_analysis)
    """
    try:
        # Create the evaluation prompt
        eval_prompt = create_evaluation_prompt(
            user_prompt=user_prompt,
            ai_output=ai_output,
            output_type=output_type,
            expected_outcome=expected_outcome,
            ai_model_used=ai_model_used,
        )

        # Use Gemini to evaluate
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )

        # Generate evaluation
        response = model.generate_content([EVALUATION_SYSTEM_PROMPT, eval_prompt])

        # Check if response has valid content
        if not response.parts:
            raise Exception(
                f"No response from Gemini. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'unknown'}"
            )

        raw_analysis = response.text

        # Parse the response
        parsed_feedback = parse_gemini_response(raw_analysis)

        # Create EvaluationFeedback object
        feedback = EvaluationFeedback(**parsed_feedback)

        return feedback, raw_analysis

    except Exception as e:
        # Return a fallback evaluation
        fallback_feedback = EvaluationFeedback(
            overall_score=50,
            prompt_quality={
                "clarity_score": 50,
                "specificity_score": 50,
                "structure_score": 50,
                "context_score": 50,
                "summary": f"Evaluation error: {str(e)}",
            },
            output_analysis={
                "relevance_score": 50,
                "completeness_score": 50,
                "quality_score": 50,
                "summary": "Could not analyze output",
            },
            what_went_wrong=[f"Error during evaluation: {str(e)}"],
            what_went_right=[],
            improvement_suggestions=["Please try again or check your API key"],
            revised_prompt=None,
        )

        return fallback_feedback, f"Error: {str(e)}"


def format_evaluation_for_display(feedback: EvaluationFeedback) -> str:
    """Format evaluation feedback for readable display"""

    output = []

    # Overall Score
    output.append(f"## Overall Score: {feedback.overall_score}/100\n")

    # Prompt Quality
    output.append("### Prompt Quality Analysis")
    pq = feedback.prompt_quality
    output.append(f"- **Clarity**: {pq.get('clarity_score', 0)}/100")
    output.append(f"- **Specificity**: {pq.get('specificity_score', 0)}/100")
    output.append(f"- **Structure**: {pq.get('structure_score', 0)}/100")
    output.append(f"- **Context**: {pq.get('context_score', 0)}/100")
    output.append(f"\n{pq.get('summary', '')}\n")

    # Output Analysis
    output.append("### Output Analysis")
    oa = feedback.output_analysis
    output.append(f"- **Relevance**: {oa.get('relevance_score', 0)}/100")
    output.append(f"- **Completeness**: {oa.get('completeness_score', 0)}/100")
    output.append(f"- **Quality**: {oa.get('quality_score', 0)}/100")
    output.append(f"\n{oa.get('summary', '')}\n")

    # What Went Right
    if feedback.what_went_right:
        output.append("### What Went Right")
        for item in feedback.what_went_right:
            output.append(f"- {item}")
        output.append("")

    # What Went Wrong
    if feedback.what_went_wrong:
        output.append("### What Went Wrong")
        for item in feedback.what_went_wrong:
            output.append(f"- {item}")
        output.append("")

    # Improvement Suggestions
    if feedback.improvement_suggestions:
        output.append("### Improvement Suggestions")
        for i, suggestion in enumerate(feedback.improvement_suggestions, 1):
            output.append(f"{i}. {suggestion}")
        output.append("")

    # Revised Prompt
    if feedback.revised_prompt:
        output.append("### Revised Prompt Suggestion")
        output.append(f"```\n{feedback.revised_prompt}\n```")

    return "\n".join(output)
