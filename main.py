from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MORVO Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("MORVO Backend starting up...")
    logger.info(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'development')}")

@app.get("/")
def root():
    return {"message": "MORVO Working", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {
        "message": "Test endpoint working",
        "port": os.environ.get("PORT", "8000"),
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "development")
    }

# Add this for Railway port:
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)