#!/usr/bin/env python3
"""
增强版股票分析 - 技术+情绪+资金流向
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("/root/.openclaw/workspace/daily-brief/stock-analysis.json")

def fetch_stock_detail(symbol):
    """获取股票详细数据（新浪财经）"""
    try:
        # 获取实时数据
        url = f"https://hq.sinajs.cn/list={symbol}"
        headers = {"Referer": "https://finance.sina.com.cn"}
        response = requests.get(url, headers=headers, timeout=10)
        
        data = response.text.split('"')[1].split(',')
        if len(data) < 30:
            return None
            
        return {
            "name": data[0],
            "price": float(data[3]),
            "open": float(data[1]),
            "high": float(data[4]),
            "low": float(data[5]),
            "prev_close": float(data[2]),
            "volume": int(data[8]),
            "amount": float(data[9]),
            "bid1": float(data[11]),
            "ask1": float(data[21]),
            "date": data[30],
            "time": data[31]
        }
    except Exception as e:
        print(f"获取{symbol}失败: {e}")
        return None

def calculate_indicators(stock):
    """计算技术指标"""
    if not stock:
        return {}
    
    price = stock["price"]
    prev_close = stock["prev_close"]
    high = stock["high"]
    low = stock["low"]
    
    # 涨跌幅
    change_pct = ((price - prev_close) / prev_close) * 100
    
    # 振幅
    amplitude = ((high - low) / prev_close) * 100
    
    # 相对位置（当日价格在高低点间的位置）
    position = ((price - low) / (high - low)) * 100 if high != low else 50
    
    # 简单趋势判断
    trend = "上涨" if change_pct > 0 else "下跌" if change_pct < 0 else "平盘"
    
    # 成交量分析（简化）
    volume_status = "放量" if stock["volume"] > 1000000 else "缩量"
    
    return {
        "change_pct": round(change_pct, 2),
        "amplitude": round(amplitude, 2),
        "position": round(position, 1),
        "trend": trend,
        "volume_status": volume_status
    }

def generate_signal(stock, indicators, news_sentiment="neutral"):
    """生成买卖信号"""
    score = 0
    reasons = []
    
    # 价格因素
    if indicators["change_pct"] > 3:
        score += 2
        reasons.append("涨幅较大，趋势强劲")
    elif indicators["change_pct"] > 1:
        score += 1
        reasons.append("温和上涨")
    elif indicators["change_pct"] < -3:
        score -= 2
        reasons.append("跌幅较大，注意风险")
    elif indicators["change_pct"] < -1:
        score -= 1
        reasons.append("小幅回调")
    
    # 位置因素
    if indicators["position"] > 80:
        score -= 1
        reasons.append("接近当日高点，追高风险")
    elif indicators["position"] < 20:
        score += 1
        reasons.append("接近当日低点，或有支撑")
    
    # 振幅因素
    if indicators["amplitude"] > 5:
        reasons.append("波动剧烈，谨慎操作")
    
    # 综合判断
    if score >= 2:
        signal = "买入"
        confidence = "强" if score >= 3 else "中"
        action = "可考虑逢低介入，设置止损"
    elif score >= 0:
        signal = "持有"
        confidence = "中"
        action = "趋势不明，建议观望"
    else:
        signal = "卖出"
        confidence = "强" if score <= -2 else "中"
        action = "建议减仓避险，等待企稳"
    
    return {
        "signal": signal,
        "confidence": confidence,
        "score": score,
        "action": action,
        "reasons": reasons
    }

def analyze_all():
    """分析所有股票"""
    symbols = [
        ("sh000001", "上证指数"),
        ("sz399001", "深证成指"),
        ("sz399006", "创业板指"),
        ("sh600519", "贵州茅台"),
        ("sz000858", "五粮液"),
        ("sh601318", "中国平安"),
        ("sz002594", "比亚迪"),
        ("sh600036", "招商银行")
    ]
    
    results = []
    for symbol, name in symbols:
        print(f"分析 {name}...")
        stock = fetch_stock_detail(symbol)
        if stock:
            indicators = calculate_indicators(stock)
            signal = generate_signal(stock, indicators)
            
            results.append({
                "symbol": symbol,
                "name": name,
                "price": stock["price"],
                "change": indicators["change_pct"],
                "indicators": indicators,
                "signal": signal,
                "update_time": f"{stock['date']} {stock['time']}"
            })
    
    # 保存结果
    data = {
        "last_update": datetime.now().isoformat(),
        "stocks": results
    }
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"分析完成，共 {len(results)} 只股票")
    return data

if __name__ == "__main__":
    analyze_all()
