// Daily Brief - User Features
// 账号系统、收藏功能、主题切换、专注模式（含番茄钟）

(function() {
    'use strict';

    // ==================== 用户账号系统 ====================
    const UserSystem = {
        init() {
            this.user = this.loadUser();
            if (!this.user) {
                this.createUser();
            }
            this.renderUserUI();
        },

        loadUser() {
            const data = localStorage.getItem('db_user');
            return data ? JSON.parse(data) : null;
        },

        createUser() {
            this.user = {
                id: 'user_' + Date.now().toString(36),
                name: '访客' + Math.floor(Math.random() * 1000),
                createdAt: new Date().toISOString(),
                visitCount: 1
            };
            this.saveUser();
        },

        saveUser() {
            localStorage.setItem('db_user', JSON.stringify(this.user));
        },

        renderUserUI() {
            const userEl = document.getElementById('user-display');
            if (userEl) {
                userEl.textContent = this.user.name;
            }
        }
    };

    // ==================== 收藏系统 ====================
    const BookmarkSystem = {
        init() {
            this.bookmarks = this.loadBookmarks();
            this.renderBookmarkButtons();
        },

        loadBookmarks() {
            const data = localStorage.getItem('db_bookmarks');
            return data ? JSON.parse(data) : [];
        },

        saveBookmarks() {
            localStorage.setItem('db_bookmarks', JSON.stringify(this.bookmarks));
        },

        add(sectionId, title, content) {
            const bookmark = {
                id: Date.now().toString(),
                sectionId,
                title,
                content: content.substring(0, 200) + '...',
                date: document.querySelector('.date')?.textContent || '',
                url: window.location.href,
                createdAt: new Date().toISOString()
            };
            this.bookmarks.unshift(bookmark);
            this.saveBookmarks();
            this.renderBookmarkButtons();
            this.showToast('已收藏');
        },

        remove(id) {
            this.bookmarks = this.bookmarks.filter(b => b.id !== id);
            this.saveBookmarks();
            this.renderBookmarkButtons();
            this.showToast('已取消收藏');
        },

        isBookmarked(sectionId) {
            const date = document.querySelector('.date')?.textContent || '';
            return this.bookmarks.some(b => b.sectionId === sectionId && b.date === date);
        },

        renderBookmarkButtons() {
            document.querySelectorAll('.section').forEach(section => {
                const titleEl = section.querySelector('.section-title');
                if (!titleEl || titleEl.querySelector('.bookmark-btn')) return;

                const btn = document.createElement('button');
                btn.className = 'bookmark-btn';
                btn.innerHTML = this.isBookmarked(section.id) ? '★' : '☆';
                btn.onclick = (e) => {
                    e.stopPropagation();
                    if (this.isBookmarked(section.id)) {
                        const bm = this.bookmarks.find(b => b.sectionId === section.id);
                        if (bm) this.remove(bm.id);
                    } else {
                        const title = titleEl.textContent.trim();
                        const content = section.textContent.substring(0, 300);
                        this.add(section.id, title, content);
                    }
                };
                titleEl.appendChild(btn);
            });
        },

        showToast(msg) {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = msg;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2000);
        }
    };

    // ==================== 主题系统（6种视觉风格） ====================
    const ThemeSystem = {
        themes: [
            { id: 'zen', name: '禅意', icon: '🍵', desc: '温暖米色调，适合静心阅读' },
            { id: 'dark', name: '暗黑', icon: '🌙', desc: '深蓝紫色，夜间护眼' },
            { id: 'modern', name: '现代', icon: '⚡', desc: '简洁白灰，商务风格' },
            { id: 'paper', name: '纸质', icon: '📜', desc: '仿纸张纹理，复古感' },
            { id: 'forest', name: '森林', icon: '🌲', desc: '绿色调，自然清新' },
            { id: 'auto', name: '跟随系统', icon: '⚙️', desc: '自动切换明暗' }
        ],

        init() {
            this.currentTheme = localStorage.getItem('db_theme') || 'zen';
            this.applyTheme(this.currentTheme);
            this.renderThemeUI();
            this.listenSystemTheme();
        },

        applyTheme(themeId) {
            document.documentElement.setAttribute('data-theme', themeId);
            document.body.className = document.body.className.replace(/theme-\w+/g, '');
            document.body.classList.add(`theme-${themeId}`);
            
            if (themeId === 'auto') {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.body.classList.toggle('dark-mode', prefersDark);
            }
            
            localStorage.setItem('db_theme', themeId);
        },

        listenSystemTheme() {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (this.currentTheme === 'auto') {
                    document.body.classList.toggle('dark-mode', e.matches);
                }
            });
        },

        openThemeSelector() {
            const modal = document.createElement('div');
            modal.className = 'theme-modal';
            modal.innerHTML = `
                <div class="theme-content">
                    <div class="theme-header">
                        <h3>选择主题</h3>
                        <button class="close-btn">✕</button>
                    </div>
                    <div class="theme-list">
                        ${this.themes.map(t => `
                            <div class="theme-item ${this.currentTheme === t.id ? 'active' : ''}" data-theme="${t.id}">
                                <span class="theme-icon">${t.icon}</span>
                                <div class="theme-info">
                                    <div class="theme-name">${t.name}</div>
                                    <div class="theme-desc">${t.desc}</div>
                                </div>
                                ${this.currentTheme === t.id ? '<span class="check">✓</span>' : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            
            modal.querySelector('.close-btn').onclick = () => modal.remove();
            modal.onclick = (e) => {
                if (e.target === modal) modal.remove();
            };
            modal.querySelectorAll('.theme-item').forEach(item => {
                item.onclick = () => {
                    this.currentTheme = item.dataset.theme;
                    this.applyTheme(this.currentTheme);
                    this.renderThemeUI();
                    modal.remove();
                    const theme = this.themes.find(t => t.id === this.currentTheme);
                    BookmarkSystem.showToast(`已切换到：${theme.icon} ${theme.name}`);
                };
            });
            
            document.body.appendChild(modal);
        },

        renderThemeUI() {
            const btn = document.getElementById('theme-toggle');
            if (btn) {
                const theme = this.themes.find(t => t.id === this.currentTheme);
                btn.textContent = theme?.icon || '🍵';
                btn.title = `当前主题：${theme?.name || '禅意'}`;
            }
        }
    };

    // ==================== 专注模式（含番茄钟） ====================
    const FocusMode = {
        timer: null,
        timeLeft: 25 * 60,
        isRunning: false,
        isActive: false,

        init() {
            this.loadSettings();
            this.renderFocusUI();
        },

        loadSettings() {
            const settings = localStorage.getItem('db_focus_settings');
            if (settings) {
                const s = JSON.parse(settings);
                this.timeLeft = s.duration || 25 * 60;
            }
        },

        saveSettings() {
            localStorage.setItem('db_focus_settings', JSON.stringify({
                duration: this.timeLeft
            }));
        },

        toggle() {
            if (!this.isActive) {
                this.enter();
            } else {
                this.exit();
            }
        },

        enter() {
            this.isActive = true;
            document.body.classList.add('focus-mode');
            this.scrollPos = window.scrollY;
            
            document.querySelectorAll('.nav, .footer, .section:not(.focus-target)').forEach(el => {
                el.style.display = 'none';
            });
            
            this.addFocusUI();
            this.startTimer();
        },

        exit() {
            this.isActive = false;
            this.pauseTimer();
            document.body.classList.remove('focus-mode');
            
            document.querySelectorAll('.nav, .footer, .section').forEach(el => {
                el.style.display = '';
            });
            
            document.getElementById('focus-ui')?.remove();
            window.scrollTo(0, this.scrollPos || 0);
        },

        addFocusUI() {
            const ui = document.createElement('div');
            ui.id = 'focus-ui';
            ui.innerHTML = `
                <div class="pomodoro-timer">
                    <div class="timer-display">${this.formatTime()}</div>
                    <div class="timer-controls">
                        <button id="timer-toggle">${this.isRunning ? '⏸️' : '▶️'}</button>
                        <button id="timer-reset">🔄</button>
                        <button id="timer-settings">⚙️</button>
                    </div>
                    <div class="timer-status">${this.isRunning ? '专注中...' : '已暂停'}</div>
                </div>
                <button class="focus-exit-btn">✕ 退出专注</button>
            `;
            document.body.appendChild(ui);
            
            ui.querySelector('.focus-exit-btn').onclick = () => this.exit();
            ui.querySelector('#timer-toggle').onclick = () => this.toggleTimer();
            ui.querySelector('#timer-reset').onclick = () => this.resetTimer();
            ui.querySelector('#timer-settings').onclick = () => this.openSettings();
        },

        startTimer() {
            this.isRunning = true;
            this.updateTimerUI();
            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                    this.updateTimerUI();
                } else {
                    this.completeTimer();
                }
            }, 1000);
        },

        pauseTimer() {
            this.isRunning = false;
            clearInterval(this.timer);
            this.updateTimerUI();
        },

        toggleTimer() {
            if (this.isRunning) {
                this.pauseTimer();
            } else {
                this.startTimer();
            }
        },

        resetTimer() {
            this.pauseTimer();
            this.timeLeft = 25 * 60;
            this.updateTimerUI();
        },

        completeTimer() {
            this.pauseTimer();
            BookmarkSystem.showToast('🎉 专注时间结束！');
        },

        formatTime() {
            const mins = Math.floor(this.timeLeft / 60);
            const secs = this.timeLeft % 60;
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        },

        updateTimerUI() {
            const display = document.querySelector('.timer-display');
            const status = document.querySelector('.timer-status');
            const toggle = document.getElementById('timer-toggle');
            if (display) display.textContent = this.formatTime();
            if (status) status.textContent = this.isRunning ? '专注中...' : '已暂停';
            if (toggle) toggle.textContent = this.isRunning ? '⏸️' : '▶️';
        },

        openSettings() {
            const mins = Math.floor(this.timeLeft / 60);
            const newMins = prompt('设置专注时长（分钟）：', mins);
            if (newMins && !isNaN(newMins)) {
                this.timeLeft = parseInt(newMins) * 60;
                this.saveSettings();
                this.updateTimerUI();
            }
        },

        renderFocusUI() {
            document.querySelectorAll('.section').forEach(section => {
                section.addEventListener('dblclick', () => {
                    section.classList.add('focus-target');
                    this.toggle();
                });
            });
        }
    };

    // ==================== 初始化 ====================
    document.addEventListener('DOMContentLoaded', () => {
        UserSystem.init();
        BookmarkSystem.init();
        ThemeSystem.init();
        FocusMode.init();
        addControlBar();
    });

    function addControlBar() {
        const bar = document.createElement('div');
        bar.className = 'control-bar';
        bar.innerHTML = `
            <div class="control-left">
                <span class="user-greeting">👋 <span id="user-display">访客</span></span>
            </div>
            <div class="control-right">
                <button id="bookmark-view" title="我的收藏">★</button>
                <button id="theme-toggle" title="切换主题">🍵</button>
                <button id="focus-toggle" title="专注模式">🎯</button>
            </div>
        `;
        document.body.insertBefore(bar, document.body.firstChild);
        
        document.getElementById('theme-toggle')?.addEventListener('click', () => ThemeSystem.openThemeSelector());
        document.getElementById('focus-toggle')?.addEventListener('click', () => FocusMode.toggle());
        document.getElementById('bookmark-view')?.addEventListener('click', showBookmarks);
    }

    function showBookmarks() {
        const bookmarks = BookmarkSystem.bookmarks;
        if (bookmarks.length === 0) {
            BookmarkSystem.showToast('暂无收藏');
            return;
        }
        
        const modal = document.createElement('div');
        modal.className = 'bookmark-modal';
        modal.innerHTML = `
            <div class="bookmark-content">
                <div class="bookmark-header">
                    <h3>我的收藏 (${bookmarks.length})</h3>
                    <button class="close-btn">✕</button>
                </div>
                <div class="bookmark-list">
                    ${bookmarks.map(b => `
                        <div class="bookmark-item">
                            <div class="bookmark-title">${b.title}</div>
                            <div class="bookmark-date">${b.date}</div>
                            <div class="bookmark-preview">${b.content}</div>
                            <button class="delete-btn" data-id="${b.id}">删除</button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        modal.querySelector('.close-btn').onclick = () => modal.remove();
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };
        modal.querySelectorAll('.delete-btn').forEach(btn => {
            btn.onclick = () => {
                BookmarkSystem.remove(btn.dataset.id);
                showBookmarks();
            };
        });
        
        document.body.appendChild(modal);
    }
})();