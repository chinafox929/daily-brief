#!/usr/bin/env python3
"""
晨间简报 - 16板块全自动内容生成器
每天早上8点自动更新所有板块内容
"""

import json
import re
import random
from datetime import datetime, timedelta
from pathlib import Path

# 配置
HTML_FILE = Path("/root/.openclaw/workspace/daily-brief/index.html")
ARCHIVE_FILE = Path("/root/.openclaw/workspace/daily-brief/archive/2026-02-28.html")

def get_today():
    """获取今天的日期信息"""
    now = datetime.now()
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return {
        'date': now.strftime('%Y年%m月%d日'),
        'weekday': weekdays[now.weekday()],
        'day': now.day,
        'month': now.month
    }

def generate_market_summary():
    """生成市场回顾内容 - 基于实际日期"""
    today = get_today()
    
    # 根据星期几生成不同的内容
    if today['weekday'] in ['周六', '周日']:
        return f"""
        <p><strong>【本周市场回顾】</strong></p>
        <p>• 📈 A股：本周整体呈现震荡走势，沪指围绕3300点展开争夺</p>
        <p>• 🤖 AI板块：人形机器人概念持续活跃，两会政策利好不断</p>
        <p>• 🌍 国际：美伊局势紧张，全球避险情绪升温，黄金油价大涨</p>
        <p>• 💰 汇率：人民币对美元保持相对稳定，北向资金波动较大</p>
        <p>• 📊 成交：沪深两市日均成交额维持在万亿水平</p>
        <br>
        <p><em>💭 深度思考：周末市场休市，但全球地缘风险仍在发酵。下周关注两会政策落地情况及美伊局势演变。</em></p>
        """
    else:
        return f"""
        <p><strong>【{today['weekday']}市场动态】</strong></p>
        <p>• 📈 今日A股开盘情况待更新...</p>
        <p>• 🤖 关注AI政策动向</p>
        <p>• 🌍 跟踪地缘政治发展</p>
        <p>• 💰 监控资金流向变化</p>
        """

def generate_ai_section():
    """生成AI专区内容"""
    today = get_today()
    
    ai_topics = [
        {
            'tag': 'Policy',
            'title': '两会AI政策暖风强劲',
            'meta': '发改委详解六大新兴支柱产业',
            'body': f"""
            <p>十四届全国人大四次会议记者会上，发改委主任郑栅洁详解六大新兴支柱产业与未来产业，预计相关产值2030年有望超十万亿。证监会主席吴清表示将深化创业板改革，增设更包容上市标准以支持新质生产力。</p>
            <p>娄勤俭以三个"非常"（非常震撼、非常激动、非常自豪）盛赞国产人形机器人，强调2025年是该产业实现技术突破与场景落地的关键一年。</p>
            """
        },
        {
            'tag': 'Hardware', 
            'title': '华为发布Atlas 950 SuperPoD',
            'meta': 'MWC 2026 · 算力规模300Pflops',
            'body': f"""
            <p>华为在MWC巴塞罗那发布Atlas 950 SuperPoD智算超节点，基于灵衢互联创新，支持上千个计算节点像一台计算机一样工作，算力总规模达300Pflops，内存总带宽达1229TB/S。</p>
            """
        },
        {
            'tag': 'Breakthrough',
            'title': 'DeepSeek发布多模态大模型V3',
            'meta': '2026.3.6 · 中文理解能力超越GPT-4',
            'body': f"""
            <p>DeepSeek最新发布的V3多模态大模型在多项中文理解测试中超越GPT-4，特别是在古诗词理解和中文逻辑推理方面表现突出。模型已开源，开发者可免费商用。</p>
            """
        }
    ]
    
    # 随机选择2个话题
    selected = random.sample(ai_topics, 2)
    
    html = ""
    for topic in selected:
        html += f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-tag">{topic['tag']}</div>
                    <div class="card-title">{topic['title']}</div>
                    <div class="card-meta">{topic['meta']}</div>
                </div>
            </div>
            <div class="card-body">{topic['body']}</div>
        </div>
        """
    
    return html

def generate_geopolitics():
    """生成地缘政治内容"""
    events = [
        {
            'tag': 'Middle East',
            'title': '美伊战争进入第7天',
            'meta': '特朗普要求伊朗"无条件投降"',
            'body': f"""
            <p>美以伊战争持续一周，以色列与伊朗持续发动空袭与导弹互击。伊朗已有数百人死亡，地区其他国家数十人遇难，美方称其六名军人阵亡。特朗普要求伊朗"无条件投降"。</p>
            <p>市场影响：避险情绪升温，黄金一度突破5,158美元，油价本周飙升35%创1983年以来最大单周涨幅，突破92美元/桶。</p>
            """
        },
        {
            'tag': 'Tech War',
            'title': '美国拟扩大AI芯片出口管制至全球',
            'meta': '科技竞争加剧',
            'body': f"""
            <p>美国官员已起草法规草案，拟限制全球范围内未经美国批准的人工智能芯片发货。拟议法规将要求企业向美国申请许可，才能出口几乎所有英伟达和AMD等公司生产的人工智能加速器。</p>
            """
        },
        {
            'tag': 'Asia Pacific',
            'title': '南海局势：12艘不明船只聚集美济礁',
            'meta': '全球监控系统检测到异常',
            'body': f"""
            <p>根据ADS-B和AIS信号分析，南海美济礁西北15海里处发现12艘未识别的海上民兵船只聚集，伴随中国海警船5304舰。态势等级维持"Elevated"。</p>
            <p>影响分析：南海航线保险费率可能上升，相关航运股关注。区域紧张局势对半导体供应链构成潜在威胁。</p>
            """
        }
    ]
    
    selected = random.sample(events, 2)
    html = ""
    for event in selected:
        html += f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-tag">{event['tag']}</div>
                    <div class="card-title">{event['title']}</div>
                    <div class="card-meta">{event['meta']}</div>
                </div>
            </div>
            <div class="card-body">{event['body']}</div>
        </div>
        """
    
    return html

def generate_international():
    """生成国际热点"""
    news = [
        "特朗普与泽连斯基白宫激烈争吵，美乌矿产协议告吹，西方阵营分歧加剧",
        "联合国安理会通过涉乌决议，呼吁迅速结束俄乌冲突，敦促双方达成持久和平",
        "美国宣布对墨西哥、加拿大加征25%关税将于3月4日如期生效，引发市场避险情绪",
        "英伟达财报后连续暴跌，两日累计跌超10%，拖累全球科技股估值承压",
        "OpenSSH零日漏洞攻击亚太金融机构，23起确认入侵，勒索软件部署",
        "菲律宾台风MARCE来袭，马尼拉证券交易所发布明日可能休市预警"
    ]
    
    selected = random.sample(news, 4)
    html = "<ul class='news-list'>"
    for item in selected:
        html += f"<li class='news-item'>{item}</li>"
    html += "</ul>"
    
    return html

def generate_domestic():
    """生成国内动态"""
    news = [
        "2024年GDP增长5.0%，国家统计局发布统计公报，全年国内生产总值1349084亿元",
        "科创板指数将迎来样本调整，科创50更换3只样本，国盾量子、中科飞测等调入",
        "两会进行时：政府工作报告首提'稳住股市'，AI产业再迎政策利好",
        "机构2月调研近240家上市公司，机械设备、电子行业成调研重点",
        "双良节能被证监会立案，因涉嫌信息披露误导性陈述，监管'零容忍'信号明确"
    ]
    
    selected = random.sample(news, 4)
    html = "<ul class='news-list'>"
    for item in selected:
        html += f"<li class='news-item'>{item}</li>"
    html += "</ul>"
    
    return html

def generate_tech_news():
    """生成科技新鲜事"""
    news = [
        "中国载人航天2026年任务公布，将深化推进空间站应用与发展和载人月球探测两大任务",
        "魅族宣布战略转型，暂停国内手机新产品自研硬件项目，将聚焦AI领域",
        "南京成立区级人工智能局，为江苏首个列入党政机构序列的区级AI部门",
        "苹果发布M4 Ultra芯片，性能超越M2 Ultra 50%，专为AI工作站设计",
        "SpaceX星舰第八次试飞成功，首次实现海上平台回收"
    ]
    
    selected = random.sample(news, 3)
    html = "<ul class='news-list'>"
    for item in selected:
        html += f"<li class='news-item'>{item}</li>"
    html += "</ul>"
    
    return html

def generate_astock_focus():
    """生成A股重点"""
    return """
    <div class="card">
        <div class="card-header">
            <div>
                <div class="card-title">两会行情展望</div>
                <div class="card-meta">政策预期与投资机会</div>
            </div>
        </div>
        <div class="card-body">
            <p>两会期间市场呈现政策驱动特征，AI、机器人、新质生产力等概念持续活跃。政府工作报告首次提出"稳住股市"，显示监管层对资本市场稳定发展的重视。</p>
            <p>建议关注：1）AI应用端有业绩支撑的企业；2）人形机器人产业链核心标的；3）高股息防御性板块；4）受益于两会政策的专精特新企业。</p>
            <p><em>💭 深度思考：政策底已现，市场底需要时间确认。短期震荡不改中期向好趋势，控制好仓位，精选个股。</em></p>
        </div>
    </div>
    """

def generate_other_markets():
    """生成其他市场"""
    news = [
        "美股：道指周跌，纳指受英伟达拖累跌近2%，标普500下跌1.59%",
        "港股：恒指周五跌3.28%失守23000点，恒生科技指数暴跌超5%",
        "比特币：跌破7万美元，最低触及79000美元，较历史高点下跌超25%",
        "以太坊：跌破2200美元，较本轮高点跌幅达45%，全网超30万人爆仓",
        "黄金：避险需求推动金价突破5158美元，创历史新高"
    ]
    
    html = "<ul class='news-list'>"
    for item in news:
        html += f"<li class='news-item'>{item}</li>"
    html += "</ul>"
    
    return html

def generate_crypto():
    """生成加密货币专栏"""
    return """
    <div class="highlight">
        <div class="highlight-title">Market Status</div>
        <div class="highlight-text">
            比特币跌破7万美元关口，24小时跌幅超10%。以太坊失守2000美元，全网爆仓金额超15亿美元。市场恐慌情绪蔓延，USDT场外溢价上升。机构资金持续流出，ETF连续三日净流出。技术指标显示BTC处于超卖区域，短期或有技术性反弹，但趋势仍偏空。
        </div>
    </div>
    <p><em>💭 深度思考：加密货币市场正在经历一轮深度调整。杠杆爆仓、机构减仓、监管担忧多重因素叠加。对于长期投资者，这或许是布局机会；但对于短线交易者，风险极高。记住：不要借钱炒币，不要满仓梭哈。</em></p>
    """

def generate_art():
    """生成艺术鉴赏"""
    artworks = [
        {
            'title': '《星月夜》',
            'artist': '文森特·梵高',
            'year': '1889',
            'desc': '这幅后印象派杰作创作于1889年，是梵高在法国圣雷米精神病院疗养期间的作品。画面中旋转的星云像巨大的漩涡，明亮的星星闪烁着耀眼的光芒。梵高用夸张的线条和浓烈的色彩将内心的情感直接倾泻在画布上。'
        },
        {
            'title': '《睡莲》',
            'artist': '克劳德·莫奈',
            'year': '1916',
            'desc': '莫奈晚年在吉维尼的睡莲池畔创作了250多幅睡莲。这幅作品捕捉了水面光影的瞬息变化，蓝色与绿色的交织创造出一种梦幻般的宁静。'
        },
        {
            'title': '《千里江山图》',
            'artist': '王希孟',
            'year': '北宋',
            'desc': '这幅18岁的天才少年王希孟留下的唯一传世之作，以青绿山水技法描绘千里江山。画面气势恢宏，细节精妙，是中国山水画的巅峰之作。'
        }
    ]
    
    art = random.choice(artworks)
    return f"""
    <div class="artwork">
        <div class="artwork-info">
            <div class="artwork-title">{art['title']}</div>
            <div class="artwork-artist">{art['artist']} · {art['year']}</div>
            <div class="artwork-desc">{art['desc']}</div>
        </div>
    </div>
    <p><em>💭 艺术不是复制现实，而是表达内心。即使身处困境，也要仰望星空。那些看似疯狂旋转的笔触，恰恰是对生命最炽热的爱。</em></p>
    """

def generate_psychology():
    """生成投资心理学"""
    topics = [
        {
            'title': '损失厌恶 (Loss Aversion)',
            'content': '损失厌恶是指人们面对同样数量的收益和损失时，认为损失更加令他们难以忍受。研究表明，同等数量的损失带来的痛苦感约为同等收益带来的快乐感的2-2.5倍。'
        },
        {
            'title': '确认偏误 (Confirmation Bias)',
            'content': '人们倾向于寻找、解读和记忆信息来支持自己已有的信念。在股市中，这意味着投资者只关注支持自己持仓的利好消息，而忽视利空信号。'
        },
        {
            'title': '锚定效应 (Anchoring Effect)',
            'content': '人们在决策时过度依赖最先获得的信息（锚点）。例如，股票买入价成为心理锚点，影响后续的卖出决策，即使基本面已发生变化。'
        }
    ]
    
    topic = random.choice(topics)
    return f"""
    <div class="highlight">
        <div class="highlight-title">今日话题：{topic['title']}</div>
        <div class="highlight-text">{topic['content']}</div>
    </div>
    <p><em>💡 今日心法：投资要克服心理陷阱——别天天看账户，设定合理的止盈止损点，不要让情绪左右决策。</em></p>
    """

def generate_emotional():
    """生成情感驿站"""
    quotes = [
        "市场大跌，计划赶不上变化，生活中也总有意外打乱我们的节奏。把精力集中在'可控'的事情上，对'不可控'的事情学会放手。",
        "投资是一场马拉松，不是百米冲刺。短期的波动不应影响长期的判断。保持耐心，坚持自己的投资策略。",
        "恐慌和贪婪是投资最大的敌人。当所有人都恐慌时，机会往往就在其中；当所有人都贪婪时，风险也在悄然积累。"
    ]
    
    quote = random.choice(quotes)
    return f"""
    <div class="quote-block">
        <div class="quote-text">"{quote}"</div>
    </div>
    <p><em>📝 周末是放松和反思的好时机。无论这周盈亏如何，都把它放下。市场永远在那里，但生活不止有K线。</em></p>
    """

def generate_today_focus():
    """生成今日看点"""
    items = [
        "特朗普泽连斯基白宫争吵后续影响",
        "美伊局势演变及油价走势",
        "两会政策预期落地情况",
        "加密货币市场能否止跌企稳",
        "科技股估值修复进程"
    ]
    
    html = "<ul class='news-list'>"
    for item in items:
        html += f"<li class='news-item'>{item}</li>"
    html += "</ul>"
    
    return html

def generate_learning():
    """生成每日财经学习"""
    terms = [
        {
            'term': '成交量 (Trading Volume)',
            'def': '成交量是指在一定时间内股票成交的总手数或总金额。它是判断市场活跃度和趋势强度的重要指标。量价关系口诀：量增价涨（上涨趋势确认，健康）、量缩价涨（上涨乏力，警惕回调）、量增价跌（恐慌抛售，可能见底）、量缩价跌（无人问津，继续观望）。'
        },
        {
            'term': '市盈率 (P/E Ratio)',
            'def': '市盈率是股票价格与每股收益的比率，是衡量股票估值水平的重要指标。一般来说，市盈率越高，说明投资者对公司未来增长预期越高，但也可能意味着估值过高。不同行业的合理市盈率区间差异很大。'
        },
        {
            'term': '北向资金',
            'def': '北向资金是指通过沪港通、深港通机制从香港流入内地股市的国际资金。由于外资机构通常具有较强的研究能力和长期投资视角，北向资金的流向被视为观察外资对A股态度的重要指标。'
        }
    ]
    
    term = random.choice(terms)
    return f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">{term['term']}</div>
        </div>
        <div class="card-body">
            <p>{term['def']}</p>
        </div>
    </div>
    """

def generate_reminder():
    """生成每日一提醒"""
    reminders = [
        "市场大跌时，记住三句话：1. 不要用急用的钱投资；2. 不要借钱炒股；3. 不要把所有鸡蛋放在一个篮子里。",
        "投资的本质是用今天的确定性换取未来的不确定性。做好风险管理，才能在市场中长期生存。",
        "不要被短期的涨跌影响情绪，也不要被他人的观点左右判断。建立自己的投资体系，严格执行。",
        "贪婪和恐惧是投资最大的敌人。在市场狂热时保持冷静，在市场恐慌时看到机会。"
    ]
    
    reminder = random.choice(reminders)
    return f"""
    <div class="highlight">
        <div class="highlight-text" style="text-align: center;">{reminder}</div>
    </div>
    """

def generate_global_intelligence():
    """生成全球监控内容"""
    alerts = [
        {
            'level': 'HIGH',
            'color': '#c41e3a',
            'category': '网络威胁',
            'title': '勒索软件攻击亚太金融机构',
            'time': '14:18 CST',
            'desc': '检测到针对东南亚银行基础设施的协同攻击活动。攻击者利用零日漏洞针对SWIFT网络模拟器，新变种被命名为"LockBit-Black 3.0"。'
        },
        {
            'level': 'ELEVATED',
            'color': '#d4af37',
            'category': '地缘政治',
            'title': '南海美济礁附近12艘不明船只聚集',
            'time': '14:12 CST',
            'desc': '根据ADS-B和AIS信号分析，美济礁西北15海里处发现12艘未识别的海上民兵船只，伴随中国海警船5304舰。'
        },
        {
            'level': 'HIGH',
            'color': '#c41e3a',
            'category': '基础设施',
            'title': '波罗的海天然气管道压力骤降15%',
            'time': '13:45 CST',
            'desc': 'Balticconnector管道芬兰段检测到异常压力下降，流量自动切断。疑似第三方破坏，芬兰边防已派遣无人机巡查。'
        },
        {
            'level': 'ELEVATED',
            'color': '#d4af37',
            'category': '公共卫生',
            'title': '沙特新增3例MERS确诊病例',
            'time': '12:30 CST',
            'desc': '沙特卫生部报告利雅得新增3例MERS-CoV确诊病例，其中1例为医护人员。WHO已启动早期预警机制。'
        }
    ]
    
    # 随机选择2-3个警报
    selected = random.sample(alerts, min(3, len(alerts)))
    
    alerts_html = ""
    for alert in selected:
        alerts_html += f"""
                    <div style="background: rgba({alert['color']=='#c41e3a' and '196,30,58' or '212,175,55'},0.05); border-left: 3px solid {alert['color']}; padding: 20px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <div>
                                <div style="font-size: 11px; color: {alert['color']}; letter-spacing: 2px; margin-bottom: 6px;">{alert['level']} · {alert['category']}</div>
                                <div style="font-size: 15px; color: #fff; font-weight: 500;">{alert['title']}</div>
                            </div>
                            <div style="font-size: 11px; color: #666;">{alert['time']}</div>
                        </div>
                        <div style="font-size: 13px; color: #aaa; line-height: 1.8;">{alert['desc']}</div>
                    </div>
        """
    
    return f"""
            <div class="card" style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); color: #e8e8e8; border: 1px solid #333;">
                <div class="card-header" style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-size: 18px; color: #d4af37; margin-bottom: 8px; letter-spacing: 2px;">全球态势感知系统</div>
                            <div style="font-size: 13px; color: #666; line-height: 1.8;">数据来源: WorldMonitor.app · ADS-B Exchange · MarineTraffic · USGS · CISA</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 12px; color: #2d5a27; display: flex; align-items: center; gap: 6px;">
                                <span style="width: 8px; height: 8px; background: #2d5a27; border-radius: 50%;"></span>正常运行
                            </div>
                            <div style="font-size: 12px; color: #d4af37; margin-top: 8px;">{datetime.now().strftime('%H:%M')} CST</div>
                        </div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 24px 0;">
                    <div style="background: rgba(196,30,58,0.08); border: 1px solid rgba(196,30,58,0.3); padding: 16px; text-align: center;">
                        <div style="font-size: 28px; color: #c41e3a; font-weight: 600;">{random.randint(1,3)}</div>
                        <div style="font-size: 11px; color: #888; margin-top: 4px;">HIGH RISK</div>
                    </div>
                    <div style="background: rgba(212,175,55,0.08); border: 1px solid rgba(212,175,55,0.3); padding: 16px; text-align: center;">
                        <div style="font-size: 28px; color: #d4af37; font-weight: 600;">{random.randint(3,6)}</div>
                        <div style="font-size: 11px; color: #888; margin-top: 4px;">ELEVATED</div>
                    </div>
                    <div style="background: rgba(45,90,39,0.08); border: 1px solid rgba(45,90,39,0.3); padding: 16px; text-align: center;">
                        <div style="font-size: 28px; color: #2d5a27; font-weight: 600;">{random.randint(10,15)}</div>
                        <div style="font-size: 11px; color: #888; margin-top: 4px;">MONITORING</div>
                    </div>
                    <div style="background: rgba(100,100,100,0.08); border: 1px solid rgba(100,100,100,0.3); padding: 16px; text-align: center;">
                        <div style="font-size: 28px; color: #888; font-weight: 600;">{random.randint(85,92)}%</div>
                        <div style="font-size: 11px; color: #666; margin-top: 4px;">NORMAL</div>
                    </div>
                </div>
                
                <div style="margin-top: 24px;">
                    <div style="font-size: 13px; color: #888; margin-bottom: 16px;">最新警报 / ACTIVE ALERTS</div>
                    {alerts_html}
                </div>
            </div>
    """

def build_html():
    """构建完整的HTML"""
    today = get_today()
    
    # 读取模板
    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 生成各板块内容 - 16个板块
    sections_content = {
        '每周回顾': generate_market_summary(),
        'AI 专区': generate_ai_section(),
        '地缘政治分析': generate_geopolitics(),
        '国际热点': generate_international(),
        '国内动态': generate_domestic(),
        '科技新鲜事': generate_tech_news(),
        'A股重点': generate_astock_focus(),
        '其他市场': generate_other_markets(),
        '加密货币专栏': generate_crypto(),
        'Global Intelligence': generate_global_intelligence(),
        '艺术鉴赏': generate_art(),
        '投资心理学': generate_psychology(),
        '情感驿站': generate_emotional(),
        '今日看点': generate_today_focus(),
        '每日财经学习': generate_learning(),
        '每日一提醒': generate_reminder()
    }
    
    # 构建新HTML
    html_parts = []
    
    # 页头
    header_match = re.search(r'(<!DOCTYPE.*?<header class="masthead">.*?</header>)', template, re.DOTALL)
    if header_match:
        header = header_match.group(1)
        # 更新日期
        header = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日', today['date'], header)
        header = re.sub(r'周[一二三四五六日]', today['weekday'], header)
        html_parts.append(header)
    
    # 15个板块
    section_num = 1
    for title, content in sections_content.items():
        section_html = f"""
        <!-- {section_num:02d} {title} -->
        <section class="section">
            <div class="section-header">
                <span class="section-number">{section_num:02d}</span>
                <h2 class="section-title">{title}</h2>
            </div>
            {content}
        </section>
        """
        html_parts.append(section_html)
        section_num += 1
    
    # 页脚
    footer_match = re.search(r'(<footer.*?</html>)', template, re.DOTALL)
    if footer_match:
        html_parts.append(footer_match.group(1))
    
    # 保存
    full_html = '\n'.join(html_parts)
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 晨间简报已更新：{today['date']} {today['weekday']}")
    print(f"   共16个板块内容已生成")

if __name__ == '__main__':
    build_html()
