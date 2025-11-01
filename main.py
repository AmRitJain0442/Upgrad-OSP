"""
Main FastAPI application
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.prompting import router as prompting_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    logger.info("Starting Upgrad OSP application...")
    yield
    logger.info("Shutting down Upgrad OSP application...")


# Create FastAPI app
app = FastAPI(
    title="Upgrad OSP - Prompt Engineering Platform",
    description="Comprehensive prompt engineering learning platform with AI-powered guidance",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include routers
app.include_router(prompting_router)


@app.get("/")
async def root():
    """Root endpoint - redirect to prompting module"""
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/prompting/")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "upgrad-osp"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
