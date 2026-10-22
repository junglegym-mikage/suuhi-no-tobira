"""ふたりの相性鑑定書（PDF）を作る。
使い方:
  python3 report/make_pair_report.py --name1 "山田 花子" --romaji1 "YAMADA HANAKO" --birth1 1996-08-12 \
      --name2 "佐藤 太郎" --romaji2 "SATO TARO" --birth2 1994-03-05 [--out 出力.pdf]
"""
import argparse, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_report as R  # noqa: E402  (フォント・スタイル・数字計算を共有)
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "content"))
from compat_texts import TRAITS  # noqa: E402

NUMBERS, S = R.NUMBERS, R.S

def level(a, b):
    if a == b: return "似た者同士"
    if b in NUMBERS[a]["compat"] or a in NUMBERS[b]["compat"]: return "好相性"
    ta, tb = TRAITS[a], TRAITS[b]
    if ta["style"] == tb["style"]: return "共感しやすい"
    if ta["pace"] != tb["pace"]: return "補い合う"
    return "刺激し合う"

LEVEL_TXT = {
 "似た者同士": "考え方や大切にしているものが近く、言葉にしなくても通じ合いやすい組み合わせです。苦手なことも重なりやすいので、補い合う工夫が鍵になります。",
 "好相性": "数秘術で相性がよいとされる組み合わせです。お互いの持ち味が自然にかみ合い、一緒にいると心地よさを感じやすいでしょう。",
 "共感しやすい": "物事の進め方が似ていて、価値観をわかり合いやすい組み合わせです。同じ目標に向かうと大きな力を発揮します。",
 "補い合う": "ペースが違うぶん、互いにないものを持っている組み合わせです。違いを認め合えると、とても心強いパートナーになります。",
 "刺激し合う": "大切にしているものが少し違う組み合わせです。違いが新鮮な刺激になり、相手から学べることが多い関係です。",
}

def pair_block(P, x, y, nx, ny, label):
    """数字xの人とyの人の関係を1セクション書く"""
    tx, ty = TRAITS[x], TRAITS[y]
    P(label, "h2")
    if x == y:
        P(f"同じ数字{x}どうし。どちらにも「{tx['give']}」があり、同じものを大切にできます。一方で「{tx['clash']}」も共通するので、同じ場面で行き詰まらないよう、役割を分けるのがおすすめです。")
    else:
        P(f"{nx}さん（{x}）の「{tx['give']}」と、{ny}さん（{y}）の「{ty['give']}」。それぞれが相手にないものを持ち寄れます。{nx}さんは「{tx['need']}」を、{ny}さんは「{ty['need']}」を求めているので、そこを満たし合えると関係が深まります。")

def build(n1, r1, b1, n2, r2, b2, out):
    A, B = R.numbers_for(b1, r1), R.numbers_for(b2, r2)
    s1, s2 = n1.split()[-1] if " " in n1 else n1, n2.split()[-1] if " " in n2 else n2
    a, b = A["life"], B["life"]
    lv = level(a, b)
    doc = BaseDocTemplate(out, pagesize=A5, leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm,
                          title=f"{n1}様・{n2}様 相性鑑定書", author="数秘のとびら")
    def deco(c, d):
        c.saveState(); c.setFillColor(R.PAPER); c.rect(0, 0, A5[0], A5[1], stroke=0, fill=1)
        c.setStrokeColor(R.LINE); c.setLineWidth(.5); c.rect(8*mm, 8*mm, A5[0]-16*mm, A5[1]-16*mm)
        c.setFont("JP", 7); c.setFillColor(R.SOFT)
        if d.page > 1: c.drawString(16*mm, 11*mm, f"{n1}様・{n2}様 相性鑑定書"); c.drawRightString(A5[0]-16*mm, 11*mm, str(d.page))
        c.restoreState()
    doc.addPageTemplates([PageTemplate(frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)], onPage=deco)])
    st = []; P = lambda t, s="body": st.append(Paragraph(t, S[s]))
    center = ParagraphStyle("cc", parent=S["h1"], alignment=TA_CENTER)

    # 1 表紙
    st.append(Spacer(1, 26*mm)); P("数秘のとびら", "center"); st.append(Spacer(1, 6*mm))
    st.append(Paragraph(f"{n1} 様<br/>{n2} 様", center)); P("ふたりの相性鑑定書", "center"); st.append(Spacer(1, 10*mm))
    st.append(Paragraph(f"{a} × {b}", ParagraphStyle("bb", parent=S["big"], fontSize=48, leading=56)))
    P(f"運命数{a}（{NUMBERS[a]['name']}）× 運命数{b}（{NUMBERS[b]['name']}）", "center"); st.append(Spacer(1, 6*mm))
    P(f"ふたりの相性：{lv}", "center"); st.append(Spacer(1, 16*mm))
    P(f"作成日　{datetime.date.today():%Y年%m月%d日}", "center"); st.append(PageBreak())

    # 2 ふたりの数字
    P("NUMBERS", "eyebrow"); P("ふたりの数字", "h1")
    rows = [["数字", n1, n2], ["運命数（本質）", str(a), str(b)], ["誕生数（才能）", str(A["day"]), str(B["day"])],
            ["表現数（見られ方）", str(A["expr"] or "－"), str(B["expr"] or "－")], ["ソウル数（心の願い）", str(A["soul"] or "－"), str(B["soul"] or "－")]]
    t = Table(rows, colWidths=[38*mm, 32*mm, 32*mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "JP", 9), ("TEXTCOLOR", (0, 0), (-1, 0), R.SOFT), ("LINEBELOW", (0, 0), (-1, -1), .4, R.LINE),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"), ("TEXTCOLOR", (1, 1), (-1, -1), R.GOLD), ("FONTSIZE", (1, 1), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    st += [Spacer(1, 3*mm), t, Spacer(1, 4*mm)]
    P(f"ふたりの運命数の組み合わせは「{lv}」。{LEVEL_TXT[lv]}"); st.append(PageBreak())

    # 3 それぞれの本質
    P("EACH OTHER", "eyebrow"); P("ふたりそれぞれの本質", "h1")
    for nm, n in ((n1, a), (n2, b)):
        P(f"{nm}さん　運命数{n}「{NUMBERS[n]['name']}」", "h2"); P(NUMBERS[n]["personality"])
    st.append(PageBreak())

    # 4 関係のよいところ／すれ違い
    P("RELATION", "eyebrow"); P("ふたりの関係", "h1")
    pair_block(P, a, b, s1, s2, "本質どうしの相性（運命数）")
    P("すれ違いやすいところ", "h2")
    if a == b: P(f"ふたりとも「{TRAITS[a]['clash']}」があるため、同じタイミングで意地を張りやすい面があります。")
    else: P(f"{s1}さんの「{TRAITS[a]['clash']}」と、{s2}さんの「{TRAITS[b]['clash']}」がぶつかると、すれ違いが起きやすくなります。性質の違いだと知っておくだけで、受けとめ方がやわらぎます。")
    if A["soul"] and B["soul"]:
        pair_block(P, A["soul"], B["soul"], s1, s2, "心の奥の願いどうし（ソウル数）")
    st.append(PageBreak())

    # 5 うまくいくコツ
    P("TIPS", "eyebrow"); P("うまくいくコツ", "h1")
    P(f"{s1}さんへ", "h2"); P(f"{s2}さんに対しては「{TRAITS[b]['tip']}」を意識してみてください。{s2}さんが求めている「{TRAITS[b]['need']}」を満たせると、信頼がぐっと深まります。")
    P(f"{s2}さんへ", "h2"); P(f"{s1}さんに対しては「{TRAITS[a]['tip']}」を意識してみてください。{s1}さんが求めている「{TRAITS[a]['need']}」を大切にすると、関係が安定します。")
    P("ふたりで大切にしたいこと", "h2"); P(f"運命数{a}の「{NUMBERS[a]['kw']}」と、運命数{b}の「{NUMBERS[b]['kw']}」。ふたりのキーワードを並べてみると、関係のテーマが見えてきます。違いは欠点ではなく、ふたりで一人分以上の力を出すための材料です。")
    st.append(PageBreak())

    # 6 恋愛・結婚／仕事
    P("LOVE & WORK", "eyebrow"); P("恋愛・結婚と、一緒に何かをするとき", "h1")
    P("恋愛・結婚", "h2"); P(f"{s1}さんの恋愛傾向：{NUMBERS[a]['love']}"); P(f"{s2}さんの恋愛傾向：{NUMBERS[b]['love']}")
    P("仕事・友情", "h2"); P(f"{s1}さんは{TRAITS[a]['give']}、{s2}さんは{TRAITS[b]['give']}を活かせる役割分担がおすすめです。")
    st.append(PageBreak())

    # 7 ふたりの年運
    y = datetime.date.today().year
    P("YEAR", "eyebrow"); P(f"{y}年・{y+1}年のふたり", "h1")
    rows = [["年", f"{s1}さん", f"{s2}さん"]]
    for yy in (y, y + 1):
        p1, p2 = R.personal_year(b1, yy), R.personal_year(b2, yy)
        rows.append([f"{yy}年", f"{p1}　{R.YEAR[p1][:R.YEAR[p1].index('。')]}", f"{p2}　{R.YEAR[p2][:R.YEAR[p2].index('。')]}"])
    t = Table(rows, colWidths=[20*mm, 41*mm, 41*mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "JP", 8.5), ("TEXTCOLOR", (0, 0), (-1, 0), R.SOFT), ("LINEBELOW", (0, 0), (-1, -1), .4, R.LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    st += [Spacer(1, 3*mm), t, Spacer(1, 4*mm)]
    p1, p2 = R.personal_year(b1, y), R.personal_year(b2, y)
    P("今年のふたりへのヒント", "h2")
    P(f"{s1}さんは「{R.YEAR[p1][:R.YEAR[p1].index('。')]}」、{s2}さんは「{R.YEAR[p2][:R.YEAR[p2].index('。')]}」。相手が今どんな流れにいるのかを知っておくと、言葉や行動の受けとめ方が変わります。")
    st.append(PageBreak())

    # 8 おわりに
    st.append(Spacer(1, 18*mm)); P("おわりに", "h1")
    P("相性は、ふたりの未来を決めるものではありません。お互いの持ち味を知り、違いを面白がるための手がかりです。迷ったときや節目に、この鑑定書をふたりで開いてみてください。")
    st.append(Spacer(1, 8*mm)); P("数秘のとびら", "center")
    P("※本鑑定書は数秘術にもとづく読み物です。医療・法律・金融などの判断の代わりにはなりません。", "small")
    doc.build(st)
    return a, b, lv

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("name1", "romaji1", "birth1", "name2", "romaji2", "birth2"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--out"); a = ap.parse_args()
    out = a.out or f"相性鑑定書_{a.name1.replace(' ', '')}_{a.name2.replace(' ', '')}.pdf"
    print(build(a.name1, a.romaji1, datetime.date.fromisoformat(a.birth1), a.name2, a.romaji2, datetime.date.fromisoformat(a.birth2), out), "->", out)
