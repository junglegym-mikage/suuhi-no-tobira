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
    cl = "・".join(f'<a href="../compat/{min(n,m)}-{max(n,m)}.html">{m}</a>' for m in ORDER)
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
<h2>運命数{n}と他の数字の相性</h2><p>{cl}</p>
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

# 3b) 運命数どうしの相性ページ（78ペア）
from compat_texts import TRAITS  # noqa: E402
os.makedirs(os.path.join(OUT, "compat"), exist_ok=True)
FOOT_C = FOOT
CSTYLE = STYLE.replace("</style>", """
.pair{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding-block:20px 12px;border-bottom:1px solid var(--line)}
.pair .big{font-size:5.5rem}
.pair .x{font-size:2rem;color:var(--soft)}
.badge{display:inline-block;font-family:"Shippori Mincho B1",serif;font-weight:800;font-size:1.05rem;padding:2px 12px;border:1px solid var(--gold);color:var(--gold)}
.grid{overflow-x:auto;margin-top:8px}
.grid table{border-collapse:collapse;font-variant-numeric:tabular-nums}
.grid th,.grid td{border:1px solid var(--line);padding:6px 8px;text-align:center;min-width:2.4rem}
.grid th{color:var(--soft);font-weight:500}
.grid a{text-decoration:none;font-weight:700}
.calc{background:var(--card);border:1px solid var(--line);padding:16px;margin-top:16px;display:grid;gap:8px}
.calc input{font:inherit;padding:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);width:10em}
.calc button{font:inherit;font-weight:700;background:var(--ink);color:var(--paper);border:0;padding:10px 16px;cursor:pointer;justify-self:start}
</style>""")

def level(a, b):
    if a == b: return ("似た者同士", "同じ数字どうし。考え方や大切にしているものが近く、言葉にしなくても通じ合いやすい組み合わせです。そのぶん、苦手なことも同じになりやすいので、補い合う工夫がポイントです。")
    if b in NUMBERS[a]["compat"] or a in NUMBERS[b]["compat"]: return ("好相性", "数秘術で相性がよいとされる組み合わせです。お互いの持ち味が自然にかみ合い、一緒にいると心地よさを感じやすいでしょう。")
    ta, tb = TRAITS[a], TRAITS[b]
    if ta["style"] == tb["style"]: return ("共感しやすい", "物事の進め方が似ている組み合わせです。価値観をわかり合いやすく、同じ目標に向かうと力を発揮します。")
    if ta["pace"] != tb["pace"]: return ("補い合う", "ペースが違うふたり。最初はテンポの違いに戸惑うこともありますが、互いにないものを持っているので、うまくかみ合うと心強いパートナーになります。")
    return ("刺激し合う", "大切にしているものが少し違う組み合わせです。違いが新鮮な刺激になり、相手から学べることが多い関係です。")

def pair_page(a, b):
    A, B, ta, tb = NUMBERS[a], NUMBERS[b], TRAITS[a], TRAITS[b]
    lv, lvtxt = level(a, b)
    title = f"運命数{a}と運命数{b}の相性｜恋愛・友情・仕事"
    desc = f"数秘術で運命数{a}（{A['name']}）と運命数{b}（{B['name']}）の相性を解説。ふたりの関係のよいところ、すれ違いやすいところ、うまくいくコツを紹介します。"
    if a == b:
        good = f"ふたりとも{ta['give']}を持っています。同じものを大切にできるので、一緒にいて安心しやすい関係です。"
        bad = f"どちらにも{ta['clash']}があります。同じ場面で同じように行き詰まりやすいので、どちらかが一歩引く役を意識すると楽になります。"
        tips = f"<li>相手に対しては「{ta['tip']}」が基本です。</li><li>得意なことが重なるぶん、苦手な作業は外の力を借りるのも手です。</li>"
    else:
        good = f"運命数{a}の{ta['give']}と、運命数{b}の{tb['give']}。それぞれが相手にないものを持ち寄れるのが、この組み合わせのよさです。運命数{a}の人は{ta['need']}を、運命数{b}の人は{tb['need']}を求めているので、そこを満たし合えると関係が深まります。"
        bad = f"運命数{a}の{ta['clash']}と、運命数{b}の{tb['clash']}がぶつかると、すれ違いが起きやすくなります。どちらが悪いということではなく、もともとの性質の違いだと知っておくだけで、受けとめ方が変わります。"
        tips = f"<li>運命数{a}の人は、相手に対して「{tb['tip']}」を意識してみて。</li><li>運命数{b}の人は、相手に対して「{ta['tip']}」を意識してみて。</li>"
    love = f"恋愛では、運命数{a}の「{A['kw'].split('・')[0]}」と運命数{b}の「{B['kw'].split('・')[0]}」がどう重なるかがポイント。相手が大事にしているもの（{tb['need']}／{ta['need']}）を尊重すると、長く続く関係になりやすいでしょう。"
    work = f"仕事では、運命数{a}は{ta['give']}、運命数{b}は{tb['give']}を活かせる役割分担がおすすめです。"
    nav = f'<p>運命数{a}の相手：' + "・".join(f'<a href="{min(a,n)}-{max(a,n)}.html">{n}</a>' for n in ORDER) + '</p>'
    body = f"""<div class="wrap">
<p class="crumb"><a href="../index.html">数秘のとびら</a> › <a href="index.html">運命数の相性</a> › {a}と{b}</p>
<div class="pair"><span class="big">{a}</span><span class="x">×</span><span class="big">{b}</span><div><h1>運命数{a}と運命数{b}の相性</h1><span class="badge">{lv}</span></div></div>
<p style="margin-top:16px">{lvtxt}</p>
<dl class="facts"><dt>運命数{a}</dt><dd><a href="../number/{a}.html">{A['name']}</a>（{A['kw']}）</dd><dt>運命数{b}</dt><dd><a href="../number/{b}.html">{B['name']}</a>（{B['kw']}）</dd></dl>
<h2>ふたりの関係のよいところ</h2><p>{good}</p>
<h2>すれ違いやすいところ</h2><p>{bad}</p>
<h2>うまくいくコツ</h2><ul>{tips}</ul>
<h2>恋愛・結婚</h2><p>{love}</p>
<h2>仕事・友情</h2><p>{work}</p>
<div class="cta"><strong>ふたりの相性を、もっと詳しく</strong><p>運命数だけでなく、誕生数・表現数・ソウル数も使って、おふたりの関係を読み解く「ふたりの相性鑑定書」（PDF・約8ページ、2,980円）をご用意しています。</p><a class="btn" href="https://suuhinotobira.stores.jp/items/6ad97e7c10a5c693044ffbde">相性鑑定書を見る</a> <a href="../index.html" style="margin-left:12px">まずは無料で自分の数字を調べる</a></div>
<h2>ほかの組み合わせ</h2>{nav}<p><a href="index.html">相性の一覧表を見る</a></p>
<p style="font-size:.8rem;color:var(--soft)">※相性は数秘術にもとづく読み物です。ふたりの関係を考えるきっかけとしてお楽しみください。</p>
{FOOT_C}</div>"""
    open(os.path.join(OUT, "compat", f"{a}-{b}.html"), "w", encoding="utf-8").write(
        f'<!doctype html>\n<html lang="ja"><head>{META}<title>{title}｜数秘のとびら</title>{og(title, desc, f"compat/{a}-{b}.html")}{CSTYLE}</head><body>{body}</body></html>\n')

compat_urls = []
for i, a in enumerate(ORDER):
    for b in ORDER[i:]:
        pair_page(a, b); compat_urls.append(f"compat/{a}-{b}.html")

head = "".join(f"<th>{n}</th>" for n in ORDER)
rows_c = "".join("<tr><th>%d</th>%s</tr>" % (a, "".join(f'<td><a href="{min(a,b)}-{max(a,b)}.html" title="{level(a,b)[0]}">{"◎" if level(a,b)[0]=="好相性" else "○"}</a></td>' for b in ORDER)) for a in ORDER)
ct, cd = "運命数の相性一覧", "数秘術の運命数1〜9・11・22・33、全78通りの組み合わせの相性を一覧で紹介。ふたりの生年月日から相性ページを開けます。"
calc = """<form class="calc" id="pf"><strong>ふたりの生年月日から相性を見る</strong>
<label>あなた <input id="d1" inputmode="numeric" placeholder="19960812" maxlength="8"></label>
<label>お相手 <input id="d2" inputmode="numeric" placeholder="19940305" maxlength="8"></label>
<button type="submit">相性を見る</button><span id="pe" style="color:var(--seal)"></span></form>
<script>
const M=new Set([11,22,33]);const lp=s=>{let n=[...s].reduce((a,c)=>a+ +c,0);while(n>9&&!M.has(n))n=[...String(n)].reduce((a,c)=>a+ +c,0);return n};
document.getElementById('pf').addEventListener('submit',e=>{e.preventDefault();const a=d1.value.trim(),b=d2.value.trim();
if(!/^\\d{8}$/.test(a)||!/^\\d{8}$/.test(b)){pe.textContent='生年月日を8桁の数字で入れてください（例 19960812）';return}
const x=lp(a),y=lp(b);location.href=Math.min(x,y)+'-'+Math.max(x,y)+'.html'});
</script>"""
open(os.path.join(OUT, "compat", "index.html"), "w", encoding="utf-8").write(
    f'<!doctype html>\n<html lang="ja"><head>{META}<title>{ct}｜数秘のとびら</title>{og(ct, cd, "compat/")}{CSTYLE}</head><body><div class="wrap">'
    f'<p class="crumb"><a href="../index.html">数秘のとびら</a> › 運命数の相性</p><h1 style="margin-top:16px">{ct}</h1><p>{cd}</p>{calc}'
    f'<h2>相性早見表</h2><p>◎は数秘術で相性がよいとされる組み合わせ。表の記号を押すと、その組み合わせの解説が開きます。</p>'
    f'<div class="grid"><table><tr><th></th>{head}</tr>{rows_c}</table></div>{FOOT_C}</div></body></html>\n')

# 4) サイトマップ・robots
urls = ["", "number/", "compat/"] + [f"number/{n}.html" for n in ORDER] + compat_urls + ["legal.html", "privacy.html", "terms.html"]
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("built:", len(urls), "pages")
