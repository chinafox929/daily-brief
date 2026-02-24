#!/bin/bash
# Daily Brief Docker 一键部署脚本
# 在阿里云服务器上运行：curl -fsSL https://your-cdn.com/install.sh | bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Daily Brief 一键部署${NC}"
echo ""

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 sudo 运行${NC}"
    exit 1
fi

# 获取用户输入
read -p "请输入你的域名 (如: daily.example.com): " DOMAIN
read -p "请输入邮箱 (用于 SSL 证书): " EMAIL
read -p "是否安装 Docker? (y/n): " INSTALL_DOCKER

if [ "$INSTALL_DOCKER" = "y" ]; then
    echo -e "${YELLOW}📦 安装 Docker...${NC}"
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    
    # 安装 docker-compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 创建项目目录
PROJECT_DIR="/opt/daily-brief"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo -e "${YELLOW}📥 下载项目代码...${NC}"
# 这里可以从 GitHub 克隆，或者本地复制
# git clone https://github.com/yourname/daily-brief.git .

# 生成随机密钥
JWT_SECRET=$(openssl rand -base64 32)
MONGO_PASSWORD=$(openssl rand -base64 16)

echo -e "${YELLOW}📝 创建环境配置...${NC}"
cat > .env << EOF
# 数据库
MONGO_PASSWORD=$MONGO_PASSWORD

# JWT 密钥
JWT_SECRET=$JWT_SECRET

# 支付配置（部署后手动填写）
ALIPAY_APP_ID=
ALIPAY_PRIVATE_KEY=
ALIPAY_PUBLIC_KEY=
WECHAT_APP_ID=
WECHAT_MCH_ID=
WECHAT_API_KEY=
EOF

echo -e "${YELLOW}🐳 启动服务...${NC}"
docker-compose up -d

# 等待服务启动
sleep 5

echo -e "${YELLOW}🔒 配置 SSL 证书...${NC}"
docker run -it --rm \
    -v "$PROJECT_DIR/ssl:/etc/letsencrypt" \
    -v "$PROJECT_DIR/nginx.conf:/etc/nginx/conf.d/default.conf" \
    -p 80:80 \
    certbot/certbot certonly \
    --standalone \
    -d $DOMAIN \
    --agree-tos \
    -m $EMAIL \
    --non-interactive

# 更新 nginx 配置使用 SSL
sed -i "s/listen 80;/listen 443 ssl;/" nginx.conf
cat >> nginx.conf << 'EOF'

server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}
EOF

docker-compose restart nginx

echo ""
echo -e "${GREEN}✅ 部署完成！${NC}"
echo ""
echo "📋 访问地址："
echo "   网站: https://$DOMAIN"
echo "   后台: https://$DOMAIN/admin/"
echo ""
echo "🔐 重要信息（请保存）："
echo "   JWT 密钥: $JWT_SECRET"
echo "   数据库密码: $MONGO_PASSWORD"
echo ""
echo "⚠️  后续步骤："
echo "   1. 编辑 .env 文件，填入支付宝/微信支付参数"
echo "   2. 重启服务: docker-compose restart"
echo "   3. 查看日志: docker-compose logs -f"
echo ""
echo "📖 常用命令："
echo "   启动: docker-compose up -d"
echo "   停止: docker-compose down"
echo "   重启: docker-compose restart"
echo "   更新: docker-compose pull && docker-compose up -d"
