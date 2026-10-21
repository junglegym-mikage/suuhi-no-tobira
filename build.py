import os
os.chdir("/home/claude/suuhi-no-tobira/src")
head='''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@@TITLE@@｜数秘のとびら</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@700&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">
<style>
:root{--paper:#f3f0e8;--ink:#1d2433;--soft:#4d566a;--line:#cfc8b6;--fill:#9a7428;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#151a24;--ink:#ece6d8;--soft:#a9adb8;--line:#343c4d;--fill:#d2ab5c;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#151a24;--ink:#ece6d8;--soft:#a9adb8;--line:#343c4d;--fill:#d2ab5c;color-scheme:dark}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Zen Kaku Gothic New","Hiragino Sans",system-ui,sans-serif;line-height:1.9;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:760px;margin:0 auto;padding-block:32px 48px}
a{color:var(--ink)}
h1{font-family:"Shippori Mincho B1",serif;font-size:1.6rem;border-bottom:1px solid var(--line);padding-bottom:8px}
h2{font-family:"Shippori Mincho B1",serif;font-size:1.1rem;margin-top:28px}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;vertical-align:top;padding:10px 8px;border-bottom:1px solid var(--line)}
th{width:32%;font-weight:500;color:var(--soft)}
.todo{color:var(--fill);font-weight:500}
@media (max-width:560px){th,td{display:block;width:auto;padding:4px 0}td{padding-bottom:12px}}
</style></head><body><main>
<p><a href="index.html">← 数秘のとびら トップへ</a></p>
'''
foot='</main></body></html>\n'
T='<span class="todo">【要記入】</span>'
legal=f'''<h1>特定商取引法に基づく表記</h1>
<table>
<tr><th>販売事業者</th><td>{T}氏名または屋号</td></tr>
<tr><th>運営責任者</th><td>{T}氏名</td></tr>
<tr><th>所在地</th><td>{T}住所（個人の場合、請求があれば遅滞なく開示する旨の記載も可）</td></tr>
<tr><th>電話番号</th><td>{T}電話番号（請求があれば遅滞なく開示する旨の記載も可）</td></tr>
<tr><th>メールアドレス</th><td>{T}お問い合わせ用メールアドレス</td></tr>
<tr><th>販売価格</th><td>詳しい鑑定書：1,980円（税込）</td></tr>
<tr><th>商品代金以外の必要料金</th><td>インターネット接続にかかる通信料はお客様のご負担となります。</td></tr>
<tr><th>お支払い方法</th><td>クレジットカード決済（Stripe）</td></tr>
<tr><th>お支払い時期</th><td>ご注文時にお支払いが確定します。</td></tr>
<tr><th>商品の引き渡し時期</th><td>決済完了後、ご登録のメールアドレスへ3営業日以内にPDFでお送りします。</td></tr>
<tr><th>返品・キャンセル</th><td>デジタルコンテンツの性質上、お届け後の返品・返金はお受けできません。お届けしたファイルに不備があった場合は、再送または返金にて対応いたします。</td></tr>
</table>'''
privacy=f'''<h1>プライバシーポリシー</h1>
<p>数秘のとびら（以下「当サイト」）は、お客様の個人情報を以下のとおり取り扱います。</p>
<h2>取得する情報</h2><p>無料診断で入力された生年月日は、お使いのブラウザ内でのみ計算に使用し、当サイトのサーバーには送信・保存しません。有料鑑定のお申し込み時には、お名前・メールアドレス・生年月日など鑑定に必要な情報をお預かりします。</p>
<h2>利用目的</h2><p>鑑定書の作成とお届け、お問い合わせへの対応、サービス改善のために利用します。</p>
<h2>第三者への提供</h2><p>法令に基づく場合を除き、ご本人の同意なく第三者に提供しません。決済は決済代行会社（Stripe）が行い、当サイトはカード情報を保持しません。</p>
<h2>アクセス解析</h2><p>当サイトでは、利用状況の把握のためアクセス解析ツールを使用する場合があります。これらは個人を特定する情報を含みません。</p>
<h2>お問い合わせ</h2><p>{T}お問い合わせ用メールアドレス</p>
<p>制定日：2026年10月21日</p>'''
terms='''<h1>利用規約</h1>
<h2>第1条（適用）</h2><p>本規約は、数秘のとびら（以下「当サイト」）が提供するすべてのサービスに適用されます。</p>
<h2>第2条（占いの性質）</h2><p>当サイトの診断・鑑定は、数秘術にもとづく読み物としてお楽しみいただくものです。医療・法律・金融などの専門的な判断の代わりにはなりません。重要なご判断は、ご自身の責任で、必要に応じて専門家にご相談ください。</p>
<h2>第3条（禁止事項）</h2><p>当サイトのコンテンツの無断転載・再配布、営利目的での利用、当サイトの運営を妨げる行為を禁止します。</p>
<h2>第4条（免責）</h2><p>当サイトは、診断・鑑定の内容によって生じたいかなる損害についても責任を負いません。</p>
<h2>第5条（規約の変更）</h2><p>当サイトは必要に応じて本規約を変更できるものとします。変更後の規約は当ページに掲載した時点で効力を生じます。</p>
<p>制定日：2026年10月21日</p>'''
for name,title,body in [("legal","特定商取引法に基づく表記",legal),("privacy","プライバシーポリシー",privacy),("terms","利用規約",terms)]:
    open(f"{name}.html","w").write(head.replace("@@TITLE@@",title)+body+foot)

# GitHub Pages用：index.htmlを完全なHTML文書に包む
frag=open("index.html").read()
os.makedirs("../docs",exist_ok=True)
full='<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+frag.replace("<script>","</head><body>\n<script>",0)
# head部（title〜</style>）とbody部を分ける
i=frag.index("</style>")+len("</style>")
full='<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+frag[:i]+'\n<style>body{margin:0}[hidden]{display:none!important}</style>\n</head><body>'+frag[i:]+'\n</body></html>\n'
open("../docs/index.html","w").write(full)
import shutil
for n in ("legal","privacy","terms"): shutil.copy(f"{n}.html",f"../docs/{n}.html")
print("ok")
