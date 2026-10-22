#!/bin/sh
# 数秘のとびら 公開手順: ビルド → 新サイト(suuhi-tobira.github.io)へ反映 → 旧URLの転送ページを反映
set -e
cd "$(dirname "$0")"
python3 build.py
SITE_REPO=../suuhi-tobira.github.io
[ -d "$SITE_REPO/.git" ] || git clone --depth 1 https://github.com/suuhi-tobira/suuhi-tobira.github.io "$SITE_REPO"
find "$SITE_REPO" -mindepth 1 -maxdepth 1 ! -name .git ! -name README.md -exec rm -rf {} +
cp -r site/. "$SITE_REPO/"
( cd "$SITE_REPO" && git add -A && (git diff --cached --quiet || git -c user.name="reiyujiro" -c user.email="reiyujiro260@gmail.com" commit -q -m "サイト更新" ) && git push -q origin main )
git add -A && (git diff --cached --quiet || git -c user.name="reiyujiro" -c user.email="reiyujiro260@gmail.com" commit -q -m "ソース・旧URL転送ページ更新") && git push -q origin main
echo deployed
