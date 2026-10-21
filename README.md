# 数秘のとびら

生年月日から運命数（数秘術）と個人年数を無料診断し、有料の鑑定書へ案内する占いサイト。

- `src/` 編集用のソース（index.html はページ本体の断片）
- `docs/` GitHub Pages で公開されるファイル（`python3 build.py` で生成）

## 公開
GitHub の Settings → Pages で「Deploy from a branch」→ `main` / `/docs` を選ぶ。

## 決済
Stripe の Payment Link を作成し、`src/index.html` の `PAYMENT_LINK` に URL を入れてビルドする。
