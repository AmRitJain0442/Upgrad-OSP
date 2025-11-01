"""
In-memory session manager for prompting module
"""
import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class SessionData:
    """Session data container"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        
        # Learning state
        self.current_module: Optional[str] = None
        self.current_submodule: Optional[int] = None
        self.current_step: str = "welcome"  # welcome, upload, prompt, generate, feedback, quiz
        
        # Document storage (in memory)
        self.uploaded_document: Optional[str] = None
        self.document_filename: Optional[str] = None
        
        # Progress tracking
        self.completed_modules: Dict[str, list[int]] = {}  # module_id -> [completed_submodule_ids]
        self.prompt_attempts: int = 0
        self.lesson_complete: bool = False
        
        # Conversation history
        self.tutor_history: list[Dict[str, str]] = []
        self.workspace_history: list[Dict[str, str]] = []
    
    def update_access_time(self):
        """Update last accessed timestamp"""
        self.last_accessed = datetime.now()
    
    def set_document(self, text: str, filename: str):
        """Store uploaded document"""
        self.uploaded_document = text[:10000]  # Store first 10k chars
        self.document_filename = filename
        logger.info(f"Document stored for session {self.session_id}: {filename}")
    
    def mark_submodule_complete(self, module_id: str, submodule_id: int):
        """Mark a submodule as completed"""
        if module_id not in self.completed_modules:
            self.completed_modules[module_id] = []
        if submodule_id not in self.completed_modules[module_id]:
            self.completed_modules[module_id].append(submodule_id)
        logger.info(f"Submodule {module_id}/{submodule_id} completed in session {self.session_id}")
    
    def is_submodule_completed(self, module_id: str, submodule_id: int) -> bool:
        """Check if submodule is completed"""
        return module_id in self.completed_modules and submodule_id in self.completed_modules[module_id]
    
    def add_tutor_message(self, role: str, content: str):
        """Add message to tutor history"""
        self.tutor_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_workspace_message(self, role: str, content: str):
        """Add message to workspace history"""
        self.workspace_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


class SessionManager:
    """Manages user sessions in memory"""
    
    def __init__(self, session_timeout_minutes: int = 120):
        self.sessions: Dict[str, SessionData] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        logger.info(f"SessionManager initialized with {session_timeout_minutes}min timeout")
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionData(session_id)
        logger.info(f"New session created: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID, return None if not found or expired"""
        if session_id not in self.sessions:
            logger.warning(f"Session not found: {session_id}")
            return None
        
        session = self.sessions[session_id]
        
        # Check if session expired
        if datetime.now() - session.last_accessed > self.session_timeout:
            logger.info(f"Session expired: {session_id}")
            del self.sessions[session_id]
            return None
        
        session.update_access_time()
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions, return count of removed sessions"""
        now = datetime.now()
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if now - session.last_accessed > self.session_timeout
        ]
        
        for sid in expired_sessions:
            del self.sessions[sid]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_active_session_count(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)


# Global session manager instance
session_manager = SessionManager()
