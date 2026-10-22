"""有料鑑定書（PDF）を作る。
使い方:
  python3 report/make_report.py --name "山田 花子" --romaji "YAMADA HANAKO" --birth 1996-08-12 [--out 出力.pdf]
"""
import argparse, os, sys, datetime
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                PageBreak, Table, TableStyle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "content"))
from number_texts import NUMBERS  # noqa: E402

FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
pdfmetrics.registerFont(TTFont("JP", FONT))

INK, SOFT, GOLD, SEAL, LINE = (colors.HexColor(c) for c in ("#1d2433", "#4d566a", "#9a7428", "#a83a2c", "#cfc8b6"))
PAPER = colors.HexColor("#f6f3ec")

S = {
 "body": ParagraphStyle("body", fontName="JP", fontSize=9.5, leading=17, textColor=INK, spaceAfter=6, wordWrap="CJK"),
 "h1": ParagraphStyle("h1", fontName="JP", fontSize=15, leading=22, textColor=INK, spaceAfter=4, wordWrap="CJK"),
 "h2": ParagraphStyle("h2", fontName="JP", fontSize=11, leading=17, textColor=SEAL, spaceBefore=10, spaceAfter=3, wordWrap="CJK"),
 "eyebrow": ParagraphStyle("eb", fontName="JP", fontSize=7.5, leading=11, textColor=GOLD),
 "big": ParagraphStyle("big", fontName="JP", fontSize=64, leading=70, textColor=GOLD, alignment=TA_CENTER),
 "center": ParagraphStyle("c", fontName="JP", fontSize=10, leading=18, textColor=INK, alignment=TA_CENTER, wordWrap="CJK"),
 "small": ParagraphStyle("s", fontName="JP", fontSize=7.5, leading=12, textColor=SOFT, wordWrap="CJK"),
}

MASTER = {11, 22, 33}
def dsum(n): return sum(int(c) for c in str(n))
def reduce(n, keep=True):
    while n > 9 and not (keep and n in MASTER):
        n = dsum(n)
    return n
PY = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
VOWELS = set("AEIOU")

def numbers_for(birth, romaji):
    letters = [c for c in romaji.upper() if c.isalpha()]
    return dict(
        life=reduce(dsum(birth.strftime("%Y%m%d"))),
        day=reduce(birth.day),
        expr=reduce(sum(PY[c] for c in letters)) if letters else None,
        soul=reduce(sum(PY[c] for c in letters if c in VOWELS)) if letters else None,
    )

DAY = {1:"自分で決めて動くことで、運が開けていく人です。",2:"人とのつながりの中で、才能が育っていく人です。",3:"楽しむ気持ちが、そのまま才能になる人です。",
 4:"コツコツ積み上げた経験が、大きな財産になる人です。",5:"新しい場所や人との出会いが、成長のきっかけになる人です。",6:"誰かのために動くとき、いちばん力が出る人です。",
 7:"ひとつのことを深く知るほど、自信が増していく人です。",8:"目標が大きいほど、底力を発揮する人です。",9:"多くの経験をやさしさに変えていける人です。",
 11:"直感にしたがうと、思いがけない扉が開く人です。",22:"大きな構想を、現実に落とし込める人です。",33:"いるだけで場をやわらげる、不思議な魅力の人です。"}
EXPR = {1:"周囲からは、頼れるリーダーとして見られています。",2:"周囲からは、話しやすく安心できる人として見られています。",3:"周囲からは、明るく華やかなムードメーカーとして見られています。",
 4:"周囲からは、約束を守る誠実な人として見られています。",5:"周囲からは、行動的でおもしろい人として見られています。",6:"周囲からは、面倒見のよい、あたたかい人として見られています。",
 7:"周囲からは、知的でミステリアスな人として見られています。",8:"周囲からは、実力があり堂々とした人として見られています。",9:"周囲からは、懐の深い、大人な人として見られています。",
 11:"周囲からは、感性の鋭い、特別な雰囲気の人として見られています。",22:"周囲からは、スケールの大きなことを成し遂げる人として見られています。",33:"周囲からは、型にはまらない、愛にあふれた人として見られています。"}
SOUL = {1:"心の奥では、自分の力で道を切りひらきたいと願っています。",2:"心の奥では、大切な人と心を通わせたいと願っています。",3:"心の奥では、自由に表現し、人生を楽しみたいと願っています。",
 4:"心の奥では、安心できる居場所と確かな土台を求めています。",5:"心の奥では、何にも縛られず、世界を広げたいと願っています。",6:"心の奥では、愛し愛される、あたたかな関係を求めています。",
 7:"心の奥では、物事の本当の意味を知りたいと願っています。",8:"心の奥では、努力を形にし、認められたいと願っています。",9:"心の奥では、誰かや社会の役に立ちたいと願っています。",
 11:"心の奥では、自分にしかできない使命を果たしたいと願っています。",22:"心の奥では、後の世に残る何かを築きたいと願っています。",33:"心の奥では、すべての人をまるごと受けとめたいと願っています。"}
YEAR = {1:"始まりの年。新しい挑戦の種をまくとき。",2:"育てる年。人との信頼関係を深めるとき。",3:"楽しむ年。発信と表現で縁が広がるとき。",
 4:"固める年。生活と仕事の土台を整えるとき。",5:"動く年。変化を受け入れて世界を広げるとき。",6:"つながる年。家族や身近な人を大切にするとき。",
 7:"深める年。学びと内省で自分を見つめるとき。",8:"実る年。努力が成果や収入として表れるとき。",9:"しめくくりの年。手放して次に備えるとき。"}
MONTH = {1:"新しく始める",2:"協力を得る",3:"楽しく発信する",4:"足元を固める",5:"変化に乗る",6:"人を大切にする",7:"立ち止まって考える",8:"結果を取りにいく",9:"整理して手放す"}

def personal_year(birth, y): return reduce(dsum(birth.month) + dsum(birth.day) + dsum(y), keep=False)
def personal_month(birth, y, m): return reduce(personal_year(birth, y) + dsum(m), keep=False)

def build(name, romaji, birth, out):
    n = numbers_for(birth, romaji)
    L = NUMBERS[n["life"]]
    doc = BaseDocTemplate(out, pagesize=A5, leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm,
                          title=f"{name}様 数秘術鑑定書", author="数秘のとびら")
    def deco(c, d):
        c.saveState(); c.setFillColor(PAPER); c.rect(0, 0, A5[0], A5[1], stroke=0, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(.5); c.rect(8*mm, 8*mm, A5[0]-16*mm, A5[1]-16*mm)
        c.setFont("JP", 7); c.setFillColor(SOFT)
        if d.page > 1:
            c.drawString(16*mm, 11*mm, f"{name}様 数秘術鑑定書"); c.drawRightString(A5[0]-16*mm, 11*mm, f"{d.page}")
        c.restoreState()
    doc.addPageTemplates([PageTemplate(frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=deco)])
    st = []
    P = lambda t, s="body": st.append(Paragraph(t, S[s]))

    # 1 表紙
    st += [Spacer(1, 30*mm)]; P("数秘のとびら", "center"); st.append(Spacer(1, 6*mm))
    P(f"{name} 様", "h1"); st[-1].style = ParagraphStyle("t", parent=S["h1"], alignment=TA_CENTER)
    P("数秘術鑑定書", "center"); st.append(Spacer(1, 12*mm))
    P(str(n["life"]), "big"); P(f"運命数 {n['life']}　{L['name']}", "center"); st.append(Spacer(1, 18*mm))
    P(f"生年月日　{birth.year}年{birth.month}月{birth.day}日<br/>作成日　{datetime.date.today():%Y年%m月%d日}", "center")
    st.append(PageBreak())

    # 2 4つの数字
    P("YOUR NUMBERS", "eyebrow"); P("あなたを形づくる4つの数字", "h1")
    P("数秘術では、生年月日と名前からいくつかの数字を導き、その組み合わせで人を読み解きます。この鑑定書では、次の4つの数字をもとにお伝えします。")
    rows = [["数字", "意味", "あなたの数"],
            ["運命数", "人生全体のテーマ・本質", str(n["life"])],
            ["誕生数", "生まれ持った才能", str(n["day"])],
            ["表現数", "周囲から見たあなた", str(n["expr"] or "－")],
            ["ソウル数", "心の奥の願い", str(n["soul"] or "－")]]
    t = Table(rows, colWidths=[22*mm, 60*mm, 20*mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "JP", 9), ("TEXTCOLOR", (0, 0), (-1, 0), SOFT),
        ("LINEBELOW", (0, 0), (-1, -1), .4, LINE), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("TEXTCOLOR", (2, 1), (2, -1), GOLD), ("FONTSIZE", (2, 1), (2, -1), 13), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    st += [Spacer(1, 4*mm), t, Spacer(1, 4*mm)]
    P(f"計算方法：運命数は生年月日の数字をすべて足して一桁に（{birth:%Y%m%d} → {dsum(birth.strftime('%Y%m%d'))} → {n['life']}）。誕生数は生まれた日。表現数・ソウル数はローマ字の名前（{romaji.upper()}）をピタゴラス式で数字に置きかえて求めます。", "small")
    st.append(PageBreak())

    # 3 運命数
    P("LIFE PATH", "eyebrow"); P(f"運命数{n['life']}　{L['name']}", "h1"); P(L["kw"], "h2")
    P(L["intro"]); P("あなたの本質", "h2"); P(L["personality"]); P("あなたへのメッセージ", "h2"); P(L["advice"])
    st.append(PageBreak())

    # 4 誕生数・表現数・ソウル数
    P("THREE NUMBERS", "eyebrow"); P("もうひとつの顔", "h1")
    P(f"誕生数 {n['day']}　生まれ持った才能", "h2"); P(DAY[n["day"]] + f" キーワードは「{NUMBERS[n['day']]['kw']}」。" + NUMBERS[n["day"]]["work"])
    if n["expr"]:
        P(f"表現数 {n['expr']}　周囲から見たあなた", "h2"); P(EXPR[n["expr"]] + f" 「{NUMBERS[n['expr']]['kw']}」の印象を与えやすく、それがあなたの評判や仕事のチャンスにつながります。")
        P(f"ソウル数 {n['soul']}　心の奥の願い", "h2"); P(SOUL[n["soul"]] + " この願いが満たされているとき、あなたは心から満足し、ほかの数字の力もいちばん発揮されます。")
        if n["soul"] != n["expr"]:
            P(f"表現数{n['expr']}とソウル数{n['soul']}が異なるため、人から見られている姿と、心の中で求めているものに少し差があるかもしれません。ときどき「本当はどうしたい？」と自分に聞いてみると、迷いが減っていきます。")
    st.append(PageBreak())

    # 5 恋愛・相性
    P("LOVE", "eyebrow"); P("恋愛・結婚と相性", "h1"); P(L["love"])
    P("相性のよい運命数", "h2")
    for c in L["compat"]:
        P(f"<font color='#9a7428'>運命数{c}（{NUMBERS[c]['name']}）</font>　{NUMBERS[c]['kw']}。おだやかに支え合える組み合わせです。")
    if n["soul"]:
        P("恋愛で大切にしたいこと", "h2"); P(f"ソウル数{n['soul']}のあなたは、{SOUL[n['soul']].replace('心の奥では、', '')}恋愛でもこの気持ちを満たしてくれる相手を選ぶと、長く幸せな関係を築けます。")
    st.append(PageBreak())

    # 6 仕事・お金
    P("WORK & MONEY", "eyebrow"); P("仕事とお金の流れ", "h1"); P("向いている働き方", "h2"); P(L["work"])
    P("お金との付き合い方", "h2"); P(L["money"])
    P("才能を収入につなげるヒント", "h2"); P(f"誕生数{n['day']}の「{NUMBERS[n['day']]['kw']}」を活かせる場面を、仕事の中に意識してつくりましょう。得意なことを任されるほど、評価と収入は自然についてきます。")
    st.append(PageBreak())

    # 7-8 年運
    this = datetime.date.today().year
    for y in (this, this + 1):
        py = personal_year(birth, y)
        P(f"YEAR {y}", "eyebrow"); P(f"{y}年のあなた　個人年数{py}", "h1"); P(YEAR[py], "h2")
        P(f"9年でひとめぐりする数秘術のサイクルで、{y}年のあなたは「{NUMBERS[py]['kw']}」の流れの中にいます。運命数{n['life']}のあなたらしさ（{L['kw']}）を、この年のテーマにどう重ねるかがポイントです。")
        P("この年にやるとよいこと", "h2"); P({1:"新しい習慣や挑戦を、ひとつだけ決めて始める。",2:"信頼できる人との関係に時間を使う。",3:"発信・表現・趣味を増やす。",4:"お金と生活の仕組みを見直す。",5:"行ったことのない場所へ行き、会ったことのない人に会う。",6:"家族やパートナーとの時間を優先する。",7:"本を読む、学ぶ、ひとりで考える時間をつくる。",8:"仕事で成果を取りにいく。値上げや昇進の交渉も吉。",9:"使っていない物や関係を整理する。"}[py])
        st.append(PageBreak())

    # 9 月ごとカレンダー
    P("CALENDAR", "eyebrow"); P("月ごとの運気カレンダー", "h1")
    P("個人月数は、個人年数に月の数を足して求めます。毎月のテーマとしてお使いください。", "small")
    rows = [["年月", "個人月数", "テーマ"]]
    for y in (this, this + 1):
        for m in range(1, 13):
            pm = personal_month(birth, y, m); rows.append([f"{y}年{m}月", str(pm), MONTH[pm]])
    t = Table(rows, colWidths=[30*mm, 20*mm, 52*mm], rowHeights=6.6*mm)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "JP", 8), ("TEXTCOLOR", (0, 0), (-1, 0), SOFT),
        ("LINEBELOW", (0, 0), (-1, -1), .3, LINE), ("ALIGN", (1, 0), (1, -1), "CENTER"), ("TEXTCOLOR", (1, 1), (1, -1), GOLD),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    st += [Spacer(1, 2*mm), t, PageBreak()]

    # 10 おわりに
    st.append(Spacer(1, 20*mm)); P("おわりに", "h1")
    P(f"{name}様、最後までお読みいただきありがとうございました。数字は、あなたの未来を決めるものではなく、あなたがもともと持っている力に気づくための手がかりです。迷ったときや節目のときに、この鑑定書をまた開いてみてください。")
    P("この鑑定書が、あなたの扉をひらくきっかけになりますように。")
    st.append(Spacer(1, 10*mm)); P("数秘のとびら", "center")
    P("※本鑑定書は数秘術にもとづく読み物です。医療・法律・金融などの判断の代わりにはなりません。", "small")
    doc.build(st)
    return n

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True); ap.add_argument("--romaji", required=True)
    ap.add_argument("--birth", required=True); ap.add_argument("--out")
    a = ap.parse_args()
    b = datetime.date.fromisoformat(a.birth)
    out = a.out or f"鑑定書_{a.name.replace(' ', '')}.pdf"
    print(build(a.name, a.romaji, b, out), "->", out)
