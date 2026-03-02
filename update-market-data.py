#!/usr/bin/env python3
"""
实时行情抓取 - 免费API
"""

import json
import requests
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("/root/.openclaw/workspace/daily-brief/market-data.json")

def fetch_crypto():
    """CoinGecko 免费API - 加密货币"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": "bitcoin,ethereum,solana,ripple,cardano",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h"
        }
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        result = []
        for coin in data:
            result.append({
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "price": coin["current_price"],
                "change_24h": coin["price_change_percentage_24h"],
                "market_cap": coin["market_cap"],
                "volume": coin["total_volume"]
            })
        return result
    except Exception as e:
        print(f"CoinGecko 抓取失败: {e}")
        return []

def fetch_stock_cn():
    """新浪财经 - A股行情"""
    try:
        # 上证指数、深证成指、创业板指
        symbols = ["sh000001", "sz399001", "sz399006"]
        result = []
        
        for symbol in symbols:
            url = f"https://hq.sinajs.cn/list={symbol}"
            headers = {"Referer": "https://finance.sina.com.cn"}
            response = requests.get(url, headers=headers, timeout=10)
            
            # 解析返回数据
            data = response.text.split('"')[1].split(',')
            if len(data) > 3:
                name = data[0]
                price = float(data[3])
                prev_close = float(data[2])
                change = ((price - prev_close) / prev_close) * 100
                
                result.append({
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "change": round(change, 2)
                })
        return result
    except Exception as e:
        print(f"新浪财经抓取失败: {e}")
        return []

def generate_signals(crypto, stocks):
    """生成简单的买卖信号"""
    signals = []
    
    # 加密信号
    for coin in crypto:
        if coin["change_24h"] > 5:
            signals.append({
                "asset": coin["symbol"],
                "type": "crypto",
                "signal": "强势",
                "suggestion": "可考虑减仓锁定利润",
                "change": coin["change_24h"]
            })
        elif coin["change_24h"] < -5:
            signals.append({
                "asset": coin["symbol"],
                "type": "crypto", 
                "signal": "超跌",
                "suggestion": "谨慎观望，等待企稳",
                "change": coin["change_24h"]
            })
    
    # A股信号
    for stock in stocks:
        if stock["change"] > 2:
            signals.append({
                "asset": stock["name"],
                "type": "stock",
                "signal": "上涨",
                "suggestion": "趋势良好",
                "change": stock["change"]
            })
        elif stock["change"] < -2:
            signals.append({
                "asset": stock["name"],
                "type": "stock",
                "signal": "下跌", 
                "suggestion": "注意风险",
                "change": stock["change"]
            })
    
    return signals

def update_market_data():
    """更新行情数据"""
    print(f"[{datetime.now()}] 开始抓取行情...")
    
    crypto = fetch_crypto()
    stocks = fetch_stock_cn()
    signals = generate_signals(crypto, stocks)
    
    data = {
        "lastUpdate": datetime.now().isoformat(),
        "crypto": crypto,
        "stocks": stocks,
        "signals": signals
    }
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"更新完成: {len(crypto)} 个加密货币, {len(stocks)} 个股票, {len(signals)} 个信号")
    return data

if __name__ == "__main__":
    update_market_data()
