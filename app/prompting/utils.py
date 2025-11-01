"""
Utility functions for prompting module
"""
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_txt(filepath: Path) -> str:
    """Extract text from .txt file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading txt file: {e}")
        raise ValueError(f"Could not read text file: {str(e)}")


def extract_text_from_pdf(filepath: Path) -> str:
    """Extract text from .pdf file"""
    try:
        import PyPDF2
        
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = " ".join([page.extract_text() for page in reader.pages])
        return text
    except ImportError:
        logger.error("PyPDF2 not installed")
        raise ValueError("PDF support not available. Please install PyPDF2.")
    except Exception as e:
        logger.error(f"Error reading PDF file: {e}")
        raise ValueError(f"Could not read PDF file: {str(e)}")


def extract_text_from_docx(filepath: Path) -> str:
    """Extract text from .docx file"""
    try:
        import docx
        
        doc = docx.Document(str(filepath))
        text = " ".join([para.text for para in doc.paragraphs])
        return text
    except ImportError:
        logger.error("python-docx not installed")
        raise ValueError("DOCX support not available. Please install python-docx.")
    except Exception as e:
        logger.error(f"Error reading DOCX file: {e}")
        raise ValueError(f"Could not read DOCX file: {str(e)}")


def extract_text(filepath: Path) -> str:
    """
    Extract text from file based on extension
    Returns cleaned text with normalized whitespace
    """
    ext = filepath.suffix.lower().lstrip(".")
    
    if ext == "txt":
        text = extract_text_from_txt(filepath)
    elif ext == "pdf":
        text = extract_text_from_pdf(filepath)
    elif ext == "docx":
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Clean up excessive whitespace - normalize all whitespace to single spaces
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    
    if not text:
        raise ValueError("No text could be extracted from the file")
    
    logger.info(f"Extracted {len(text)} characters from {filepath.name}")
    return text


def analyze_prompt_quality(prompt: str) -> dict:
    """
    Analyze prompt quality and provide suggestions
    Returns dict with analysis results
    """
    prompt_lower = prompt.lower()
    
    # Check for constraints
    constraint_keywords = ["based on", "only", "don't", "do not", "avoid", "without", "must", "should not", "exclude"]
    has_constraints = any(keyword in prompt_lower for keyword in constraint_keywords)
    
    # Check for role assignment
    role_keywords = ["you are", "act as", "as a", "role:", "expert", "professional"]
    has_role = any(keyword in prompt_lower for keyword in role_keywords)
    
    # Check for structure/steps
    structure_keywords = ["step by step", "first", "then", "finally", "1.", "2.", "bullet points", "list", "format"]
    has_structure = any(keyword in prompt_lower for keyword in structure_keywords)
    
    # Generate suggestions
    suggestions = []
    
    if not has_constraints:
        suggestions.append("Consider adding constraints to prevent hallucination (e.g., 'Based only on the provided text')")
    
    if not has_role and len(prompt.split()) > 10:
        suggestions.append("Try assigning a specific role or perspective (e.g., 'You are an expert analyst...')")
    
    if not has_structure and len(prompt.split()) > 15:
        suggestions.append("Consider adding structure (e.g., 'First analyze... then conclude...' or 'List the key points')")
    
    # Calculate quality score (0-100)
    score = 40  # Base score
    if has_constraints:
        score += 30
    if has_role:
        score += 20
    if has_structure:
        score += 10
    
    return {
        "has_constraints": has_constraints,
        "has_role": has_role,
        "has_structure": has_structure,
        "suggestions": suggestions,
        "score": min(score, 100)
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove path components
    filename = Path(filename).name
    # Remove unsafe characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        filename = name[:250] + ("." + ext if ext else "")
    return filename
