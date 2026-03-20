# 晨间简报 (Morning Brief) - 产品需求文档

## 产品定位
每日晨间情报简报网站，定位为"高端财经杂志感"的资讯聚合页面，每天早上8点自动更新，为用户提供一站式的股市、AI、国际新闻和艺术鉴赏内容。

## 设计语言规范

| 维度 | 规范 |
|------|------|
| **风格** | 高端、精致、杂志感 (Kinfolk杂志风格) |
| **配色** | 米白背景(#faf9f7) + 金色点缀(#c9a96e) + 深黑文字(#1a1a1a) |
| **字体** | 标题: Cormorant Garamond (serif) + 正文: Inter (sans-serif) |
| **布局** | 充足留白、网格对齐、编号分节 (01/02/03...) |
| **排版** | 大章节编号 + 小标题 + 正文三段式 |

## 页面结构

```
【Header】日期 + 品牌标识 (晨间简报 · Morning Brief)

01 股市概览
   - 三大指数卡片 (沪指/深成指/创业板指)
   - 涨跌幅颜色标识 (红跌绿涨)
   - 成交额、涨跌家数
   - 热点板块标签

02 AI 动态
   - 2-3条AI行业重要新闻
   - 标签分类 (Hardware/Policy/Industry)
   - 来源标注

03 地缘政治 / 国际热点
   - 重要国际事件
   - 影响分析 (市场/政策/产业链)
   - 数据可视化区块

04 热点聚焦
   - 社交媒体热搜汇总
   - 简短点评

05 艺术鉴赏
   - 每日一幅名画
   - 高清图片 (Wikimedia Commons)
   - 作品背景、艺术家介绍
   - 鉴赏心得

【Footer】数据来源声明 + 更新时间
```

## HTML模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>晨间简报 | Morning Brief</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style type="text/tailwindcss">
        @layer base {
            body {
                font-family: 'Inter', sans-serif;
                background-color: #faf9f7;
                color: #1a1a1a;
            }
            h1, h2, h3, .serif {
                font-family: 'Cormorant Garamond', serif;
            }
        }
        @layer components {
            .gold-accent { color: #c9a96e; }
            .gold-border { border-color: #c9a96e; }
            .section-number {
                font-family: 'Cormorant Garamond', serif;
                font-size: 3rem;
                font-weight: 300;
                color: #c9a96e;
                line-height: 1;
            }
        }
    </style>
</head>
<body class="min-h-screen">
    <div class="max-w-5xl mx-auto px-6 py-12">
        
        <!-- Header -->
        <header class="mb-16 pb-8 border-b border-gray-200">
            <div class="flex items-baseline justify-between">
                <div>
                    <p class="text-xs tracking-widest text-gray-500 uppercase mb-2">Daily Intelligence Briefing</p>
                    <h1 class="text-5xl font-light tracking-tight serif">晨间简报</h1>
                </div>
                <div class="text-right">
                    <p class="text-3xl serif gold-accent">03.16</p>
                    <p class="text-sm text-gray-500 mt-1">2026年3月16日 · 周一</p>
                </div>
            </div>
        </header>

        <!-- 01 股市概览 -->
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <span class="section-number">01</span>
                <h2 class="text-2xl font-light serif">股市概览</h2>
            </div>
            
            <div class="grid grid-cols-3 gap-6 mb-8">
                <div class="bg-white p-6 shadow-sm">
                    <p class="text-xs text-gray-500 mb-2">上证指数</p>
                    <p class="text-3xl serif">4066.40</p>
                    <p class="text-red-500 text-sm mt-1">-0.71%</p>
                </div>
                <div class="bg-white p-6 shadow-sm">
                    <p class="text-xs text-gray-500 mb-2">深证成指</p>
                    <p class="text-3xl serif">14181.29</p>
                    <p class="text-red-500 text-sm mt-1">-0.70%</p>
                </div>
                <div class="bg-white p-6 shadow-sm">
                    <p class="text-xs text-gray-500 mb-2">创业板指</p>
                    <p class="text-3xl serif">3316.25</p>
                    <p class="text-green-600 text-sm mt-1">+0.18%</p>
                </div>
            </div>
        </section>

        <!-- 02 AI专区 -->
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <span class="section-number">02</span>
                <h2 class="text-2xl font-light serif">AI 动态</h2>
            </div>
            
            <div class="bg-white p-8 shadow-sm">
                <div class="flex items-start gap-4">
                    <div class="w-2 h-2 rounded-full bg-yellow-400 mt-2 shrink-0"></div>
                    <div>
                        <h3 class="text-lg font-medium mb-2">新闻标题</h3>
                        <p class="text-gray-600 text-sm leading-relaxed">新闻内容...</p>
                        <p class="text-xs text-gray-400 mt-3">来源：新浪科技 · 3月16日</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 03 地缘政治 -->
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <span class="section-number">03</span>
                <h2 class="text-2xl font-light serif">地缘政治</h2>
            </div>
            
            <div class="bg-white p-8 shadow-sm border-l-4 border-red-500">
                <h3 class="text-xl font-medium mb-4 text-red-700">标题</h3>
                <p class="text-gray-700 leading-relaxed">内容...</p>
            </div>
        </section>

        <!-- 04 热点聚焦 -->
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <span class="section-number">04</span>
                <h2 class="text-2xl font-light serif">热点聚焦</h2>
            </div>
            
            <div class="space-y-4">
                <div class="bg-white p-6 shadow-sm flex items-start gap-4">
                    <span class="text-xs font-medium text-white bg-yellow-500 px-2 py-1 rounded">标签</span>
                    <div>
                        <h4 class="font-medium">标题</h4>
                        <p class="text-sm text-gray-600 mt-1">内容...</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 05 艺术鉴赏 -->
        <section class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <span class="section-number">05</span>
                <h2 class="text-2xl font-light serif">艺术鉴赏</h2>
            </div>
            
            <div class="bg-white shadow-sm overflow-hidden">
                <div class="grid md:grid-cols-2">
                    <div class="aspect-square bg-gray-100 flex items-center justify-center">
                        <img src="https://upload.wikimedia.org/..." alt="作品名" class="w-full h-full object-cover">
                    </div>
                    <div class="p-8 flex flex-col justify-center">
                        <p class="text-xs tracking-widest text-gray-500 uppercase mb-2">艺术家 · 年份</p>
                        <h3 class="text-3xl serif mb-4">作品名</h3>
                        <p class="text-gray-600 text-sm leading-relaxed">作品介绍...</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="pt-8 border-t border-gray-200 text-center text-sm text-gray-400">
            <p>晨间简报 · Morning Brief</p>
            <p class="mt-1">每日更新于 08:00 · 数据截至午间收盘</p>
        </footer>

    </div>
</body>
</html>
```

## 技术实现
- **前端**: 纯HTML + TailwindCSS (CDN引入)
- **字体**: Google Fonts (Cormorant Garamond + Inter)
- **部署**: Nginx静态托管
- **自动化**: OpenClaw Cron定时任务
- **数据源**: 实时股市API + 网络搜索 + 人工审核
