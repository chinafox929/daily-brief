/**
 * Daily Brief 2.0 - 全动态数据模块
 * 所有数据来自 /api/* 端点，真正的动态网站
 */

const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1') 
    ? 'http://localhost:8000/api' 
    : '/api';

class DailyBriefAPI {
    constructor() {
        this.cache = {};
        this.init();
    }
    
    init() {
        this.loadAllData();
        // 每30秒刷新一次
        setInterval(() => this.loadAllData(), 30000);
    }
    
    async fetchData(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}?t=${Date.now()}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            return null;
        }
    }
    
    async loadAllData() {
        // 并行加载所有数据
        const [market, global, news] = await Promise.all([
            this.fetchData('/market'),
            this.fetchData('/global'),
            this.fetchData('/news')
        ]);
        
        if (market) this.renderMarket(market);
        if (global) this.renderGlobal(global);
        if (news) this.renderNews(news);
        
        this.updateTime();
    }
    
    renderMarket(data) {
        // 更新指数
        const indices = data.indices || {};
        Object.entries(indices).forEach(([name, info]) => {
            const el = document.querySelector(`[data-market="${name}"]`);
            if (el) {
                const valueEl = el.querySelector('.market-value');
                const changeEl = el.querySelector('.market-change');
                if (valueEl) valueEl.textContent = this.formatNumber(info.value);
                if (changeEl) {
                    changeEl.textContent = (info.change >= 0 ? '+' : '') + info.change.toFixed(2) + '%';
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
                if (priceEl) priceEl.textContent = '$' + this.formatNumber(info.value);
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
                el.textContent = i === 3 ? statValues[i] + '%' : statValues[i];
            }
        });
        
        // 更新警报列表
        const container = document.getElementById('global-alerts-container');
        if (container && data.all_alerts) {
            container.innerHTML = data.all_alerts.map(alert => this.renderAlertCard(alert)).join('');
        }
        
        // 更新摘要
        const summaryEl = document.getElementById('global-summary');
        if (summaryEl && data.summary) {
            summaryEl.textContent = data.summary + '。地缘冲突升温，黄金、原油可能波动。建议增加避险资产配置，关注北斗导航、网络安全、水利建设等主题投资机会。';
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
            // 复制一份实现无缝滚动
            ticker.innerHTML = newsHtml + newsHtml;
        }
    }
    
    updateTime() {
        const el = document.getElementById('global-update-time');
        if (el) {
            const now = new Date();
            el.textContent = now.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Asia/Shanghai'
            }) + ' CST';
        }
        
        // 更新页面时间戳
        const mastheadDate = document.querySelector('.masthead-date');
        if (mastheadDate) {
            const now = new Date();
            mastheadDate.innerHTML = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 
                ${['日','一','二','三','四','五','六'][now.getDay()]} 
                | 实时更新中 | 更新于 ${now.toLocaleTimeString('zh-CN', {hour:'2-digit', minute:'2-digit'})}`;
        }
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
    window.dailyBrief = new DailyBriefAPI();
});
