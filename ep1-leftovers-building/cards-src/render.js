// Render every card frame by frame and encode to MP4.
// usage: node render.js <outDir> [fps] [cardId ...]   (needs playwright and ffmpeg)
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");
// CARDS_MODULE picks another episode's card list (it must export CARDS and page); default is Episode 1.
const { CARDS, page } = require(process.env.CARDS_MODULE || "./cards");

const outDir = path.resolve(process.argv[2] || "out");
const FPS = +(process.argv[3] || 30);
const only = process.argv.slice(4);
const HOLD = 0.6; // seconds held on the final frame

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const tab = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const c of CARDS) {
    if (only.length && !only.includes(c.id)) continue;
    const htmlFile = path.join(outDir, c.id + ".html");
    fs.writeFileSync(htmlFile, page(c));
    await tab.goto("file://" + htmlFile);
    await tab.evaluate(() => document.fonts.ready);
    const total = Math.round((c.dur + HOLD) * FPS);
    const mp4 = path.join(outDir, c.id + ".mp4");
    const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", mp4]);
    const done = new Promise((res, rej) => ff.on("close", (code) => (code ? rej(new Error("ffmpeg " + code)) : res())));
    for (let f = 0; f < total; f++) {
      await tab.evaluate((t) => window.render(t), Math.min(f / FPS, c.dur + 1));
      const buf = await tab.screenshot({ type: "jpeg", quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
      if (f === total - 1) fs.writeFileSync(path.join(outDir, c.id + ".jpg"), buf);
    }
    ff.stdin.end();
    await done;
    fs.unlinkSync(htmlFile);
    console.log("rendered", c.id, (c.dur + HOLD).toFixed(1) + "s");
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
