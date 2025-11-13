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

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


async def generate_workflow_questions(task_input: str) -> List[WorkflowQuestion]:
    """
    Use Gemini to generate follow-up questions about the task
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
                    "model": "llama-3.1-sonar-small-128k-online",
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
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        tools_summary = "\n".join([
            f"- {tool.tool_name}: {tool.description} ({tool.url})"
            for tool in ai_tools[:10]
        ])
        
        answers_summary = "\n".join([f"- {q}: {a}" for q, a in answers.items()])
        
        prompt = f"""Create a detailed workflow roadmap for this task:

TASK: {task_description}

USER REQUIREMENTS:
{answers_summary}

AVAILABLE AI TOOLS:
{tools_summary}

Create a step-by-step workflow. Each step should include:
1. A clear title and description
2. Which AI tool to use
3. 3-5 specific prompts/commands for that tool
4. 3-5 practical tips
5. 3 pros and 3 cons of using this tool
6. Estimated time
7. Dependencies on previous steps
8. Alternative tools (if any)

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


async def search_ai_tools(task_description: str, answers: Dict[str, str]) -> List[AIToolSearchResult]:
    """
    Search for AI tools using both Perplexity and Tavily
    """
    # Create search query from task and answers
    query_parts = [task_description]
    query_parts.extend(answers.values())
    search_query = " ".join(query_parts)
    
    # Search both APIs concurrently
    perplexity_results = await search_perplexity(search_query)
    tavily_results = await search_tavily(search_query)
    
    # Combine and deduplicate results
    all_results = perplexity_results + tavily_results
    seen_tools = set()
    unique_results = []
    
    for tool in all_results:
        tool_key = tool.tool_name.lower()
        if tool_key not in seen_tools:
            seen_tools.add(tool_key)
            unique_results.append(tool)
    
    return unique_results[:15]  # Return top 15 unique tools
