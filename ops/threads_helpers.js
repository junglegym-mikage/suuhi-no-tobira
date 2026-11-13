// Threads 予約投稿ヘルパー（threads.com のホームで javascript_exec に貼って使う。ページを再読み込みしたら再実行）
// 1件ごとの手順:
//   1) await __open()            … 「新しいスレッド」を開く（開いていれば何もしない）
//   2) computer left_click で本文欄（「最近どう？」, 800x600 の座標で約 230,274）をクリック
//   3) computer type で本文 + "\n\n#数秘術" を入力（JS で文字を入れると改行やトピック欄が崩れる）
//   4) await __go(日, '07'|'12'|'21', 本文の先頭, 文字数)
//      … 本文チェック → もっと見る → 日時を指定 → 日付・時刻 → 完了 → 「投稿予定」の表示を確認 → 予約 → 次の作成画面を開く
//   {ok: '…投稿予定', open: 'open'} なら完了。{err:'nocal'} はカレンダーの表示待ち切れ → __pickDT と __submit を手で続ける。
// 注意：__go の open が 'fail' でも、少し遅れて作成画面が開くことがある。3秒待って作成画面が0個のときだけ __open() する（重ねて開くと空の画面が下に残り、次の本文チェックが失敗する）。
// 予約は最大25件（下書きアイコンの一覧で数を確認）。月をまたぐ予約はこのヘルパーでは扱わない（11月専用：__pickDT の month 引数で確認だけする）。
{
window.__sl = ms => new Promise(r => setTimeout(r, ms));
window.__leaf = (root, txt) => Array.from(root.querySelectorAll('div,span')).filter(e => e.childElementCount === 0 && e.textContent.trim() === txt);
const composers = () => Array.from(document.querySelectorAll('[role=dialog]')).filter(x => /新しいスレッド/.test(x.innerText));
const composer = () => composers().pop();
window.__cnt = () => composers().length;
window.__calRoot = () => { const d = __leaf(document, '完了')[0]; if (!d) return null; let r = d; while (r && !/\d{4}年\d+月/.test(r.innerText || '')) r = r.parentElement; return r; };
window.__setIn = (el, v) => { const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; el.focus(); s.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); el.blur(); };
window.__open = async () => {
  if (composer()) return 'already open';
  const b = __leaf(document, '投稿').find(e => !e.closest('[role=dialog]')); if (!b) return 'no btn';
  (b.closest('[role=button],button') || b).click(); for (let i = 0; i < 10; i++) { await __sl(500); if (composer()) return 'open'; } return 'fail';
};
window.__body = () => { const d = composer(); const e = d && d.querySelector('[contenteditable=true]'); return e ? e.innerText : null; };
window.__menuSched = async () => {
  const d = composer(); let h = __leaf(d, '新しいスレッド')[0]; while (h && h.querySelectorAll('svg').length < 2) h = h.parentElement; if (!h) return 'no header';
  const svgs = h.querySelectorAll('svg'); const s = svgs[svgs.length - 1]; (s.closest('[role=button],button') || s).click(); await __sl(700);
  const it = Array.from(document.querySelectorAll('div,span')).find(e => e.childElementCount === 0 && /^日時を指定/.test(e.textContent.trim()) && !(e.closest('[role=dialog]') || {}).innerText?.includes('投稿オプション'));
  if (!it) return 'no item'; (it.closest('[role=button],[role=menuitem]') || it).click();
  for (let i = 0; i < 12; i++) { await __sl(400); if (__calRoot()) return 'cal'; } return 'nocal';
};
window.__pickDT = async (month, day, hh, mm) => {
  const r = __calRoot(); if (!r) return 'no cal'; const head = (r.innerText.match(/\d{4}年(\d+)月/) || [])[1]; if (+head !== month) return 'month is ' + head;
  const cells = __leaf(r, String(day)); if (!cells.length) return 'no day'; (cells[0].closest('[role=button],button,[role=gridcell]') || cells[0]).click(); await __sl(400);
  const h = document.querySelector('input[placeholder=hh]'), m = document.querySelector('input[placeholder=mm]'); __setIn(h, hh); __setIn(m, mm); await __sl(300);
  const vals = [h.value, m.value]; const dn = __leaf(r, '完了')[0]; (dn.closest('[role=button],button') || dn).click(); await __sl(800);
  const d = composer(); return { vals, banner: ((d && d.innerText.match(/[^\n]*投稿予定[^\n]*/)) || [''])[0] };
};
window.__submit = async () => {
  const d = composer(); if (!d || !/投稿予定/.test(d.innerText)) return 'no banner';
  const b = __leaf(d, '日時を指定').pop(); if (!b) return 'no btn'; (b.closest('[role=button],button') || b).click();
  for (let i = 0; i < 20; i++) { await __sl(500); if (!composer()) return 'scheduled'; } return 'dialog still open';
};
window.__go = async (day, hh, start, len, month = 11) => {
  if (__cnt() !== 1) return { err: 'composers=' + __cnt() };
  const b = __body(); if (!b || !b.startsWith(start) || Math.abs(b.length - len) > 2) return { err: 'body', got: b && b.slice(0, 20), n: b && b.length };
  const m = await __menuSched(); if (m !== 'cal') return { err: m };
  const p = await __pickDT(month, day, hh, '00'); if (!p.banner || !p.banner.includes(String(+hh) + ':00')) return { err: 'banner', p };
  const s = await __submit(); if (s !== 'scheduled') return { err: s }; await __sl(3000); return { ok: p.banner, open: __cnt() ? 'open' : await __open(), n: __cnt() };
};
}
'threads helpers loaded';
