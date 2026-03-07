/**
 * Daily Brief 3.0 - WebSocket 实时数据客户端
 * 无需刷新页面，数据实时推送
 */

class DailyBriefRealtime {
    constructor() {
        this.ws = null;
        this.reconnectInterval = 5000;
        this.heartbeatInterval = null;
        this.isConnected = false;
        
        // 数据缓存
        this.cache = {
            market: null,
            global: null,
            news: null
        };
        
        this.init();
    }
    
    init() {
        this.connect();
        
        // 页面可见性变化时重新连接
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.isConnected) {
                this.connect();
            }
        });
    }
    
    connect() {
        const wsUrl = this.getWebSocketUrl();
        console.log('[WebSocket] 正在连接:', wsUrl);
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('[WebSocket] 已连接');
                this.isConnected = true;
                this.showConnectionStatus('已连接', 'connected');
                this.startHeartbeat();
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (e) {
                    console.error('[WebSocket] 消息解析错误:', e);
                }
            };
            
            this.ws.onclose = () => {
                console.log('[WebSocket] 连接断开');
                this.isConnected = false;
                this.showConnectionStatus('断开', 'disconnected');
                this.stopHeartbeat();
                setTimeout(() => this.connect(), this.reconnectInterval);
            };
            
            this.ws.onerror = (error) => {
                console.error('[WebSocket] 错误:', error);
                this.showConnectionStatus('错误', 'error');
            };
            
        } catch (e) {
            console.error('[WebSocket] 连接失败:', e);
            setTimeout(() => this.connect(), this.reconnectInterval);
        }
    }
    
    getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws`;
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'connected':
                console.log('[WebSocket] 服务器:', data.message);
                break;
                
            case 'market':
                this.cache.market = data;
                this.renderMarket(data);
                break;
                
            case 'global':
                this.cache.global = data;
                this.renderGlobal(data);
                break;
                
            case 'news':
                this.cache.news = data;
                this.renderNews(data);
                break;
                
            case 'pong':
                // 心跳响应
                break;
        }
    }
    
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.isConnected && this.ws) {
                this.ws.send(JSON.stringify({action: 'ping'}));
            }
        }, 30000); // 每30秒心跳
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }
    
    showConnectionStatus(status, type) {
        // 可以添加连接状态指示器到页面
        console.log(`[WebSocket] 状态: ${status}`);
    }
    
    // ============ 渲染函数 ============
    renderMarket(data) {
        // 更新指数
        const indices = data.indices || {};
        Object.entries(indices).forEach(([name, info]) => {
            const el = document.querySelector(`[data-market="${name}"]`);
            if (el) {
                const valueEl = el.querySelector('.market-value');
                const changeEl = el.querySelector('.market-change');
                if (valueEl) {
                    const oldValue = valueEl.textContent;
                    const newValue = this.formatNumber(info.value);
                    if (oldValue !== newValue) {
                        valueEl.textContent = newValue;
                        this.flashUpdate(valueEl);
                    }
                }
                if (changeEl) {
                    const newChange = (info.change >= 0 ? '+' : '') + info.change.toFixed(2) + '%';
                    changeEl.textContent = newChange;
                    changeEl.className = 'market-change ' + (info.change >= 0 ? 'up' : 'down');
                }
            }
        });
        
        // 更新加密货币
        const crypto = data.crypto || {};
        Object.entries(crypto).forEach(([name, info]) => {
            const el = document.querySelector(`[data-crypto="${name}"]`);
            if (el) {
                const priceEl = el.querySelector('.crypto-price');
                const changeEl = el.querySelector('.crypto-change');
                if (priceEl) {
                    const newPrice = '$' + this.formatNumber(info.value);
                    if (priceEl.textContent !== newPrice) {
                        priceEl.textContent = newPrice;
                        this.flashUpdate(priceEl);
                    }
                }
                if (changeEl) {
                    changeEl.textContent = (info.change >= 0 ? '+' : '') + info.change.toFixed(1) + '%';
                    changeEl.className = 'crypto-change ' + (info.change >= 0 ? 'up' : 'down');
                }
            }
        });
    }
    
    renderGlobal(data) {
        // 更新统计数据
        const stats = data.stats || {};
        const statEls = document.querySelectorAll('.global-stat-value');
        const statValues = [stats.high || 0, stats.elevated || 0, stats.monitoring || 0, stats.normal || 89];
        statEls.forEach((el, i) => {
            if (statValues[i] !== undefined) {
                const newValue = i === 3 ? statValues[i] + '%' : statValues[i];
                if (el.textContent !== String(newValue)) {
                    el.textContent = newValue;
                    this.flashUpdate(el);
                }
            }
        });
        
        // 更新警报列表
        const container = document.getElementById('global-alerts-container');
        if (container && data.all_alerts) {
            const currentIds = Array.from(container.querySelectorAll('[data-alert-id]')).map(el => el.dataset.alertId);
            const newIds = data.all_alerts.map(a => a.id);
            
            // 只在警报变化时更新
            if (JSON.stringify(currentIds) !== JSON.stringify(newIds)) {
                container.innerHTML = data.all_alerts.map(alert => this.renderAlertCard(alert)).join('');
            }
        }
        
        // 更新摘要
        const summaryEl = document.getElementById('global-summary');
        if (summaryEl && data.summary) {
            const fullSummary = data.summary + '。地缘冲突升温，黄金、原油可能波动。建议增加避险资产配置，关注北斗导航、网络安全、水利建设等主题投资机会。';
            if (summaryEl.textContent !== fullSummary) {
                summaryEl.textContent = fullSummary;
            }
        }
        
        // 更新时间
        const timeEl = document.getElementById('global-update-time');
        if (timeEl && data.updateTime) {
            timeEl.textContent = data.updateTime.split(' ')[1] + ' CST';
        }
    }
    
    renderAlertCard(alert) {
        const colors = {
            high: { border: '#c41e3a', bg: 'rgba(196,30,58,0.05)', text: '#c41e3a', label: 'HIGH RISK' },
            elevated: { border: '#d4af37', bg: 'rgba(212,175,55,0.05)', text: '#d4af37', label: 'ELEVATED' },
            monitoring: { border: '#2d5a27', bg: 'rgba(45,90,39,0.05)', text: '#2d5a27', label: 'MONITORING' }
        };
        
        const c = colors[alert.level] || colors.monitoring;
        
        return `
            <div style="background: ${c.bg}; border-left: 3px solid ${c.border}; padding: 20px; margin-bottom: 12px; animation: fadeIn 0.3s ease;"
                 data-alert-id="${alert.id}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 11px; color: ${c.text}; letter-spacing: 2px; margin-bottom: 6px;">${c.label} · ${alert.category}</div>
                        <div style="font-size: 15px; color: #fff; font-weight: 500;">${alert.title}</div>
                    </div>
                    <div style="font-size: 11px; color: #666;">${alert.time}</div>
                </div>
                
                <div style="font-size: 13px; color: #aaa; line-height: 1.8; margin-bottom: 12px;">
                    ${alert.details}
                </div>
                
                <div style="background: rgba(0,0,0,0.3); padding: 12px; margin-bottom: 12px;">
                    <div style="font-size: 11px; color: #666; margin-bottom: 6px;">影响分析</div>
                    <div style="font-size: 12px; color: #888; line-height: 1.6;">
                        <strong style="color: #d4af37;">对中国影响：</strong> ${alert.china_relevance === 'direct' ? '直接' : alert.china_relevance === 'indirect' ? '间接' : '全球'}。
                        ${alert.impact || ''}
                    </div>
                </div>
                
                <div style="font-size: 11px; color: #666;">
                    区域: ${alert.region} | 关联性: ${alert.china_relevance === 'direct' ? '直接相关' : alert.china_relevance === 'indirect' ? '间接相关' : '全球关注'}
                </div>
            </div>
        `;
    }
    
    renderNews(data) {
        const ticker = document.querySelector('.ticker');
        if (ticker && data.breakingNews) {
            const newsHtml = data.breakingNews.map(news => `
                <div class="ticker-item">${news.title}</div>
            `).join('');
            ticker.innerHTML = newsHtml + newsHtml;
        }
    }
    
    flashUpdate(element) {
        element.style.transition = 'background-color 0.3s';
        element.style.backgroundColor = 'rgba(201, 169, 110, 0.2)';
        setTimeout(() => {
            element.style.backgroundColor = 'transparent';
        }, 500);
    }
    
    formatNumber(num) {
        if (num >= 10000) {
            return num.toLocaleString('en-US', {maximumFractionDigits: 0});
        }
        return num.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    }
}

// CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    window.dailyBrief = new DailyBriefRealtime();
});
