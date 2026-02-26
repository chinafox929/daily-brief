// Daily Brief - User Features
// 账号系统、收藏功能、主题切换、专注模式

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

        updateName(name) {
            this.user.name = name;
            this.saveUser();
            this.renderUserUI();
        },

        incrementVisit() {
            this.user.visitCount++;
            this.saveUser();
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

    // ==================== 主题系统 ====================
    const ThemeSystem = {
        init() {
            this.currentTheme = localStorage.getItem('db_theme') || 'auto';
            this.applyTheme(this.currentTheme);
            this.renderThemeUI();
            this.listenSystemTheme();
        },

        applyTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            
            if (theme === 'auto') {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.body.classList.toggle('dark-mode', prefersDark);
            } else {
                document.body.classList.toggle('dark-mode', theme === 'dark');
            }
            
            localStorage.setItem('db_theme', theme);
        },

        listenSystemTheme() {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (this.currentTheme === 'auto') {
                    document.body.classList.toggle('dark-mode', e.matches);
                }
            });
        },

        cycleTheme() {
            const themes = ['light', 'dark', 'auto'];
            const currentIndex = themes.indexOf(this.currentTheme);
            const nextIndex = (currentIndex + 1) % themes.length;
            this.currentTheme = themes[nextIndex];
            this.applyTheme(this.currentTheme);
            this.renderThemeUI();
            
            const names = { light: '☀️ 日常', dark: '🌙 暗黑', auto: '⚙️ 跟随系统' };
            BookmarkSystem.showToast(names[this.currentTheme]);
        },

        renderThemeUI() {
            const btn = document.getElementById('theme-toggle');
            if (btn) {
                const icons = { light: '☀️', dark: '🌙', auto: '⚙️' };
                btn.textContent = icons[this.currentTheme];
                btn.title = `当前: ${this.currentTheme}`;
            }
        }
    };

    // ==================== 专注模式 ====================
    const FocusMode = {
        init() {
            this.isActive = false;
            this.renderFocusUI();
        },

        toggle() {
            this.isActive = !this.isActive;
            document.body.classList.toggle('focus-mode', this.isActive);
            
            if (this.isActive) {
                // 保存当前滚动位置
                this.scrollPos = window.scrollY;
                // 隐藏非内容元素
                document.querySelectorAll('.nav, .footer, .section:not(.focus-target)').forEach(el => {
                    el.style.display = 'none';
                });
                // 添加退出按钮
                this.addExitButton();
            } else {
                // 恢复所有元素
                document.querySelectorAll('.nav, .footer, .section').forEach(el => {
                    el.style.display = '';
                });
                // 移除退出按钮
                document.getElementById('focus-exit')?.remove();
                // 恢复滚动位置
                window.scrollTo(0, this.scrollPos || 0);
            }
            
            BookmarkSystem.showToast(this.isActive ? '专注模式已开启' : '已退出专注模式');
        },

        addExitButton() {
            const btn = document.createElement('button');
            btn.id = 'focus-exit';
            btn.className = 'focus-exit-btn';
            btn.innerHTML = '✕ 退出专注';
            btn.onclick = () => this.toggle();
            document.body.appendChild(btn);
        },

        renderFocusUI() {
            // 为每个section添加专注模式入口
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
        
        // 添加控制栏
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
                <button id="theme-toggle" title="切换主题">☀️</button>
                <button id="focus-toggle" title="专注模式 (双击段落进入)">🎯</button>
            </div>
        `;
        document.body.insertBefore(bar, document.body.firstChild);
        
        // 绑定事件
        document.getElementById('theme-toggle')?.addEventListener('click', () => ThemeSystem.cycleTheme());
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
                showBookmarks(); // 刷新
            };
        });
        
        document.body.appendChild(modal);
    }
})();