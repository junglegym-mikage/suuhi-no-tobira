"""数秘のとびら ビルド: src/ と content/ から docs/（GitHub Pages 公開用）を作る。
使い方: python3 build.py
"""
import os, shutil, sys, html, glob
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "content"))
from number_texts import NUMBERS  # noqa: E402

SITE = "https://suuhi-tobira.github.io"
GA_ID = "G-8YJF5P338Z"  # Google アナリティクスの測定ID（例 "G-XXXXXXXXXX"）。入れてビルドすると全ページに計測タグが入る
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "site")  # 新サイト（suuhi-tobira.github.io）の出力先
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

FOOT = ('<footer><span>© 2026 数秘のとびら</span><a href="../column/index.html">コラム</a><a href="../legal.html">特定商取引法に基づく表記</a>'
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

# 3c) 年の運勢（個人年数1〜9）。YEAR_THEMES は年に依存しない文なので、年ごとにページを作る
from year_texts import YEAR_THEMES  # noqa: E402
YEARS = [2026, 2027]
YNAV = lambda cur=None: '<div class="others">' + "".join(f'<a href="{n}.html"{" aria-current=\"page\"" if n == cur else ""}>{n}</a>' for n in range(1, 10)) + "</div>"
def ycalc(Y):
    return f"""<form class="calc" id="yf"><strong>あなたの{Y}年の個人年数を計算する</strong>
<label>生まれた月 <input id="ym" inputmode="numeric" placeholder="8" maxlength="2" style="width:5em"></label>
<label>生まれた日 <input id="yd" inputmode="numeric" placeholder="12" maxlength="2" style="width:5em"></label>
<button type="submit">計算する</button><span id="ye" style="color:var(--seal)"></span></form>
<script>
document.getElementById('yf').addEventListener('submit',e=>{{e.preventDefault();const m=+ym.value,d=+yd.value;
if(!(m>=1&&m<=12&&d>=1&&d<=31)){{ye.textContent='月と日を数字で入れてください';return}}
let n=[...String(m)+String(d)+'{Y}'].reduce((a,c)=>a+ +c,0);while(n>9)n=[...String(n)].reduce((a,c)=>a+ +c,0);
location.href=n+'.html'}});
</script>"""
year_urls = []
for Y in YEARS:
    os.makedirs(os.path.join(OUT, str(Y)), exist_ok=True)
    other_y = " ".join(f'<a href="../{z}/index.html">{z}年の運勢</a>' for z in YEARS if z != Y)
    for n, y in YEAR_THEMES.items():
        title = f"{Y}年の運勢・個人年数{n}「{y['name']}」｜数秘術"
        desc = f"数秘術で{Y}年の個人年数が{n}の人の運勢。テーマは「{y['name']}」（{y['kw']}）。恋愛・仕事・金運と、{Y}年にやるとよいことを解説します。"
        tips = "".join(f"<li>{t}</li>" for t in y["tips"])
        body = f"""<div class="wrap">
<p class="crumb"><a href="../index.html">数秘のとびら</a> › <a href="index.html">{Y}年の運勢</a> › 個人年数{n}</p>
<div class="head"><div class="big">{n}</div><div><h1>{Y}年は「{y['name']}」<br>個人年数{n}の運勢</h1><p class="kw">{y['kw']}</p></div></div>
<p style="margin-top:16px">{y['overview']}</p>
<h2>{Y}年の恋愛運</h2><p>{y['love']}</p>
<h2>{Y}年の仕事運</h2><p>{y['work']}</p>
<h2>{Y}年の金運</h2><p>{y['money']}</p>
<h2>{Y}年にやるとよいこと</h2><ul>{tips}</ul>
<div class="cta"><strong>月ごとの流れまで知りたい方へ</strong><p>「数秘術鑑定書」（PDF・約11ページ、1,980円）では、2026年・2027年の月ごとの運気カレンダーと、あなたの4つの数字からみる性格・恋愛・仕事を読み解きます。</p><a class="btn" href="https://suuhinotobira.stores.jp/items/6ad96e649e2872f0141245c3">鑑定書を見る</a> <a href="../index.html" style="margin-left:12px">まずは無料診断</a></div>
<h2>ほかの個人年数</h2>{YNAV(n)}
<p>{other_y}</p>
<p style="font-size:.8rem;color:var(--soft)">※個人年数は「誕生月＋誕生日＋その年の西暦」の数字をすべて足して一桁にした数字です。占いは人生の参考としてお楽しみください。</p>
{FOOT}</div>"""
        open(os.path.join(OUT, str(Y), f"{n}.html"), "w", encoding="utf-8").write(
            f'<!doctype html>\n<html lang="ja"><head>{META}<title>{title}｜数秘のとびら</title>{og(title, desc, f"{Y}/{n}.html")}{CSTYLE}</head><body>{body}</body></html>\n')
    yt, yd = f"{Y}年の運勢｜数秘術の個人年数でみる1年", f"数秘術の個人年数（パーソナルイヤー）でみる{Y}年の運勢。誕生月と誕生日から、あなたの{Y}年のテーマ・恋愛運・仕事運・金運がわかります。"
    rows_y = "".join(f'<h2><a href="{n}.html">個人年数{n}　{y["name"]}</a></h2><p>{y["kw"]}。{y["overview"][:60]}…</p>' for n, y in YEAR_THEMES.items())
    open(os.path.join(OUT, str(Y), "index.html"), "w", encoding="utf-8").write(
        f'<!doctype html>\n<html lang="ja"><head>{META}<title>{yt}｜数秘のとびら</title>{og(yt, yd, f"{Y}/")}{CSTYLE}</head><body><div class="wrap">'
        f'<p class="crumb"><a href="../index.html">数秘のとびら</a> › {Y}年の運勢</p><h1 style="margin-top:16px">{Y}年の運勢</h1><p>{yd}</p>{ycalc(Y)}{YNAV()}{rows_y}<p>{other_y}</p>{FOOT}</div></body></html>\n')
    year_urls += [f"{Y}/"] + [f"{Y}/{n}.html" for n in range(1, 10)]

# 3d) コラム（検索から来てもらう記事）。content/articles/*.md を column/<slug>.html にする
#  書式：先頭に「key: value」の行（title, description, date, keyword）、空行、本文（簡易Markdown）
import re
ART_DIR = os.path.join(ROOT, "content", "articles")
def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
def md_to_html(src):
    out, para, lst, tbl = [], [], None, []
    def flush():
        nonlocal para, lst, tbl
        if para: out.append("<p>" + md_inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{lst[0]}>" + "".join(f"<li>{md_inline(i)}</li>" for i in lst[1]) + f"</{lst[0]}>"); lst = None
        if tbl:
            rows = [r for r in tbl if not re.fullmatch(r"\|[\s:|-]+\|", r)]
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            out.append('<div class="grid"><table><tr>' + "".join(f"<th>{md_inline(c)}</th>" for c in cells[0]) + "</tr>"
                       + "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:]) + "</table></div>"); tbl = []
    for line in src.splitlines():
        l = line.rstrip()
        if not l: flush(); continue
        m = re.match(r"(#{2,3}) (.+)", l)
        if m: flush(); out.append(f"<h{len(m.group(1))}>{md_inline(m.group(2))}</h{len(m.group(1))}>"); continue
        if l.startswith("|"):
            if para or lst: flush()
            tbl.append(l); continue
        m = re.match(r"(?:- |(\d+)\. )(.+)", l)
        if m:
            kind = "ol" if m.group(1) else "ul"
            if para or tbl or (lst and lst[0] != kind): flush()
            lst = lst or (kind, []); lst[1].append(m.group(2)); continue
        if lst or tbl: flush()
        para.append(l.strip())
    flush(); return "\n".join(out)
def read_article(path):
    raw = open(path, encoding="utf-8").read().lstrip("﻿")
    head, _, body = raw.partition("\n\n")
    meta = dict(l.split(":", 1) for l in head.splitlines() if ":" in l)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    for k in ("title", "description", "date"):
        if not meta.get(k): raise SystemExit(f"記事 {path} に {k} がありません")
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["body"] = body
    return meta
articles = sorted((read_article(f) for f in glob.glob(os.path.join(ART_DIR, "*.md"))) if os.path.isdir(ART_DIR) else [],
                  key=lambda a: a["date"], reverse=True)
import datetime as _dt
today = _dt.date.today().isoformat()
articles = [a for a in articles if a["date"] <= today]  # 日付が未来の記事はまだ公開しない
ASTYLE = CSTYLE.replace("</style>", """
.art h2{margin-top:36px}.art h3{font-size:1.05rem;margin:20px 0 4px}
.art ul,.art ol{padding-left:1.4em;margin:0 0 8px}.meta{font-size:.82rem;color:var(--soft);margin:8px 0 0}
.toc{background:var(--card);border:1px solid var(--line);padding:12px 16px;margin-top:16px;font-size:.92rem}.toc ol{margin:4px 0 0;padding-left:1.4em}
.list h2{font-size:1.05rem}
</style>""")
column_urls = []
if articles:
    os.makedirs(os.path.join(OUT, "column"), exist_ok=True)
    for a in articles:
        body_html = md_to_html(a["body"])
        heads = re.findall(r"<h2>(.+?)</h2>", body_html)
        for i, h in enumerate(heads):
            body_html = body_html.replace(f"<h2>{h}</h2>", f'<h2 id="s{i+1}">{h}</h2>', 1)
        toc = ('<nav class="toc"><strong>目次</strong><ol>' + "".join(f'<li><a href="#s{i+1}">{re.sub("<[^>]+>", "", h)}</a></li>' for i, h in enumerate(heads)) + "</ol></nav>") if len(heads) >= 3 else ""
        rel = [x for x in articles if x["slug"] != a["slug"]][:4]
        rel_html = ("<h2>ほかのコラム</h2><ul>" + "".join(f'<li><a href="{x["slug"]}.html">{html.escape(x["title"])}</a></li>' for x in rel) + "</ul>") if rel else ""
        ld = ('<script type="application/ld+json">' + __import__("json").dumps({"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"],
              "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "author": {"@type": "Organization", "name": "数秘のとびら"},
              "publisher": {"@type": "Organization", "name": "数秘のとびら"}, "mainEntityOfPage": f"{SITE}/column/{a['slug']}.html"}, ensure_ascii=False) + "</script>")
        page = f"""<div class="wrap art">
<p class="crumb"><a href="../index.html">数秘のとびら</a> › <a href="index.html">コラム</a></p>
<h1 style="margin-top:16px">{html.escape(a['title'])}</h1>
<p class="meta">公開：{a['date']}{('　更新：' + a['updated']) if a.get('updated') else ''}　文：数秘のとびら編集部</p>
{toc}
{body_html}
<div class="cta"><strong>あなたの数字を無料で調べる</strong><p>生年月日を入れるだけで、運命数と今年の流れがわかります。登録不要です。</p><a class="btn" href="../index.html">無料で診断する</a>
<p style="margin-top:12px;font-size:.92rem">くわしく知りたい方には、性格・恋愛・仕事と月ごとの運気カレンダーをまとめた<a href="https://suuhinotobira.stores.jp/items/6ad96e649e2872f0141245c3">数秘術鑑定書（PDF・1,980円）</a>もあります。</p></div>
{rel_html}
<p style="font-size:.8rem;color:var(--soft)">※数秘術をもとにした占いです。人生の参考としてお楽しみください。</p>
{FOOT}</div>"""
        open(os.path.join(OUT, "column", f"{a['slug']}.html"), "w", encoding="utf-8").write(
            f'<!doctype html>\n<html lang="ja"><head>{META}<title>{html.escape(a["title"])}｜数秘のとびら</title>{og(a["title"], a["description"], f"column/{a["slug"]}.html").replace("og:type\" content=\"website", "og:type\" content=\"article")}{ld}{ASTYLE}</head><body>{page}</body></html>\n')
        column_urls.append((f"column/{a['slug']}.html", a.get("updated", a["date"])))
    ct, cd = "数秘術コラム", "数秘術の基本や数字の意味、相性、運勢の読み方を、はじめての方にもわかりやすく解説するコラムです。"
    rows_c = "".join(f'<h2><a href="{a["slug"]}.html">{html.escape(a["title"])}</a></h2><p>{html.escape(a["description"])}</p>' for a in articles)
    open(os.path.join(OUT, "column", "index.html"), "w", encoding="utf-8").write(
        f'<!doctype html>\n<html lang="ja"><head>{META}<title>{ct}｜数秘のとびら</title>{og(ct, cd, "column/")}{ASTYLE}</head><body><div class="wrap list">'
        f'<p class="crumb"><a href="../index.html">数秘のとびら</a> › コラム</p><h1 style="margin-top:16px">{ct}</h1><p>{cd}</p>{rows_c}{FOOT}</div></body></html>\n')
    column_urls.insert(0, ("column/", articles[0].get("updated", articles[0]["date"])))

# 4) サイトマップ・robots
urls = ["", "number/", "compat/"] + [f"number/{n}.html" for n in ORDER] + compat_urls + year_urls + [u for u, _ in column_urls] + ["legal.html", "privacy.html", "terms.html"]
lastmod = dict(column_urls)
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}/{u}</loc>" + (f"<lastmod>{lastmod[u]}</lastmod>" if u in lastmod else "") + "</url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
# 5) サンプル画像を新サイトへ、旧URL（docs/）は新URLへの転送ページにする
if os.path.isdir(os.path.join(ROOT, "docs", "samples")) and not os.path.isdir(os.path.join(OUT, "samples")):
    shutil.copytree(os.path.join(ROOT, "docs", "samples"), os.path.join(OUT, "samples"))
OLD = os.path.join(ROOT, "docs")
import glob
for g in glob.glob(os.path.join(OLD, "google*.html")):
    shutil.copy(g, OUT)
for u in urls + ["sitemap.xml"]:
    if u.endswith(".xml"): continue
    path = os.path.join(OLD, u if u and not u.endswith("/") else (u + "index.html"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    dest = f"{SITE}/{u}"
    open(path, "w", encoding="utf-8").write(
        f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>数秘のとびら（移転しました）</title>'
        f'<link rel="canonical" href="{dest}"><meta http-equiv="refresh" content="0; url={dest}">'
        f'<meta name="robots" content="noindex"></head><body><p>数秘のとびらは <a href="{dest}">{dest}</a> に移転しました。</p>'
        f'<script>location.replace({dest!r}+location.hash)</script></body></html>\n')
open(os.path.join(OLD, "robots.txt"), "w").write("User-agent: *\nAllow: /\n")
for f in ("sitemap.xml",):
    fp = os.path.join(OLD, f)
    if os.path.exists(fp): os.remove(fp)
# 6) アクセス計測タグ（GA_ID が入っているときだけ）。STORESへのクリックは GA4 の「離脱クリック」で自動計測される
if GA_ID:
    tag = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
           f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>")
    for g in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
        if os.path.basename(g).startswith("google"): continue
        t = open(g, encoding="utf-8").read()
        if "googletagmanager" not in t and "<head>" in t:
            open(g, "w", encoding="utf-8").write(t.replace("<head>", "<head>" + tag, 1))
print("built:", len(urls), "pages (site/) + redirects (docs/)")
