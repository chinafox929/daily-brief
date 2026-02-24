#!/bin/bash
# daily-brief 一键部署脚本
# 用法: ./deploy.sh

set -e

echo "🚀 开始部署 Daily Brief 网站..."

# ============ 配置区域 ============
DOMAIN="your-domain.com"           # 改成你的域名
EMAIL="your-email@example.com"     # 用于 SSL 证书
MONGO_PASSWORD="$(openssl rand -base64 32)"  # 自动生成数据库密码
JWT_SECRET="$(openssl rand -base64 32)"      # 自动生成 JWT 密钥
# ==================================

echo "📦 安装依赖..."
sudo apt update
sudo apt install -y nginx nodejs npm mongodb docker.io docker-compose git

# 启动 MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# 创建应用目录
mkdir -p ~/daily-brief
cd ~/daily-brief

# 克隆代码（假设代码已推送到 GitHub）
# git clone https://github.com/yourname/daily-brief.git .

echo "📝 创建配置文件..."

# 后端环境变量
cat > backend/.env << EOF
PORT=3000
MONGODB_URI=mongodb://localhost:27017/dailybrief
JWT_SECRET=$JWT_SECRET
NODE_ENV=production

# 支付宝配置（后续填入）
ALIPAY_APP_ID=
ALIPAY_PRIVATE_KEY=
ALIPAY_PUBLIC_KEY=

# 微信支付配置（后续填入）
WECHAT_APP_ID=
WECHAT_MCH_ID=
WECHAT_API_KEY=
EOF

echo "🔧 安装后端依赖..."
cd backend
npm install express mongoose bcryptjs jsonwebtoken cors dotenv express-rate-limit
npm install --save-dev nodemon
cd ..

echo "🔧 安装前端依赖（如需要）..."
cd frontend
# npm install  # 如果用 Vue/React 才需要
cd ..

echo "⚙️ 配置 PM2 进程管理..."
sudo npm install -g pm2

cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'daily-brief-api',
    cwd: './backend',
    script: 'src/app.js',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    },
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    error_log: './logs/err.log',
    out_log: './logs/out.log'
  }]
};
EOF

mkdir -p logs

echo "🌐 配置 Nginx..."

sudo tee /etc/nginx/sites-available/daily-brief << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # 前端静态文件
    location / {
        root /home/$(whoami)/daily-brief/frontend/public;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }
    
    # 后端 API
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # 管理后台
    location /admin/ {
        alias /home/$(whoami)/daily-brief/admin/;
        index login.html;
        try_files \$uri \$uri/ =404;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/daily-brief /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "🔒 配置 SSL (Let's Encrypt)..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $EMAIL

sudo systemctl enable certbot.timer

echo "🚀 启动服务..."
pm2 start ecosystem.config.js
pm2 save
pm2 startup systemd

echo "✅ 部署完成！"
echo ""
echo "📋 重要信息："
echo "   网站地址: https://$DOMAIN"
echo "   管理后台: https://$DOMAIN/admin/"
echo "   API 地址: https://$DOMAIN/api/"
echo ""
echo "🔐 安全密钥（请保存）："
echo "   MongoDB 密码: $MONGO_PASSWORD"
echo "   JWT 密钥: $JWT_SECRET"
echo ""
echo "⚠️  下一步："
echo "   1. 配置支付宝/微信支付参数（backend/.env）"
echo "   2. 重启服务: pm2 restart daily-brief-api"
echo "   3. 查看日志: pm2 logs"
