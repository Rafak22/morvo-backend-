import os
from supabase import create_client, Client
from typing import Optional
import httpx
import asyncio

# Initialize Supabase client
SUPABASE_URL = os.getenv("https://ctcnutpnikiwvqbekdnp.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0Y251dHBuaWtpd3ZxYmVrZG5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3Njg3NTQsImV4cCI6MjA2OTM0NDc1NH0.WVtvJKZxsJ4zAoxRUDyqFWekkV3UQ9Kk0HOzE78rMTo")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def test_supabase_connection() -> bool:
    """Test connection to Supabase"""
    try:
        # Simple query to test connection
        result = supabase.table("seo_signals").select("*").limit(1).execute()
        return True
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return False

async def fetch_seo_data():
    """Fetch SEO data from Phase 4"""
    try:
        result = supabase.table("seo_signals").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching SEO data: {e}")
        return []

async def fetch_mentions_data():
    """Fetch brand mentions from Phase 4"""
    try:
        result = supabase.table("mentions").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching mentions: {e}")
        return []

async def fetch_posts_data():
    """Fetch social media posts from Phase 4"""
    try:
        result = supabase.table("posts").select("*").order("created_at", desc=True).limit(10).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []