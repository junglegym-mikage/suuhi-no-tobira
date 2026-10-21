"""数秘のとびら ビルド: src/ と content/ から docs/（GitHub Pages 公開用）を作る。
使い方: python3 build.py
"""
import os, shutil, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "content"))
from number_texts import NUMBERS  # noqa: E402

SITE = "https://junglegym-mikage.github.io/suuhi-no-tobira"
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "docs")
os.makedirs(os.path.join(OUT, "number"), exist_ok=True)

META = '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'

def og(title, desc, path):
    return (f'<meta name="description" content="{html.escape(desc)}">'
            f'<link rel="canonical" href="{SITE}/{path}">'
            f'<meta property="og:title" content="{html.escape(title)}">'
            f'<meta property="og:description" content="{html.escape(desc)}">'
            f'<meta property="og:type" content="website"><meta property="og:url" content="{SITE}/{path}">'
            '<meta property="og:site_name" content="数秘のとびら"><meta name="twitter:card" content="summary">')

# 1) トップページ: 断片を完全なHTML文書に包む
frag = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
i = frag.index("</style>") + len("</style>")
top_desc = "生年月日を入れるだけ。数秘術であなたの運命数と、2026年の流れを無料で診断します。"
frag_head = frag[:i].replace(f'<meta name="description" content="{top_desc}">', og("数秘のとびら｜無料の数秘術診断", top_desc, ""))
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    f'<!doctype html>\n<html lang="ja"><head>{META}\n{frag_head}\n'
    '<style>body{margin:0}[hidden]{display:none!important}</style>\n</head><body>'
    + frag[i:] + "\n</body></html>\n")

# 2) 法的ページはそのままコピー
for n in ("legal", "privacy", "terms"):
    shutil.copy(os.path.join(SRC, f"{n}.html"), os.path.join(OUT, f"{n}.html"))

# 3) 運命数ごとの解説ページ
STYLE = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Cormorant+Garamond:wght@600&display=swap">
<style>
:root{--paper:#f3f0e8;--ink:#1d2433;--soft:#4d566a;--line:#cfc8b6;--gold:#9a7428;--seal:#a83a2c;--card:#fbf9f4;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#151a24;--ink:#ece6d8;--soft:#a9adb8;--line:#343c4d;--gold:#d2ab5c;--seal:#e07a63;--card:#1a2030;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#151a24;--ink:#ece6d8;--soft:#a9adb8;--line:#343c4d;--gold:#d2ab5c;--seal:#e07a63;--card:#1a2030;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Zen Kaku Gothic New","Hiragino Sans",system-ui,sans-serif;line-height:1.95;font-size:16px;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:760px;margin:0 auto;padding-block:20px 48px}
a{color:var(--ink)}
.crumb{font-size:.82rem;color:var(--soft)}
.crumb a{color:var(--soft)}
.head{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:end;border-bottom:1px solid var(--line);padding-block:24px 16px}
.big{font-family:"Cormorant Garamond",serif;font-weight:600;font-size:7rem;line-height:.85;color:var(--gold)}
h1{font-family:"Shippori Mincho B1",serif;font-weight:800;font-size:clamp(1.4rem,4vw,2rem);line-height:1.4;margin:0;text-wrap:balance}
.kw{color:var(--seal);font-size:.85rem;letter-spacing:.15em;margin:4px 0 0}
h2{font-family:"Shippori Mincho B1",serif;font-size:1.2rem;margin:32px 0 4px;padding-bottom:4px;border-bottom:1px solid var(--line)}
p{margin:0 0 8px}
dl.facts{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;margin:16px 0 0;font-size:.95rem}
dl.facts dt{color:var(--soft)}
dl.facts dd{margin:0}
.cta{margin-top:40px;background:var(--card);border:1px solid var(--line);padding:24px}
.cta a.btn{display:inline-block;margin-top:8px;background:var(--ink);color:var(--paper);text-decoration:none;font-family:"Shippori Mincho B1",serif;font-weight:700;letter-spacing:.15em;padding:12px 20px}
.others{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.others a{font-family:"Cormorant Garamond",serif;font-size:1.3rem;font-weight:600;text-decoration:none;border:1px solid var(--line);min-width:3rem;text-align:center;padding:2px 8px}
.others a[aria-current]{background:var(--ink);color:var(--paper)}
footer{border-top:1px solid var(--line);margin-top:40px;padding-top:16px;font-size:.78rem;color:var(--soft);display:flex;flex-wrap:wrap;gap:8px 20px}
footer a{color:var(--soft)}
@media (max-width:560px){.big{font-size:5rem}.head{gap:16px}}
</style>"""

ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]

def others(cur=None):
    return '<div class="others">' + "".join(
        f'<a href="{n}.html"{" aria-current=\"page\"" if n == cur else ""}>{n}</a>' for n in ORDER) + "</div>"

FOOT = ('<footer><span>© 2026 数秘のとびら</span><a href="../legal.html">特定商取引法に基づく表記</a>'
        '<a href="../privacy.html">プライバシーポリシー</a><a href="../terms.html">利用規約</a></footer>')

for n, d in NUMBERS.items():
    title = f"運命数{n}の性格・恋愛・仕事・相性｜{d['name']}"
    desc = f"数秘術の運命数{n}（{d['kw']}）の性格、恋愛傾向、向いている仕事、金運、相性のよい数字を解説します。"
    master = "（マスターナンバー）" if n in (11, 22, 33) else ""
    compat = "・".join(str(c) for c in d["compat"])
    body = f"""<div class="wrap">
<p class="crumb"><a href="../index.html">数秘のとびら</a> › <a href="index.html">運命数の意味</a> › 運命数{n}</p>
<div class="head"><div class="big">{n}</div><div><h1>運命数{n}{master}<br>{d['name']}</h1><p class="kw">{d['kw']}</p></div></div>
<p style="margin-top:16px">{d['intro']}</p>
<dl class="facts"><dt>キーワード</dt><dd>{d['kw']}</dd><dt>相性のよい数字</dt><dd>{compat}</dd><dt>ラッキーカラー</dt><dd>{d['color']}</dd></dl>
<h2>運命数{n}の性格</h2><p>{d['personality']}</p>
<h2>運命数{n}の恋愛・結婚</h2><p>{d['love']}</p>
<h2>運命数{n}に向いている仕事</h2><p>{d['work']}</p>
<h2>運命数{n}の金運</h2><p>{d['money']}</p>
<h2>運命数{n}の人へのメッセージ</h2><p>{d['advice']}</p>
<div class="cta"><strong>あなたの運命数は？</strong><p>生年月日を入れるだけで、運命数と2026年の流れがわかります。登録不要・無料です。</p><a class="btn" href="../index.html">無料で診断する</a></div>
<h2>ほかの運命数を見る</h2>{others(n)}
{FOOT}</div>"""
    open(os.path.join(OUT, "number", f"{n}.html"), "w", encoding="utf-8").write(
        f'<!doctype html>\n<html lang="ja"><head>{META}<title>{title}｜数秘のとびら</title>{og(title, desc, f"number/{n}.html")}{STYLE}</head><body>{body}</body></html>\n')

# 一覧ページ
rows = "".join(f'<h2><a href="{n}.html">運命数{n}　{d["name"]}</a></h2><p>{d["kw"]}。{d["intro"]}</p>' for n, d in NUMBERS.items())
idx_title = "運命数1〜33の意味一覧"
idx_desc = "数秘術の運命数1〜9とマスターナンバー11・22・33の意味を一覧で紹介します。"
open(os.path.join(OUT, "number", "index.html"), "w", encoding="utf-8").write(
    f'<!doctype html>\n<html lang="ja"><head>{META}<title>{idx_title}｜数秘のとびら</title>{og(idx_title, idx_desc, "number/")}{STYLE}</head><body><div class="wrap">'
    f'<p class="crumb"><a href="../index.html">数秘のとびら</a> › 運命数の意味</p><h1 style="margin-top:16px">{idx_title}</h1>'
    f'<p>{idx_desc}運命数は、生年月日の数字をすべて足して一桁にした数字です（11・22・33はそのまま扱います）。</p>{others()}{rows}'
    '<div class="cta"><strong>自分の運命数を知りたい方へ</strong><p>生年月日を入れるだけで自動で計算します。</p><a class="btn" href="../index.html">無料で診断する</a></div>'
    f'{FOOT}</div></body></html>\n')

# 4) サイトマップ・robots
urls = ["", "number/"] + [f"number/{n}.html" for n in ORDER] + ["legal.html", "privacy.html", "terms.html"]
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("built:", len(urls), "pages")
