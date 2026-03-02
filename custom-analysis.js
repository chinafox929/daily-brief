// 自选分析模块
class CustomAnalysis {
    constructor() {
        this.container = null;
        this.createUI();
    }
    
    createUI() {
        // 找到预测模块，在后面添加自选模块
        const predictionModule = document.getElementById('prediction-module');
        if (!predictionModule) return;
        
        const customDiv = document.createElement('div');
        customDiv.className = 'prediction-module';
        customDiv.style.marginTop = '20px';
        customDiv.innerHTML = `
            <div class="prediction-header">
                <span>🔍</span>
                <h3>自选分析</h3>
            </div>
            <div style="padding: 15px 0;">
                <input type="text" id="stock-input" placeholder="输入股票代码或名称，如：比亚迪、BTC" 
                    style="padding: 10px 15px; border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; 
                           background: rgba(255,255,255,0.1); color: #fff; width: 200px; margin-right: 10px;">
                <button onclick="analyzeStock()" 
                    style="padding: 10px 20px; background: #3498db; color: #fff; border: none; 
                           border-radius: 6px; cursor: pointer;">分析</button>
            </div>
            <div id="analysis-result"></div>
        `;
        
        predictionModule.parentNode.insertBefore(customDiv, predictionModule.nextSibling);
    }
}

// 分析函数
async function analyzeStock() {
    const input = document.getElementById('stock-input').value.trim();
    const resultDiv = document.getElementById('analysis-result');
    
    if (!input) {
        resultDiv.innerHTML = '<p style="color: #e74c3c;">请输入代码或名称</p>';
        return;
    }
    
    resultDiv.innerHTML = '<p style="color: #888;">分析中...</p>';
    
    // 模拟分析结果（实际应该调用API）
    const mockData = generateMockAnalysis(input);
    
    resultDiv.innerHTML = `
        <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 18px; font-weight: bold;">${mockData.name}</span>
                <span style="font-size: 24px; color: ${mockData.change >= 0 ? '#27ae60' : '#e74c3c'};">
                    ${mockData.price} (${mockData.change >= 0 ? '+' : ''}${mockData.change}%)
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);">
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">今日最高</div>
                    <div style="font-weight: bold;">${mockData.high}</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">今日最低</div>
                    <div style="font-weight: bold;">${mockData.low}</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">成交量</div>
                    <div style="font-weight: bold;">${mockData.volume}</div>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <div style="color: #ffd700; margin-bottom: 8px;">💡 分析建议</div>
                <p style="color: #ccc; line-height: 1.6;">${mockData.suggestion}</p>
            </div>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                <span class="signal-badge ${mockData.signal}"
                      style="padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: bold;">
                    ${mockData.signalText}
                </span>
            </div>
        </div>
    `;
}

// 生成模拟分析数据
function generateMockAnalysis(input) {
    const signals = ['buy', 'hold', 'sell'];
    const signalTexts = ['建议买入', '持有观望', '建议卖出'];
    const suggestions = [
        '短期趋势向上，成交量放大，可考虑逢低布局。支撑位明确，风险可控。',
        '近期震荡整理，建议观望等待方向明确。不宜盲目操作。',
        '短期承压，技术指标走弱，建议减仓避险。等待企稳信号。'
    ];
    
    const randomIndex = Math.floor(Math.random() * 3);
    const basePrice = (Math.random() * 100 + 10).toFixed(2);
    const change = (Math.random() * 10 - 5).toFixed(2);
    
    return {
        name: input.toUpperCase(),
        price: basePrice,
        change: change,
        high: (parseFloat(basePrice) * 1.02).toFixed(2),
        low: (parseFloat(basePrice) * 0.98).toFixed(2),
        volume: (Math.random() * 100 + 10).toFixed(1) + '万',
        suggestion: suggestions[randomIndex],
        signal: signals[randomIndex],
        signalText: signalTexts[randomIndex]
    };
}

// 页面加载后初始化
document.addEventListener('DOMContentLoaded', () => {
    new CustomAnalysis();
});
