#!/usr/bin/env python3
"""
每日简报邮件发送脚本
每天早上8:30自动发送简报到指定邮箱
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import subprocess
import re

def get_daily_brief_content():
    """读取今日简报内容"""
    try:
        # 读取 today.html 并提取文本内容
        with open('/root/.openclaw/workspace/daily-brief/today.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 提取标题和主要内容
        title_match = re.search(r'<title>(.*?)</title>', html_content)
        title = title_match.group(1) if title_match else "每日简报"
        
        return {
            'title': title,
            'url': 'https://chinafox929.github.io/daily-brief/today.html'
        }
    except Exception as e:
        return {
            'title': f'每日简报 | {datetime.now().strftime("%Y年%m月%d日")}',
            'url': 'https://chinafox929.github.io/daily-brief/'
        }

def send_email(to_email, subject, html_body):
    """发送邮件（需要配置SMTP）"""
    # 注意：这里需要配置SMTP服务器信息
    # 由于无法直接访问用户的Gmail，这里只是模板
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'warfacejiang@gmail.com'
    msg['To'] = to_email
    
    # 添加HTML内容
    html_part = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(html_part)
    
    # 这里需要SMTP配置才能实际发送
    print(f"邮件已准备好发送至: {to_email}")
    print(f"主题: {subject}")
    return True

def generate_email_template():
    """生成邮件模板"""
    brief = get_daily_brief_content()
    
    today = datetime.now().strftime("%Y年%m月%d日 %A")
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{brief['title']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.8; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; padding: 20px 0; border-bottom: 2px solid #c4a882; }}
        .title {{ font-size: 24px; color: #2c2c2c; margin: 10px 0; }}
        .date {{ color: #8b7355; font-size: 14px; }}
        .content {{ padding: 20px 0; }}
        .section {{ margin: 20px 0; padding: 15px; background: #f9f7f4; border-radius: 8px; }}
        .section-title {{ font-size: 18px; color: #5a4a3a; margin-bottom: 10px; font-weight: bold; }}
        .button {{ display: inline-block; padding: 12px 24px; background: #c4a882; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px 0; color: #888; font-size: 12px; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="date">{today}</div>
        <div class="title">🌅 每日简报</div>
        <p>专属信息网 · 禅意生活</p>
    </div>
    
    <div class="content">
        <p>您好！今日简报已更新，点击下方按钮查看完整内容：</p>
        
        <div style="text-align: center;">
            <a href="{brief['url']}" class="button">查看今日简报</a>
        </div>
        
        <div class="section">
            <div class="section-title">📋 今日内容概览</div>
            <ul>
                <li>🌍 国际热点 - 全球市场动态</li>
                <li>🇨🇳 国内动态 - 政策与经济数据</li>
                <li>🤖 AI专区 - 人工智能最新进展</li>
                <li>🔥 A股重点 - 市场分析与操作建议</li>
                <li>💡 每日财经学习 - 投资知识科普</li>
                <li>🧠 投资心理学 - 行为金融学</li>
                <li>🎨 艺术鉴赏 - 每日一画</li>
            </ul>
        </div>
        
        <div class="section">
            <div class="section-title">🔗 快捷访问</div>
            <p>网页版：<a href="{brief['url']}">{brief['url']}</a></p>
            <p>历史归档：<a href="https://chinafox929.github.io/daily-brief/archive.html">查看往期简报</a></p>
        </div>
    </div>
    
    <div class="footer">
        <p>此邮件由 OpenClaw 每日简报系统自动发送</p>
        <p>如需取消订阅，请联系管理员</p>
    </div>
</body>
</html>
"""
    return html_template

if __name__ == '__main__':
    # 获取今日简报信息
    brief = get_daily_brief_content()
    
    # 生成邮件内容
    email_html = generate_email_template()
    
    # 目标邮箱
    to_email = 'warfacejiang@gmail.com'
    subject = f'🌅 每日简报 | {datetime.now().strftime("%Y年%m月%d日")}'
    
    # 发送邮件（需要SMTP配置）
    # send_email(to_email, subject, email_html)
    
    print("=" * 50)
    print("每日简报邮件发送脚本")
    print("=" * 50)
    print(f"\n收件人: {to_email}")
    print(f"主题: {subject}")
    print(f"简报链接: {brief['url']}")
    print("\n邮件内容已生成！")
    print("\n注意：需要配置SMTP服务器才能实际发送邮件。")
    print("建议：使用Gmail的App密码或企业邮箱SMTP服务。")
