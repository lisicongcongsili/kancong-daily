#!/bin/bash
# ============================================================
# deploy.sh — 将 public/ 目录部署到 GitHub Pages
# 完全免费，无需付费
# 使用前请填写下方变量
# ============================================================

GITHUB_USERNAME="YOUR_GITHUB_USERNAME"   # 你的 GitHub 用户名
REPO_NAME="kancong-daily"                # 仓库名（建议保持不变）

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PUBLIC_DIR="$SCRIPT_DIR/public"

echo "🚀 开始部署到 GitHub Pages..."

# 检查 git 是否安装
if ! command -v git &> /dev/null; then
  echo "❌ 未找到 git，请先安装 Xcode Command Line Tools: xcode-select --install"
  exit 1
fi

# 检查是否已初始化 git 仓库
if [ ! -d "$SCRIPT_DIR/.git" ]; then
  echo "📦 初始化 Git 仓库..."
  cd "$SCRIPT_DIR"
  git init
  git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
fi

cd "$SCRIPT_DIR"

# 将 public/ 内容推送到 gh-pages 分支
echo "📤 推送到 gh-pages 分支..."

# 使用 git worktree 方式部署（不污染主分支）
TMPDIR=$(mktemp -d)
cp -r "$PUBLIC_DIR/." "$TMPDIR/"

git fetch origin gh-pages 2>/dev/null || true

# 切换到 gh-pages 分支
if git show-ref --verify --quiet refs/heads/gh-pages; then
  git checkout gh-pages
else
  git checkout --orphan gh-pages
  git rm -rf . 2>/dev/null || true
fi

# 复制新内容
cp -r "$TMPDIR/." .

# 提交并推送
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M')" --allow-empty
git push origin gh-pages --force

# 切回主分支
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true

rm -rf "$TMPDIR"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 部署成功！"
  echo "🌐 访问地址: https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
  echo "⏱  首次部署约需 1-2 分钟生效"
else
  echo "❌ 部署失败，请检查 GitHub 用户名和仓库是否存在"
  exit 1
fi
