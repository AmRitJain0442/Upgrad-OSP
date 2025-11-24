"""
Pydantic-AI agents for prompting module with streaming support
"""

import logging
from typing import AsyncIterator, cast
from pydantic_ai import Agent
from pydantic import BaseModel

from app.base_model import get_google_model
from app.prompting.utils import analyze_prompt_quality

logger = logging.getLogger(__name__)


class PromptAnalysisResult(BaseModel):
    """Structured output for prompt analysis"""

    feedback: str
    has_constraints: bool
    has_role: bool
    has_structure: bool
    suggestions: list[str]


class SummaryResult(BaseModel):
    """Structured output for document summarization"""

    summary: str
    quality_score: int


# AI Tutor Agent - Fast model for real-time guidance
tutor_agent = Agent(
    model=get_google_model("gemini-2.5-flash", thinking_enabled=False),
    system_prompt="""You are an expert AI prompt engineering tutor guiding learners through a structured curriculum.

    🎯 YOUR ROLE:
    - Guide learners through progressive lessons (Foundations → Advanced Patterns → Optimization → Real-World)
    - Provide CONTEXTUAL help based on where they are in their learning journey
    - Give NUDGES, not answers - help users discover solutions through guided questions
    - Be encouraging, patient, and celebratory of progress

    📚 CURRICULUM STRUCTURE YOU'RE TEACHING:
    
    **Module 1: Foundations**
    1. Focused Summarization - Teaching constraint-based prompts to prevent hallucination
    2. Role Assignment - Teaching how to assign AI specific perspectives/expertise
    3. Chain-of-Thought - Teaching step-by-step reasoning prompts
    4. Real-world Practice - Combining all foundation techniques
    
    **Module 2: Advanced Patterns**
    1. Few-Shot Learning - Teaching through examples
    2. Output Formatting - Controlling structure (JSON, tables, etc.)
    3. Conditional Logic - Dynamic prompts with if/then logic
    4. Multi-step Workflows - Chaining multiple AI tasks
    
    **Module 3: Optimization**
    1. Token Efficiency - Concise yet effective prompts
    2. Context Management - Handling large documents
    3. Error Handling - Building robust prompts
    4. Performance Tuning - Speed vs quality tradeoffs
    
    **Module 4: Real-World Applications**
    1. Business Reports - Professional documentation
    2. Technical Documentation - API docs, guides
    3. Creative Content - Marketing, storytelling
    4. Data Analysis - Insights and recommendations

    💡 TEACHING APPROACH:
    1. **Context Awareness**: You'll receive info about:
       - Current lesson and learning objective
       - User's attempt number (1st try vs 3rd try needs different help)
       - What they've already tried
       - Their specific prompt and output
    
    2. **Progressive Hints**: 
       - First attempt: Gentle nudge toward the concept (e.g., "Think about adding rules...")
       - Second attempt: More specific guidance (e.g., "Try starting with 'Based only on...'")
       - Third attempt: Near-example (e.g., "Structure it like: [Role] + [Task] + [Constraint]")
       - NEVER give the exact answer - always leave room for learning
    
    3. **Socratic Method**: Ask questions that guide discovery:
       - "What might happen if the AI uses external knowledge?"
       - "How could you make the AI think step-by-step?"
       - "What role would give the best perspective here?"
    
    4. **Positive Reinforcement**:
       - Always acknowledge what they did RIGHT first
       - Then suggest ONE improvement area (don't overwhelm)
       - Celebrate when they apply a concept correctly
    
    5. **Formatting**:
       - Use **bold** for key concepts
       - Use `code blocks` for example phrases
       - Keep responses 2-4 sentences (concise but helpful)
       - Use emojis sparingly for emphasis (✅ ❌ 💡 🎯)

    🚫 WHAT NOT TO DO:
    - Don't write the prompt for them
    - Don't give multiple suggestions at once (overwhelming)
    - Don't assume they know terminology - explain briefly
    - Don't be discouraging - frame everything as learning
    - Don't contradict the curriculum structure or lesson objectives
    
    Remember: You're teaching THINKING, not just techniques. Help them understand WHY each concept matters.
    """,
    retries=2,
)


# Workspace Agent - For executing user prompts on documents
workspace_agent = Agent(
    model=get_google_model("gemini-2.5-flash"),
    system_prompt="""You are a Workspace AI assistant helping learners practice prompt engineering.

    🎯 YOUR PURPOSE:
    You're part of a learning platform where users are testing their prompts. Your job is to execute their 
    prompts EXACTLY as written, demonstrating how well (or poorly) their prompt works.

    ✅ CORE PRINCIPLES:
    
    1. **Follow Instructions Precisely**:
       - If they say "based only on the document," use ONLY the document
       - If they say "do not use external knowledge," don't add anything external
       - If they forget to add constraints, you WILL add external knowledge (to teach them why constraints matter)
    
    2. **Respect Role Assignment**:
       - If they say "You are a [role]", fully adopt that persona and expertise level
       - If no role is specified, respond as a general AI assistant
    
    3. **Follow Structure Instructions**:
       - If they ask for "step by step", show your reasoning process
       - If they specify a format (JSON, table, bullets), use it exactly
       - If they say "First... Then... Finally...", follow that sequence
    
    4. **Demonstrate Prompt Quality**:
       - A well-constrained prompt = focused, accurate response
       - A vague prompt = generic or potentially hallucinated response
       - A structured prompt = organized, systematic response
       - Your output quality should REFLECT their prompt quality
    
    5. **Output Formatting**:
       - Use markdown for readability (headings, bold, lists, code blocks)
       - Be professional and clear
       - Match the tone/style if they specified one
    
    🎓 TEACHING THROUGH EXECUTION:
    - If their prompt is strong (has constraints, role, structure) → deliver excellent results
    - If their prompt is weak (vague, no constraints) → deliver okay but generic results
    - If they forgot constraints → you might add info beyond the document (teaching moment!)
    - If they forgot structure → give an unstructured response (teaching moment!)
    
    Your behavior teaches them: "Good prompts get good results. Specific prompts get specific results."
    
    ⚠️ IMPORTANT:
    - Never explain what you're doing or why (you're not the tutor)
    - Just execute the prompt as written
    - Let your output quality demonstrate the prompt's effectiveness
    - The Tutor AI will provide learning feedback - you just show results
    """,
    retries=1,
)


# Prompt Analysis Agent - For real-time analysis with structured output
analysis_agent = Agent(
    model=get_google_model("gemini-flash-lite-latest"),
    output_type=PromptAnalysisResult,
    system_prompt="""You provide real-time analysis of prompts as learners type them in a prompt engineering course.

    🎯 YOUR TASK:
    Analyze prompts for quality and provide quick, actionable feedback that appears as they type.
    
    📊 EVALUATION CRITERIA:
    
    1. **Constraints** (Prevents hallucination):
       ✅ Good: "based only on", "using only the information provided", "do not use external knowledge"
       ❌ Missing: No mention of limiting to provided information
       
    2. **Role Assignment** (Provides perspective):
       ✅ Good: "You are a [specific expert/role]", "As a [profession]"
       ❌ Missing: No role or perspective assigned
       
    3. **Structure** (Organizes thinking):
       ✅ Good: "step by step", "First... Then... Finally", "Let's think through", specific format requests
       ❌ Missing: No guidance on how to approach the task
    
    📝 FEEDBACK GUIDELINES:
    
    1. **Keep it Short**: 1-2 sentences max - they're reading while typing
    
    2. **Be Specific**: Don't say "add constraints" - say "Consider adding 'based only on the document'"
    
    3. **One Thing at a Time**: Focus on the MOST important missing element
       - Lesson 1 (Focused Summarization) → Emphasize constraints
       - Lesson 2 (Role Assignment) → Emphasize roles
       - Lesson 3 (Chain-of-Thought) → Emphasize structure
       - Lesson 4+ → Look for combinations
    
    4. **Positive Framing**: 
       - ✅ "Try adding a constraint like 'based only on...'"
       - ❌ "Your prompt is missing constraints"
    
    5. **Context-Aware**: If you're told what lesson they're on, focus on THAT technique
    
    6. **Progressive**: 
       - If they have nothing → suggest the main concept
       - If they have something → suggest refinement
       - If it's good → acknowledge and suggest optional enhancement
    
    🎓 LEARNING FOCUS:
    Your suggestions should guide them toward the lesson objective without giving them the exact answer.
    Make them think about WHY each element matters, not just WHAT to add.
    
    📤 OUTPUT FORMAT:
    - feedback: Short, encouraging guidance (1-2 sentences)
    - suggestions: 1-3 concrete, actionable improvements (if needed)
    - Keep suggestions brief - they're hints, not instructions
    
    Remember: You're the "smart autocomplete" - helpful but not intrusive, specific but not prescriptive.
    """,
)


async def stream_tutor_response(
    message: str, lesson_context: dict | None = None
) -> AsyncIterator[str]:
    """
    Stream AI tutor response in real-time with lesson context

    Args:
        message: User's message to the tutor
        lesson_context: Dict containing:
            - module: Current module name
            - lesson: Current lesson name and objective
            - step: Current lesson step (upload, prompt, review, etc.)
            - attempts: Number of attempts on current prompt
            - last_prompt: The user's last prompt (if any)
            - last_feedback: Previous feedback given (if any)

    Yields:
        str: Chunks of the response as they're generated
    """
    try:
        # Build contextual prompt
        if lesson_context:
            context_parts = []

            if lesson_context.get("module"):
                context_parts.append(f"Module: {lesson_context['module']}")

            if lesson_context.get("lesson"):
                context_parts.append(f"Current Lesson: {lesson_context['lesson']}")

            if lesson_context.get("step"):
                context_parts.append(f"Lesson Step: {lesson_context['step']}")

            if lesson_context.get("attempts") and lesson_context["attempts"] > 0:
                context_parts.append(f"Attempt Number: {lesson_context['attempts']}")

            if lesson_context.get("last_prompt"):
                context_parts.append(
                    f"User's Last Prompt: {lesson_context['last_prompt']}"
                )

            context_str = "\n".join(context_parts)
            full_prompt = (
                f"[LESSON CONTEXT]\n{context_str}\n\n[USER MESSAGE]\n{message}"
            )
        else:
            full_prompt = message

        async with tutor_agent.run_stream(full_prompt) as response:
            async for text in response.stream_text(delta=True):
                yield text

    except Exception as e:
        logger.error(f"Error in tutor streaming: {e}")
        yield "I apologize, but I encountered an error. Please try again."


async def analyze_prompt_realtime(
    prompt: str, lesson_info: dict | None = None
) -> PromptAnalysisResult:
    """
    Analyze prompt in real-time and provide structured feedback

    Args:
        prompt: User's prompt to analyze
        lesson_info: Dict containing:
            - submodule_id: Current submodule number (1-4)
            - lesson_name: Name of current lesson
            - focus: Primary technique being taught (constraints, role, structure, etc.)

    Returns:
        PromptAnalysisResult with feedback and suggestions
    """
    try:
        # Get basic analysis first
        basic_analysis = analyze_prompt_quality(prompt)

        # Build context with lesson awareness
        context_parts = [f'Prompt to analyze: "{prompt}"']

        if lesson_info:
            if lesson_info.get("lesson_name"):
                context_parts.append(f"\nLesson Context: {lesson_info['lesson_name']}")

            if lesson_info.get("submodule_id"):
                lesson_focus = {
                    1: "Focus on CONSTRAINTS to prevent hallucination",
                    2: "Focus on ROLE ASSIGNMENT for perspective",
                    3: "Focus on STRUCTURE for step-by-step reasoning",
                    4: "Focus on COMBINING all techniques",
                }
                focus = lesson_focus.get(lesson_info["submodule_id"], "")
                if focus:
                    context_parts.append(f"Lesson Focus: {focus}")

        context_parts.append(f"""
Basic detection results:
- Has constraints: {basic_analysis["has_constraints"]}
- Has role assignment: {basic_analysis["has_role"]}  
- Has structure: {basic_analysis["has_structure"]}

Provide brief, lesson-appropriate feedback and specific suggestions.""")

        context = "\n".join(context_parts)

        # Get AI feedback - Pydantic-AI guarantees output type
        result = await analysis_agent.run(context)
        # Type annotation: agent with output_type=PromptAnalysisResult guarantees this type
        output = cast(PromptAnalysisResult, result.output)

        # Override detection flags with our basic analysis (more reliable for keyword detection)
        output.has_constraints = basic_analysis["has_constraints"]
        output.has_role = basic_analysis["has_role"]
        output.has_structure = basic_analysis["has_structure"]

        # Merge suggestions if AI didn't provide enough
        if len(output.suggestions) < 2 and basic_analysis["suggestions"]:
            output.suggestions.extend(basic_analysis["suggestions"][:2])

        return output

    except Exception as e:
        logger.error(f"Error in prompt analysis: {e}")
        # Return basic analysis on error
        basic = analyze_prompt_quality(prompt)
        return PromptAnalysisResult(
            feedback="Could not get AI feedback, but here are some suggestions:",
            has_constraints=basic["has_constraints"],
            has_role=basic["has_role"],
            has_structure=basic["has_structure"],
            suggestions=basic["suggestions"],
        )


async def stream_workspace_response(
    prompt: str, document_text: str
) -> AsyncIterator[str]:
    """
    Stream workspace AI response for document summarization

    Args:
        prompt: User's prompt for summarization
        document_text: The document content to summarize

    Yields:
        str: Chunks of the summary as they're generated
    """
    try:
        full_prompt = f"{prompt}\n\nDocument:\n{document_text}"

        async with workspace_agent.run_stream(full_prompt) as response:
            async for text in response.stream_text(delta=True):
                yield text

    except Exception as e:
        logger.error(f"Error in workspace streaming: {e}")
        yield "An error occurred during summarization. Please try again."


async def generate_tutor_message(
    message: str, lesson_context: dict | None = None
) -> str:
    """
    Generate a complete tutor message (non-streaming)

    Args:
        message: Message to the tutor
        lesson_context: Dict with lesson information (module, lesson, step, attempts, etc.)

    Returns:
        str: Complete response
    """
    try:
        # Build contextual prompt
        if lesson_context:
            context_parts = []

            if lesson_context.get("module"):
                context_parts.append(f"Module: {lesson_context['module']}")

            if lesson_context.get("lesson"):
                context_parts.append(f"Current Lesson: {lesson_context['lesson']}")

            if lesson_context.get("step"):
                context_parts.append(f"Lesson Step: {lesson_context['step']}")

            if lesson_context.get("attempts") and lesson_context["attempts"] > 0:
                context_parts.append(f"Attempt Number: {lesson_context['attempts']}")

            if lesson_context.get("last_prompt"):
                context_parts.append(
                    f"User's Last Prompt: {lesson_context['last_prompt']}"
                )

            context_str = "\n".join(context_parts)
            full_prompt = (
                f"[LESSON CONTEXT]\n{context_str}\n\n[USER MESSAGE]\n{message}"
            )
        else:
            full_prompt = message

        result = await tutor_agent.run(full_prompt)
        return result.output
    except Exception as e:
        logger.error(f"Error generating tutor message: {e}")
        return "I apologize, but I encountered an error. Please try again."


async def generate_workspace_summary(
    prompt: str, document_text: str
) -> tuple[str, bool]:
    """
    Generate a complete workspace summary (non-streaming)

    Args:
        prompt: User's summarization prompt
        document_text: Document to summarize

    Returns:
        tuple: (summary text, has_constraints)
    """
    try:
        full_prompt = f"{prompt}\n\nDocument:\n{document_text}"
        result = await workspace_agent.run(full_prompt)

        # Analyze if prompt had constraints
        analysis = analyze_prompt_quality(prompt)

        return result.output, analysis["has_constraints"]
    except Exception as e:
        logger.error(f"Error generating workspace summary: {e}")
        return "An error occurred during summarization. Please try again.", False


async def generate_presentation_analysis(presentation_text: str, topic: str):
    """
    Analyze a presentation using Gemini API with structured feedback

    Args:
        presentation_text: The full presentation content
        topic: The presentation topic

    Returns:
        PresentationAnalysis with strengths, improvements, and suggestions
    """
    from app.prompting.models import PresentationAnalysis

    try:
        analysis_prompt = f"""You are an expert presentation designer and trainer. Analyze this presentation and provide constructive feedback.

PRESENTATION TOPIC: {topic}

PRESENTATION CONTENT:
{presentation_text}

Please analyze this presentation and provide feedback in 3 categories. Be specific, constructive, and supportive.

For each category, provide 3-4 specific points (not generic feedback).

Return your analysis in this exact JSON format:
{{
    "strengths": [
        "Specific thing done well #1",
        "Specific thing done well #2",
        "Specific thing done well #3"
    ],
    "improvements": [
        "Specific area for improvement #1",
        "Specific area for improvement #2",
        "Specific area for improvement #3"
    ],
    "suggestions": [
        "Actionable suggestion #1",
        "Actionable suggestion #2",
        "Actionable suggestion #3"
    ]
}}

Focus on:
- Content clarity and organization
- Visual presentation effectiveness
- Audience engagement potential
- Message coherence
- Practical applicability"""

        # Create a specialized analysis agent
        from pydantic import BaseModel

        class AnalysisOutput(BaseModel):
            strengths: list[str]
            improvements: list[str]
            suggestions: list[str]

        analysis_agent = Agent(
            model=get_google_model("gemini-flash-latest", thinking_enabled=False),
            result_type=AnalysisOutput,
            system_prompt="You are an expert presentation analyst. Provide constructive, specific feedback.",
        )

        result = await analysis_agent.run(analysis_prompt)

        return PresentationAnalysis(
            strengths=result.data.strengths,
            improvements=result.data.improvements,
            suggestions=result.data.suggestions,
        )

    except Exception as e:
        logger.error(f"Error generating presentation analysis: {e}")
        # Return default analysis if API fails
        return PresentationAnalysis(
            strengths=["Well-structured content", "Clear topic focus"],
            improvements=[
                "Consider adding more visual elements",
                "Expand on key points",
            ],
            suggestions=["Add more examples", "Include interactive elements"],
        )
