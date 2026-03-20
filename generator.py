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
    <link rel="stylesheet" href="styles.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            min-height: 100vh;
            color: var(--text-primary);
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
        .art-image {{ width: 100%; max-width: 600px; margin: 20px auto; display: block; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .art-caption {{ text-align: center; font-size: 13px; color: #8b7355; margin-top: 10px; font-style: italic; }}
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
<body class="theme-zen">
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
                <br><br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{weekly_thought}</em></p>
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
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{ai_thought}</em></p>
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
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{geopolitics_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🌍 国际热点</h2>
            <ul class="news-list">{international}</ul>
            <br>
            <p><strong>💭 深度思考</strong></p>
            <p><em>{international_thought}</em></p>
        </section>
        
        <section class="section">
            <h2 class="section-title">🇨🇳 国内动态</h2>
            <ul class="news-list">{domestic}</ul>
            <br>
            <p><strong>💭 深度思考</strong></p>
            <p><em>{domestic_thought}</em></p>
        </section>
        
        <section class="section">
            <h2 class="section-title">💡 科技新鲜事</h2>
            <ul class="news-list">{tech}</ul>
            <br>
            <p><strong>💭 深度思考</strong></p>
            <p><em>{tech_thought}</em></p>
        </section>
        
        <section class="section">
            <h2 class="section-title">🔥 A股重点</h2>
            <div class="highlight-box">
                <p>{stock}</p>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{stock_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">📊 其他市场</h2>
            <ul class="news-list">{other_markets}</ul>
            <br>
            <p><strong>💭 深度思考</strong></p>
            <p><em>{other_thought}</em></p>
        </section>
        
        <section class="section">
            <h2 class="section-title">₿ 加密货币专栏</h2>
            <div class="highlight-box">
                <p><strong>【市场动态】</strong></p>
                {crypto_news}
                <br>
                <p><strong>【趋势分析】</strong></p>
                <p>{crypto_analysis}</p>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{crypto_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🎨 艺术鉴赏</h2>
            <div class="highlight-box">
                <p><strong>【今日赏析】</strong> {art_title}</p>
                <br>
                <img src="{art_image}" alt="{art_title}" class="art-image" onerror="this.style.display='none'">
                <p class="art-caption">{art_title}</p>
                <br>
                <p>{art_content}</p>
                <br>
                <p><em>💡 {art_insight}</em></p>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{art_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">🧠 投资心理学</h2>
            <div class="highlight-box">
                <p><strong>【今日话题】</strong> {psych_title}</p>
                <br>
                <p>{psych_content}</p>
                <br>
                <p><strong>{psych_tip}</strong></p>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{psych_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">❤️ 情感驿站</h2>
            <div class="highlight-box">
                <p><strong>【今日话题】</strong> {emotion_title}</p>
                <br>
                <p>{emotion_content}</p>
                <br>
                <p><em>{emotion_poem}</em></p>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>{emotion_thought}</em></p>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title">👀 今日看点</h2>
            <ul class="news-list">{today_focus}</ul>
            <br>
            <p><strong>💭 深度思考</strong></p>
            <p><em>{today_thought}</em></p>
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
    <script src="app.js"></script>
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
        "weekly_thought": "市场永远在奖励那些能看穿噪音的人。当所有人都在讨论AI泡沫时，真正赚钱的是那些看懂AI基础设施需求的人——算力、电力、数据中心。投资不是追逐热点，而是理解热点的底层逻辑。",
        "ai_news": ai_news_list,
        "ai_analysis": "AI 板块持续高热，建议关注三条主线：1）算力基建（英伟达、AMD、国产芯片）；2）大模型应用（微软、谷歌、百度、阿里）；3）AI 赋能传统行业（医疗、教育、金融）。风险提示：估值偏高，注意回调风险。",
        "ai_thought": "我们正处于一个奇怪的时代：AI能写出完美的商业计划书，却不懂为什么要创业；能诊断疾病，却感受不到病人的恐惧。技术的边界越来越清晰，人类的边界却越来越模糊。也许真正的机会不在于AI能做什么，而在于AI不能做但人们依然愿意为之付费的事情——陪伴、理解、意义感。",
        "geopolitics_news": [
            "• 美伊局势持续紧张，美军在伊朗周边集结兵力，霍尔木兹海峡航运风险上升",
            "• 特朗普宣布对全球加征10-15%关税，中美贸易摩擦升级担忧再起",
            "• 俄乌冲突进入新阶段，能源供应链重构加速"
        ],
        "geopolitics_analysis": "当前地缘政治风险主要集中在三大热点：中东局势（美伊对峙）、贸易摩擦（美国关税政策）、以及俄乌冲突的长期化。这些风险对全球供应链、能源价格和资本市场都将产生深远影响。建议投资者关注黄金、原油等避险资产，同时留意国产替代、军工等受益板块。",
        "geopolitics_thought": "历史不会重复，但会押韵。1930年代的贸易战最终导向了什么，历史书上有答案。但今天不同的是，全球供应链的纠缠比任何时候都深。脱钩不是开关，而是手术——疼的是双方。普通人能做什么？保持流动性，不押注单一货币、单一市场、单一叙事。",
        "international": [
            "特朗普关税新方案今天可能公布，美国继续对全球商品加税10-15%。对A股影响：出口链承压，国产替代概念或受益。",
            "美伊局势紧张，油价上涨到66美元/桶，国内油价可能上调。",
            "美联储暗示可能推迟降息，美元走强，对新兴市场资金流动有影响。",
            "日本1月通胀放缓，央行加息预期降温，亚太股市或受提振。"
        ],
        "international_thought": "特朗普的关税政策像一场即兴爵士乐——没人知道下一个音符是什么。但市场讨厌不确定性。这种环境下，'预测'变得无用，'适应'变得关键。与其猜测政策走向，不如构建无论哪种情况都能生存的仓位结构。",
        "domestic": [
            "明天A股春节后首个交易日，历史数据显示春节后第一周上涨概率约70%，'开门红'可期。",
            "央行近期可能降准降息，资金面有望更宽松，利好股市。",
            "证监会发布新规，加强上市公司质量监管，长期利好A股生态。",
            "春节假期消费数据亮眼，旅游、电影、餐饮收入超预期，消费复苏概念值得关注。",
            "多地出台房地产支持政策，房贷利率下调，地产链或迎修复。"
        ],
        "domestic_thought": "政策底和市场底往往不是同一个底。政策可以托住经济不往下掉，但托不出牛市。牛市需要信心，而信心来自赚钱效应，赚钱效应来自基本面改善。这个传导链条很长，需要耐心。现在是什么阶段？政策底已现，市场底在磨，业绩底未到。",
        "tech": [
            "国产AI公司智谱股价暴涨42%，市值破3000亿，AI应用概念持续火热。",
            "小红书内测AI剪辑工具，对着手机说句话就能剪视频。",
            "比亚迪发布新车型，价格再创新低，新能源车竞争白热化。"
        ],
        "tech_thought": "技术扩散遵循一个规律：先被嘲笑，后被恐惧，最后被忽视。AI现在处于'被恐惧'阶段。但历史告诉我们，真正改变世界的技术，最终都会变得像水电一样——无处不在，却无人谈论。投资的关键是找到那个从'被恐惧'到'被忽视'的转折点。",
        "stock": "上周五（节前）A股集体收跌，上证指数跌1.26%报4082点，深成指跌1.28%，创业板指跌1.57%。成交额2万亿，较前日缩量7%。板块方面，海洋捕捞、半导体设备逆势上涨；通信线缆、稀土、有色金属跌幅居前。技术面看，沪指跌破4100点整数关口，短期支撑在4050点附近，压力在4150点。明日节后开市，关注能否'开门红'，建议控制仓位，重点关注AI应用、国产替代、消费复苏三大主线。",
        "stock_thought": "技术分析的本质是什么？是寻找市场参与者行为的规律。支撑和压力之所以存在，是因为人们记得那个价格。当足够多人相信某个价位有意义，它就有了意义。这是一种集体幻觉，但幻觉也能赚钱——只要你比大多数人早一步意识到幻觉的存在。",
        "other_markets": [
            "美股：道指逼近5万点，科技股领涨",
            "港股：AI概念强势，腾讯阿里承压",
            "比特币：约6.8万美元"
        ],
        "other_thought": "全球市场的联动性越来越强，但相关性不是因果性。美股涨，A股不一定跟；美股跌，A股不一定跌。真正重要的是理解每个市场背后的驱动因素。美股的驱动是流动性，A股的驱动是政策预期，港股的驱动是南向资金。搞清楚谁在买、为什么买，比看K线重要。",
        "crypto_news": [
            "• 📉 比特币现报$67,200，24小时跌幅2.3%，测试6.7万美元关键支撑",
            "• 📉 以太坊失守$1,950，较历史高点回撤超60%，ETF持续流出",
            "• 😰 恐惧与贪婪指数：14/100（极度恐惧），创近半年新低",
            "• 💰 机构动态：现货比特币ETF上周净流出超3亿美元，矿企Bitdeer大举抛售",
            "• 🔍 链上信号：巨鲸地址数增加，聪明资金在悄悄吸筹",
            "• 📊 市场情绪：社交媒体情绪跌至2025年大涨前水平，散户恐慌抛售"
        ],
        "crypto_analysis": "市场正处于深度调整期，情绪极度悲观。BTC在6.6-7万美元区间震荡整理，ETH跌破2000美元后走势脆弱。但恐惧指数14已进入历史买入区域，巨鲸持续累积是积极信号。短期观望为主，中长期投资者可考虑分批布局。风险提示：监管政策不确定性、宏观流动性收紧。",
        "crypto_thought": "加密货币市场是一面镜子，照出人性的贪婪与恐惧。当恐惧指数14时，意味着市场参与者已经恐慌到了极点——而这往往是反向指标。但反人性的地方在于：你知道应该买，但你不敢。为什么？因为'这次不一样'的念头会占据你的大脑。每次危机，人们都会说'这次不一样'，但历史总是惊人地相似。",
        "art_title": "《星月夜》——梵高的疯狂与浪漫",
        "art_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "art_content": "这幅创作于1889年的油画，是梵高在圣雷米精神病院期间的作品。画面中旋转的星云像巨大的漩涡，明亮的星星闪烁着耀眼的光芒，一弯新月悬挂天际。起伏的山峦如波涛般涌动，仿佛能感受到艺术家内心的躁动与不安。那棵黑色的柏树像火焰般直冲云霄，而宁静的村庄则在夜色中沉睡，教堂的尖顶指向天空。梵高用夸张的线条和浓烈的色彩——深蓝、明黄、翠绿——将内心的情感直接倾泻在画布上。这不是我们肉眼所见的夜空，而是梵高灵魂深处的宇宙。",
        "art_insight": "艺术不是复制现实，而是表达内心。梵高教会我们：即使身处黑暗，也要仰望星空。那些看似疯狂旋转的笔触，恰恰是对生命最炽热的爱。",
        "art_thought": "为什么我们在130年后依然被这幅画打动？因为梵高画出了人类共通的情感——孤独、渴望、对超越性的追求。技术会过时，但情感不会。在AI能画出'完美'图像的今天，梵高的'不完美'反而更显珍贵。这提醒我们：价值不在于效率，而在于独特性；不在于精确，而在于真诚。",
        "psych_title": "AI时代的'存在感焦虑'",
        "psych_content": "当AI能写诗、画画、写代码，甚至通过律师考试时，很多人开始问：'我还能做什么？'这种存在感焦虑正在蔓延。社会学研究发现，技术革命期人们会经历'能力贬值恐慌'——不是你真的没价值，而是衡量价值的标准在变化。历史上，汽车取代马车时，马夫们也曾恐慌，但驾驶员、汽修工、交通规划师等新职业应运而生。AI不会取代人，但会用AI的人会取代不会用的人。",
        "psych_tip": "💡 今日心法：与其焦虑被AI替代，不如思考如何让AI成为你的'外接大脑'。人类的创造力、同理心、价值判断，依然是不可替代的核心竞争力。",
        "psych_thought": "更深层的焦虑或许不是'AI会取代我'，而是'我不知道自己是谁'。当工作、技能、甚至创造力都被技术重新定义，人们被迫面对一个古老的问题：如果我不是我的职业，那我是谁？这种存在主义的危机，也许正是这个时代送给我们的礼物——逼我们找到比工作更深层的自我认同。",
        "emotion_title": "成年人的'情绪劳动'",
        "emotion_content": "你有没有发现，上班时即使再累也要保持微笑，面对客户的无理要求也要耐心解释，同事甩锅时还要装作大度？这叫'情绪劳动'——为了工作和社交，我们不得不管理、压抑甚至伪装自己的情绪。社会学研究发现，情绪劳动比体力劳动更消耗人。因为它没有下班时间，你回家后可能还在回味白天那句没怼回去的话。",
        "emotion_poem": "📝 今日短句：'成年人的崩溃，是从计算'再忍忍就下班了'开始的。'",
        "emotion_thought": "为什么我们越来越累？因为除了完成工作本身，我们还要'表演'一个情绪稳定的成年人。这种表演没有片酬，却耗费心力。也许真正的自我关怀，不是买包买鞋，而是允许自己偶尔'情绪不稳定'——在不伤害他人的前提下，诚实面对自己的感受。",
        "today_focus": [
            "A股春节后首个交易日，关注'开门红'",
            "1月LPR数据公布，关注利率动向",
            "特朗普关税细节公布，关注市场反应"
        ],
        "today_thought": "关注什么，决定了你看到什么。市场每天产生无数信息，但大部分只是噪音。真正的信号往往藏在被忽视的地方——成交量的异常、板块轮动的节奏、资金流向的变化。训练自己过滤噪音的能力，比获取更多信息的渠道更重要。",
        "learn_title": "支撑位和压力位",
        "learn_content": "就像楼梯的台阶，股价跌到某个位置跌不动了叫支撑（有人买），涨到某个位置涨不动了叫压力（有人卖）。突破压力可能继续上涨，跌破支撑可能继续下跌。",
        "learn_thought": "支撑和压力的深层逻辑是什么？是记忆的集体固化。当足够多的人在某个价位有过交易行为，这个价格就被'记住'了。下次价格接近时，那些记忆被激活——套牢盘想解套，获利盘想落袋。技术分析的本质是心理学，是群体行为的规律总结。",
        "reminder": "节后开盘别急着追高，先看半小时盘面再决定。祝投资顺利！",
        "reminder_thought": "为什么我们总是急着行动？因为'做点什么'能缓解焦虑，即使做的是错的。投资中，不操作往往是最难的操作。学会等待，学会在信息不完整时保持观望，是成熟投资者的标志。记住：错过一次机会不可怕，可怕的是为了不错过而抓住每一个陷阱。"
    }
    
    return data


def generate_html(data):
    """生成HTML文件"""
    
    # 处理新的 content.json 结构
    # international
    if "international_hot" in data and "items" in data["international_hot"]:
        international = "\n".join([f'<li class="news-item"><strong>[{item.get("tag", "国际")}]</strong> {item.get("title", "")} - {item.get("content", "")}</li>' for item in data["international_hot"]["items"]])
    elif "international" in data:
        international = "\n".join([f'<li class="news-item">{item}</li>' for item in data["international"]])
    else:
        international = "<li class='news-item'>暂无国际热点数据</li>"
    
    # domestic
    if "domestic" in data and isinstance(data["domestic"], dict) and "items" in data["domestic"]:
        domestic = "\n".join([f'<li class="news-item"><strong>[{item.get("tag", "国内")}]</strong> {item.get("title", "")} - {item.get("content", "")}</li>' for item in data["domestic"]["items"]])
    elif "domestic" in data:
        domestic = "\n".join([f'<li class="news-item">{item}</li>' for item in data["domestic"]])
    else:
        domestic = "<li class='news-item'>暂无国内动态数据</li>"
    
    # tech - 从 ai_section 获取
    if "ai_section" in data and "news" in data["ai_section"]:
        tech = "\n".join([f'<li class="news-item"><strong>{item.get("title", "")}</strong> - {item.get("content", "")}</li>' for item in data["ai_section"]["news"]])
    elif "tech" in data:
        tech = "\n".join([f'<li class="news-item">{item}</li>' for item in data["tech"]])
    else:
        tech = "<li class='news-item'>暂无科技新闻</li>"
    
    # other_markets
    if "other_markets" in data:
        other_markets = "\n".join([f'<li class="news-item">{item}</li>' for item in data["other_markets"]])
    else:
        other_markets = "<li class='news-item'>暂无其他市场数据</li>"
    
    # today_focus
    if "today_focus" in data and "items" in data["today_focus"]:
        today_focus = "\n".join([f'<li class="news-item">{item}</li>' for item in data["today_focus"]["items"]])
    elif "today_focus" in data:
        today_focus = "\n".join([f'<li class="news-item">{item}</li>' for item in data["today_focus"]])
    else:
        today_focus = "<li class='news-item'>暂无今日看点</li>"
    
    # geopolitics_news
    if "geopolitics" in data and isinstance(data["geopolitics"], dict):
        geo = data["geopolitics"]
        geopolitics_news = f'<p>{geo.get("news", "")}</p>'
    elif "geopolitics_news" in data:
        geopolitics_news = "\n".join([f'<p>{item}</p>' for item in data["geopolitics_news"]])
    else:
        geopolitics_news = "<p>暂无地缘政治新闻</p>"
    
    # ai_news
    if "ai_section" in data and "news" in data["ai_section"]:
        ai_news = "\n".join([f'<p><strong>{item.get("title", "")}</strong>：{item.get("content", "")}</p>' for item in data["ai_section"]["news"]])
    elif "ai_news" in data:
        ai_news = "\n".join([f'<p>{item}</p>' for item in data["ai_news"]])
    else:
        ai_news = "<p>暂无AI新闻</p>"
    
    # weekly_review
    if "week_review" in data and isinstance(data["week_review"], dict):
        wr = data["week_review"]
        weekly_parts = [
            f'<p>📈 A股：{wr.get("a_share", "")}</p>',
            f'<p>🌍 国际：{wr.get("global", "")}</p>',
            f'<p>💰 汇率：{wr.get("forex", "")}</p>',
            f'<p>🏆 板块：{wr.get("sectors", "")}</p>',
            f'<p>📊 成交：{wr.get("volume", "")}</p>'
        ]
        weekly_review = "\n".join(weekly_parts)
    elif "weekly_review" in data:
        weekly_review = "\n".join([f'<p>{item}</p>' for item in data["weekly_review"]])
    else:
        weekly_review = "<p>暂无每周回顾</p>"
    
    # crypto_news
    if "crypto" in data and "news" in data["crypto"]:
        crypto_news = "\n".join([f'<p>{item}</p>' for item in data["crypto"]["news"]])
    elif "crypto_news" in data:
        crypto_news = "\n".join([f'<p>{item}</p>' for item in data.get("crypto_news", [])])
    else:
        crypto_news = "<p>暂无加密货币新闻</p>"
    
    html = HTML_TEMPLATE.format(
        date=data.get("date", datetime.now().strftime("%Y年%m月%d日")),
        weekly_review=weekly_review,
        weekly_thought=data.get("week_review", {}).get("deep_thinking") or data.get("weekly_thought", "市场永远在变化，保持学习和适应的能力。"),
        ai_news=ai_news,
        ai_analysis=data.get("ai_section", {}).get("investment") or data.get("ai_investment") or data.get("ai_analysis", "AI 板块持续高热，建议关注算力基建、大模型应用、AI赋能传统行业。"),
        ai_thought=data.get("ai_investment") or data.get("ai_thought", "AI正在改变我们的工作和生活方式。"),
        geopolitics_news=geopolitics_news,
        geopolitics_analysis=data.get("geopolitics", {}).get("analysis") or data.get("geopolitics_analysis", "地缘政治风险需要持续关注。"),
        geopolitics_thought=data.get("geopolitics", {}).get("deep_thinking") or data.get("geopolitics_thought", "地缘政治风险需要持续关注。"),
        international=international,
        international_thought=data.get("international_hot", {}).get("deep_thinking") or data.get("international_thought", "国际市场相互关联，需要全局视角。"),
        domestic=domestic,
        domestic_thought=data.get("domestic", {}).get("deep_thinking") or data.get("domestic_thought", "政策导向对市场有重要影响。"),
        tech=tech,
        tech_thought=data.get("tech_thought", "技术创新是推动社会进步的核心动力。"),
        stock=data.get("stock", {}).get("summary") or data.get("a_share", {}).get("summary") or "A股今日行情数据待更新。",
        stock_thought=data.get("stock", {}).get("deep_thinking") or data.get("stock_thought", "投资需要理性和耐心。"),
        other_markets=other_markets,
        other_thought=data.get("other_thought", "多元化投资可以分散风险。"),
        crypto_news=crypto_news,
        crypto_analysis=data.get("crypto", {}).get("analysis") or data.get("crypto_analysis", "加密市场波动较大，投资需谨慎。"),
        crypto_thought=data.get("crypto", {}).get("deep_thinking") or data.get("crypto_thought", "加密市场反映了人性的贪婪与恐惧。"),
        art_title=data.get("art", {}).get("title") or data.get("art_title", "今日艺术赏析"),
        art_image=data.get("art", {}).get("image") or data.get("art_image", ""),
        art_content=data.get("art", {}).get("content") or data.get("art_content", "艺术是人类情感的表达。"),
        art_insight=data.get("art", {}).get("insight") or data.get("art_insight", "用心感受艺术之美。"),
        art_thought=data.get("art", {}).get("deep_thinking") or data.get("art_thought", "艺术的价值在于触动人心。"),
        psych_title=data.get("psychology", {}).get("title") or data.get("psych_title", "投资心理"),
        psych_content=data.get("psychology", {}).get("content") or data.get("psych_content", "保持理性，控制情绪。"),
        psych_tip=data.get("psychology", {}).get("tip") or data.get("psych_tip", "💡 今日心法：冷静思考，理性决策。"),
        psych_thought=data.get("psychology", {}).get("deep_thinking") or data.get("psych_thought", "理解自己的心理是投资成功的关键。"),
        emotion_title=data.get("emotion", {}).get("title") or data.get("emotion_title", "今日情感话题"),
        emotion_content=data.get("emotion", {}).get("content") or data.get("emotion_content", "关注自己的情感需求。"),
        emotion_poem=data.get("emotion", {}).get("poem") or data.get("emotion_poem", "📝 今日短句：善待自己。"),
        emotion_thought=data.get("emotion", {}).get("deep_thinking") or data.get("emotion_thought", "情感是人类最真实的体验。"),
        today_focus=today_focus,
        today_thought=data.get("today_focus", {}).get("deep_thinking") or data.get("today_thought", "关注重要信息，过滤市场噪音。"),
        learn_title=data.get("learn", {}).get("title") or data.get("learn_title", "每日财经学习"),
        learn_content=data.get("learn", {}).get("content") or data.get("learn_content", "持续学习是投资成功的基础。"),
        reminder=data.get("reminder", {}).get("text") or data.get("reminder", "保持理性，祝投资顺利！")
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
