from fastapi import APIRouter, HTTPException
from ..supabase_client import fetch_seo_data, fetch_mentions_data, fetch_posts_data
from ..models import DashboardData
import statistics

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_summary():
    """Get complete dashboard summary"""
    try:
        # Fetch all data
        seo_data = await fetch_seo_data()
        mentions_data = await fetch_mentions_data()
        posts_data = await fetch_posts_data()
        
        # Process SEO summary
        seo_summary = {
            "total_keywords": len(seo_data),
            "avg_position": statistics.mean([item.get('position', 0) for item in seo_data]) if seo_data else 0,
            "trending_up": len([item for item in seo_data if item.get('change', 0) > 0]),
            "trending_down": len([item for item in seo_data if item.get('change', 0) < 0])
        }
        
        # Process mentions summary  
        mentions_summary = {
            "total_mentions": len(mentions_data),
            "avg_sentiment": statistics.mean([item.get('sentiment', 0) for item in mentions_data]) if mentions_data else 0,
            "positive_mentions": len([item for item in mentions_data if item.get('sentiment', 0) > 0.6]),
            "negative_mentions": len([item for item in mentions_data if item.get('sentiment', 0) < 0.4])
        }
        
        # Process social summary
        social_summary = {
            "total_posts": len(posts_data),
            "total_engagement": sum([item.get('likes', 0) + item.get('shares', 0) for item in posts_data]),
            "avg_reach": statistics.mean([item.get('reach', 0) for item in posts_data]) if posts_data else 0,
            "platforms": list(set([item.get('platform', 'Unknown') for item in posts_data]))
        }
        
        # Generate alerts
        alerts = []
        if seo_summary['trending_down'] > seo_summary['trending_up']:
            alerts.append("⚠️ More keywords trending down than up")
        if mentions_summary['avg_sentiment'] < 0.5:
            alerts.append("📉 Brand sentiment below average")
        if social_summary['total_engagement'] < 100:
            alerts.append("📱 Social engagement could be improved")
        
        return DashboardData(
            seo_summary=seo_summary,
            mentions_summary=mentions_summary,
            social_summary=social_summary,
            alerts=alerts
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}")

@router.get("/dashboard/seo")
async def get_seo_widget():
    """Get SEO widget HTML"""
    data = await fetch_seo_data()
    if not data:
        return "<p class='text-gray-500'>No SEO data available</p>"
    
    html = "<div class='space-y-2'>"
    for item in data[:5]:
        change_color = "text-green-500" if item.get('change', 0) > 0 else "text-red-500" if item.get('change', 0) < 0 else "text-gray-500"
        change_icon = "↗️" if item.get('change', 0) > 0 else "↘️" if item.get('change', 0) < 0 else "➡️"
        html += f"""
        <div class='flex justify-between items-center'>
            <span class='font-medium'>{item.get('keyword', 'Unknown')}</span>
            <span class='{change_color}'>{change_icon} #{item.get('position', 'N/A')}</span>
        </div>
        """
    html += "</div>"
    return html

@router.get("/dashboard/mentions")
async def get_mentions_widget():
    """Get mentions widget HTML"""
    data = await fetch_mentions_data()
    if not data:
        return "<p class='text-gray-500'>No mentions data available</p>"
    
    positive = len([item for item in data if item.get('sentiment', 0) > 0.6])
    negative = len([item for item in data if item.get('sentiment', 0) < 0.4])
    neutral = len(data) - positive - negative
    
    return f"""
    <div class='space-y-2'>
        <div class='flex justify-between'>
            <span>😊 Positive</span>
            <span class='text-green-500 font-bold'>{positive}</span>
        </div>
        <div class='flex justify-between'>
            <span>😐 Neutral</span>
            <span class='text-gray-500 font-bold'>{neutral}</span>
        </div>
        <div class='flex justify-between'>
            <span>😞 Negative</span>
            <span class='text-red-500 font-bold'>{negative}</span>
        </div>
        <div class='pt-2 border-t'>
            <span class='text-sm text-gray-600'>Total: {len(data)} mentions</span>
        </div>
    </div>
    """

@router.get("/dashboard/social") 
async def get_social_widget():
    """Get social media widget HTML"""
    data = await fetch_posts_data()
    if not data:
        return "<p class='text-gray-500'>No social data available</p>"
    
    platforms = {}
    for post in data:
        platform = post.get('platform', 'Unknown')
        if platform not in platforms:
            platforms[platform] = {'posts': 0, 'engagement': 0}
        platforms[platform]['posts'] += 1
        platforms[platform]['engagement'] += post.get('likes', 0) + post.get('shares', 0)
    
    html = "<div class='space-y-2'>"
    for platform, stats in platforms.items():
        html += f"""
        <div class='flex justify-between items-center'>
            <span class='font-medium'>{platform}</span>
            <span class='text-blue-500'>{stats['posts']} posts, {stats['engagement']} eng.</span>
        </div>
        """
    html += "</div>"
    return html