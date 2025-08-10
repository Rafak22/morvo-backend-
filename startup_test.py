#!/usr/bin/env python3
"""
Minimal startup test to debug Railway deployment issues
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported"""
    try:
        logger.info("Testing imports...")
        import fastapi
        logger.info(f"FastAPI version: {fastapi.__version__}")
        
        import uvicorn
        logger.info(f"Uvicorn version: {uvicorn.__version__}")
        
        # Test optional imports
        try:
            from supabase import create_client
            logger.info("Supabase import successful")
        except ImportError as e:
            logger.warning(f"Supabase import failed: {e}")
        
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    logger.info("Testing environment...")
    
    port = os.environ.get("PORT")
    logger.info(f"PORT: {port}")
    
    railway_env = os.environ.get("RAILWAY_ENVIRONMENT")
    logger.info(f"RAILWAY_ENVIRONMENT: {railway_env}")
    
    # List all environment variables (without sensitive values)
    for key, value in os.environ.items():
        if not any(sensitive in key.lower() for sensitive in ['key', 'secret', 'password', 'token']):
            logger.info(f"{key}: {value}")

def test_main_app():
    """Test if main app can be created"""
    try:
        logger.info("Testing main app creation...")
        from main import app
        logger.info("Main app created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create main app: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting startup test...")
    
    success = True
    success &= test_imports()
    test_environment()
    success &= test_main_app()
    
    if success:
        logger.info("All tests passed!")
        sys.exit(0)
    else:
        logger.error("Some tests failed!")
        sys.exit(1) 