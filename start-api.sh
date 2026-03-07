#!/bin/bash
# Daily Brief API 启动脚本

cd "$(dirname "$0")"

echo "🚀 启动 Daily Brief API Server..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -q -r api/requirements.txt

# 启动服务
echo "🌐 API Server 启动在 http://localhost:8000"
echo "📊 数据端点:"
echo "   - /api/market     市场数据"
echo "   - /api/global     全球监控"
echo "   - /api/news       突发新闻"
echo "   - /api/brief      完整简报"
echo ""

python api/main.py
