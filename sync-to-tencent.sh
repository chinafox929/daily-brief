#!/bin/bash
# 同步到腾讯服务器 - 使用密码登录

SERVER="43.139.1.235"
USER="ubuntu"
PASSWORD="Open123456"

echo "🔄 同步 Daily Brief 到腾讯服务器..."

# 使用 sshpass 进行密码认证同步
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no ${USER}@${SERVER} "mkdir -p /var/www/daily-brief/data"

# 同步文件
sshpass -p "$PASSWORD" rsync -avz --exclude '.git' --exclude 'venv' \
    -e "ssh -o StrictHostKeyChecking=no" \
    /root/.openclaw/workspace/daily-brief/ \
    ${USER}@${SERVER}:/var/www/daily-brief/

echo "✅ 同步完成"

# 重启远程服务（如果需要）
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no ${USER}@${SERVER} "
    cd /var/www/daily-brief
    # 如果使用 PM2 管理 API 服务
    pm2 restart daily-brief-api 2>/dev/null || echo 'PM2 服务未运行'
    echo '文件已同步'
"

echo "✅ 全部完成"
