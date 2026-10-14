// Builds index.html from src/, embedding a pre-rendered plate and study notes
// so previews that don't run JavaScript (iPhone Files / Quick Look) still show content.
// Usage: NODE_PATH=<dir with playwright> node build.js
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const dir = __dirname, src = f => fs.readFileSync(path.join(dir, "src", f), "utf8");
const assemble = (shell) => `${shell}<script>\n${src("2-data.js")}\n${src("3-app.js")}</script>\n`;
(async () => {
  const shell = src("1-shell.html");
  const tmp = path.join(dir, ".build-tmp.html");
  fs.writeFileSync(tmp, assemble(shell));
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH });
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await p.goto("file://" + tmp); await p.waitForTimeout(600);
  const plate = await p.evaluate(() => {
    const svg = document.querySelector("#stage svg").cloneNode(true);
    svg.querySelectorAll(".hit").forEach(e => e.remove());
    return svg.outerHTML;
  });
  const notes = await p.evaluate(() => {
    const e = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    const L = { o: "Origin", c: "Course", r: "Relations", b: "Branches", e: "Termination", s: "Supplies", p: "Palpate", i: "Insertion", a: "Action", n: "Nerve", t: "Test", k: "Clinical" };
    const groups = {};
    for (const id in S) { const o = S[id]; if (o.sys === "bone" && o.pt === undefined && id === "skull") continue; const gk = (o.sys === "muscle" ? "Muscles: " : "") + o.grp; (groups[gk] = groups[gk] || []).push(o); }
    let h = `<section class="static-notes" id="static-notes"><h3>Study notes: every structure</h3>`;
    for (const g in groups) {
      h += `<details><summary>${e(g)} (${groups[g].length})</summary>`;
      for (const o of groups[g]) {
        h += `<h4>${e(o.n)}</h4><p>${e(o.sum || "")}</p>`;
        if (o.steps) h += `<p><b>Trace the course:</b></p><ol>${o.steps.map(s => `<li>${e(s[2])}</li>`).join("")}</ol>`;
        for (const k in (o.f || {})) h += `<p><b>${L[k] || k}:</b> ${e(o.f[k])}</p>`;
      }
      h += `</details>`;
    }
    return h + `</section>`;
  });
  await b.close(); fs.unlinkSync(tmp);
  const out = shell.replace("<!--STATIC_PLATE-->", `<div id="static-plate">${plate}</div>`).replace("<!--STATIC_NOTES-->", notes);
  fs.writeFileSync(path.join(dir, "index.html"), assemble(out));
  console.log("built index.html", fs.statSync(path.join(dir, "index.html")).size, "bytes");
})();
