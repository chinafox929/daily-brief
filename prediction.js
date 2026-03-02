// 推荐预测模块
class PredictionModule {
    constructor() {
        this.data = null;
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.render();
    }
    
    async loadData() {
        try {
            const response = await fetch('market-data.json?t=' + Date.now());
            this.data = await response.json();
        } catch (error) {
            console.error('加载行情数据失败:', error);
            this.data = { stocks: [], crypto: [], signals: [] };
        }
    }
    
    render() {
        const container = document.getElementById('prediction-module');
        if (!container) return;
        
        const lastUpdate = this.data.lastUpdate 
            ? new Date(this.data.lastUpdate).toLocaleString('zh-CN')
            : '未知';
        
        let html = `
            <div class="prediction-header">
                <span>📊</span>
                <h3>实时行情 & 预测</h3>
                <span class="prediction-time">更新: ${lastUpdate}</span>
            </div>
            
            <div class="market-grid">
        `;
        
        // A股行情
        this.data.stocks.forEach(stock => {
            const isUp = stock.change >= 0;
            html += `
                <div class="market-card ${isUp ? 'up' : 'down'}">
                    <div class="market-name">${stock.name}</div>
                    <div class="market-price">${stock.price.toFixed(2)}</div>
                    <span class="market-change ${isUp ? 'up' : 'down'}">
                        ${isUp ? '+' : ''}${stock.change}%
                    </span>
                </div>
            `;
        });
        
        html += `</div>
            <div class="signals-section">
                <div class="signals-title">💡 今日信号</div>
        `;
        
        // 生成简单信号
        const signals = this.generateSignals();
        if (signals.length > 0) {
            signals.forEach(signal => {
                html += `
                    <div class="signal-item">
                        <span class="signal-badge ${signal.type}">${signal.label}</span>
                        <div class="signal-info">
                            <div class="signal-asset">${signal.asset}</div>
                            <div class="signal-suggestion">${signal.suggestion}</div>
                        </div>
                    </div>
                `;
            });
        } else {
            html += `<div style="color: #888; font-size: 14px;">暂无明确信号，建议观望</div>`;
        }
        
        html += `
            </div>
            <div class="disclaimer">
                ⚠️ 仅供参考，不构成投资建议。投资有风险，入市需谨慎。
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    generateSignals() {
        const signals = [];
        
        // 基于A股数据生成信号
        this.data.stocks.forEach(stock => {
            if (stock.change > 1) {
                signals.push({
                    asset: stock.name,
                    label: 'hold',
                    type: 'hold',
                    suggestion: '趋势偏强，可持有观望'
                });
            } else if (stock.change < -1) {
                signals.push({
                    asset: stock.name,
                    label: 'caution',
                    type: 'sell',
                    suggestion: '短期偏弱，注意风险'
                });
            }
        });
        
        return signals;
    }
}

// 页面加载后初始化
document.addEventListener('DOMContentLoaded', () => {
    new PredictionModule();
});
