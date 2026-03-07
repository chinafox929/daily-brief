from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import uvicorn

app = FastAPI(title="Daily Brief API - Realtime", version="3.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[{datetime.now()}] 新客户端连接，当前连接数: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"[{datetime.now()}] 客户端断开，当前连接数: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接的客户端"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# ============ 数据生成函数 ============
def get_market_data():
    """实时市场数据"""
    now = datetime.now()
    return {
        "type": "market",
        "timestamp": now.isoformat(),
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

def get_global_intelligence():
    """全球实时监控数据"""
    now = datetime.now()
    
    alerts = [
        {
            "id": "alert_001",
            "type": "cyber",
            "level": "high",
            "category": "网络安全",
            "title": "BlackCurrent勒索软件爆发 · 亚太能源SCADA系统遭攻击",
            "region": "Singapore, Vietnam",
            "time": now.strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "新型勒索软件变种攻击能源基础设施，已提取47个IoC，CISA发布AA26-066紧急警报",
            "impact": "能源网络安全概念股关注，SCADA系统供应商或受益"
        },
        {
            "id": "alert_002",
            "type": "military",
            "level": "elevated",
            "category": "地缘政治",
            "title": "南海多国海军集结 · 西沙群岛附近航行警告",
            "region": "Paracel Islands (12°N, 117°E)",
            "time": (now - timedelta(minutes=10)).strftime("%H:%M"),
            "china_relevance": "direct",
            "details": "卫星图像显示多国海军舰队在西沙群岛12海里内集结",
            "impact": "建议关注军工、北斗导航板块，商业航运需调整航线"
        },
        {
            "id": "alert_003",
            "type": "infrastructure",
            "level": "high",
            "category": "自然灾害",
            "title": "台风Maliksi形成 · 48小时内登陆菲律宾",
            "region": "Philippines, Luzon",
            "time": (now - timedelta(minutes=20)).strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "热带低压03W已增强，JMA预测48小时内发展为台风，路径指向吕宋岛北部",
            "impact": "航运板块短期承压，灾害预警概念股关注"
        },
        {
            "id": "alert_004",
            "type": "infrastructure",
            "level": "elevated",
            "category": "基础设施",
            "title": "AAG海底光缆香港段异常 · 东南亚至北美延迟上升",
            "region": "Hong Kong, APAC Gateway",
            "time": (now - timedelta(minutes=25)).strftime("%H:%M"),
            "china_relevance": "direct",
            "details": "检测到异常信号衰减，丢包率上升至12%，疑似渔船作业损伤，维修船已dispatch",
            "impact": "跨境电商、云服务短期可能受影响，关注通信设备板块"
        },
        {
            "id": "alert_005",
            "type": "infrastructure",
            "level": "monitoring",
            "category": "公共卫生",
            "title": "阿根廷不明原因肺炎聚集性病例 · WHO启动监测",
            "region": "Buenos Aires, Argentina",
            "time": (now - timedelta(minutes=40)).strftime("%H:%M"),
            "china_relevance": "global",
            "details": "14例不明原因肺炎，正在排除军团菌感染，目前无明确人传人证据",
            "impact": "医药板块关注，疫情防控概念股或异动"
        },
        {
            "id": "alert_006",
            "type": "economic",
            "level": "elevated",
            "category": "供应链",
            "title": "苏伊士运河通行量骤降18% · 红海航线保险上涨",
            "region": "Suez Canal, Egypt",
            "time": (now - timedelta(minutes=60)).strftime("%H:%M"),
            "china_relevance": "indirect",
            "details": "保险费率周环比+12%，马士基暂停3条亚欧航线",
            "impact": "航运股成本承压，关注中远海控"
        }
    ]
    
    high_risk = len([a for a in alerts if a["level"] == "high"])
    elevated = len([a for a in alerts if a["level"] == "elevated"])
    
    return {
        "type": "global",
        "timestamp": now.isoformat(),
        "updateTime": now.strftime("%Y-%m-%d %H:%M:%S"),
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

def get_breaking_news():
    """突发新闻"""
    now = datetime.now()
    return {
        "type": "news",
        "timestamp": now.isoformat(),
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

# ============ WebSocket 端点 ============
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 实时数据推送"""
    await manager.connect(websocket)
    
    try:
        # 发送初始数据
        await websocket.send_json({
            "type": "connected",
            "message": "已连接到实时数据流",
            "timestamp": datetime.now().isoformat()
        })
        
        # 发送当前完整数据
        await websocket.send_json(get_market_data())
        await websocket.send_json(get_global_intelligence())
        await websocket.send_json(get_breaking_news())
        
        # 保持连接，监听客户端消息
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
            except:
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[{datetime.now()}] WebSocket错误: {e}")
        manager.disconnect(websocket)

# ============ 定时广播任务 ============
@app.on_event("startup")
async def startup_event():
    """启动定时广播任务"""
    asyncio.create_task(broadcast_timer())

async def broadcast_timer():
    """每30秒广播一次数据更新"""
    while True:
        await asyncio.sleep(30)
        
        # 广播市场数据
        await manager.broadcast(get_market_data())
        
        # 广播全球监控数据
        await manager.broadcast(get_global_intelligence())
        
        print(f"[{datetime.now()}] 数据广播完成，连接数: {len(manager.active_connections)}")

# ============ HTTP API 端点（兼容旧版） ============
@app.get("/api/market")
def api_market():
    return get_market_data()

@app.get("/api/global")
def api_global():
    return get_global_intelligence()

@app.get("/api/news")
def api_news():
    return get_breaking_news()

@app.get("/api/brief")
def api_brief():
    now = datetime.now()
    return {
        "date": now.strftime("%Y年%m月%d日"),
        "updateTime": now.strftime("%H:%M"),
        "market": get_market_data(),
        "global": get_global_intelligence(),
        "news": get_breaking_news()
    }

# ============ 静态文件服务 ============
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = Path(__file__).parent / ".." / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Daily Brief Realtime API Running", "version": "3.0"}

# 挂载静态文件
static_dir = Path(__file__).parent / ".."
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
