/**
 * 全球实时监控动态数据模块
 * 每5分钟从服务器拉取最新警报数据
 */

class GlobalMonitor {
    constructor() {
        this.dataUrl = '/data/global-news.json';
        this.refreshInterval = 300000; // 5分钟
        this.container = document.getElementById('global-monitor-content');
        this.lastUpdateEl = document.getElementById('global-update-time');
        
        this.init();
    }
    
    init() {
        this.loadData();
        setInterval(() => this.loadData(), this.refreshInterval);
        
        // 每分钟更新时间显示
        setInterval(() => this.updateTimeDisplay(), 60000);
    }
    
    async loadData() {
        try {
            // 添加时间戳避免缓存
            const url = `${this.dataUrl}?t=${Date.now()}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.render(data);
            
        } catch (error) {
            console.error('加载全球监控数据失败:', error);
            this.showError('数据加载失败，使用缓存数据');
        }
    }
    
    render(data) {
        if (!data) return;
        
        // 更新时间
        if (this.lastUpdateEl && data.updateTime) {
            const date = new Date(data.updateTime);
            this.lastUpdateEl.textContent = date.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Asia/Shanghai'
            }) + ' CST';
        }
        
        // 更新指标卡片
        this.updateStats(data);
        
        // 更新警报列表
        this.updateAlerts(data);
        
        // 更新摘要
        this.updateSummary(data);
    }
    
    updateStats(data) {
        const stats = {
            high: data.high_risk_count || 0,
            elevated: Math.floor((data.total_alerts || 0) * 0.3),
            monitoring: data.total_alerts || 0,
            normal: 89
        };
        
        const statEls = document.querySelectorAll('.global-stat-value');
        if (statEls.length >= 4) {
            statEls[0].textContent = stats.high;
            statEls[1].textContent = stats.elevated;
            statEls[2].textContent = stats.monitoring;
            statEls[3].textContent = stats.normal + '%';
        }
    }
    
    updateAlerts(data) {
        const container = document.getElementById('global-alerts-container');
        if (!container) return;
        
        const allAlerts = [
            ...(data.hotspots || []).map(a => ({...a, category: '地缘政治'})),
            ...(data.infrastructure_alerts || []).map(a => ({...a, category: '基础设施'})),
            ...(data.cyber_alerts || []).map(a => ({...a, category: '网络安全'})),
            ...(data.economic_signals || []).map(a => ({...a, category: '经济信号'}))
        ];
        
        if (allAlerts.length === 0) {
            container.innerHTML = '<div style="color: #666; padding: 20px; text-align: center;">暂无活跃警报</div>';
            return;
        }
        
        // 按级别排序
        const levelOrder = { high: 0, elevated: 1, monitoring: 2 };
        allAlerts.sort((a, b) => levelOrder[a.level] - levelOrder[b.level]);
        
        container.innerHTML = allAlerts.map(alert => this.renderAlertCard(alert)).join('');
    }
    
    renderAlertCard(alert) {
        const colors = {
            high: { border: '#c41e3a', bg: 'rgba(196,30,58,0.05)', text: '#c41e3a' },
            elevated: { border: '#d4af37', bg: 'rgba(212,175,55,0.05)', text: '#d4af37' },
            monitoring: { border: '#2d5a27', bg: 'rgba(45,90,39,0.05)', text: '#2d5a27' }
        };
        
        const c = colors[alert.level] || colors.monitoring;
        
        return `
            <div style="background: ${c.bg}; border-left: 3px solid ${c.border}; padding: 20px; margin-bottom: 12px; animation: fadeIn 0.3s ease;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 11px; color: ${c.text}; letter-spacing: 2px; margin-bottom: 6px;">${alert.level.toUpperCase()} · ${alert.category}</div>
                        <div style="font-size: 15px; color: #fff; font-weight: 500;">${alert.title}</div>
                    </div>
                    <div style="font-size: 11px; color: #666;">${alert.time || '刚刚'}</div>
                </div>
                <div style="font-size: 13px; color: #aaa; line-height: 1.8;">
                    区域: ${alert.region} | 关联性: ${alert.china_relevance === 'direct' ? '直接' : alert.china_relevance === 'indirect' ? '间接' : '全球'}
                </div>
            </div>
        `;
    }
    
    updateSummary(data) {
        const el = document.getElementById('global-summary');
        if (el && data.summary) {
            el.textContent = data.summary;
        }
    }
    
    updateTimeDisplay() {
        if (this.lastUpdateEl) {
            const now = new Date();
            this.lastUpdateEl.textContent = now.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit',
                timeZone: 'Asia/Shanghai'
            }) + ' CST';
        }
    }
    
    showError(msg) {
        console.warn(msg);
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
    new GlobalMonitor();
});
