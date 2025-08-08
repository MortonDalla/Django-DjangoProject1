import os
import redis.asyncio as redis
from supabase import create_client, Client
from app.config import Config

# Initialize Supabase client
url: str = Config.SUPABASE_PROJECT_URL
key: str = Config.SUPABASE_SERVICE_ROLE_KEY
supabase: Client = create_client(url, key)

# Initialize Redis client
redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)

async def get_supabase_client() -> Client:
    """
    Returns the shared Supabase client instance.
    """
    return supabase

async def get_redis_client():
    """
    Returns the shared Redis client instance.
    """
    return redis_client
