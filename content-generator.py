#!/usr/bin/env python3
"""
每日简报内容生成器
每天早上8点自动更新所有板块内容
"""

from datetime import datetime, timedelta
import random
import json
from pathlib import Path

# 配置
HTML_FILE = Path("/root/.openclaw/workspace/daily-brief/index.html")

# ===== 艺术鉴赏数据 =====
ARTWORKS = [
    {
        "title": "《星月夜》——梵高的疯狂与浪漫",
        "artist": "文森特·梵高 (Vincent van Gogh)",
        "year": "1889",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "desc": "这幅创作于1889年的油画，是梵高在圣雷米精神病院期间的作品。画面中旋转的星云像巨大的漩涡，明亮的星星闪烁着耀眼的光芒。",
        "thought": "为什么我们在130年后依然被这幅画打动？因为梵高画出了人类共通的情感——孤独、渴望、对超越性的追求。技术会过时，但情感不会。"
    },
    {
        "title": "《睡莲》——莫奈的光影诗篇",
        "artist": "克劳德·莫奈 (Claude Monet)",
        "year": "1906",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Claude_Monet_-_Water_Lilies_-_1906%2C_Ryerson.jpg",
        "desc": "莫奈晚年在吉维尼花园创作的《睡莲》系列，捕捉了水面光影的瞬间变化。没有轮廓线，只有色彩在流动。",
        "thought": "莫奈教会我们：美不在于细节的精确，而在于瞬间的感受。在AI能画出'完美'图像的今天，这种'不完美'反而更显珍贵。"
    },
    {
        "title": "《格尔尼卡》——毕加索的反战呐喊",
        "artist": "巴勃罗·毕加索 (Pablo Picasso)",
        "year": "1937",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Mural_del_Gernika.jpg",
        "desc": "这幅巨作描绘了纳粹轰炸西班牙小镇格尔尼卡的惨状。扭曲的人体、嘶鸣的马匹、哭泣的母亲——立体主义成为控诉战争的武器。",
        "thought": "艺术的力量不在于美，而在于真实。当世界选择遗忘，一幅画可以记住一切。"
    }
]

# ===== 投资心理学数据 =====
PSYCHOLOGY_TOPICS = [
    {
        "title": "FOMO：错失恐惧症的陷阱",
        "content": "看到别人赚钱就忍不住跟进，结果买在高点。FOMO让你追涨杀跌，成为市场的'接盘侠'。",
        "solution": "建立自己的投资系统，不随大流。别人的机会不一定是你的机会。",
        "thought": "市场永远在制造FOMO。从2015年的创业板到2021年的白酒，再到今天的AI，每一轮牛市都有人说'这次不一样'。但历史告诉我们，树不会长到天上去。"
    },
    {
        "title": "损失厌恶：亏损的痛苦是盈利快乐的2倍",
        "content": "行为经济学发现，人类对损失的痛苦是获得同等收益快乐的约2倍。这就是为什么股票涨了舍不得卖，跌了更舍不得卖。",
        "solution": "设定明确的止损点和止盈点，让规则代替情绪。",
        "thought": "损失厌恶是进化留给我们的遗产——在原始社会，失去一天的粮食可能意味着死亡。但在投资市场，它让我们无法理性面对波动。"
    },
    {
        "title": "锚定效应：被第一印象绑架的决策",
        "content": "买入价格成为你的'锚'。跌到这个价格以下就觉得便宜，涨到这个价格以上就觉得贵——不管实际价值如何。",
        "solution": "每次决策前重新评估基本面，不要被成本价影响判断。",
        "thought": "锚定效应告诉我们：过去的投入是沉没成本，不应该影响未来的决策。但知易行难，这就是为什么'割肉'如此痛苦。"
    }
]

# ===== 情感驿站数据 =====
EMOTION_TOPICS = [
    {
        "title": "成年人的'情绪劳动'",
        "content": "上班时即使再累也要保持微笑，面对客户的无理要求也要耐心解释。这叫'情绪劳动'——为了工作，我们不得不伪装自己的情绪。",
        "quote": "成年人的崩溃，是从计算'再忍忍就下班了'开始的。",
        "thought": "为什么我们越来越累？因为除了完成工作本身，我们还要'表演'一个情绪稳定的成年人。这种表演没有片酬，却耗费心力。"
    },
    {
        "title": "周末焦虑：休息也停不下来",
        "content": "周六早上醒来第一件事是看美股收盘，周日晚上开始担心周一行情。周末不是用来休息的，是用来'准备下一周战斗'的。",
        "quote": "真正的休息不是身体的静止，而是大脑的放空。",
        "thought": "投资成了生活的全部，这是危险的信号。市场永远在那里，但生活只有一次。当你发现自己无法享受周末，也许是时候调整仓位了。"
    },
    {
        "title": "对比的痛苦：为什么别人总是赚得比我多",
        "content": "群里有人晒收益率，你就开始怀疑自己。社交媒体上全是'年化50%'的高手，只有你在亏钱。",
        "quote": "投资是一场与自己的比赛，不是与他人的比较。",
        "thought": "幸存者偏差让我们只看到赢家。那些爆仓的人不会发帖，那些亏光的人已经退群。你看到的'人均股神'，其实是精心筛选后的幻觉。"
    }
]

# ===== 财经学习数据 =====
FINANCE_TOPICS = [
    {
        "title": "PE（市盈率）：股票的'性价比'",
        "content": "PE = 股价 ÷ 每股收益。简单来说，就是你多少年能靠公司盈利回本。PE越高，说明市场对公司未来越乐观，但也可能被高估。",
        "example": "茅台PE 30倍 vs 银行PE 5倍，不代表茅台贵、银行便宜。不同行业合理PE区间不同。",
        "thought": "PE只是一个工具，不是真理。低PE可能是价值陷阱，高PE可能是成长溢价。关键不是数字本身，而是理解数字背后的故事。"
    },
    {
        "title": "复利：时间的朋友",
        "content": "复利被称为'世界第八大奇迹'。年化15%收益，10年变成4倍，20年变成16倍。时间是复利最好的朋友。",
        "example": "巴菲特99%的财富是50岁后赚的。不是因为他50岁前不努力，而是因为复利需要时间。",
        "thought": "复利的反人性在于：前几年几乎看不到效果。大多数人在这个阶段放弃，错过了后面的爆发。耐心，是复利最珍贵的输入。"
    },
    {
        "title": "支撑位与压力位",
        "content": "就像楼梯的台阶，股价跌到某个位置跌不动了叫支撑（有人买），涨到某个位置涨不动了叫压力（有人卖）。",
        "example": "突破压力可能继续上涨，跌破支撑可能继续下跌。但注意：这些只是概率，不是确定性。",
        "thought": "技术分析的本质是什么？是寻找市场参与者行为的规律。支撑和压力之所以存在，是因为人们记得那个价格。这是一种集体幻觉，但幻觉也能赚钱。"
    }
]

# ===== 今日看点生成 =====
def generate_today_watch():
    """根据真实日期生成今日看点"""
    today = datetime.now()
    weekday = today.weekday()  # 0=周一
    
    if weekday == 0:  # 周一
        return [
            "周末消息面汇总，关注'开门红'概率",
            "本周重磅财经事件预览",
            "全球市场联动性观察"
        ]
    elif weekday == 4:  # 周五
        return [
            "周末持仓还是持币？",
            "本周涨跌幅回顾",
            "下周重要事件预告"
        ]
    else:
        return [
            "当日热点板块资金流向",
            "北向资金实时动向",
            "重要个股龙虎榜数据"
        ]

def get_daily_content():
    """获取每日轮换内容"""
    day_of_year = datetime.now().timetuple().tm_yday
    
    # 根据一年中的第几天选择内容，确保每天不同
    art = ARTWORKS[day_of_year % len(ARTWORKS)]
    psycho = PSYCHOLOGY_TOPICS[day_of_year % len(PSYCHOLOGY_TOPICS)]
    emotion = EMOTION_TOPICS[day_of_year % len(EMOTION_TOPICS)]
    finance = FINANCE_TOPICS[day_of_year % len(FINANCE_TOPICS)]
    watch = generate_today_watch()
    
    return {
        "art": art,
        "psycho": psycho,
        "emotion": emotion,
        "finance": finance,
        "watch": watch,
        "date": datetime.now().strftime("%Y年%m月%d日")
    }

def generate_html_sections(content):
    """生成HTML板块内容"""
    
    # 06 艺术鉴赏
    art_section = f'''
        <!-- 06 🎨 艺术鉴赏 -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">06</span>
                <h2 class="section-title">🎨 艺术鉴赏</h2>
            </div>
            
            <div class="card">
                <div class="highlight-box">
                    <p><strong>【今日赏析】</strong> {content['art']['title']}</p>
                    <br>
                    <img src="{content['art']['image']}" alt="{content['art']['title']}" class="art-image" onerror="this.style.display='none'">
                    <p class="art-caption">{content['art']['title']} · {content['art']['artist']} · {content['art']['year']}</p>
                    <br>
                    <p>{content['art']['desc']}</p>
                    <br>
                    <p><em>💡 {content['art']['thought']}</em></p>
                </div>
            </div>
        </section>'''
    
    # 07 投资心理学
    psycho_section = f'''
        <!-- 07 🧠 投资心理学 -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">07</span>
                <h2 class="section-title">🧠 投资心理学</h2>
            </div>
            
            <div class="card">
                <div class="highlight-box">
                    <p><strong>【今日话题】</strong> {content['psycho']['title']}</p>
                    <br>
                    <p>{content['psycho']['content']}</p>
                    <br>
                    <p><strong>💡 应对心法：</strong> {content['psycho']['solution']}</p>
                    <br>
                    <p><strong>💭 深度思考</strong></p>
                    <p><em>{content['psycho']['thought']}</em></p>
                </div>
            </div>
        </section>'''
    
    # 08 情感驿站
    emotion_section = f'''
        <!-- 08 ❤️ 情感驿站 -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">08</span>
                <h2 class="section-title">❤️ 情感驿站</h2>
            </div>
            
            <div class="card">
                <div class="highlight-box">
                    <p><strong>【今日话题】</strong> {content['emotion']['title']}</p>
                    <br>
                    <p>{content['emotion']['content']}</p>
                    <br>
                    <p><em>📝 {content['emotion']['quote']}</em></p>
                    <br>
                    <p><strong>💭 深度思考</strong></p>
                    <p><em>{content['emotion']['thought']}</em></p>
                </div>
            </div>
        </section>'''
    
    # 09 今日看点
    watch_items = '\n'.join([f'<li class="news-item">{item}</li>' for item in content['watch']])
    watch_section = f'''
        <!-- 09 👀 今日看点 -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">09</span>
                <h2 class="section-title">👀 今日看点</h2>
            </div>
            
            <div class="card">
                <ul class="news-list">
                    {watch_items}
                </ul>
                <br>
                <p><strong>💭 深度思考</strong></p>
                <p><em>关注什么，决定了你看到什么。市场每天产生无数信息，但大部分只是噪音。真正的信号往往藏在被忽视的地方——成交量的异常、板块轮动的节奏、资金流向的变化。训练自己过滤噪音的能力，比获取更多信息的渠道更重要。</em></p>
            </div>
        </section>'''
    
    # 10 每日财经学习
    learn_section = f'''
        <!-- 10 📚 每日财经学习 -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">10</span>
                <h2 class="section-title">📚 每日财经学习</h2>
            </div>
            
            <div class="card">
                <div class="learn-box">
                    <div class="learn-title">{content['finance']['title']}</div>
                    <p>{content['finance']['content']}</p>
                    <br>
                    <p><strong>举例说明：</strong> {content['finance']['example']}</p>
                    <br>
                    <p><strong>💭 深度思考</strong></p>
                    <p><em>{content['finance']['thought']}</em></p>
                </div>
            </div>
        </section>'''
    
    return art_section + psycho_section + emotion_section + watch_section + learn_section

def update_index_html():
    """更新index.html文件"""
    
    # 读取当前HTML
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 获取今日内容
    content = get_daily_content()
    
    # 生成新板块
    new_sections = generate_html_sections(content)
    
    # 找到Footer位置并插入
    footer_pos = html.find('<!-- Footer -->')
    if footer_pos == -1:
        footer_pos = html.find('<footer class="footer">')
    
    if footer_pos == -1:
        print("错误：找不到Footer位置")
        return False
    
    # 插入新内容
    new_html = html[:footer_pos] + new_sections + '\n        ' + html[footer_pos:]
    
    # 保存
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ 已更新 {HTML_FILE}")
    print(f"📅 日期: {content['date']}")
    print(f"🎨 艺术: {content['art']['title']}")
    print(f"🧠 心理: {content['psycho']['title']}")
    print(f"❤️ 情感: {content['emotion']['title']}")
    print(f"📚 财经: {content['finance']['title']}")
    
    return True

if __name__ == "__main__":
    update_index_html()
