from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import uvicorn

app = FastAPI(title="Daily Brief API", version="2.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据目录
DATA_DIR = Path(__file__).parent / ".." / "data"
DATA_DIR.mkdir(exist_ok=True)

# ============ 市场数据 ============
@app.get("/api/market")
def get_market_data():
    """实时市场数据 - 统一使用美元计价"""
    return {
        "updateTime": datetime.now().isoformat(),
        "indices": {
            "CSI300": {"value": 3847.23, "change": -0.42, "currency": "CNY"},
            "Shanghai": {"value": 3247.89, "change": +0.15, "currency": "CNY"},
            "Shenzhen": {"value": 10523.45, "change": -0.28, "currency": "CNY"},
            "ChiNext": {"value": 2156.78, "change": +0.63, "currency": "CNY"},
            "HSI": {"value": 24215.00, "change": +1.23, "currency": "HKD"},
            "DJI": {"value": 42801.55, "change": -0.95, "currency": "USD"},
            "NASDAQ": {"value": 18432.15, "change": -1.59, "currency": "USD"},
            "SP500": {"value": 5847.23, "change": -1.33, "currency": "USD"},
        },
        "crypto": {
            "BTC": {"value": 87432.50, "change": +1.24, "currency": "USD", "volume": "28.4B"},
            "ETH": {"value": 4156.80, "change": +0.89, "currency": "USD", "volume": "12.1B"},
            "SOL": {"value": 128.50, "change": -12.3, "currency": "USD"},
        },
        "commodities": {
            "GOLD": {"value": 5158.00, "change": +1.58, "currency": "USD"},
            "OIL_BRENT": {"value": 92.40, "change": +12.3, "currency": "USD"},
            "COPPER": {"value": 9845.00, "change": +9.75, "currency": "USD"},
        }
    }

# ============ 全球监控数据 ============
@app.get("/api/global")
def get_global_intelligence():
    """全球实时监控数据"""
    now = datetime.now()
    
    alerts = [
        {
            "id": "alert_001",
            "type": "military",
            "level": "high",
            "category": "地缘政治",
            "title": "南海区域AIS信号异常 · 不明海警船进入争议水域",
            "region": "South China Sea (12°N, 117°E)",
            "time": now.strftime("%H:%M"),
            "china_relevance": "direct",
            "details": "侦测到菲律宾以西海域3艘unidentified海警船",
            "impact": "建议关注军工、北斗导航板块"
        },
        {
            "id": "alert_002",
            "type": "cyber",
            "level": "elevated",
            "category": "网络安全",
            "title": "ShadowGate-7供应链攻击 · 东南亚能源部门",
            "region": "Singapore, Southeast Asia",
            "time": (now - timedelta(minutes=15)).strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "CVSS评分8.7，已确认影响2家新加坡能源公司",
            "impact": "网络安全概念股或受益"
        },
        {
            "id": "alert_003",
            "type": "economic",
            "level": "elevated",
            "category": "供应链",
            "title": "苏伊士运河通行量骤降18% · 红海航线保险上涨",
            "region": "Suez Canal, Egypt",
            "time": (now - timedelta(minutes=30)).strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "保险费率周环比+12%，马士基暂停3条亚欧航线",
            "impact": "航运股成本承压，关注中远海控"
        },
        {
            "id": "alert_004",
            "type": "cyber",
            "level": "monitoring",
            "category": "金融异常",
            "title": "全球加密货币异常大额转账监测",
            "region": "Global",
            "time": (now - timedelta(minutes=5)).strftime("%H:%M"),
            "china_relevance": "global",
            "details": "12,000 BTC转移至多个混币器，链上分析显示可能与欧盟新监管法案有关",
            "impact": "加密市场波动风险"
        },
        {
            "id": "alert_005",
            "type": "infrastructure",
            "level": "monitoring",
            "category": "自然灾害",
            "title": "日本樱岛火山喷发预警 · 福冈空域影响",
            "region": "Japan, Kyushu",
            "time": (now - timedelta(minutes=45)).strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "VEI 3级喷发，火山灰扩散模型显示未来6-12小时影响",
            "impact": "中日航线可能延误"
        }
    ]
    
    high_risk = len([a for a in alerts if a["level"] == "high"])
    elevated = len([a for a in alerts if a["level"] == "elevated"])
    
    return {
        "updateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "lastUpdate": now.isoformat(),
        "hotspots": [a for a in alerts if a["type"] == "military"],
        "infrastructure_alerts": [a for a in alerts if a["type"] == "infrastructure"],
        "cyber_alerts": [a for a in alerts if a["type"] == "cyber"],
        "economic_signals": [a for a in alerts if a["type"] == "economic"],
        "all_alerts": alerts,
        "summary": f"检测到{high_risk}个高风险事件，{elevated}个中风险指标需要留意",
        "total_alerts": len(alerts),
        "high_risk_count": high_risk,
        "stats": {
            "high": high_risk,
            "elevated": elevated,
            "monitoring": len([a for a in alerts if a["level"] == "monitoring"]),
            "normal": 89
        }
    }

# ============ 突发新闻 ============
@app.get("/api/news")
def get_breaking_news():
    """突发新闻"""
    now = datetime.now()
    return {
        "lastUpdate": now.isoformat(),
        "breakingNews": [
            {
                "id": "news_001",
                "title": "🔥 美伊局势持续紧张，特朗普要求伊朗'无条件投降'",
                "time": now.strftime("%H:%M"),
                "category": "国际",
                "urgency": "high"
            },
            {
                "id": "news_002", 
                "title": "📈 本周油价飙升35%，创1983年以来最大单周涨幅",
                "time": (now - timedelta(minutes=10)).strftime("%H:%M"),
                "category": "财经",
                "urgency": "high"
            },
            {
                "id": "news_003",
                "title": "💰 美股周五收跌，道指跌0.95%，纳指跌1.59%",
                "time": (now - timedelta(minutes=20)).strftime("%H:%M"),
                "category": "股市",
                "urgency": "medium"
            },
            {
                "id": "news_004",
                "title": "🪙 比特币波动加剧，24小时振幅超8%",
                "time": (now - timedelta(minutes=5)).strftime("%H:%M"),
                "category": "加密",
                "urgency": "medium"
            },
            {
                "id": "news_005",
                "title": "🇨🇳 两会进行时：政府工作报告首提'稳住股市'",
                "time": (now - timedelta(minutes=30)).strftime("%H:%M"),
                "category": "国内",
                "urgency": "high"
            }
        ]
    }

# ============ 完整简报数据 ============
@app.get("/api/brief")
def get_full_brief():
    """获取完整简报数据"""
    return {
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "updateTime": datetime.now().strftime("%H:%M"),
        "market": get_market_data(),
        "global": get_global_intelligence(),
        "news": get_breaking_news()
    }

# ============ 静态文件服务 ============
@app.get("/", response_class=HTMLResponse)
def serve_index():
    """主页 - 返回动态渲染的HTML"""
    index_path = Path(__file__).parent / ".." / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Daily Brief API Running", "version": "2.0"}

# 挂载静态文件目录
static_dir = Path(__file__).parent / ".."
if (static_dir / "styles.css").exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
