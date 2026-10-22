// 数秘のとびら Instagram投稿ヘルパー（instagram.com のページ内で javascript_exec に貼って使う）
// 使い方: 1) このファイル全体を実行 → 2) await __igOpen() → 3) await __igAttach(spec)
//        → 4) await __igToCaption() → 5) キャプションを入力 → 6) await __igShare()
{
window.__sleep = ms => new Promise(r => setTimeout(r, ms));
window.__waitFor = async (fn, ms = 8000) => { const t = Date.now(); while (Date.now() - t < ms) { const v = fn(); if (v) return v; await __sleep(200); } return null; };
const F = { serif: '"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif', sans: '"Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif' };
const C = { paper: '#f3f0e8', ink: '#1d2433', soft: '#5a6276', gold: '#9a7428', seal: '#a83a2c', line: '#cfc8b6' };
function base() {
  const c = document.createElement('canvas'); c.width = 1080; c.height = 1080; const x = c.getContext('2d');
  x.fillStyle = C.paper; x.fillRect(0, 0, 1080, 1080); x.strokeStyle = C.line; x.lineWidth = 3; x.strokeRect(40, 40, 1000, 1000);
  x.lineWidth = 1; x.strokeRect(54, 54, 972, 972); x.textAlign = 'center'; x.textBaseline = 'top'; return [c, x];
}
function t(x, txt, y, size, font, color, weight = '', xpos = 540, align = 'center') { x.font = `${weight} ${size}px ${font}`; x.fillStyle = color; x.textAlign = align; x.fillText(txt, xpos, y); x.textAlign = 'center'; }
function footer(x) { t(x, '数秘のとびら', 940, 34, F.serif, C.ink, 'bold'); t(x, 'プロフのリンクから無料診断', 984, 26, F.sans, C.soft); }
window.__igDraw = (spec) => {
  const [c, x] = base();
  if (spec.type === 'card') {
    t(x, '運命数', 120, 46, F.serif, C.soft, 'bold');
    t(x, String(spec.n), spec.n < 10 ? 170 : 220, spec.n < 10 ? 420 : 330, F.serif, C.gold, 'bold');
    t(x, spec.name, 660, 72, F.serif, C.ink, 'bold'); t(x, spec.kw, 770, 36, F.sans, C.seal);
    x.strokeStyle = C.line; x.lineWidth = 2; x.beginPath(); x.moveTo(480, 840); x.lineTo(600, 840); x.stroke();
  } else if (spec.type === 'aisho') {
    t(x, '保存版', 110, 40, F.sans, C.soft); t(x, '運命数の相性早見表', 165, 76, F.serif, C.ink, 'bold');
    spec.rows.forEach(([n, s], i) => { const y = 300 + i * 66; t(x, String(n), y, 52, F.serif, C.gold, 'bold', 320); t(x, '×', y + 8, 40, F.sans, C.soft, '', 400); t(x, s, y + 2, 48, F.serif, C.ink, 'bold', 450, 'left'); });
  } else if (spec.type === 'year2026') {
    t(x, '誕生月＋誕生日＋2026 を一桁に', 110, 36, F.sans, C.soft); t(x, '2026年、あなたは何の年？', 165, 66, F.serif, C.ink, 'bold');
    ['始まりの年', '育てる年', '楽しむ年', '固める年', '動く年', 'つながる年', '深める年', '実る年', 'しめくくりの年'].forEach((s, i) => { const y = 300 + i * 66; t(x, String(i + 1), y, 52, F.serif, C.gold, 'bold', 350); t(x, s, y + 6, 46, F.serif, C.ink, 'bold', 420, 'left'); });
  }
  footer(x); return c;
};
window.__igOpen = async () => {
  const s = document.querySelector('svg[aria-label="新しい投稿"]'); if (!s) return 'no create button';
  (s.closest('a,[role=button],button') || s).click(); await __sleep(1200);
  const sub = Array.from(document.querySelectorAll('span')).find(e => e.textContent.trim() === '投稿'); if (sub) (sub.closest('a,[role=button],button,[role=link]') || sub).click();
  return (await __waitFor(() => document.querySelector('input[type=file]'))) ? 'ok' : 'no file input';
};
window.__igAttach = async (spec) => {
  const c = __igDraw(spec); const blob = await new Promise(r => c.toBlob(r, 'image/jpeg', 0.93));
  const inp = document.querySelector('input[type=file]'); const dt = new DataTransfer(); dt.items.add(new File([blob], 'post.jpg', { type: 'image/jpeg' }));
  inp.files = dt.files; inp.dispatchEvent(new Event('change', { bubbles: true }));
  return (await __waitFor(() => Array.from(document.querySelectorAll('[role=dialog] div,[role=dialog] span')).find(e => e.childElementCount === 0 && e.textContent.trim() === '次へ'))) ? 'attached' : 'attach failed';
};
const clickText = async (txt) => { const b = await __waitFor(() => Array.from(document.querySelectorAll('[role=dialog] div,[role=dialog] span,[role=dialog] button')).find(e => e.childElementCount === 0 && e.textContent.trim() === txt)); if (!b) return false; (b.closest('[role=button],button') || b).click(); await __sleep(1500); return true; };
window.__igToCaption = async () => { await clickText('次へ'); await clickText('次へ'); const el = await __waitFor(() => document.querySelector('[role=dialog] div[contenteditable=true]')); if (!el) return 'no caption box'; el.focus(); return 'caption ready'; };
window.__igShare = async () => { if (!(await clickText('シェア'))) return 'no share button'; const ok = await __waitFor(() => Array.from(document.querySelectorAll('span,div')).find(e => e.childElementCount === 0 && /シェアされました/.test(e.textContent)), 30000); return ok ? 'shared' : 'not confirmed'; };
window.__igAccount = () => Array.from(document.querySelectorAll('a[href^="/"]')).map(a => a.getAttribute('href')).filter(h => /^\/[a-z0-9._]+\/$/.test(h) && !/^\/(explore|reels|notifications|direct)\/$/.test(h))[0] || null;
}
'ig helpers loaded';
