"""
Pydantic models for prompting module
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model"""

    message: str = Field(..., description="User message to AI tutor")
    context: str = Field(default="", description="Context for the conversation")
    session_id: str = Field(..., description="Session ID for tracking")


class ChatResponse(BaseModel):
    """AI tutor response with markdown support"""

    response: str = Field(..., description="AI response in markdown format")
    analysis: Optional[Dict[str, Any]] = Field(
        default=None, description="Prompt analysis details"
    )


class PromptAnalysisRequest(BaseModel):
    """Request for real-time prompt analysis"""

    prompt: str = Field(..., description="User's prompt to analyze")
    session_id: str = Field(..., description="Session ID")


class PromptAnalysis(BaseModel):
    """Real-time prompt analysis response"""

    has_constraints: bool = Field(..., description="Whether prompt has constraints")
    has_role: bool = Field(..., description="Whether prompt assigns a role")
    has_structure: bool = Field(..., description="Whether prompt has clear structure")
    suggestions: List[str] = Field(
        default_factory=list, description="Improvement suggestions"
    )
    score: int = Field(..., ge=0, le=100, description="Prompt quality score")


class UploadResponse(BaseModel):
    """File upload response"""

    success: bool
    filename: Optional[str] = None
    preview: Optional[str] = None
    file_url: Optional[str] = None
    error: Optional[str] = None


class SummarizeRequest(BaseModel):
    """Request to summarize uploaded document"""

    prompt: str = Field(..., description="User's summarization prompt")
    session_id: str = Field(..., description="Session ID to get document")


class WorkspaceResponse(BaseModel):
    """Workspace AI response with structured feedback"""

    summary: str = Field(..., description="AI-generated summary in markdown")
    has_constraints: bool = Field(
        ..., description="Whether user prompt had constraints"
    )
    quality_feedback: Optional[str] = Field(
        default=None, description="Feedback on prompt quality"
    )


class QuizAnswer(BaseModel):
    """User's quiz answer"""

    question_id: str
    answer_index: int
    session_id: str


class QuizResult(BaseModel):
    """Quiz validation result"""

    correct: bool
    explanation: Optional[str] = None
    next_action: Optional[str] = None


class SessionInfo(BaseModel):
    """Session information"""

    session_id: str
    current_module: str
    current_submodule: int
    document_uploaded: bool
    progress: Dict[str, Any] = Field(default_factory=dict)


class SubmoduleUnlockRequest(BaseModel):
    """Request to unlock next submodule"""

    session_id: str
    module_id: str
    submodule_id: int


class StreamChunk(BaseModel):
    """Streaming response chunk"""

    chunk: str = Field(..., description="Text chunk")
    done: bool = Field(default=False, description="Whether streaming is complete")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class PresentationAnalysisRequest(BaseModel):
    """Request for presentation analysis"""

    slides: List[Dict[str, Any]] = Field(..., description="List of presentation slides")
    topic: str = Field(..., description="Presentation topic")
    session_id: str = Field(..., description="Session ID")


class PresentationAnalysis(BaseModel):
    """Presentation analysis response"""

    strengths: List[str] = Field(..., description="List of things done well")
    improvements: List[str] = Field(..., description="Areas for improvement")
    suggestions: List[str] = Field(..., description="Constructive suggestions")
