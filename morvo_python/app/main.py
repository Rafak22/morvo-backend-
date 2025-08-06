from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from .routers import dashboard, chat
from .supabase_client import test_supabase_connection

app = FastAPI(
    title="MORVO Phase 6 - Marketing Dashboard",
    description="Complete MORVO marketing intelligence platform",
    version="6.0.0"
)

# CORS middleware for frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "🚀 MORVO Phase 6 - Complete Marketing Intelligence Platform",
        "status": "Phase 6 Ready!",
        "features": [
            "Real-time SEO tracking",
            "Brand mention monitoring", 
            "Social media analytics",
            "AI-powered insights",
            "Interactive dashboard"
        ],
        "endpoints": {
            "dashboard": "/api/dashboard",
            "chat": "/api/chat", 
            "health": "/health",
            "docs": "/docs"
        },
        "supported_languages": ["English", "Arabic (العربية)"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = await test_supabase_connection()
    return {
        "status": "healthy",
        "database": "connected" if db_status else "disconnected",
        "phase": "6 - Complete System"
    }

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MORVO Marketing Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">
                🚀 MORVO Marketing Intelligence
            </h1>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-white p-6 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-4">📈 SEO Performance</h2>
                    <div hx-get="/api/dashboard/seo" hx-trigger="load" hx-swap="innerHTML">
                        Loading SEO data...
                    </div>
                </div>
                
                <div class="bg-white p-6 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-4">💬 Brand Mentions</h2>
                    <div hx-get="/api/dashboard/mentions" hx-trigger="load" hx-swap="innerHTML">
                        Loading mentions...
                    </div>
                </div>
                
                <div class="bg-white p-6 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-4">📱 Social Media</h2>
                    <div hx-get="/api/dashboard/social" hx-trigger="load" hx-swap="innerHTML">
                        Loading social data...
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">🤖 AI Marketing Assistant</h2>
                <div class="flex gap-2">
                    <input type="text" id="chatInput" placeholder="Ask about your marketing performance..." 
                           class="flex-1 p-2 border rounded">
                    <button hx-post="/api/chat" 
                            hx-include="#chatInput"
                            hx-target="#chatResponse"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                        Send
                    </button>
                </div>
                <div id="chatResponse" class="mt-4 p-4 bg-gray-50 rounded min-h-[100px]">
                    👋 Hi! I'm your MORVO AI assistant. Ask me anything about your marketing performance!
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))