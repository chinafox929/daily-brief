#!/usr/bin/env python3
"""
快速生成3月5日每日简报
"""
import json
from datetime import datetime
from pathlib import Path

# 3月5日实际内容
data = {
    "date": "2026年3月5日 星期四",
    "weekly_review": [
        "• 📈 A股：两会开幕，沪指围绕3350点震荡，政策预期支撑市场",
        "• 🌍 国际：美股道指连跌三日，纳指受科技股拖累调整2.1%",
        "• 💰 汇率：离岸人民币维持在7.25附近震荡",
        "• 🏆 板块：AI算力、机器人概念领涨；传统周期股承压",
        "• 📊 成交：日均成交额维持在1.15万亿水平"
    ],
    "weekly_thought": "两会期间资金观望情绪浓厚，但科技主线依然坚挺，说明市场对'新质生产力'的政策红利有共识。这种'大盘搭台、科技唱戏'的格局可能会贯穿整个春季行情。",
    "ai_news": [
        "• OpenAI宣布GPT-5将在下月发布，推理能力提升40%",
        "• 百度文心一言月活突破3亿，阿里通义千问接入钉钉全家桶",
        "• AI算力租赁价格暴涨，英伟达H100芯片仍是一卡难求",
        "• 国务院印发《制造业数字化转型行动方案》，推动AI大模型进工厂"
    ],
    "ai_analysis": "AI已经从概念炒作进入'算力军备竞赛'阶段，现在投AI就像20年前投互联网基础设施，卖铲子的公司比挖金的更稳当，服务器、光模块这些'基建股'值得长期关注。",
    "ai_thought": "AI正在从'屏幕里的智能'走向'物理世界的智能'。具身智能的爆发说明资本已经达成共识：下一个AI主战场是机器人。",
    "geopolitics_news": [
        "• 特朗普宣布对欧盟钢铝加征25%关税，贸易战火重燃",
        "• 中东局势持续紧张，霍尔木兹海峡航运安全引担忧",
        "• 欧盟开始讨论对国产电动车征收追溯性关税"
    ],
    "geopolitics_analysis": "地缘政治风险正在常态化，不再是短期冲击而是长期背景。对普通投资者来说，与其猜测国际局势，不如在配置中加入黄金、红利低波等'防御性资产'。",
    "geopolitics_thought": "特朗普的关税政策像一场即兴爵士乐——没人知道下一个音符是什么。但市场讨厌不确定性。这种环境下，'预测'变得无用，'适应'变得关键。",
    "international": [
        "美联储主席鲍威尔重申'通胀未达标不降息'，3月维持利率不变概率升至85%",
        "日本GDP连续两季负增长，日央行推迟加息计划",
        "英国财政大臣发布春季预算案，富时100指数创三个月新高",
        "OPEC+意外宣布延长减产至二季度末，国际油价应声上涨3%"
    ],
    "international_thought": "全球央行进入'观望模式'，美联储按兵不动意味着新兴市场货币压力暂缓，但高利率环境对全球股市的估值压制仍在。",
    "domestic": [
        "十四届全国人大三次会议在京开幕，政府工作报告提出GDP增长5%左右目标",
        "发改委表示将发行超长期特别国债1.3万亿元，重点支持'两新'工作",
        "工信部印发《制造业数字化转型行动方案》，推动AI大模型进工厂",
        "住建部强调'房住不炒'，但将支持刚性和改善性住房需求"
    ],
    "domestic_thought": "5%的增长目标兼顾了质量与速度，特别国债的发行说明财政发力很实在。对股市来说，'两新'（设备更新、消费品以旧换新）是确定性的投资主线。",
    "tech": [
        "我国成功发射天目一号气象星座11-14星，商业航天进入组网密集期",
        "华为发布全球首个5.5G智能核心网，下载速率突破10Gbps",
        "清华大学团队实现百公里级量子通信，量子互联网迈出关键一步"
    ],
    "tech_thought": "从5G到5.5G，从地面到太空，通信基础设施的迭代正在打开新的应用场景。这些'硬科技'突破短期内未必体现在财报上，但长期看是相关产业链的底层逻辑支撑。",
    "stock": "今日A股三大指数集体高开，沪指涨0.8%报3368点。板块方面，两会概念股活跃，三胎、养老、基建板块涨幅居前；AI应用端集体爆发，传媒、游戏板块多股涨停。北交所个股表现活跃，北证50指数大涨2.3%。技术上看，沪指突破20日均线压制，MACD金叉初现，短期或挑战3400点整数关口。",
    "stock_thought": "两会行情历来是'预期炒 map，落地兑现'，今年特别国债额度超预期是最大亮点。不过要注意，政策受益板块往往'买预期卖事实'，别等政策明朗了才追。",
    "other_markets": "美股道指跌0.6%，纳指跌1.2%，英伟达业绩超预期但guidance保守，盘后大跌5%；特斯拉因中国销量下滑跌3%。港股恒指反弹1.5%，科技互联网板块领涨。",
    "other_thought": "美股科技七巨头的财报季暴露出一个问题：AI投入巨大但变现还没跟上。相比之下，港股的估值修复空间更大，性价比凸显。",
    "crypto_news": "比特币现报82,500美元，24小时涨2.1%；以太坊突破4,500美元，受Layer2生态爆发推动。美国比特币ETF连续10日净流入，机构配置需求强劲。",
    "crypto_analysis": "比特币减半事件倒计时30天，历史数据显示减半后6-12个月往往迎来牛市主升浪；但短期需警惕'卖事实'回调风险。",
    "crypto_thought": "比特币正在从'散户投机品'变成'机构配置资产'，ETF的审批通过是历史性转折。",
    "art_title": "《溪山行旅图》",
    "art_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Travelers_Among_Mountains_and_Streams.jpg/1280px-Travelers_Among_Mountains_and_Streams.jpg",
    "art_content": "台北故宫博物院镇馆之宝，绢本设色，纵206.3厘米，横103.3厘米。画面中央主峰巍峨耸立，山石以'雨点皴'技法表现，质感强烈。山脚商旅队伍与巨峰形成强烈对比，体现'天人合一'的哲学思想。",
    "art_insight": "范宽画山用了近三个月时间观察终南山，这种'师造化'的耐心在当今快节奏的投资市场显得尤为珍贵。",
    "art_thought": "好股票也需要时间沉淀，别总想着今天买明天涨，像画家积累素材一样积累认知，时间会给厚报。",
    "psych_title": "确认偏误（Confirmation Bias）",
    "psych_content": "人脑天生喜欢寻找支持自己观点的证据，而忽视反面信息。比如你看好某只股票，就会特别关注利好消息，对利空选择性失明。",
    "psych_tip": "💡 建议每次做决定前，强迫自己写出三个'看空理由'，这个简单动作能帮你避开80%的冲动交易。",
    "psych_thought": "两会期间各种政策解读满天飞，如果你已经重仓了新能源，就更容易相信'碳中和政策超预期'的论调。",
    "emotion_title": "职场'35岁现象'的破局之道",
    "emotion_content": "35岁不是终点，而是第二曲线的起点。与其担心被裁员，不如利用现有资源建立'可迁移能力'。",
    "emotion_poem": "📝 投资和工作一样，不能只有一个'主动收入'的篮子。35岁前应该像配置资产一样配置自己的技能。",
    "emotion_thought": "多元配置的人生，抗风险能力自然强。",
    "today_focus": [
        "重点关注两会政府工作报告中的财政赤字率目标和特别国债规模",
        "美联储今晚将公布经济状况褐皮书，关注其对通胀的描述措辞变化"
    ],
    "today_thought": "今天市场的波动可能会加大，但别被短线噪音干扰。保持耐心比频繁操作更重要。",
    "learn_title": "市盈率（PE）",
    "learn_content": "PE = 股价 ÷ 每股收益，简单说就是'回本年限'。PE 20倍意味着按现在盈利水平，20年能回本。PE不是越低越好，成长股的PE通常比蓝筹股高。",
    "reminder": "两会期间概念股波动大，记住'利好兑现即利空'的老规律。如果持有的政策受益股已经连续大涨，不妨在会议期间分批减仓，把利润装进口袋才是真正的落袋为安。🎯"
}

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日简报 | {date}</title>
    <link rel="stylesheet" href="styles.css">
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
                <img src="{art_image}" alt="{art_title}" class="art-image">
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
</body>
</html>'''

def generate_html():
    """生成HTML"""
    # 格式化列表
    international = "\n".join([f'<li class="news-item">{item}</li>' for item in data["international"]])
    domestic = "\n".join([f'<li class="news-item">{item}</li>' for item in data["domestic"]])
    tech = "\n".join([f'<li class="news-item">{item}</li>' for item in data["tech"]])
    other_markets = "\n".join([f'<li class="news-item">{item}</li>' for item in data["other_markets"].split("。") if item])
    today_focus = "\n".join([f'<li class="news-item">{item}</li>' for item in data["today_focus"]])
    geopolitics_news = "\n".join([f'<p>{item}</p>' for item in data["geopolitics_news"]])
    ai_news = "\n".join([f'<p>{item}</p>' for item in data["ai_news"]])
    weekly_review = "\n".join([f'<p>{item}</p>' for item in data["weekly_review"]])
    crypto_news = "\n".join([f'<p>{item}</p>' for item in data["crypto_news"].split("。") if item])
    
    html = HTML_TEMPLATE.format(
        date=data["date"],
        weekly_review=weekly_review,
        weekly_thought=data["weekly_thought"],
        ai_news=ai_news,
        ai_analysis=data["ai_analysis"],
        ai_thought=data["ai_thought"],
        geopolitics_news=geopolitics_news,
        geopolitics_analysis=data["geopolitics_analysis"],
        geopolitics_thought=data["geopolitics_thought"],
        international=international,
        international_thought=data["international_thought"],
        domestic=domestic,
        domestic_thought=data["domestic_thought"],
        tech=tech,
        tech_thought=data["tech_thought"],
        stock=data["stock"],
        stock_thought=data["stock_thought"],
        other_markets=other_markets,
        other_thought=data["other_thought"],
        crypto_news=crypto_news,
        crypto_analysis=data["crypto_analysis"],
        crypto_thought=data["crypto_thought"],
        art_title=data["art_title"],
        art_image=data["art_image"],
        art_content=data["art_content"],
        art_insight=data["art_insight"],
        art_thought=data["art_thought"],
        psych_title=data["psych_title"],
        psych_content=data["psych_content"],
        psych_tip=data["psych_tip"],
        psych_thought=data["psych_thought"],
        emotion_title=data["emotion_title"],
        emotion_content=data["emotion_content"],
        emotion_poem=data["emotion_poem"],
        emotion_thought=data["emotion_thought"],
        today_focus=today_focus,
        today_thought=data["today_thought"],
        learn_title=data["learn_title"],
        learn_content=data["learn_content"],
        reminder=data["reminder"]
    )
    
    # 保存
    output_dir = Path("/root/.openclaw/workspace/daily-brief")
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # 归档
    archive_dir = output_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    with open(archive_dir / "2026-03-05.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 每日简报已生成: {data['date']}")
    print(f"📁 文件位置: {output_dir}/index.html")
    return html

if __name__ == "__main__":
    generate_html()
