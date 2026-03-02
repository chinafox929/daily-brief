// 实时自选分析 - 支持任意股票查询
class RealtimeStockQuery {
    constructor() {
        this.stockMap = {
            "腾讯": "hk00700", "腾讯控股": "hk00700", "00700": "hk00700",
            "阿里巴巴": "hk09988", "阿里": "hk09988", "09988": "hk09988",
            "比亚迪": "sz002594", "002594": "sz002594",
            "茅台": "sh600519", "贵州茅台": "sh600519", "600519": "sh600519",
            "宁德时代": "sz300750", "300750": "sz300750",
            "中国平安": "sh601318", "601318": "sh601318",
            "招商银行": "sh600036", "600036": "sh600036"
        };
        this.currentSymbol = null;
        this.autoRefreshInterval = null;
    }
    
    async query(input) {
        const symbol = this.stockMap[input] || this.guessSymbol(input);
        if (!symbol) return { error: "未找到股票" };
        
        const data = await this.fetchData(symbol);
        if (!data) return { error: "获取数据失败" };
        
        return this.analyze(data);
    }
    
    guessSymbol(input) {
        if (/^\d{6}$/.test(input)) {
            if (input.startsWith('6')) return `sh${input}`;
            if (input.startsWith('0') || input.startsWith('3')) return `sz${input}`;
        }
        return null;
    }
    
    async fetchData(symbol) {
        try {
            const url = `https://hq.sinajs.cn/list=${symbol}`;
            const response = await fetch(url);
            const text = await response.text();
            const data = text.split('"')[1].split(',');
            if (data.length < 30) return null;
            
            return {
                symbol, name: data[0], price: parseFloat(data[3]),
                open: parseFloat(data[1]), high: parseFloat(data[4]),
                low: parseFloat(data[5]), prevClose: parseFloat(data[2]),
                volume: parseInt(data[8])
            };
        } catch (e) { return null; }
    }
    
    analyze(stock) {
        const change = ((stock.price - stock.prevClose) / stock.prevClose * 100);
        const position = ((stock.price - stock.low) / (stock.high - stock.low) * 100);
        
        let score = 0, signals = [];
        
        if (change > 3) { score += 3; signals.push("涨幅超3%，短期强势"); }
        else if (change > 1) { score += 1; signals.push("小幅上涨"); }
        else if (change < -3) { score -= 3; signals.push("跌幅较大"); }
        
        if (position > 90) { score -= 2; signals.push("接近高点，追高风险"); }
        else if (position < 10) { score += 2; signals.push("接近低点，或有支撑"); }
        
        let signal = score >= 3 ? "买入" : score > 0 ? "买入" : score === 0 ? "持有" : score > -3 ? "卖出" : "卖出";
        let action = score >= 3 ? "趋势向好，可考虑介入" : score > 0 ? "有上涨迹象" : score === 0 ? "观望为主" : "建议减仓避险";
        
        const tradePoints = [];
        if (change < -2 && position < 20) tradePoints.push({ type: "买入时机", price: stock.low.toFixed(2), reason: "超跌反弹" });
        if (change > 3 && position > 80) tradePoints.push({ type: "卖出时机", price: stock.high.toFixed(2), reason: "高位获利" });
        
        return { ...stock, change: change.toFixed(2), position: position.toFixed(1), signal, action, score, signals, tradePoints };
    }
}

async function queryStockRealtime() {
    const input = document.getElementById('stock-input').value.trim();
    const resultDiv = document.getElementById('analysis-result');
    
    if (!input) { resultDiv.innerHTML = '<p style="color:#e74c3c">请输入股票名称或代码</p>'; return; }
    
    resultDiv.innerHTML = '<p style="color:#888">分析中...</p>';
    
    const query = new RealtimeStockQuery();
    const data = await query.query(input);
    
    if (data.error) { resultDiv.innerHTML = `<p style="color:#e74c3c">${data.error}</p>`; return; }
    
    const colors = { '买入': '#27ae60', '卖出': '#e74c3c', '持有': '#f39c12' };
    const cColor = data.change >= 0 ? '#27ae60' : '#e74c3c';
    
    let html = `<div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:15px;margin-top:15px">`;
    html += `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px">`;
    html += `<div><span style="font-size:18px;font-weight:bold">${data.name}</span>`;
    html += `<span style="color:#888;font-size:12px;margin-left:8px">${data.symbol}</span></div>`;
    html += `<div style="text-align:right"><div style="font-size:24px;font-weight:bold">${data.price.toFixed(2)}</div>`;
    html += `<div style="color:${cColor}">${data.change >= 0 ? '+' : ''}${data.change}%</div></div></div>`;
    
    html += `<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:15px 0;padding:10px 0;border-top:1px solid rgba(255,255,255,0.1);border-bottom:1px solid rgba(255,255,255,0.1);font-size:13px">`;
    html += `<div style="text-align:center"><div style="color:#888">最高</div><div>${data.high.toFixed(2)}</div></div>`;
    html += `<div style="text-align:center"><div style="color:#888">最低</div><div>${data.low.toFixed(2)}</div></div>`;
    html += `<div style="text-align:center"><div style="color:#888">位置</div><div>${data.position}%</div></div></div>`;
    
    html += `<div style="display:flex;justify-content:space-between;align-items:center;margin:15px 0">`;
    html += `<span style="background:${colors[data.signal]};color:#fff;padding:5px 15px;border-radius:15px;font-weight:bold">${data.signal}</span>`;
    html += `<span style="color:#aaa;font-size:13px">${data.action}</span></div>`;
    
    html += `<div style="margin:15px 0;padding:10px;background:rgba(255,215,0,0.1);border-radius:6px">`;
    html += `<div style="color:#ffd700;margin-bottom:8px">📊 分析要点</div>`;
    data.signals.forEach(s => html += `<div style="color:#ccc;font-size:13px;margin:4px 0">• ${s}</div>`);
    html += `</div>`;
    
    if (data.tradePoints.length > 0) {
        html += `<div style="margin:15px 0;padding:10px;background:rgba(39,174,96,0.1);border-radius:6px">`;
        html += `<div style="color:#27ae60;margin-bottom:8px">⏰ 买卖时机</div>`;
        data.tradePoints.forEach(p => {
            html += `<div style="color:#ccc;font-size:13px;margin:4px 0">${p.type}: ${p.price} - ${p.reason}</div>`;
        });
        html += `</div>`;
    }
    
    html += `</div>`;
    resultDiv.innerHTML = html;
    
    // 启动自动刷新
    startAutoRefresh(input);
}

// 自动刷新功能
function startAutoRefresh(symbol) {
    // 清除之前的定时器
    if (window.autoRefreshInterval) {
        clearInterval(window.autoRefreshInterval);
    }
    
    // 每30秒刷新一次
    window.autoRefreshInterval = setInterval(() => {
        console.log('自动刷新:', symbol);
        queryStockRealtime();
    }, 30000);
    
    // 显示刷新提示
    const resultDiv = document.getElementById('analysis-result');
    const refreshIndicator = document.createElement('div');
    refreshIndicator.id = 'refresh-indicator';
    refreshIndicator.style.cssText = 'text-align:center;color:#888;font-size:12px;margin-top:10px;';
    refreshIndicator.innerHTML = '⏱️ 每30秒自动刷新';
    resultDiv.appendChild(refreshIndicator);
}

// 页面关闭时清除定时器
window.addEventListener('beforeunload', () => {
    if (window.autoRefreshInterval) {
        clearInterval(window.autoRefreshInterval);
    }
});
