# 云上美术馆 (Cloud Art Museum) - 产品需求文档

## 产品定位
沉浸式在线美术馆体验，以"博物馆级展示"为标准，通过高清艺术图片和深度解读，让用户在数字空间中享受艺术之美。

## 设计语言规范

| 维度 | 规范 |
|------|------|
| **风格** | 深色沉浸感、博物馆氛围 |
| **配色** | 深黑背景(#0a0a0a → #1a1a2e) + 金色点缀(#c4a882) |
| **字体** | 系统字体 + 细体中文 |
| **布局** | 单页长滚动 + 卡片式网格 |
| **动效** | 悬停浮起、渐变过渡 |

## 页面结构

```
【导航栏】Logo + 展馆分类导航

【Hero区】
   - 大标题: "光影与灵魂的对话"
   - 副标题: 介绍语
   - CTA按钮: "开始探索"

【每日精选】
   - 大幅 featured 展示
   - 左图右文布局
   - 作品名 + 艺术家 + 年代
   - 深度鉴赏文字 (200字左右)

【展馆导览】(卡片网格)
   - 现代艺术馆 🎭
   - 印象派馆 🌸
   - 中国书画馆 🏔️
   - 文艺复兴馆 🏛️
   
【页脚】版权信息
```

## HTML模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>云上美术馆 | 沉浸式艺术体验</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            line-height: 1.8;
        }
        .navbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            background: rgba(10,10,10,0.95);
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .logo { font-size: 24px; font-weight: 300; letter-spacing: 4px; }
        .nav-links { display: flex; gap: 30px; }
        .nav-links a { color: #aaa; text-decoration: none; transition: color 0.3s; }
        .nav-links a:hover { color: #fff; }
        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0 20px;
            background: radial-gradient(ellipse at center, rgba(196,168,130,0.1) 0%, transparent 70%);
        }
        .hero h1 { font-size: 72px; font-weight: 200; margin-bottom: 20px; letter-spacing: 12px; }
        .hero p { font-size: 18px; color: #888; max-width: 600px; margin-bottom: 40px; }
        .btn {
            padding: 15px 40px;
            border: 1px solid rgba(196,168,130,0.5);
            background: transparent;
            color: #c4a882;
            text-decoration: none;
            transition: all 0.3s;
            letter-spacing: 2px;
        }
        .btn:hover { background: rgba(196,168,130,0.1); border-color: #c4a882; }
        .section { padding: 80px 40px; max-width: 1400px; margin: 0 auto; }
        .section-title { font-size: 36px; text-align: center; margin-bottom: 60px; font-weight: 300; letter-spacing: 4px; }
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }
        .art-card {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .art-card:hover { transform: translateY(-10px); box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
        .art-img { 
            width: 100%; 
            height: 250px; 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%); 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 60px; 
        }
        .art-info { padding: 25px; }
        .art-info h3 { font-size: 20px; margin-bottom: 8px; font-weight: 400; }
        .art-info p { color: #888; font-size: 14px; margin-bottom: 5px; }
        .art-info .artist { color: #c4a882; }
        .featured {
            background: linear-gradient(135deg, rgba(196,168,130,0.05) 0%, transparent 100%);
            border-left: 3px solid #c4a882;
            padding: 40px;
            margin: 40px 0;
            border-radius: 0 12px 12px 0;
        }
        .featured h2 { font-size: 28px; margin-bottom: 20px; color: #c4a882; }
        .featured-content { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center; }
        .featured-img { 
            height: 400px; 
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            text-align: center;
            padding: 20px;
        }
        .footer {
            text-align: center;
            padding: 60px 40px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #666;
        }
        @media (max-width: 768px) {
            .hero h1 { font-size: 40px; }
            .featured-content { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">云上美术馆</div>
        <div class="nav-links">
            <a href="index.html">首页</a>
            <a href="modern.html">现代艺术</a>
            <a href="chinese.html">中国书画</a>
            <a href="impressionism.html">印象派</a>
            <a href="about.html">关于</a>
        </div>
    </nav>

    <section class="hero">
        <h1>光影与灵魂的对话</h1>
        <p>探索人类艺术史上最伟大的杰作，从文艺复兴到现代主义，从东方水墨到西方油画，在云上美术馆开启一场穿越时空的艺术之旅。</p>
        <a href="#galleries" class="btn">开始探索</a>
    </section>

    <section class="section" id="galleries">
        <h2 class="section-title">今日推荐 · 3月16日</h2>
        
        <div class="featured">
            <h2>🌟 每日精选：《戴珍珠耳环的少女》</h2>
            <div class="featured-content">
                <div class="featured-img">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/0/0f/1665_Girl_with_a_Pearl_Earring.jpg" 
                         alt="戴珍珠耳环的少女" 
                         style="width:100%;height:100%;object-fit:cover;border-radius:8px;">
                </div>
                <div>
                    <p style="font-size: 16px; margin-bottom: 20px;">
                        这幅被誉为"荷兰的蒙娜丽莎"的画作，是维米尔最负盛名的作品。画中少女回眸一瞬，珍珠耳环在暗色背景中熠熠生辉，展现了"光影魔术"的巅峰造诣。
                    </p>
                    <p style="font-size: 14px; color: #888; margin-bottom: 20px;">
                        约翰内斯·维米尔 · 1665年 · 布面油画
                    </p>
                    <a href="modern.html" class="btn">查看详情 →</a>
                </div>
            </div>
        </div>

        <h2 class="section-title" style="margin-top: 80px;">展馆导览</h2>
        
        <div class="gallery-grid">
            <a href="modern.html" class="art-card">
                <div class="art-img" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🎭</div>
                <div class="art-info">
                    <h3>现代艺术馆</h3>
                    <p>表现主义、立体主义、抽象艺术</p>
                    <p class="artist">毕加索、蒙克、康定斯基</p>
                </div>
            </a>
            
            <a href="impressionism.html" class="art-card">
                <div class="art-img" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">🌸</div>
                <div class="art-info">
                    <h3>印象派馆</h3>
                    <p>光影的诗人，色彩的魔术师</p>
                    <p class="artist">莫奈、梵高、雷诺阿</p>
                </div>
            </a>
            
            <a href="chinese.html" class="art-card">
                <div class="art-img" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">🏔️</div>
                <div class="art-info">
                    <h3>中国书画馆</h3>
                    <p>水墨意境，东方美学</p>
                    <p class="artist">范宽、郭熙、张大千</p>
                </div>
            </a>
            
            <a href="renaissance.html" class="art-card">
                <div class="art-img" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">🏛️</div>
                <div class="art-info">
                    <h3>文艺复兴馆</h3>
                    <p>人文主义的曙光</p>
                    <p class="artist">达芬奇、米开朗基罗、拉斐尔</p>
                </div>
            </a>
        </div>
    </section>

    <footer class="footer">
        <p>云上美术馆 · Cloud Art Museum</p>
        <p style="margin-top: 10px;">每日更新 · 图片来源于 Wikimedia Commons</p>
    </footer>
</body>
</html>
```

## 子展馆设计规范

每个子展馆 (modern.html / impressionism.html / chinese.html) 包含：

### 结构
```
【导航栏】同主页

【展馆标题区】
   - 大标题 (如: 现代艺术馆)
   - 简介文字 (50-100字)

【作品网格】
   - 3列响应式网格
   - 每幅作品: 图片 + 名称 + 艺术家 + 简短描述
   
【页脚】同主页
```

### 作品卡片样式
```html
<div class="art-card">
    <img src="Wikimedia图片URL" alt="作品名" class="art-img" style="width:100%;height:300px;object-fit:cover;">
    <div class="art-info">
        <h3>《作品名》</h3>
        <p class="artist">艺术家 · 年份</p>
        <p>作品简介 (50字以内)</p>
    </div>
</div>
```

## 图片来源规范
- **来源**: Wikimedia Commons (公开领域)
- **格式**: 使用高清原图链接
- **示例**: 
  - 《戴珍珠耳环的少女》: https://upload.wikimedia.org/wikipedia/commons/0/0f/1665_Girl_with_a_Pearl_Earring.jpg
  - 《呐喊》: https://upload.wikimedia.org/wikipedia/commons/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg
  - 《星月夜》: https://upload.wikimedia.org/wikipedia/commons/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg

## 技术实现
- **前端**: 纯HTML + CSS (无框架，纯原生)
- **样式**: CSS Grid布局 + Flexbox + 渐变背景
- **图片**: Wikimedia Commons 公开领域高清原图
- **部署**: Nginx静态托管，子目录 `/museum/`
- **自动化**: 每日自动更换"今日推荐"作品

## 文件结构
```
/museum/
├── index.html          # 美术馆主页
├── modern.html         # 现代艺术馆
├── impressionism.html  # 印象派馆
├── chinese.html        # 中国书画馆
├── renaissance.html    # 文艺复兴馆
└── about.html          # 关于页面
```
