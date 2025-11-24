"""
Evaluator Models
Pydantic models for prompt evaluation requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class PromptEvaluationRequest(BaseModel):
    """Request model for prompt evaluation"""

    user_prompt: str = Field(..., description="The prompt the user provided to the AI")
    ai_output: str = Field(..., description="The output received from the AI")
    output_type: Literal["text", "image_url", "pdf_url"] = Field(
        default="text", description="Type of AI output"
    )
    expected_outcome: Optional[str] = Field(
        None, description="What the user expected to achieve (optional)"
    )
    ai_model_used: Optional[str] = Field(
        None, description="Which AI model was used (e.g., ChatGPT, Claude, Gemini)"
    )


class EvaluationFeedback(BaseModel):
    """Feedback structure from evaluation"""

    overall_score: int = Field(
        ..., ge=0, le=100, description="Overall quality score (0-100)"
    )
    prompt_quality: dict = Field(..., description="Analysis of prompt quality")
    output_analysis: dict = Field(..., description="Analysis of the AI output")
    what_went_wrong: list[str] = Field(
        default_factory=list, description="List of issues identified"
    )
    what_went_right: list[str] = Field(
        default_factory=list, description="List of strengths identified"
    )
    improvement_suggestions: list[str] = Field(
        default_factory=list, description="Actionable suggestions for improvement"
    )
    revised_prompt: Optional[str] = Field(
        None, description="Suggested improved version of the prompt"
    )


class PromptEvaluationResponse(BaseModel):
    """Response model for prompt evaluation"""

    session_id: str
    feedback: EvaluationFeedback
    timestamp: datetime
    raw_analysis: str = Field(..., description="Raw analysis from Gemini")


class EvaluationHistory(BaseModel):
    """Model for storing evaluation history"""

    session_id: str
    evaluations: list[PromptEvaluationResponse]
    created_at: datetime
    updated_at: datetime
