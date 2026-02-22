#!/usr/bin/env python3
"""
每日简报网站生成器
每天自动生成静态HTML文件
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 网站模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日简报 | {date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #f5f0e8 0%, #e8e0d5 100%);
            min-height: 100vh;
            color: #3a3a3a;
            line-height: 1.8;
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .header {{ text-align: center; padding: 60px 0 40px; border-bottom: 1px solid #d4c9b8; margin-bottom: 40px; }}
        .date {{ font-size: 14px; color: #8b7355; letter-spacing: 3px; margin-bottom: 10px; }}
        .title {{ font-size: 32px; font-weight: 300; color: #2c2c2c; letter-spacing: 8px; }}
        .zen-circle {{ width: 80px; height: 80px; border: 2px solid #c4b8a8; border-radius: 50%; margin: 30px auto; position: relative; opacity: 0.6; }}
        .zen-circle::before {{ content: ""; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 40px; height: 40px; border: 1px solid #d4c9b8; border-radius: 50%; }}
        .section {{ background: rgba(255, 255, 255, 0.6); border-radius: 8px; padding: 30px; margin-bottom: 25px; box-shadow: 0 2px 15px rgba(0,0,0,0.03); border: 1px solid rgba(212, 201, 184, 0.3); }}
        .section-title {{ font-size: 18px; color: #5a4a3a; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #e0d8cd; display: flex; align-items: center; gap: 10px; }}
        .news-list {{ list-style: none; }}
        .news-item {{ padding: 12px 0; border-bottom: 1px dashed #e0d8cd; position: relative; padding-left: 20px; }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item::before {{ content: "•"; position: absolute; left: 0; color: #a09080; }}
        .highlight-box {{ background: linear-gradient(135deg, #faf8f5 0%, #f5f2ed 100%); border-left: 3px solid #c4a882; padding: 20px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
        .learn-box {{ background: #f9f7f4; padding: 20px; border-radius: 8px; border: 1px solid #e8e0d5; }}
        .learn-title {{ font-size: 14px; color: #8b7355; margin-bottom: 10px; }}
        .reminder {{ background: linear-gradient(135deg, #f5f0e8 0%, #ebe5dc 100%); padding: 20px; border-radius: 8px; text-align: center; font-size: 15px; color: #5a4a3a; }}
        .footer {{ text-align: center; padding: 40px 0; color: #a09080; font-size: 12px; letter-spacing: 2px; }}
        .nav {{ text-align: center; margin-bottom: 30px; }}
        .nav a {{ color: #8b7355; text-decoration: none; margin: 0 15px; font-size: 14px; }}
        .nav a:hover {{ color: #5a4a3a; }}
        @media (max-width: 600px) {{ .title {{ font-size: 24px; letter-spacing: 4px; }} .section {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="index.html">今日</a>
            <a href="archive.html">归档</a>
            <a href="about.html">关于</a>
        </div>
        
        <header class="header">
            <div class="date">{date}</div>
            <h1 class="title">每日简报</h1>
            <div class="zen-circle"></div>
            <div class="subtitle">专属信息网 · 禅意生活</div>
        </header>
        
        <section class="section">
            <h2 class="section-title">🌍 国际热点</h2>
            <ul class="news-list">{international}</ul>
        </section>
        
        <section class="section">
            <h2 class="section-title">🇨🇳 国内动态</h2>
            <ul class="news-list">{domestic}</ul>
        </section>
        
        <section class="section">
            <h2 class="section-title">💡 科技新鲜事</h2>
            <ul class="news-list">{tech}</ul>
        </section>
        
        <section class="section">
            <h2 class="section-title">🔥 A股重点</h2>
            <div class="highlight-box">{stock}</div>
        </section>
        
        <section class="section">
            <h2 class="section-title">📊 其他市场</h2>
            <ul class="news-list">{other_markets}</ul>
        </section>
        
        <section class="section">
            <h2 class="section-title">👀 今日看点</h2>
            <ul class="news-list">{today_focus}</ul>
        </section>
        
        <section class="section">
            <h2 class="section-title">📚 每日财经学习</h2>
            <div class="learn-box">
                <div class="learn-title">{learn_title}</div>
                <p>{learn_content}</p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">💡 每日一提醒</h2>
            <div class="reminder">
                <div style="font-size: 24px; margin-bottom: 10px;">☀️</div>
                <p>{reminder}</p>
            </div>
        </section>
        
        <footer class="footer">
            <p>专属信息网 · 每日更新</p>
            <p style="margin-top: 10px; opacity: 0.6;">禅意 · 简约 · 专注</p>
        </footer>
    </div>
</body>
</html>'''


def generate_brief():
    """生成每日简报内容"""
    
    # 获取日期
    today = datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    date_str = f"{today.year}年{today.month}月{today.day}日 {weekdays[today.weekday()]}"
    
    # 示例数据（实际应从API获取）
    data = {
        "date": date_str,
        "international": [
            "特朗普关税新方案今天可能公布，美国继续对全球商品加税10-15%。对A股影响：出口链承压，国产替代概念或受益。",
            "美伊局势紧张，油价上涨到66美元/桶，国内油价可能上调。",
            "美联储暗示可能推迟降息，美元走强，对新兴市场资金流动有影响。",
            "日本1月通胀放缓，央行加息预期降温，亚太股市或受提振。"
        ],
        "domestic": [
            "明天A股春节后首个交易日，历史数据显示春节后第一周上涨概率约70%，'开门红'可期。",
            "央行近期可能降准降息，资金面有望更宽松，利好股市。",
            "证监会发布新规，加强上市公司质量监管，长期利好A股生态。",
            "春节假期消费数据亮眼，旅游、电影、餐饮收入超预期，消费复苏概念值得关注。",
            "多地出台房地产支持政策，房贷利率下调，地产链或迎修复。"
        ],
        "tech": [
            "国产AI公司智谱股价暴涨42%，市值破3000亿，AI应用概念持续火热。",
            "小红书内测AI剪辑工具，对着手机说句话就能剪视频。",
            "比亚迪发布新车型，价格再创新低，新能源车竞争白热化。"
        ],
        "stock": "上周五（节前）A股集体收跌，上证指数跌1.26%报4082点，深成指跌1.28%，创业板指跌1.57%。成交额2万亿，较前日缩量7%。板块方面，海洋捕捞、半导体设备逆势上涨；通信线缆、稀土、有色金属跌幅居前。技术面看，沪指跌破4100点整数关口，短期支撑在4050点附近，压力在4150点。明日节后开市，关注能否'开门红'，建议控制仓位，重点关注AI应用、国产替代、消费复苏三大主线。",
        "other_markets": [
            "美股：道指逼近5万点，科技股领涨",
            "港股：AI概念强势，腾讯阿里承压",
            "比特币：约6.8万美元"
        ],
        "today_focus": [
            "A股春节后首个交易日，关注'开门红'",
            "1月LPR数据公布，关注利率动向",
            "特朗普关税细节公布，关注市场反应"
        ],
        "learn_title": "支撑位和压力位",
        "learn_content": "就像楼梯的台阶，股价跌到某个位置跌不动了叫支撑（有人买），涨到某个位置涨不动了叫压力（有人卖）。突破压力可能继续上涨，跌破支撑可能继续下跌。",
        "reminder": "节后开盘别急着追高，先看半小时盘面再决定。祝投资顺利！"
    }
    
    return data


def generate_html(data):
    """生成HTML文件"""
    
    # 格式化列表
    international = "\n".join([f'<li class="news-item">{item}</li>' for item in data["international"]])
    domestic = "\n".join([f'<li class="news-item">{item}</li>' for item in data["domestic"]])
    tech = "\n".join([f'<li class="news-item">{item}</li>' for item in data["tech"]])
    other_markets = "\n".join([f'<li class="news-item">{item}</li>' for item in data["other_markets"]])
    today_focus = "\n".join([f'<li class="news-item">{item}</li>' for item in data["today_focus"]])
    
    html = HTML_TEMPLATE.format(
        date=data["date"],
        international=international,
        domestic=domestic,
        tech=tech,
        stock=data["stock"],
        other_markets=other_markets,
        today_focus=today_focus,
        learn_title=data["learn_title"],
        learn_content=data["learn_content"],
        reminder=data["reminder"]
    )
    
    return html


def save_brief():
    """保存每日简报"""
    data = generate_brief()
    html = generate_html(data)
    
    # 保存为 index.html（今日）
    output_dir = Path("/root/.openclaw/workspace/daily-brief")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 同时保存到归档
    today_str = datetime.now().strftime("%Y-%m-%d")
    archive_dir = output_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    
    with open(archive_dir / f"{today_str}.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 每日简报已生成: {data['date']}")
    print(f"📁 文件位置: {output_dir}/index.html")
    print(f"📂 归档位置: {archive_dir}/{today_str}.html")
    
    return data['date']


if __name__ == "__main__":
    save_brief()
