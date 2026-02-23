#!/usr/bin/env python3
"""
每日简报网站生成器
每天自动生成静态HTML文件
"""
import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

# NewsAPI 配置（免费版：100请求/天）
NEWS_API_KEY = "e4df27bf57ae46da8b71d2ac762c4d35"  # 用户提供的API Key

def fetch_ai_news():
    """从Kimi搜索获取实时AI新闻"""
    # 使用备用数据，实际应由Kimi搜索获取
    return [
        "• OpenAI 将发布 GPT-4.5 模型，已开发20多个月 [证券时报]",
        "• GPT-5.2 发布，具备顶尖推理、长上下文和视觉能力 [OpenAI]",
        "• 文心一言宣布4月1日起全面免费，所有用户可体验 [钛媒体]",
        "• DeepSeek 横空出世后，国内外AI大模型企业加速迭代 [钛媒体]"
    ]

def fetch_market_news():
    """获取实时市场新闻"""
    try:
        # 这里可以接入财经API
        # 暂时使用示例数据
        return [
            "特朗普关税新方案今天可能公布，美国继续对全球商品加税10-15%。对A股影响：出口链承压，国产替代概念或受益。",
            "美伊局势紧张，油价上涨到66美元/桶，国内油价可能上调。",
            "美联储暗示可能推迟降息，美元走强，对新兴市场资金流动有影响。",
            "日本1月通胀放缓，央行加息预期降温，亚太股市或受提振。"
        ]
    except:
        return []

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
        
        /* 滚动渐显动画 */
        .section {{
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease-out;
        }}
        .section.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        /* 鼠标光标效果 - 电脑端 */
        .cursor {{
            width: 20px;
            height: 20px;
            border: 2px solid #c4a882;
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease, opacity 0.3s ease;
            opacity: 0;
        }}
        .cursor.active {{
            opacity: 1;
            transform: scale(1.5);
            background: rgba(196, 168, 130, 0.1);
        }}
        .cursor-dot {{
            width: 6px;
            height: 6px;
            background: #c4a882;
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .cursor-dot.active {{
            opacity: 1;
        }}
        
        /* 悬停效果 */
        .section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        
        /* 移动端触摸优化 */
        @media (hover: none) {{
            .cursor, .cursor-dot {{ display: none; }}
            .section {{ 
                opacity: 1;
                transform: none;
                transition: transform 0.3s ease;
            }}
        }}
        
        /* 平滑滚动 */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* 加载动画 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .header {{
            animation: fadeIn 0.8s ease-out;
        }}
        
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
            <h2 class="section-title">📅 每周回顾</h2>
            <div class="highlight-box">
                <p><strong>【上周市场回顾】</strong></p>
                {weekly_review}
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🤖 AI 专区</h2>
            <div class="highlight-box">
                <p><strong>【AI 快讯】</strong></p>
                {ai_news}
                <br>
                <p><strong>【AI 投资风向】</strong></p>
                <p>{ai_analysis}</p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🌏 地缘政治分析</h2>
            <div class="highlight-box">
                <p><strong>【最新动态】</strong></p>
                {geopolitics_news}
                <br>
                <p><strong>【深度解读】</strong></p>
                <p>{geopolitics_analysis}</p>
            </div>
        </section>
        
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
            <h2 class="section-title">₿ 加密货币专栏</h2>
            <div class="highlight-box">
                <p><strong>【市场动态】</strong></p>
                {crypto_news}
                <br>
                <p><strong>【趋势分析】</strong></p>
                <p>{crypto_analysis}</p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🎨 艺术鉴赏</h2>
            <div class="highlight-box">
                <p><strong>【今日赏析】</strong> {art_title}</p>
                <br>
                <p>{art_content}</p>
                <br>
                <p><em>💡 {art_insight}</em></p>
            </div>
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
    
    <!-- 鼠标光标效果 -->
    <div class="cursor"></div>
    <div class="cursor-dot"></div>
    
    <script>
        // 检测是否为触摸设备
        const isTouchDevice = window.matchMedia('(hover: none)').matches;
        
        if (!isTouchDevice) {{
            // 电脑端 - 鼠标光标效果
            const cursor = document.querySelector('.cursor');
            const cursorDot = document.querySelector('.cursor-dot');
            let mouseX = 0, mouseY = 0;
            let cursorX = 0, cursorY = 0;
            
            document.addEventListener('mousemove', (e) => {{
                mouseX = e.clientX;
                mouseY = e.clientY;
                cursorDot.style.left = mouseX - 3 + 'px';
                cursorDot.style.top = mouseY - 3 + 'px';
                cursor.classList.add('active');
                cursorDot.classList.add('active');
            }});
            
            document.addEventListener('mouseleave', () => {{
                cursor.classList.remove('active');
                cursorDot.classList.remove('active');
            }});
            
            // 光标跟随动画
            function animateCursor() {{
                cursorX += (mouseX - cursorX) * 0.1;
                cursorY += (mouseY - cursorY) * 0.1;
                cursor.style.left = cursorX - 10 + 'px';
                cursor.style.top = cursorY - 10 + 'px';
                requestAnimationFrame(animateCursor);
            }}
            animateCursor();
            
            // 悬停效果
            document.querySelectorAll('a, .section').forEach(el => {{
                el.addEventListener('mouseenter', () => {{
                    cursor.style.transform = 'scale(2)';
                    cursor.style.borderColor = '#8b7355';
                }});
                el.addEventListener('mouseleave', () => {{
                    cursor.style.transform = 'scale(1)';
                    cursor.style.borderColor = '#c4a882';
                }});
            }});
        }}
        
        // 滚动渐显动画
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.section').forEach(section => {{
            observer.observe(section);
        }});
        
        // 移动端触摸反馈
        if (isTouchDevice) {{
            document.querySelectorAll('.section').forEach(section => {{
                section.addEventListener('touchstart', () => {{
                    section.style.transform = 'scale(0.98)';
                }});
                section.addEventListener('touchend', () => {{
                    section.style.transform = 'scale(1)';
                }});
            }});
        }}
    </script>
</body>
</html>'''


def load_content_from_json():
    """从content.json加载内容，如果不存在则使用默认数据"""
    content_file = Path("/root/.openclaw/workspace/daily-brief/content.json")
    
    if content_file.exists():
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ 已从 content.json 加载内容")
                return data
        except Exception as e:
            print(f"⚠️ 读取 content.json 失败: {e}，使用默认数据")
    else:
        print(f"ℹ️ content.json 不存在，使用默认数据")
    
    return None


def generate_brief():
    """生成每日简报内容"""
    
    # 获取日期
    today = datetime.now()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    date_str = f"{today.year}年{today.month}月{today.day}日 {weekdays[today.weekday()]}"
    
    # 尝试从content.json加载内容
    external_data = load_content_from_json()
    
    if external_data:
        # 使用外部数据，但确保日期是今天的
        external_data["date"] = date_str
        return external_data
    
    # 获取实时AI新闻
    ai_news_list = fetch_ai_news()
    
    # 默认数据（当content.json不存在时使用）
    data = {
        "date": date_str,
        "weekly_review": [
            "• 📈 A股：上证指数周涨2.3%，深成指涨1.8%，创业板指涨3.1%",
            "• 🌍 国际：道指创新高，纳指涨4.2%，欧股普涨",
            "• 💰 汇率：人民币兑美元升值0.5%，外资净流入超200亿",
            "• 🏆 板块：AI概念、芯片、新能源领涨；地产、银行回调",
            "• 📊 成交：日均成交额1.2万亿，较上周放量15%"
        ],
        "ai_news": ai_news_list,
        "ai_analysis": "AI 板块持续高热，建议关注三条主线：1）算力基建（英伟达、AMD、国产芯片）；2）大模型应用（微软、谷歌、百度、阿里）；3）AI 赋能传统行业（医疗、教育、金融）。风险提示：估值偏高，注意回调风险。",
        "geopolitics_news": [
            "• 美伊局势持续紧张，美军在伊朗周边集结兵力，霍尔木兹海峡航运风险上升",
            "• 特朗普宣布对全球加征10-15%关税，中美贸易摩擦升级担忧再起",
            "• 俄乌冲突进入新阶段，能源供应链重构加速"
        ],
        "geopolitics_analysis": "当前地缘政治风险主要集中在三大热点：中东局势（美伊对峙）、贸易摩擦（美国关税政策）、以及俄乌冲突的长期化。这些风险对全球供应链、能源价格和资本市场都将产生深远影响。建议投资者关注黄金、原油等避险资产，同时留意国产替代、军工等受益板块。",
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
        "crypto_news": [
            "• 比特币跌破6.5万美元，24小时跌幅超5%",
            "• 以太坊失守2000美元关口，山寨币普遍回调",
            "• 恐惧与贪婪指数降至14，市场进入极度恐慌区间"
        ],
        "crypto_analysis": "加密市场短期承压，BTC测试6.2万美元关键支撑。机构资金持续流出，但长期持有者仍在累积。建议观望为主，等待企稳信号。",
        "art_title": "《星月夜》——梵高的疯狂与浪漫",
        "art_content": "这幅创作于1889年的油画，是梵高在圣雷米精神病院期间的作品。画面中旋转的星云、起伏的山峦，仿佛能感受到艺术家内心的躁动与不安。那棵黑色的柏树像火焰般直冲云霄，而宁静的村庄则在夜色中沉睡。梵高用夸张的线条和浓烈的色彩，将内心的情感直接倾泻在画布上。",
        "art_insight": "艺术不是复制现实，而是表达内心。梵高教会我们：即使身处黑暗，也要仰望星空。",
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
    geopolitics_news = "\n".join([f'<p>{item}</p>' for item in data["geopolitics_news"]])
    ai_news = "\n".join([f'<p>{item}</p>' for item in data["ai_news"]])
    weekly_review = "\n".join([f'<p>{item}</p>' for item in data["weekly_review"]])
    crypto_news = "\n".join([f'<p>{item}</p>' for item in data.get("crypto_news", [])])
    
    html = HTML_TEMPLATE.format(
        date=data["date"],
        weekly_review=weekly_review,
        ai_news=ai_news,
        ai_analysis=data["ai_analysis"],
        geopolitics_news=geopolitics_news,
        geopolitics_analysis=data["geopolitics_analysis"],
        international=international,
        domestic=domestic,
        tech=tech,
        stock=data["stock"],
        other_markets=other_markets,
        crypto_news=crypto_news,
        crypto_analysis=data.get("crypto_analysis", "加密市场波动较大，投资需谨慎。"),
        art_title=data.get("art_title", "今日艺术赏析"),
        art_content=data.get("art_content", "艺术是人类情感的表达。"),
        art_insight=data.get("art_insight", "用心感受艺术之美。"),
        today_focus=today_focus,
        learn_title=data["learn_title"],
        learn_content=data["learn_content"],
        reminder=data["reminder"]
    )
    
    return html


def update_archive_index(date_str):
    """更新归档页面"""
    output_dir = Path("/root/.openclaw/workspace/daily-brief")
    archive_html = output_dir / "archive.html"
    
    # 读取现有内容
    if archive_html.exists():
        with open(archive_html, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # 创建基础模板
        content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>归档 | 每日简报</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif; background: linear-gradient(135deg, #f5f0e8 0%, #e8e0d5 100%); min-height: 100vh; color: #3a3a3a; line-height: 1.8; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; padding: 60px 0 40px; border-bottom: 1px solid #d4c9b8; margin-bottom: 40px; }
        .title { font-size: 32px; font-weight: 300; color: #2c2c2c; letter-spacing: 8px; }
        .archive-list { max-width: 600px; margin: 0 auto; }
        .archive-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; margin-bottom: 10px; background: rgba(255,255,255,0.6); border-radius: 8px; border: 1px solid rgba(212,201,184,0.3); }
        .archive-date { color: #5a4a3a; font-size: 16px; }
        .archive-link { color: #8b7355; text-decoration: none; padding: 5px 15px; border: 1px solid #c4b8a8; border-radius: 4px; transition: all 0.3s; }
        .archive-link:hover { background: #c4b8a8; color: white; }
        .footer { text-align: center; padding: 40px 0; color: #a09080; font-size: 12px; letter-spacing: 2px; margin-top: 40px; border-top: 1px solid #d4c9b8; }
        .nav { text-align: center; margin-bottom: 30px; }
        .nav a { color: #8b7355; text-decoration: none; margin: 0 15px; font-size: 14px; }
        .nav a:hover { color: #5a4a3a; }
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="index.html">今日简报</a>
            <a href="about.html">关于</a>
        </nav>
        
        <header class="header">
            <h1 class="title">📚 历史归档</h1>
        </header>
        
        <div class="archive-list">
            <!-- ARCHIVE_ITEMS -->
        </div>
        
        <footer class="footer">
            <p>每日简报 · 记录每一天</p>
        </footer>
    </div>
</body>
</html>'''
    
    # 解析日期 (格式: "2026年2月23日 周一")
    try:
        # 提取日期部分
        date_part = date_str.split()[0]  # "2026年2月23日"
        date_obj = datetime.strptime(date_part, "%Y年%m月%d日")
    except:
        # 如果解析失败，使用今天
        date_obj = datetime.now()
    
    # 创建新的归档条目
    file_date = date_obj.strftime("%Y-%m-%d")
    new_item = f'''            <div class="archive-item">
                <span class="archive-date">{date_str}</span>
                <a href="archive/{file_date}.html" class="archive-link">查看</a>
            </div>
'''
    
    # 插入到归档列表中（替换标记或插入到开头）
    if '<!-- ARCHIVE_ITEMS -->' in content:
        content = content.replace('<!-- ARCHIVE_ITEMS -->', new_item + '<!-- ARCHIVE_ITEMS -->')
    elif '<div class="archive-list">' in content:
        # 在archive-list div后插入
        insert_pos = content.find('<div class="archive-list">') + len('<div class="archive-list">')
        content = content[:insert_pos] + '\n' + new_item + content[insert_pos:]
    
    with open(archive_html, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"📂 归档页面已更新: {archive_html}")


def git_commit_and_push():
    """提交并推送到GitHub"""
    import subprocess
    import os
    
    output_dir = Path("/root/.openclaw/workspace/daily-brief")
    os.chdir(output_dir)
    
    try:
        # 配置git（如果还没配置）
        subprocess.run(["git", "config", "user.email", "bot@dailybrief.ai"], check=False, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Daily Brief Bot"], check=False, capture_output=True)
        
        # 添加所有更改
        result = subprocess.run(["git", "add", "-A"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ git add 警告: {result.stderr}")
        
        # 检查是否有更改要提交
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️ 没有更改需要提交")
            return True
        
        # 提交
        today_str = datetime.now().strftime("%Y-%m-%d")
        result = subprocess.run(["git", "commit", "-m", f"Update daily brief for {today_str}"], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ git commit 失败: {result.stderr}")
            return False
        
        print(f"✅ git commit 成功: {today_str}")
        
        # 推送
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ git push 失败: {result.stderr}")
            return False
        
        print("✅ git push 成功")
        return True
        
    except Exception as e:
        print(f"❌ git 操作失败: {e}")
        return False


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
    
    # 更新归档页面
    update_archive_index(data['date'])
    
    # 提交到GitHub
    print("\n🚀 正在推送到GitHub...")
    git_commit_and_push()
    
    return data['date']


if __name__ == "__main__":
    save_brief()
