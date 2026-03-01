// 突发新闻滚动组件
class BreakingNewsTicker {
    constructor() {
        this.container = null;
        this.data = null;
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.createTicker();
        this.startAutoRefresh();
    }
    
    async loadData() {
        try {
            const response = await fetch('breaking-news.json?t=' + Date.now());
            this.data = await response.json();
        } catch (error) {
            console.error('加载突发新闻失败:', error);
            this.data = { breakingNews: [] };
        }
    }
    
    createTicker() {
        if (!this.data.breakingNews || this.data.breakingNews.length === 0) {
            return;
        }
        
        // 添加 body 类名
        document.body.classList.add('has-ticker');
        
        // 创建滚动条容器
        this.container = document.createElement('div');
        this.container.className = 'breaking-news-ticker';
        
        // 创建标签
        const label = document.createElement('div');
        label.className = 'breaking-news-label';
        label.textContent = '突发';
        this.container.appendChild(label);
        
        // 创建内容区域
        const content = document.createElement('div');
        content.className = 'breaking-news-content';
        
        // 创建滚动区域
        const scroll = document.createElement('div');
        scroll.className = 'breaking-news-scroll';
        
        // 添加新闻项（复制一份实现无缝滚动）
        const newsItems = [...this.data.breakingNews, ...this.data.breakingNews];
        
        newsItems.forEach(news => {
            const item = document.createElement('div');
            item.className = 'breaking-news-item';
            
            const time = document.createElement('span');
            time.className = 'breaking-news-time';
            time.textContent = news.time.split(' ')[1]; // 只显示时间
            
            const category = document.createElement('span');
            category.className = `breaking-news-category urgency-${news.urgency}`;
            category.textContent = news.category;
            
            const title = document.createElement('a');
            title.className = 'breaking-news-title';
            title.href = news.url;
            title.textContent = news.title;
            title.target = '_blank';
            
            item.appendChild(time);
            item.appendChild(category);
            item.appendChild(title);
            scroll.appendChild(item);
        });
        
        content.appendChild(scroll);
        this.container.appendChild(content);
        
        // 插入到 body 开头
        document.body.insertBefore(this.container, document.body.firstChild);
    }
    
    startAutoRefresh() {
        // 每5分钟刷新一次数据
        setInterval(() => {
            this.loadData().then(() => {
                this.updateTicker();
            });
        }, 5 * 60 * 1000);
    }
    
    updateTicker() {
        if (!this.container) return;
        
        const scroll = this.container.querySelector('.breaking-news-scroll');
        if (!scroll) return;
        
        // 清空并重新填充
        scroll.innerHTML = '';
        
        const newsItems = [...this.data.breakingNews, ...this.data.breakingNews];
        
        newsItems.forEach(news => {
            const item = document.createElement('div');
            item.className = 'breaking-news-item';
            
            const time = document.createElement('span');
            time.className = 'breaking-news-time';
            time.textContent = news.time.split(' ')[1];
            
            const category = document.createElement('span');
            category.className = `breaking-news-category urgency-${news.urgency}`;
            category.textContent = news.category;
            
            const title = document.createElement('a');
            title.className = 'breaking-news-title';
            title.href = news.url;
            title.textContent = news.title;
            title.target = '_blank';
            
            item.appendChild(time);
            item.appendChild(category);
            item.appendChild(title);
            scroll.appendChild(item);
        });
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new BreakingNewsTicker();
});
