"""
FastAPI router for prompting module with streaming support
"""
import json
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Form as FastAPIForm
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.prompting.models import (
    ChatMessage, PromptAnalysisRequest,
    UploadResponse, SummarizeRequest, QuizAnswer, QuizResult,
    SessionInfo, SubmoduleUnlockRequest, PresentationAnalysisRequest,
    PresentationAnalysis
)
from app.prompting.curriculum import get_curriculum, get_module, get_submodule, FULL_CURRICULUM
from app.prompting.session_manager import session_manager
from app.prompting.utils import allowed_file, extract_text, sanitize_filename
from app.prompting.agents import (
    stream_tutor_response, stream_workspace_response,
    analyze_prompt_realtime, generate_tutor_message, generate_workspace_summary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prompting", tags=["prompting"])
templates = Jinja2Templates(directory="frontend/templates")

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Sample documents directory
SAMPLES_DIR = Path("frontend/static/samples")

# Load sample document mapping
SAMPLE_MAPPING_FILE = SAMPLES_DIR / "document_mapping.json"
SAMPLE_MAPPING = {}
if SAMPLE_MAPPING_FILE.exists():
    with open(SAMPLE_MAPPING_FILE) as f:
        SAMPLE_MAPPING = json.load(f)


@router.get("/")
async def index(request: Request):
    """Main courses page"""
    curriculum = get_curriculum()
    return templates.TemplateResponse(
        "prompting/courses.html",
        {"request": request, "courses": curriculum}
    )


@router.get("/workflow")
async def workflow_page(request: Request):
    """Workflow automation module page"""
    return templates.TemplateResponse(
        "prompting/workflow.html",
        {"request": request}
    )


@router.get("/module/{module_id}/{submodule_id}")
async def module_page(request: Request, module_id: str, submodule_id: int):
    """Individual module/submodule page"""
    module = get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    submodule = get_submodule(module_id, submodule_id)
    if not submodule:
        raise HTTPException(status_code=404, detail="Submodule not found")
    
    # Create or get session
    session_id = request.cookies.get("session_id")
    if not session_id or not session_manager.get_session(session_id):
        session_id = session_manager.create_session()
    
    session = session_manager.get_session(session_id)
    if session:
        session.current_module = module_id
        session.current_submodule = submodule_id
    
    # Use different template for different modules
    if module_id == "presentation-builder":
        template_name = "prompting/presentation_module.html"
    elif module_id == "gamma-tool":
        template_name = "prompting/gamma_module.html"
    else:
        template_name = "prompting/module.html"
    
    response = templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "module": module,
            "submodule": submodule,
            "session_id": session_id
        }
    )
    response.set_cookie("session_id", session_id, httponly=True, max_age=7200)  # 2 hours
    return response


@router.post("/api/session/create")
async def create_session() -> SessionInfo:
    """Create a new session"""
    session_id = session_manager.create_session()
    session_manager.get_session(session_id)
    
    return SessionInfo(
        session_id=session_id,
        current_module="",
        current_submodule=0,
        document_uploaded=False,
        progress={}
    )


@router.post("/api/chat")
async def chat(message: ChatMessage) -> JSONResponse:
    """Chat with AI tutor (non-streaming version for compatibility)"""
    session = session_manager.get_session(message.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Build lesson context
    lesson_context = {}
    
    if session.current_module:
        module = next((m for m in FULL_CURRICULUM if m["id"] == session.current_module), None)
        if module:
            lesson_context["module"] = module["title"]
            if session.current_submodule:
                submodule = next((s for s in module["submodules"] if s["id"] == session.current_submodule), None)
                if submodule:
                    lesson_context["lesson"] = f"{submodule['title']} - {submodule['description']}"
    
    lesson_context["step"] = session.current_step
    lesson_context["attempts"] = session.prompt_attempts
    
    if message.context:
        lesson_context["additional_context"] = message.context
    
    try:
        response = await generate_tutor_message(message.message, lesson_context)
        session.add_tutor_message("user", message.message)
        session.add_tutor_message("assistant", response)
        
        return JSONResponse({"response": response})
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/chat/stream")
async def chat_stream(message: ChatMessage):
    """Stream chat response from AI tutor"""
    session = session_manager.get_session(message.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.add_tutor_message("user", message.message)
    
    # Build lesson context for the AI
    lesson_context = {}
    
    if session.current_module:
        # Find module info
        module = next((m for m in FULL_CURRICULUM if m["id"] == session.current_module), None)
        if module:
            lesson_context["module"] = module["title"]
            
            # Find current submodule
            if session.current_submodule:
                submodule = next((s for s in module["submodules"] if s["id"] == session.current_submodule), None)
                if submodule:
                    lesson_context["lesson"] = f"{submodule['title']} - {submodule['description']}"
    
    lesson_context["step"] = session.current_step
    lesson_context["attempts"] = session.prompt_attempts
    
    # Add last messages if available
    if session.workspace_history:
        last_workspace = session.workspace_history[-1]
        if last_workspace["role"] == "user":
            lesson_context["last_prompt"] = last_workspace["content"]
    
    # Add simple context text if provided (from legacy calls)
    if message.context:
        lesson_context["additional_context"] = message.context
    
    async def generate():
        full_response = ""
        try:
            async for chunk in stream_tutor_response(message.message, lesson_context):
                full_response += chunk
                # Send as SSE format
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
            
            # Save complete response to session
            session.add_tutor_message("assistant", full_response)
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/api/prompt/analyze")
async def analyze_prompt(request: PromptAnalysisRequest):
    """Analyze prompt in real-time and provide feedback"""
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Build lesson info for contextual analysis
    lesson_info = {}
    
    if session.current_module and session.current_submodule:
        module = next((m for m in FULL_CURRICULUM if m["id"] == session.current_module), None)
        if module:
            submodule = next((s for s in module["submodules"] if s["id"] == session.current_submodule), None)
            if submodule:
                lesson_info["submodule_id"] = submodule["id"]
                lesson_info["lesson_name"] = submodule["title"]
    
    try:
        analysis = await analyze_prompt_realtime(request.prompt, lesson_info)
        return analysis
    except Exception as e:
        logger.error(f"Prompt analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/sample/load")
async def load_sample_document(request: Request):
    """Load a sample document for the current lesson"""
    data = await request.json()
    session_id = data.get("session_id")
    module_id = data.get("module_id")
    submodule_id = data.get("submodule_id")
    
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get sample document for this lesson
    mapping_key = f"{module_id}-{submodule_id}"
    sample_filename = SAMPLE_MAPPING.get(mapping_key)
    
    if not sample_filename:
        return JSONResponse({
            "success": False,
            "error": "No sample document available for this lesson"
        })
    
    try:
        sample_path = SAMPLES_DIR / sample_filename
        if not sample_path.exists():
            raise FileNotFoundError(f"Sample file not found: {sample_filename}")
        
        with open(sample_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Store in session
        session.set_document(text, f"sample_{sample_filename}")
        session.current_step = "prompt"
        
        # Generate preview
        preview = text[:500] + "..." if len(text) > 500 else text
        
        return JSONResponse({
            "success": True,
            "filename": f"Sample: {sample_filename}",
            "preview": preview,
            "full_content": text
        })
    
    except Exception as e:
        logger.error(f"Error loading sample document: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@router.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = FastAPIForm(...)
):
    """Upload and process document"""
    session = session_manager.get_session(session_id)
    if not session:
        return UploadResponse(
            success=False, 
            error="Session expired. Please refresh the page (Ctrl+Shift+R) and try again."
        )
    
    if not file.filename:
        return UploadResponse(success=False, error="No file selected")
    
    if not allowed_file(file.filename):
        return UploadResponse(
            success=False,
            error="Invalid file type. Please upload PDF, DOCX, or TXT files."
        )
    
    try:
        # Save file temporarily
        safe_filename = sanitize_filename(file.filename)
        filepath = UPLOAD_DIR / f"{session_id}_{safe_filename}"
        
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Extract text
        text = extract_text(filepath)
        
        # Store in session
        session.set_document(text, safe_filename)
        session.current_step = "prompt"
        
        # Generate preview
        preview = text[:500] + "..." if len(text) > 500 else text
        
        # Clean up file
        filepath.unlink()
        
        return UploadResponse(
            success=True,
            filename=safe_filename,
            preview=preview
        )
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return UploadResponse(success=False, error=str(e))


@router.post("/api/summarize")
async def summarize(request: SummarizeRequest) -> JSONResponse:
    """Generate summary (non-streaming)"""
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.uploaded_document:
        raise HTTPException(status_code=400, detail="No document uploaded")
    
    try:
        summary, has_constraints = await generate_workspace_summary(
            request.prompt,
            session.uploaded_document
        )
        
        session.add_workspace_message("user", request.prompt)
        session.add_workspace_message("assistant", summary)
        session.prompt_attempts += 1
        
        return JSONResponse({
            "summary": summary,
            "has_constraints": has_constraints
        })
    
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/summarize/stream")
async def summarize_stream(request: SummarizeRequest):
    """Stream summarization response"""
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.uploaded_document:
        raise HTTPException(status_code=400, detail="No document uploaded")
    
    session.add_workspace_message("user", request.prompt)
    
    # Get document text (guaranteed to be str due to check above)
    document_text = session.uploaded_document
    
    async def generate():
        full_response = ""
        try:
            async for chunk in stream_workspace_response(
                request.prompt,
                document_text
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            
            # Analyze prompt quality
            from app.prompting.utils import analyze_prompt_quality
            analysis = analyze_prompt_quality(request.prompt)
            
            # Send completion with metadata
            metadata_payload = {
                'chunk': '',
                'done': True,
                'metadata': {
                    'has_constraints': analysis['has_constraints'],
                    'quality_score': analysis['score']
                }
            }
            yield f"data: {json.dumps(metadata_payload)}\n\n"
            
            # Save complete response
            session.add_workspace_message("assistant", full_response)
            session.prompt_attempts += 1
            
        except Exception as e:
            logger.error(f"Streaming summarization error: {e}")
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/api/quiz/submit")
async def submit_quiz(answer: QuizAnswer) -> QuizResult:
    """Validate quiz answer"""
    session = session_manager.get_session(answer.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.current_module or session.current_submodule is None:
        raise HTTPException(status_code=400, detail="No active lesson")
    
    # Get current submodule quiz
    submodule = get_submodule(session.current_module, session.current_submodule)
    if not submodule or "quiz" not in submodule:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = submodule["quiz"]
    correct = answer.answer_index == quiz["correct_index"]
    
    if correct:
        # Mark submodule as complete
        if session.current_module and session.current_submodule is not None:
            session.mark_submodule_complete(session.current_module, session.current_submodule)
        session.lesson_complete = True
        
        return QuizResult(
            correct=True,
            explanation="Exactly right! You've mastered this concept.",
            next_action="proceed_to_next"
        )
    else:
        return QuizResult(
            correct=False,
            explanation=f"Not quite. The correct answer is: {quiz['options'][quiz['correct_index']]}",
            next_action="retry"
        )


@router.post("/api/submodule/unlock")
async def unlock_submodule(request: SubmoduleUnlockRequest):
    """Unlock next submodule"""
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if current submodule is completed
    if not session.is_submodule_completed(request.module_id, request.submodule_id):
        raise HTTPException(status_code=403, detail="Complete current submodule first")
    
    return JSONResponse({"success": True, "unlocked": request.submodule_id + 1})


@router.get("/api/session/{session_id}")
async def get_session_info(session_id: str) -> SessionInfo:
    """Get session information"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionInfo(
        session_id=session.session_id,
        current_module=session.current_module or "",
        current_submodule=session.current_submodule or 0,
        document_uploaded=session.uploaded_document is not None,
        progress=session.completed_modules
    )


@router.post("/api/presentation/analyze")
async def analyze_presentation(request: PresentationAnalysisRequest) -> PresentationAnalysis:
    """Analyze presentation using Gemini API"""
    try:
        # Build a comprehensive presentation summary for analysis
        presentation_text = f"Topic: {request.topic}\n\nSlides:\n"
        
        for i, slide in enumerate(request.slides, 1):
            presentation_text += f"\nSlide {i}:\n"
            if isinstance(slide, dict):
                if "title" in slide:
                    presentation_text += f"Title: {slide['title']}\n"
                if "content" in slide:
                    content = slide['content']
                    if isinstance(content, str):
                        presentation_text += f"Content: {content}\n"
                    elif isinstance(content, dict):
                        presentation_text += f"Content: {str(content)}\n"
        
        # Use Gemini API to analyze the presentation
        from app.prompting.agents import generate_presentation_analysis
        
        analysis = await generate_presentation_analysis(presentation_text, request.topic)
        
        return analysis
    
    except Exception as e:
        logger.error(f"Presentation analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
