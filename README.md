# 闪购营销双轨日报 · KANCONG

每日自动更新的营销情报网站，完全免费托管在 GitHub Pages。

---

## 🚀 首次部署（只需做一次）

### 第一步：注册 GitHub 账号（免费）

打开 https://github.com/signup，注册一个免费账号，记住你的用户名。

### 第二步：创建仓库

登录后，点击右上角 **+** → **New repository**，填写：
- Repository name: `kancong-daily`
- 选择 **Public**（必须是公开仓库才能用免费 GitHub Pages）
- 点击 **Create repository**

### 第三步：配置部署脚本

打开 `deploy.sh`，把第一行的 `YOUR_GITHUB_USERNAME` 改成你的 GitHub 用户名：

```bash
GITHUB_USERNAME="你的用户名"
```

### 第四步：初始化并推送

在终端执行：

```bash
cd /Users/lisicong/Desktop/kancong-daily
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin https://github.com/你的用户名/kancong-daily.git
git push -u origin main
```

### 第五步：开启 GitHub Pages

在 GitHub 仓库页面：
1. 点击 **Settings** → 左侧 **Pages**
2. Source 选择 **Deploy from a branch**
3. Branch 选择 **gh-pages** → **/ (root)**
4. 点击 **Save**

等待约 1-2 分钟，你的网站就会在以下地址上线：

```
https://你的用户名.github.io/kancong-daily/
```

---

## 📅 每日更新流程

CatDesk Automation 每天 09:30 自动执行，流程如下：

1. 抓取当日营销快讯和机构报告
2. 生成新的 `public/index.html`
3. 运行 `deploy.sh` 推送到 GitHub Pages
4. 发送日报图片 + 网站链接到大象群 68376031970

---

## 📁 目录结构

```
kancong-daily/
├── public/           ← 网站文件（GitHub Pages 部署此目录）
│   ├── index.html    ← 当日日报
│   └── archive/      ← 历史归档
├── template.html     ← HTML 模板
├── generate.py       ← 内容生成脚本
├── deploy.sh         ← GitHub Pages 部署脚本
└── README.md
```

---

## 🔗 相关链接

- 网站地址：`https://你的用户名.github.io/kancong-daily/`
- 大象群：68376031970
- 内容来源：SocialBeta · 数英 · 刀法 · 高盛 · 瑞银 · 36kr · 晚点
