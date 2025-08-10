from fastapi import FastAPI, HTTPException, Request
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

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "development")

# Create FastAPI app with error handling
try:
    app = FastAPI(title="MORVO Backend", version="1.0.0")
    logger.info("FastAPI app created successfully")
except Exception as e:
    logger.error(f"Failed to create FastAPI app: {e}")
    raise

# Add CORS middleware with specific origins
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://magic.lovable.app",
            "http://magic.lovable.app",
            "https://lovable.app",
            "http://lovable.app",
            "https://*.lovable.app",
            "http://*.lovable.app",
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000",
            "*"  # Allow all origins for development
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    logger.info("CORS middleware added successfully with magic.lovable.app support")
except Exception as e:
    logger.error(f"Failed to add CORS middleware: {e}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests for debugging"""
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Origin: {request.headers.get('origin', 'No origin')}")
    logger.info(f"User-Agent: {request.headers.get('user-agent', 'No user-agent')}")
    
    response = await call_next(request)
    
    logger.info(f"Response status: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    """Startup event handler with comprehensive logging"""
    try:
        logger.info("=== MORVO Backend Starting Up ===")
        logger.info(f"Python version: {os.sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Environment: {RAILWAY_ENVIRONMENT}")
        logger.info(f"Port: {os.environ.get('PORT', '8000')}")
        
        # Check OpenAI API key
        if OPENAI_API_KEY:
            logger.info("✅ OpenAI API key is configured")
            # Mask the key for security
            masked_key = OPENAI_API_KEY[:8] + "..." + OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 12 else "***"
            logger.info(f"OpenAI API key: {masked_key}")
        else:
            logger.warning("⚠️ OpenAI API key not found - AI features will be disabled")
        
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

@app.get("/api-status")
def api_status():
    """Check API key status"""
    return {
        "openai_configured": bool(OPENAI_API_KEY),
        "environment": RAILWAY_ENVIRONMENT,
        "status": "ready"
    }

@app.options("/{path:path}")
async def options_handler(request: Request):
    """Handle OPTIONS requests for CORS preflight"""
    logger.info(f"OPTIONS request received for: {request.url}")
    return JSONResponse(
        content={"message": "CORS preflight handled"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@app.get("/cors-test")
def cors_test(request: Request):
    """Test endpoint to check CORS configuration"""
    origin = request.headers.get("origin", "No origin")
    return {
        "message": "CORS test successful",
        "origin": origin,
        "cors_enabled": True,
        "allowed_origins": [
            "https://magic.lovable.app",
            "http://magic.lovable.app",
            "https://lovable.app",
            "http://lovable.app"
        ]
    }

@app.get("/test")
def test():
    """Test endpoint with environment info"""
    try:
        return {
            "message": "Test endpoint working",
            "port": os.environ.get("PORT", "8000"),
            "environment": RAILWAY_ENVIRONMENT,
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
            },
            "api": {
                "openai_configured": bool(OPENAI_API_KEY),
                "environment": RAILWAY_ENVIRONMENT
            }
        }
    except Exception as e:
        logger.error(f"Debug endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_query(request: Request):
    """Handle chat queries from the frontend"""
    try:
        # Get the request body
        body = await request.json()
        query = body.get("message", "")
        logger.info(f"Chat query received: {query}")
        
        # For now, return a simple response
        # You can integrate with OpenAI here later
        return {
            "response": f"Received your query: {query}",
            "status": "success",
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def api_chat_query(request: Request):
    """Alternative chat endpoint for API calls"""
    try:
        body = await request.json()
        query = body.get("message", "")
        logger.info(f"API chat query received: {query}")
        
        return {
            "response": f"API response to: {query}",
            "status": "success",
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"API chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Supabase Table Endpoints
@app.get("/api/seo-signals")
async def get_seo_signals(limit: int = 10, offset: int = 0):
    """Get SEO signals data from Supabase"""
    try:
        from morvo_python.app.supabase_client import fetch_seo_data
        data = await fetch_seo_data()
        return {
            "status": "success",
            "count": len(data),
            "data": data,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"SEO signals endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mentions")
async def get_mentions(limit: int = 10, offset: int = 0):
    """Get brand mentions data from Supabase"""
    try:
        from morvo_python.app.supabase_client import fetch_mentions_data
        data = await fetch_mentions_data()
        return {
            "status": "success",
            "count": len(data),
            "data": data,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Mentions endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts")
async def get_posts(limit: int = 10, offset: int = 0):
    """Get social media posts data from Supabase"""
    try:
        from morvo_python.app.supabase_client import fetch_posts_data
        data = await fetch_posts_data()
        return {
            "status": "success",
            "count": len(data),
            "data": data,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Posts endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/supabase-status")
async def get_supabase_status():
    """Check Supabase connection status"""
    try:
        from morvo_python.app.supabase_client import test_supabase_connection
        is_connected = await test_supabase_connection()
        return {
            "status": "success",
            "supabase_connected": is_connected,
            "tables": ["seo_signals", "mentions", "posts"],
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Supabase status endpoint error: {e}")
        return {
            "status": "error",
            "supabase_connected": False,
            "error": str(e),
            "tables": ["seo_signals", "mentions", "posts"]
        }

@app.get("/api/all-data")
async def get_all_data(limit: int = 5):
    """Get data from all tables"""
    try:
        from morvo_python.app.supabase_client import fetch_seo_data, fetch_mentions_data, fetch_posts_data
        
        seo_data = await fetch_seo_data()
        mentions_data = await fetch_mentions_data()
        posts_data = await fetch_posts_data()
        
        return {
            "status": "success",
            "seo_signals": {
                "count": len(seo_data),
                "data": seo_data[:limit]
            },
            "mentions": {
                "count": len(mentions_data),
                "data": mentions_data[:limit]
            },
            "posts": {
                "count": len(posts_data),
                "data": posts_data[:limit]
            },
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"All data endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_data(request: Request):
    """Search across all tables"""
    try:
        body = await request.json()
        query = body.get("query", "")
        table_filter = body.get("tables", ["seo_signals", "mentions", "posts"])
        limit = body.get("limit", 10)
        
        logger.info(f"Search query: {query} in tables: {table_filter}")
        
        results = {}
        
        if "seo_signals" in table_filter:
            from morvo_python.app.supabase_client import fetch_seo_data
            seo_data = await fetch_seo_data()
            # Simple text search (you can enhance this with proper Supabase search)
            filtered_seo = [item for item in seo_data if query.lower() in str(item).lower()]
            results["seo_signals"] = filtered_seo[:limit]
        
        if "mentions" in table_filter:
            from morvo_python.app.supabase_client import fetch_mentions_data
            mentions_data = await fetch_mentions_data()
            filtered_mentions = [item for item in mentions_data if query.lower() in str(item).lower()]
            results["mentions"] = filtered_mentions[:limit]
        
        if "posts" in table_filter:
            from morvo_python.app.supabase_client import fetch_posts_data
            posts_data = await fetch_posts_data()
            filtered_posts = [item for item in posts_data if query.lower() in str(item).lower()]
            results["posts"] = filtered_posts[:limit]
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "total_results": sum(len(data) for data in results.values()),
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Search endpoint error: {e}")
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