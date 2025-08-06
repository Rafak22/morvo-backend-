from fastapi import APIRouter, HTTPException, Form
from ..models import ChatMessage, ChatResponse
from ..supabase_client import fetch_seo_data, fetch_mentions_data, fetch_posts_data
from datetime import datetime
import random

router = APIRouter()

@router.post("/chat")
async def chat_with_ai(message: str = Form(...)):
    """AI chat endpoint for marketing insights"""
    try:
        # Fetch recent data for context
        seo_data = await fetch_seo_data()
        mentions_data = await fetch_mentions_data() 
        posts_data = await fetch_posts_data()
        
        # Simple AI responses based on keywords
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['seo', 'ranking', 'keyword']):
            if seo_data:
                trending_up = len([item for item in seo_data if item.get('change', 0) > 0])
                trending_down = len([item for item in seo_data if item.get('change', 0) < 0])
                response = f"📈 SEO Analysis: {trending_up} keywords trending up, {trending_down} trending down. Your top performing keyword is '{seo_data[0].get('keyword', 'N/A')}' at position #{seo_data[0].get('position', 'N/A')}."
            else:
                response = "📊 I don't have recent SEO data. Make sure your data collection is running!"
                
        elif any(word in message_lower for word in ['mention', 'brand', 'sentiment']):
            if mentions_data:
                avg_sentiment = sum([item.get('sentiment', 0) for item in mentions_data]) / len(mentions_data)
                sentiment_text = "positive 😊" if avg_sentiment > 0.6 else "negative 😞" if avg_sentiment < 0.4 else "neutral 😐"
                response = f"💬 Brand Analysis: {len(mentions_data)} recent mentions with {sentiment_text} sentiment (score: {avg_sentiment:.2f}). Keep monitoring for reputation management!"
            else:
                response = "🔍 No recent brand mentions found. Consider increasing your online presence!"
                
        elif any(word in message_lower for word in ['social', 'post', 'engagement']):
            if posts_data:
                total_engagement = sum([item.get('likes', 0) + item.get('shares', 0) for item in posts_data])
                platforms = list(set([item.get('platform', 'Unknown') for item in posts_data]))
                response = f"📱 Social Analysis: {len(posts_data)} recent posts across {len(platforms)} platforms with {total_engagement} total engagement. Top platform: {platforms[0] if platforms else 'N/A'}"
            else:
                response = "📲 No recent social media data found. Make sure your social accounts are connected!"
                
        elif any(word in message_lower for word in ['help', 'what', 'how']):
            response = """🤖 I can help you analyze:
            • SEO performance and keyword rankings
            • Brand mentions and sentiment analysis  
            • Social media engagement and reach
            • Marketing alerts and recommendations
            
            Try asking: "How is my SEO performing?" or "What's my brand sentiment?"
            """
            
        else:
            responses = [
                "🚀 Your MORVO system is collecting valuable marketing intelligence! Ask me about SEO, brand mentions, or social media performance.",
                "📊 I can analyze your marketing data across SEO, social media, and brand monitoring. What would you like to know?",
                "🎯 Let me help you understand your marketing performance. Try asking about rankings, mentions, or engagement!",
                "💡 I'm here to provide insights from your marketing data. Ask me about specific metrics or trends!"
            ]
            response = random.choice(responses)
            
        return f"""
        <div class="space-y-2">
            <div class="bg-blue-100 p-3 rounded-lg">
                <strong>You:</strong> {message}
            </div>
            <div class="bg-green-100 p-3 rounded-lg">
                <strong>MORVO AI:</strong> {response}
            </div>
        </div>
        """
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/chat/health")
async def chat_health():
    """Check if chat system is working"""
    return {
        "status": "healthy",
        "features": ["SEO analysis", "Brand monitoring", "Social insights"],
        "message": "MORVO AI Assistant is ready! 🤖"
    }