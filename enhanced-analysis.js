// 增强版股票分析展示
class EnhancedStockAnalysis {
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
            const response = await fetch('stock-analysis.json?t=' + Date.now());
            this.data = await response.json();
        } catch (error) {
            console.error('加载分析数据失败:', error);
        }
    }
    
    render() {
        // 找到自选分析模块，替换内容
        const resultDiv = document.getElementById('analysis-result');
        if (!resultDiv || !this.data) return;
        
        let html = `
            <div style="margin-top: 20px;">
                <div style="color: #ffd700; margin-bottom: 15px; font-size: 16px;">
                    📊 实时分析 (${new Date(this.data.last_update).toLocaleTimeString('zh-CN')})
                </div>
        `;
        
        this.data.stocks.forEach(stock => {
            const signalColor = {
                '买入': '#27ae60',
                '卖出': '#e74c3c',
                '持有': '#f39c12'
            }[stock.signal.signal];
            
            const changeColor = stock.change >= 0 ? '#27ae60' : '#e74c3c';
            const changeIcon = stock.change >= 0 ? '▲' : '▼';
            
            html += `
                <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; margin-bottom: 12px; border-left: 3px solid ${signalColor};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <span style="font-size: 16px; font-weight: bold;">${stock.name}</span>
                            <span style="color: #888; font-size: 12px; margin-left: 8px;">${stock.symbol}</span>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 20px; font-weight: bold;">${stock.price.toFixed(2)}</div>
                            <div style="color: ${changeColor}; font-size: 13px;">
                                ${changeIcon} ${stock.change > 0 ? '+' : ''}${stock.change}%
                            </div>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 12px 0; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 12px;">
                        <div style="text-align: center;">
                            <div style="color: #888;">振幅</div>
                            <div>${stock.indicators.amplitude}%</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888;">位置</div>
                            <div>${stock.indicators.position}%</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888;">趋势</div>
                            <div>${stock.indicators.trend}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888;">量能</div>
                            <div>${stock.indicators.volume_status}</div>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="background: ${signalColor}; color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 13px; font-weight: bold;">
                                ${stock.signal.signal} (${stock.signal.confidence})
                            </span>
                        </div>
                        <div style="color: #aaa; font-size: 13px; max-width: 60%; text-align: right;">
                            ${stock.signal.action}
                        </div>
                    </div>
                    
                    ${stock.signal.reasons.length > 0 ? `
                        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 12px; color: #888;">
                            💡 ${stock.signal.reasons.join('；')}
                        </div>
                    ` : ''}
                </div>
            `;
        });
        
        html += `</div>
            <div style="margin-top: 15px; padding: 10px; background: rgba(255,215,0,0.1); border-radius: 6px; font-size: 11px; color: #ffd700; text-align: center;">
                ⚠️ 基于实时行情计算，仅供参考，不构成投资建议
            </div>
        `;
        
        resultDiv.innerHTML = html;
    }
}

// 页面加载后初始化
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedStockAnalysis();
    }, 1000); // 延迟1秒等页面渲染
});
