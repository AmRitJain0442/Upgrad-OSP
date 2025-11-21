"""
Evaluator Router
API endpoints for prompt evaluation functionality
"""

from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uuid
from typing import Optional

from .models import (
    PromptEvaluationRequest,
    PromptEvaluationResponse,
    EvaluationHistory
)
from .evaluator_agent import evaluate_prompt_output, format_evaluation_for_display

router = APIRouter(prefix="/evaluator", tags=["evaluator"])
templates = Jinja2Templates(directory="frontend/templates")

# In-memory storage for evaluation sessions
evaluation_sessions: dict[str, EvaluationHistory] = {}


@router.get("/", response_class=HTMLResponse)
async def evaluator_page(request: Request):
    """Render the evaluator page"""
    return templates.TemplateResponse(
        "evaluator/index.html",
        {"request": request}
    )


@router.post("/evaluate", response_model=PromptEvaluationResponse)
async def evaluate_prompt(
    user_prompt: str = Form(...),
    ai_output: str = Form(...),
    output_type: str = Form(default="text"),
    expected_outcome: Optional[str] = Form(None),
    ai_model_used: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Evaluate a user's prompt and AI output
    
    Args:
        user_prompt: The prompt the user gave to the AI
        ai_output: The output received from the AI
        output_type: Type of output (text, image_url, pdf_url)
        expected_outcome: What the user expected (optional)
        ai_model_used: Which AI model was used (optional)
        session_id: Session ID for tracking history (optional)
    """
    
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Evaluate the prompt-output pair
    feedback, raw_analysis = await evaluate_prompt_output(
        user_prompt=user_prompt,
        ai_output=ai_output,
        output_type=output_type,
        expected_outcome=expected_outcome,
        ai_model_used=ai_model_used
    )
    
    # Create response
    response = PromptEvaluationResponse(
        session_id=session_id,
        feedback=feedback,
        timestamp=datetime.now(),
        raw_analysis=raw_analysis
    )
    
    # Store in session history
    if session_id not in evaluation_sessions:
        evaluation_sessions[session_id] = EvaluationHistory(
            session_id=session_id,
            evaluations=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    evaluation_sessions[session_id].evaluations.append(response)
    evaluation_sessions[session_id].updated_at = datetime.now()
    
    return response


@router.get("/history/{session_id}")
async def get_evaluation_history(session_id: str):
    """Get evaluation history for a session"""
    if session_id not in evaluation_sessions:
        return {"error": "Session not found", "evaluations": []}
    
    return evaluation_sessions[session_id]


@router.post("/upload-file")
async def upload_file_for_evaluation(
    file: UploadFile = File(...),
    user_prompt: str = Form(...),
    expected_outcome: Optional[str] = Form(None),
    ai_model_used: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Upload a file (PDF, image) as AI output for evaluation
    
    For PDFs and images, we'll extract text or analyze the content
    """
    
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Read file content
    content = await file.read()
    
    # Determine output type and content
    if file.content_type.startswith("image/"):
        output_type = "image_url"
        # For images, we'll just note it's an image
        ai_output = f"[Image file: {file.filename}, size: {len(content)} bytes]"
        ai_output += "\nNote: Image content analysis is limited. Evaluation based on prompt structure."
    elif file.content_type == "application/pdf":
        output_type = "pdf_url"
        ai_output = f"[PDF file: {file.filename}, size: {len(content)} bytes]"
        ai_output += "\nNote: PDF content analysis is limited. Evaluation based on prompt structure."
    else:
        # Assume text
        output_type = "text"
        try:
            ai_output = content.decode("utf-8")
        except:
            ai_output = "[Could not decode file content]"
    
    # Evaluate
    feedback, raw_analysis = await evaluate_prompt_output(
        user_prompt=user_prompt,
        ai_output=ai_output,
        output_type=output_type,
        expected_outcome=expected_outcome,
        ai_model_used=ai_model_used
    )
    
    # Create response
    response = PromptEvaluationResponse(
        session_id=session_id,
        feedback=feedback,
        timestamp=datetime.now(),
        raw_analysis=raw_analysis
    )
    
    # Store in session history
    if session_id not in evaluation_sessions:
        evaluation_sessions[session_id] = EvaluationHistory(
            session_id=session_id,
            evaluations=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    evaluation_sessions[session_id].evaluations.append(response)
    evaluation_sessions[session_id].updated_at = datetime.now()
    
    return response
