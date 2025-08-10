from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with error handling
try:
    app = FastAPI(title="MORVO Backend", version="1.0.0")
    logger.info("FastAPI app created successfully")
except Exception as e:
    logger.error(f"Failed to create FastAPI app: {e}")
    raise

# Add CORS middleware
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware added successfully")
except Exception as e:
    logger.error(f"Failed to add CORS middleware: {e}")

@app.on_event("startup")
async def startup_event():
    """Startup event handler with comprehensive logging"""
    try:
        logger.info("=== MORVO Backend Starting Up ===")
        logger.info(f"Python version: {os.sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'development')}")
        logger.info(f"Port: {os.environ.get('PORT', '8000')}")
        
        # Test basic imports
        try:
            import fastapi
            logger.info(f"FastAPI version: {fastapi.__version__}")
        except Exception as e:
            logger.error(f"FastAPI import error: {e}")
        
        try:
            import uvicorn
            logger.info(f"Uvicorn version: {uvicorn.__version__}")
        except Exception as e:
            logger.error(f"Uvicorn import error: {e}")
        
        logger.info("=== Startup Complete ===")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        logger.error(traceback.format_exc())

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for debugging"""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

@app.get("/")
def root():
    """Root endpoint"""
    try:
        return {"message": "MORVO Working", "status": "success"}
    except Exception as e:
        logger.error(f"Root endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    """Health check endpoint"""
    try:
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    """Simple ping endpoint for Railway health checks"""
    return {"pong": True}

@app.get("/test")
def test():
    """Test endpoint with environment info"""
    try:
        return {
            "message": "Test endpoint working",
            "port": os.environ.get("PORT", "8000"),
            "environment": os.environ.get("RAILWAY_ENVIRONMENT", "development"),
            "python_version": os.sys.version,
            "working_directory": os.getcwd()
        }
    except Exception as e:
        logger.error(f"Test endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug")
def debug():
    """Debug endpoint with comprehensive system info"""
    try:
        import platform
        import sys
        
        return {
            "system": {
                "platform": platform.platform(),
                "python_version": sys.version,
                "python_executable": sys.executable,
                "working_directory": os.getcwd(),
                "environment_variables": {
                    k: v for k, v in os.environ.items() 
                    if not any(sensitive in k.lower() for sensitive in ['key', 'secret', 'password', 'token'])
                }
            },
            "app": {
                "title": app.title,
                "version": app.version,
                "debug": app.debug
            }
        }
    except Exception as e:
        logger.error(f"Debug endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add this for Railway port:
if __name__ == "__main__":
    try:
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error(traceback.format_exc())