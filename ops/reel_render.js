// 使い方: node ops/reel_render.js <spec.json> <out.mp4>
// ig_reel.js の __reelDraw を Chromium で1コマずつ描き、ffmpeg で 1080x1920・30fps の mp4 にする。
// 背景音楽（2026-11-07〜）: reel_music.js の自作曲を入れる（spec.music:false で無音）。
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { chromium } = require('playwright');
(async () => {
  const [specPath, out] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const code = fs.readFileSync(path.join(__dirname, 'ig_reel.js'), 'utf8');
  const browser = await chromium.launch(); const page = await browser.newPage();
  await page.setContent('<html><body></body></html>'); await page.evaluate(code);
  await page.evaluate(() => document.fonts.ready);
  const tmp = out.replace(/\.mp4$/, '') + '.tmp.mp4';
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
  if (!spec.dur) spec.dur = 8;
  const total = Math.round(spec.dur * 30);
  for (let f = 0; f < total; f++) {
    const b64 = await page.evaluate(([s, t]) => { const c = __reelCanvas(); __reelDraw(c.getContext('2d'), s, t); return c.toDataURL('image/jpeg', 0.95).split(',')[1]; }, [spec, f / 30]);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); const code2 = await new Promise(r => ff.on('close', r)); await browser.close();
  if (code2 !== 0) { console.error('ffmpeg failed'); process.exit(1); }
  const music = require('./reel_music.js'), mc = music.choose(spec);
  if (mc) {
    const wav = out.replace(/\.mp4$/, '') + '.music.wav'; fs.writeFileSync(wav, music.wav(music.render({ mood: mc.mood, seed: mc.seed, dur: spec.dur })));
    const ff2 = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', tmp, '-i', wav, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], { stdio: 'inherit' });
    const c3 = await new Promise(r => ff2.on('close', r)); fs.unlinkSync(wav); fs.unlinkSync(tmp); if (c3 !== 0) { console.error('ffmpeg (music) failed'); process.exit(1); }
  } else fs.renameSync(tmp, out);
  console.log('ok', out, fs.statSync(out).size, mc ? 'music:' + mc.mood : 'no music');
})();
