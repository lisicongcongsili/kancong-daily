#!/bin/bash
# ============================================================
# deploy.sh — 将日报部署到 GitHub Pages
# 由 CatDesk Automation 每日 09:30 自动调用
# ============================================================

GITHUB_USERNAME="lisicongcongsili"
REPO_NAME="kancong-daily"

# 从本地 .env 文件读取 Token（不上传到 GitHub）
ENV_FILE="$(dirname "$0")/.env"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ 未找到 GITHUB_TOKEN，请确保 .env 文件存在"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 开始部署到 GitHub Pages..."

cd "$SCRIPT_DIR"

# 同步 public/index.html 到根目录（GitHub Pages 从根目录读取）
cp public/index.html index.html

# 提交并推送
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M')" --allow-empty
git push https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git main

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 部署成功！"
  echo "🌐 访问地址: https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
else
  echo "❌ 部署失败"
  exit 1
fi
