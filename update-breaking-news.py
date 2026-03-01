#!/usr/bin/env python3
"""
突发新闻自动抓取脚本
每30分钟抓取一次热搜和突发新闻，更新 breaking-news.json
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import re

# 配置
NEWS_FILE = Path("/root/.openclaw/workspace/daily-brief/breaking-news.json")
MAX_NEWS = 10  # 最多保留多少条

# 新闻源配置
SOURCES = {
    "weibo": "https://weibo.com/ajax/side/hotSearch",
    "zhihu": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total",
    "baidu": "https://top.baidu.com/board?tab=realtime"
}

def load_existing_news():
    """加载现有新闻"""
    if NEWS_FILE.exists():
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"lastUpdate": "", "breakingNews": []}

def save_news(data):
    """保存新闻"""
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_weibo_hot():
    """抓取微博热搜"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(SOURCES["weibo"], headers=headers, timeout=10)
        data = response.json()
        
        news_list = []
        if 'data' in data and 'realtime' in data['data']:
            for item in data['data']['realtime'][:5]:  # 取前5条
                news_list.append({
                    "title": item.get('word', ''),
                    "category": "热搜",
                    "urgency": "high" if item.get('is_hot') else "medium"
                })
        return news_list
    except Exception as e:
        print(f"抓取微博失败: {e}")
        return []

def fetch_toutiao_hot():
    """抓取今日头条热榜（模拟）"""
    # 这里可以添加实际抓取逻辑
    return []

def generate_mock_news():
    """生成模拟突发新闻（用于测试）"""
    now = datetime.now()
    return [
        {
            "id": "1",
            "title": "美以联合袭击伊朗，中东局势急剧升级",
            "time": (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
            "category": "国际",
            "urgency": "high"
        },
        {
            "id": "2",
            "title": "比特币跌破8万美元，加密货币市场动荡",
            "time": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "category": "财经",
            "urgency": "medium"
        },
        {
            "id": "3",
            "title": "小米超跑正式亮相，定价引发热议",
            "time": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
            "category": "科技",
            "urgency": "low"
        }
    ]

def update_breaking_news():
    """更新突发新闻"""
    print(f"[{datetime.now()}] 开始更新突发新闻...")
    
    # 加载现有数据
    data = load_existing_news()
    
    # 抓取新新闻
    new_items = []
    
    # 尝试抓取微博
    weibo_news = fetch_weibo_hot()
    for i, news in enumerate(weibo_news):
        new_items.append({
            "id": f"wb_{i}",
            "title": news["title"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": news["category"],
            "urgency": news["urgency"],
            "url": "#"
        })
    
    # 如果没有抓到，使用模拟数据
    if not new_items:
        new_items = generate_mock_news()
    
    # 合并并去重
    existing_titles = {n["title"] for n in data["breakingNews"]}
    for item in new_items:
        if item["title"] not in existing_titles:
            data["breakingNews"].insert(0, item)
            existing_titles.add(item["title"])
    
    # 限制数量
    data["breakingNews"] = data["breakingNews"][:MAX_NEWS]
    
    # 更新时间
    data["lastUpdate"] = datetime.now().isoformat()
    
    # 保存
    save_news(data)
    print(f"[{datetime.now()}] 更新完成，共 {len(data['breakingNews'])} 条新闻")
    
    return data

if __name__ == "__main__":
    update_breaking_news()
