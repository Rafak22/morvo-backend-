from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    data_insights: Optional[Dict[str, Any]] = None

class DashboardData(BaseModel):
    seo_summary: Dict[str, Any]
    mentions_summary: Dict[str, Any]  
    social_summary: Dict[str, Any]
    alerts: List[str]

class SEOSignal(BaseModel):
    keyword: str
    position: int
    change: int
    volume: int
    url: Optional[str] = None
    created_at: datetime

class Mention(BaseModel):
    text: str
    sentiment: float
    source: str
    reach: Optional[int] = None
    created_at: datetime

class SocialPost(BaseModel):
    content: str
    platform: str
    likes: int
    shares: int
    comments: int
    reach: Optional[int] = None
    created_at: datetime
