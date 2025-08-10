import os
from supabase import create_client, Client
from typing import Optional
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client with proper error handling
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ctcnutpnikiwvqbekdnp.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0Y251dHBuaWtpd3ZxYmVrZG5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3Njg3NTQsImV4cCI6MjA2OTM0NDc1NH0.WVtvJKZxsJ4zAoxRUDyqFWekkV3UQ9Kk0HOzE78rMTo")

# Initialize supabase client as None initially
supabase: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """Get Supabase client with error handling"""
    global supabase
    if supabase is None:
        try:
            if SUPABASE_URL and SUPABASE_KEY:
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                logger.info("Supabase client initialized successfully")
            else:
                logger.warning("Supabase credentials not found, client not initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            supabase = None
    return supabase

async def test_supabase_connection() -> bool:
    """Test connection to Supabase"""
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        # Simple query to test connection
        result = client.table("seo_signals").select("*").limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"Supabase connection error: {e}")
        return False

async def fetch_seo_data():
    """Fetch SEO data from Phase 4"""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        result = client.table("seo_signals").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        logger.error(f"Error fetching SEO data: {e}")
        return []

async def fetch_mentions_data():
    """Fetch brand mentions from Phase 4"""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        result = client.table("mentions").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        logger.error(f"Error fetching mentions: {e}")
        return []

async def fetch_posts_data():
    """Fetch social media posts from Phase 4"""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        result = client.table("posts").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return []