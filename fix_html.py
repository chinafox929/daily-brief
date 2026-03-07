import re

with open('/root/.openclaw/workspace/daily-brief/index.html', 'r') as f:
    content = f.read()

# 1. 修改指标卡片数值，添加class以便JS更新
content = content.replace(
    '<div style="font-size: 28px; color: #c41e3a; font-weight: 600;">2</div>',
    '<div style="font-size: 28px; color: #c41e3a; font-weight: 600;" class="global-stat-value">2</div>'
)
content = content.replace(
    '<div style="font-size: 28px; color: #d4af37; font-weight: 600;">5</div>',
    '<div style="font-size: 28px; color: #d4af37; font-weight: 600;" class="global-stat-value">5</div>'
)
content = content.replace(
    '<div style="font-size: 28px; color: #2d5a27; font-weight: 600;">12</div>',
    '<div style="font-size: 28px; color: #2d5a27; font-weight: 600;" class="global-stat-value">12</div>'
)
content = content.replace(
    '<div style="font-size: 28px; color: #888; font-weight: 600;">89%</div>',
    '<div style="font-size: 28px; color: #888; font-weight: 600;" class="global-stat-value">89%</div>'
)

# 2. 找到"最新警报 / ACTIVE ALERTS"后面的内容，用容器包裹
pattern = r'(<div style="font-size: 13px; color: #888; margin-bottom: 16px; letter-spacing: 1px;">最新警报 / ACTIVE ALERTS</div>)'
replacement = r'''\1
                    
                    <!-- 动态警报容器 -->
                    <div id="global-alerts-container">'''
content = re.sub(pattern, replacement, content)

# 3. 在智能摘要之前关闭容器
pattern2 = r'(<div style="background: rgba\(212,175,55,0\.08\); border: 1px solid rgba\(212,175,55,0\.3\); padding: 20px; margin-top: 24px;">\s*<div style="font-size: 12px; color: #d4af37; margin-bottom: 12px; letter-spacing: 2px;">INTELLIGENCE SUMMARY)'
replacement2 = r'''</div>
                    
                    \1'''
content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# 4. 给智能摘要文字加上id
content = content.replace(
    '<div style="font-size: 14px; color: #ccc; line-height: 1.8;">\n                        当前全球风险指数处于',
    '<div style="font-size: 14px; color: #ccc; line-height: 1.8;" id="global-summary">\n                        当前全球风险指数处于'
)

# 5. 引入JS文件
old_script_end = '''    </script>
</body>'''
new_script_end = '''    </script>
    
    <!-- 全球监控实时数据模块 -->
    <script src="realtime-global.js"></script>
</body>'''
content = content.replace(old_script_end, new_script_end)

with open('/root/.openclaw/workspace/daily-brief/index.html', 'w') as f:
    f.write(content)

print("已修改 index.html，添加动态数据支持")