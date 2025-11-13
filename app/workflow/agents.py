"""
AI agents for workflow automation using Gemini, Perplexity, and Tavily APIs
"""
import os
import json
from typing import List, Dict, Any, Optional
import httpx
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from app.workflow.models import (
    WorkflowQuestion,
    WorkflowStep,
    WorkflowRoadmap,
    AIToolSearchResult,
    WorkflowQuestionsResponse
)
from app.workflow.ai_tools_database import (
    get_relevant_tools,
    get_all_tools,
    format_tools_for_prompt
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: No Gemini API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env")


async def generate_workflow_questions(task_input: str) -> List[WorkflowQuestion]:
    """
    Use Gemini to generate follow-up questions about the task
    """
    try:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""You are helping a user automate a mundane task using AI tools.
They want to: {task_input}

Generate 3-5 follow-up questions to better understand their needs. Questions should cover:
- Specific requirements and constraints
- Input/output formats
- Quality expectations
- Time constraints
- Technical skill level

Return ONLY a JSON array of objects with "question" and "context" fields.
Example: [{{"question": "What format is your input data?", "context": "This helps me recommend the right tools"}}]
"""

        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        # Parse JSON response
        content = response.text.strip()
        if content.startswith('```json'):
            content = content[7:-3].strip()
        elif content.startswith('```'):
            content = content[3:-3].strip()
        
        questions_data = json.loads(content)
        return [WorkflowQuestion(**q) for q in questions_data]
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        # Fallback questions
        return [
            WorkflowQuestion(
                question="What is the main input you'll be working with?",
                context="Understanding your input helps me recommend the right AI tools"
            ),
            WorkflowQuestion(
                question="What output format do you need?",
                context="This determines which tools can deliver your desired results"
            ),
            WorkflowQuestion(
                question="How much time do you have for this task?",
                context="Some AI tools are faster but less thorough than others"
            )
        ]


async def search_perplexity(query: str) -> List[AIToolSearchResult]:
    """
    Search for AI tools using Perplexity API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an AI tool expert. Return ONLY valid JSON arrays."
                        },
                        {
                            "role": "user",
                            "content": f"""Find 3-5 AI tools for this task: {query}
Return ONLY a JSON array with this structure:
[{{"tool_name": "Tool Name", "description": "Brief description", "url": "https://...", "use_case": "Specific use case", "pricing": "Free/Paid/Freemium"}}]"""
                        }
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1000
                },
                timeout=30.0
            )
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Clean up JSON
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            tools_data = json.loads(content)
            return [AIToolSearchResult(**tool) for tool in tools_data]
            
    except Exception as e:
        print(f"Perplexity search error: {e}")
        return []


async def search_tavily(query: str) -> List[AIToolSearchResult]:
    """
    Search for AI tools using Tavily API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": f"{query} AI tools automation",
                    "search_depth": "basic",
                    "include_answer": True,
                    "max_results": 5
                },
                timeout=30.0
            )
            
            data = response.json()
            results = []
            
            for item in data.get('results', [])[:5]:
                results.append(AIToolSearchResult(
                    tool_name=item.get('title', 'Unknown Tool'),
                    description=item.get('content', '')[:200],
                    url=item.get('url', ''),
                    use_case=query,
                    pricing="Check website"
                ))
            
            return results
            
    except Exception as e:
        print(f"Tavily search error: {e}")
        return []


async def generate_workflow_roadmap(
    task_description: str,
    answers: Dict[str, str],
    ai_tools: List[AIToolSearchResult]
) -> WorkflowRoadmap:
    """
    Generate a complete workflow roadmap using Gemini
    """
    try:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        tools_summary = "\n".join([
            f"- **{tool.tool_name}** ({tool.pricing})\n  URL: {tool.url}\n  Description: {tool.description}\n  Use Case: {tool.use_case}"
            for tool in ai_tools[:15]
        ])
        
        answers_summary = "\n".join([f"- {q}: {a}" for q, a in answers.items()])
        
        prompt = f"""You are an expert workflow architect with deep knowledge of AI tools. Create a COMPREHENSIVE, DETAILED, step-by-step workflow roadmap.

TASK: {task_description}

USER REQUIREMENTS:
{answers_summary}

AVAILABLE AI TOOLS (including mainstream and specialized):
{tools_summary}

Create a THOROUGH workflow that:
✓ Breaks the task into 5-8 logical, sequential steps
✓ Recommends BOTH mainstream AND lesser-known specialized tools
✓ Provides COPY-PASTE ready prompts for each tool
✓ Includes specific tips from real-world usage
✓ Lists honest pros and cons (be realistic, not promotional)
✓ Estimates accurate time requirements
✓ Suggests free alternatives where applicable
✓ Explains WHY each tool is chosen for each step

For EACH step, provide:
1. **Clear title** - What this step accomplishes
2. **Detailed description** - Exactly what to do (2-3 sentences)
3. **AI tool selection** - Which tool and WHY it's best for this step
4. **Tool URL** - Direct link to the tool
5. **5 SPECIFIC prompts** - Ready-to-use, task-specific prompts (not generic)
6. **5 practical tips** - Actionable advice for best results
7. **3 pros** - Real advantages of this approach
8. **3 cons** - Honest limitations or challenges
9. **Realistic time** - Actual estimated time needed
10. **Dependencies** - Which previous steps must be completed
11. **2 alternatives** - Other tools that could work (with free options if possible)

IMPORTANT: Make prompts SPECIFIC to the user's task, not generic templates.
IMPORTANT: Include both popular tools AND hidden gems/specialized tools.
IMPORTANT: Suggest free alternatives alongside paid options.

Return ONLY valid JSON with this exact structure:
{{
  "task_title": "Title",
  "task_description": "Description",
  "total_estimated_time": "X hours",
  "difficulty_level": "Beginner/Intermediate/Advanced",
  "steps": [
    {{
      "id": "step-1",
      "title": "Step Title",
      "description": "What to do",
      "ai_tool": "Tool Name",
      "tool_url": "https://...",
      "prompts": ["Prompt 1", "Prompt 2", "Prompt 3"],
      "tips": ["Tip 1", "Tip 2", "Tip 3"],
      "pros": ["Pro 1", "Pro 2", "Pro 3"],
      "cons": ["Con 1", "Con 2", "Con 3"],
      "estimated_time": "30 minutes",
      "dependencies": [],
      "alternatives": [{{"tool": "Alt Tool", "reason": "Why use this"}}]
    }}
  ]
}}"""

        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        content = response.text.strip()
        if content.startswith('```json'):
            content = content[7:-3].strip()
        elif content.startswith('```'):
            content = content[3:-3].strip()
        
        roadmap_data = json.loads(content)
        return WorkflowRoadmap(**roadmap_data)
        
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        # Fallback roadmap
        return WorkflowRoadmap(
            task_title=task_description,
            task_description="Automated workflow for your task",
            total_estimated_time="2-3 hours",
            difficulty_level="Intermediate",
            steps=[
                WorkflowStep(
                    id="step-1",
                    title="Research Phase",
                    description="Gather information about your task",
                    ai_tool="ChatGPT or Perplexity",
                    tool_url="https://chat.openai.com",
                    prompts=[
                        "What are the best practices for [your task]?",
                        "Show me examples of [your desired output]",
                        "What tools are commonly used for [your task]?"
                    ],
                    tips=[
                        "Be specific in your questions",
                        "Ask for examples",
                        "Request step-by-step guidance"
                    ],
                    pros=[
                        "Fast research",
                        "Comprehensive information",
                        "Interactive clarification"
                    ],
                    cons=[
                        "May need fact-checking",
                        "Could be overwhelming",
                        "Requires good prompting skills"
                    ],
                    estimated_time="30-45 minutes",
                    dependencies=[],
                    alternatives=[
                        {"tool": "Perplexity", "reason": "Better for research with citations"}
                    ]
                )
            ]
        )


async def search_with_gemini_web(task_description: str, answers: Dict[str, str]) -> List[AIToolSearchResult]:
    """
    Use Gemini with web search to find AI tools
    """
    try:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        answers_summary = "\n".join([f"- {q}: {a}" for q, a in answers.items()])
        
        # Extract keywords from task
        keywords = task_description.lower().split()
        relevant_db_tools = get_relevant_tools(keywords[:5])  # Get relevant tools from database
        
        db_tools_context = format_tools_for_prompt(relevant_db_tools[:15]) if relevant_db_tools else "No specific database matches"
        
        prompt = f"""You are an expert AI tools researcher. Find the BEST AI tools for this task using web search.

TASK: {task_description}

USER REQUIREMENTS:
{answers_summary}

REFERENCE TOOLS DATABASE (include these if relevant):
{db_tools_context}

Search the web thoroughly and recommend 8-15 specific AI tools, including:
1. Both mainstream AND lesser-known specialized tools
2. Free alternatives alongside paid options
3. Tools specifically designed for this use case
4. Mix of established and emerging AI tools

For EACH tool, provide:
- Exact official name
- Clear 1-2 sentence description of capabilities
- Official website URL (verify it's correct)
- Specific use case for THIS task
- Accurate pricing (Free/Paid/Freemium)

Return ONLY valid JSON array:
[{{
  "tool_name": "Exact Tool Name",
  "description": "Clear description focusing on key capabilities",
  "url": "https://official-website.com",
  "use_case": "Exactly how it helps with this specific task",
  "pricing": "Free/Paid/Freemium"
}}]"""

        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        content = response.text.strip()
        if content.startswith('```json'):
            content = content[7:-3].strip()
        elif content.startswith('```'):
            content = content[3:-3].strip()
        
        tools_data = json.loads(content)
        return [AIToolSearchResult(**tool) for tool in tools_data]
        
    except Exception as e:
        print(f"Gemini web search error: {e}")
        return []


async def search_with_database(task_description: str) -> List[AIToolSearchResult]:
    """
    Search the curated AI tools database
    """
    try:
        # Extract keywords from task description
        keywords = [word.lower() for word in task_description.split() if len(word) > 3]
        
        # Get relevant tools from database
        relevant_tools = get_relevant_tools(keywords)
        
        # Convert to AIToolSearchResult format
        results = []
        for tool in relevant_tools[:10]:
            results.append(AIToolSearchResult(
                tool_name=tool['tool_name'],
                description=tool['description'],
                url=tool['url'],
                use_case=tool['use_case'],
                pricing=tool['pricing']
            ))
        
        return results
        
    except Exception as e:
        print(f"Database search error: {e}")
        return []


async def search_ai_tools(task_description: str, answers: Dict[str, str]) -> List[AIToolSearchResult]:
    """
    Comprehensive AI tools search using multiple methods:
    1. Curated database search (fast, reliable)
    2. Gemini web search (thorough, up-to-date)
    3. Perplexity and Tavily (supplementary)
    """
    # Create search query from task and answers
    query_parts = [task_description]
    query_parts.extend(answers.values())
    search_query = " ".join(query_parts)
    
    # Try all search methods in parallel
    database_results = await search_with_database(task_description)
    gemini_web_results = await search_with_gemini_web(task_description, answers)
    perplexity_results = await search_perplexity(search_query)
    tavily_results = await search_tavily(search_query)
    
    # Prioritize: Database first (most reliable), then Gemini web, then others
    all_results = database_results + gemini_web_results + perplexity_results + tavily_results
    
    # If we got no results, return fallback tools
    if not all_results:
        return [
            AIToolSearchResult(
                tool_name="ChatGPT",
                description="Versatile AI assistant for text generation, analysis, and automation",
                url="https://chat.openai.com",
                use_case="General purpose automation and content creation",
                pricing="Free/Paid"
            ),
            AIToolSearchResult(
                tool_name="Claude",
                description="Advanced AI assistant with strong reasoning and long context",
                url="https://claude.ai",
                use_case="Complex task analysis and detailed workflow planning",
                pricing="Free/Paid"
            ),
            AIToolSearchResult(
                tool_name="Gemini",
                description="Google's AI model with web search and multimodal capabilities",
                url="https://gemini.google.com",
                use_case="Research and information synthesis",
                pricing="Free/Paid"
            )
        ]
    
    # Deduplicate results
    seen_tools = set()
    unique_results = []
    
    for tool in all_results:
        tool_key = tool.tool_name.lower().replace(" ", "")
        if tool_key not in seen_tools:
            seen_tools.add(tool_key)
            unique_results.append(tool)
    
    return unique_results[:12]  # Return top 12 unique tools
