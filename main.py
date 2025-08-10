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

@app.post("/")
async def root_chat(request: Request):
    """Handle chat requests to root endpoint"""
    try:
        body = await request.json()
        query = body.get("message", "")
        
        logger.info(f"Root chat query received: {query}")
        
        response_text = f"Hello! I'm MORVO. I received your message: '{query}'. I'm currently in development mode and will provide AI-powered responses soon!"
        
        return {
            "response": response_text,
            "status": "success",
            "assistant": "MORVO",
            "endpoint": "/",
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Root chat endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": "I'm sorry, but I encountered an error processing your request. Please try again.",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

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

@app.get("/api/endpoints")
def list_endpoints():
    """List all available endpoints for debugging"""
    try:
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append({
                    "path": route.path,
                    "methods": list(route.methods),
                    "name": route.name or "unnamed"
                })
        
        return {
            "status": "success",
            "total_endpoints": len(routes),
            "endpoints": routes,
            "chat_endpoints": [
                "/chat",
                "/api/chat", 
                "/api/morvo/chat"
            ],
            "data_endpoints": [
                "/api/seo-signals",
                "/api/mentions",
                "/api/posts",
                "/api/supabase-status",
                "/api/all-data"
            ],
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Endpoints list error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

@app.post("/chat")
async def chat_query(request: Request):
    """Handle chat queries from the frontend"""
    try:
        # Get the request body
        body = await request.json()
        query = body.get("message", "")
        user_id = body.get("user_id", "anonymous")
        session_id = body.get("session_id", "default")
        
        logger.info(f"Chat query received from {user_id}: {query}")
        
        # Check if OpenAI is configured
        if not OPENAI_API_KEY:
            return {
                "response": "I'm sorry, but I'm currently experiencing technical difficulties. Please try again later.",
                "status": "error",
                "error": "OpenAI API not configured",
                "timestamp": "2025-08-10T12:06:00Z"
            }
        
        # For now, return a simple response
        # TODO: Integrate with OpenAI API for actual AI responses
        response_text = f"I received your message: '{query}'. I'm currently in development mode and will provide AI-powered responses soon!"
        
        return {
            "response": response_text,
            "status": "success",
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": "I'm sorry, but I encountered an error processing your request. Please try again.",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

@app.post("/api/chat")
async def api_chat_query(request: Request):
    """Alternative chat endpoint for API calls"""
    try:
        body = await request.json()
        query = body.get("message", "")
        user_id = body.get("user_id", "anonymous")
        
        logger.info(f"API chat query received from {user_id}: {query}")
        
        # Check if OpenAI is configured
        if not OPENAI_API_KEY:
            return {
                "response": "Service temporarily unavailable. Please try again later.",
                "status": "error",
                "error": "OpenAI API not configured",
                "timestamp": "2025-08-10T12:06:00Z"
            }
        
        # For now, return a simple response
        response_text = f"API Response: I received '{query}'. AI integration coming soon!"
        
        return {
            "response": response_text,
            "status": "success",
            "user_id": user_id,
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"API chat endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": "An error occurred while processing your request.",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

# Add a catch-all endpoint for any chat-related requests
@app.post("/api/morvo/chat")
async def morvo_chat(request: Request):
    """MORVO-specific chat endpoint"""
    try:
        body = await request.json()
        query = body.get("message", "")
        user_id = body.get("user_id", "anonymous")
        
        logger.info(f"MORVO chat query received from {user_id}: {query}")
        
        # Check if OpenAI is configured
        if not OPENAI_API_KEY:
            return {
                "response": "I'm MORVO, your ROI Marketing Strategist and AI Consultant. I'm currently experiencing technical difficulties. Please try again later.",
                "status": "error",
                "error": "OpenAI API not configured",
                "timestamp": "2025-08-10T12:06:00Z"
            }
        
        # For now, return a MORVO-branded response
        response_text = f"Hello! I'm MORVO, your ROI Marketing Strategist and AI Consultant. I received your message: '{query}'. I'm currently in development mode and will provide AI-powered marketing insights soon!"
        
        return {
            "response": response_text,
            "status": "success",
            "assistant": "MORVO",
            "user_id": user_id,
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"MORVO chat endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": "I'm sorry, but I encountered an error processing your request. Please try again.",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

# Add a catch-all chat endpoint that handles any POST request to /api/*
@app.post("/api/{path:path}")
async def catch_all_api(request: Request, path: str):
    """Catch-all endpoint for any API calls"""
    try:
        logger.info(f"Catch-all API endpoint called: /api/{path}")
        
        # If it's a chat-related path, handle it
        if "chat" in path.lower():
            body = await request.json()
            query = body.get("message", "")
            
            response_text = f"Hello! I'm MORVO. I received your message: '{query}'. I'm currently in development mode and will provide AI-powered responses soon!"
            
            return {
                "response": response_text,
                "status": "success",
                "assistant": "MORVO",
                "endpoint": f"/api/{path}",
                "timestamp": "2025-08-10T12:06:00Z"
            }
        
        # For other API calls, return a generic response
        return {
            "message": f"API endpoint /api/{path} called",
            "status": "success",
            "timestamp": "2025-08-10T12:06:00Z"
        }
        
    except Exception as e:
        logger.error(f"Catch-all API endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": "I'm sorry, but I encountered an error processing your request. Please try again.",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

# Add a simple test chat endpoint that doesn't depend on any external services
@app.post("/test-chat")
async def test_chat(request: Request):
    """Simple test chat endpoint for debugging"""
    try:
        body = await request.json()
        query = body.get("message", "")
        
        logger.info(f"Test chat query received: {query}")
        
        # Simple response without any external dependencies
        response_text = f"Test successful! I received: '{query}'. This endpoint is working correctly."
        
        return {
            "response": response_text,
            "status": "success",
            "endpoint": "/test-chat",
            "timestamp": "2025-08-10T12:06:00Z"
        }
    except Exception as e:
        logger.error(f"Test chat endpoint error: {e}")
        logger.error(traceback.format_exc())
        return {
            "response": f"Test failed with error: {str(e)}",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-08-10T12:06:00Z"
        }

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