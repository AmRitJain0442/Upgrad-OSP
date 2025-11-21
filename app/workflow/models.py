"""
Pydantic models for workflow automation module
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class WorkflowQuestion(BaseModel):
    """Question for workflow discovery"""
    question: str
    context: Optional[str] = None
    options: Optional[List[str]] = None  # MCQ options for quick selection
    allow_custom: bool = True  # Allow custom text input alongside options


class WorkflowStep(BaseModel):
    """Individual step in a workflow"""
    id: str
    title: str
    description: str
    ai_tool: str
    tool_url: Optional[str] = None
    prompts: List[str]
    tips: List[str]
    pros: List[str]
    cons: List[str]
    estimated_time: str
    dependencies: List[str] = Field(default_factory=list)
    alternatives: List[Dict[str, str]] = Field(default_factory=list)
    related_course: Optional[Dict[str, str]] = None  # Course recommendation: {id, title, description, url}
    evaluator_link: str = "/evaluator/"  # Link to evaluator page
    quiz: Optional[Dict[str, Any]] = None  # MCQ quiz: {question, options, correct_index, explanation}


class WorkflowRoadmap(BaseModel):
    """Complete workflow roadmap"""
    task_title: str
    task_description: str
    steps: List[WorkflowStep]
    total_estimated_time: str
    difficulty_level: str


class TaskDiscoveryRequest(BaseModel):
    """Request to discover user's task"""
    user_input: str
    session_id: str


class WorkflowQuestionsResponse(BaseModel):
    """Response with follow-up questions"""
    questions: List[WorkflowQuestion]
    session_id: str


class WorkflowGenerationRequest(BaseModel):
    """Request to generate workflow"""
    task_description: str
    answers: Dict[str, str]
    session_id: str


class AIToolSearchResult(BaseModel):
    """Search result for AI tools"""
    tool_name: str
    description: str
    url: str
    use_case: str
    pricing: str
