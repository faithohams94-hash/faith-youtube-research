# Writer spec — "Distinction Study Book" for Kris Ohapulomuogo (2nd MBBS, Imo State University)

Reader: a busy 2nd-MBBS student (MBBS, Imo State University, Owerri) who wants a DISTINCTION.
He must (1) know the answer to every question and (2) understand it well, with diagrams.
Lecturers here reward: a clear definition/introduction, headings, numbered points,
labelled diagrams, tables for comparisons, clinical correlates, and a short conclusion.
MANDATORY SOURCE TEXTS (the user insisted — follow strictly):
- ANATOMY (gross, neuro, embryology, histology, genetics under ANA): **BD Chaurasia's Human Anatomy** (and Chaurasia's
  companion handbooks for histology/embryology/genetics where relevant). Use Chaurasia's headings, terminology, lists,
  mnemonics and diagram style. Where Chaurasia lists e.g. "relations" or "contents" in a particular order, keep that order.
- BIOCHEMISTRY (all BCM courses): **Vasudevan & Sreekumari, Textbook of Biochemistry for Medical Students** and
  **U. Satyanarayana, Biochemistry**. Use their classifications, pathway schemes, enzyme names, and clinical boxes.
- PHYSIOLOGY (all PHS/PIO courses, incl. pathophysiology & lab practicals): **K. Sembulingam, Essentials of Medical Physiology**.
  Use Sembulingam's definitions, values, classifications and headings.
STAY INSIDE PRECLINICAL (2nd MBBS) BOUNDARIES: do not go into clinical-year management, drug doses, surgical
technique, or recent research beyond what these books contain. "Clinical significance/applied" notes only at the level
these textbooks give in their applied/clinical boxes. When the question is a pathophysiology one, answer at the level
Sembulingam (and Chaurasia/Vasudevan applied notes) cover — mechanism, features — not treatment protocols
(if a question explicitly asks treatment, give a brief preclinical-level outline only).
You may add `<span class="tag freq">Source: Chaurasia Vol 3, Ch. ...</span>`-style source tag in q-meta naming the book (and chapter
topic if you are confident; do NOT invent page numbers).
Be factually precise. No made-up facts.

## Output
Write ONE HTML fragment file (no <html>/<head>/<body>) at the path you are given.
It is concatenated into a book that already links `style.css`. Use ONLY the classes below.
Do NOT use emoji (they render inconsistently). Plain text symbols like → ↑ ↓ ✓ are fine.
Do NOT use external images or scripts. Diagrams = inline SVG you draw by hand.

## Structure of your fragment

```html
<h2 class="section" id="sec-<slug>">Anatomy — Head and Neck</h2>
<div class="section-sub">One line: what this section covers + how often it is examined.</div>

<div class="paper-banner"><b>Paper 2 — 18/3/2026</b> · Answer any 4 questions · 2 hrs</div>

<section class="q" id="q8">
  <div class="q-head">
    <div class="q-num">Q8</div>
    <div class="q-body-head">
      <div class="q-meta"><span class="tag course">Anatomy · Head &amp; Neck</span><span class="tag year">Paper 2 · 18/3/2026</span><span class="tag marks">Essay</span></div>
      <h3 class="q-title">Explain the blood supply, nerve supply ... (EXACT question wording)</h3>
      <div class="revise">Revision tracker: <span class="cb"></span>Read <span class="cb"></span>Drew diagram <span class="cb"></span>Wrote from memory</div>
    </div>
  </div>

  <div class="box examiner"><span class="box-t">What the examiner wants</span> 1–3 lines: the marking points / keywords that earn marks.</div>

  <div class="answer">
    <h4>Introduction / Definition</h4> ...
    <h4>...headings exactly as he should write them...</h4> numbered points, tables
    <figure class="diagram"> <svg ...>...</svg>
      <figcaption><b>Fig 8.1</b> Layers of the scalp (SCALP). <span class="draw-tip">Exam drawing tip: draw 5 parallel bands, label left side, 3 minutes.</span></figcaption>
    </figure>
    <h4>Clinical significance</h4> ...
    <h4>Conclusion</h4> 1–2 lines.
  </div>

  <div class="box understand"><span class="box-t">Understand it (plain English)</span> explain the logic like a friend, so it sticks.</div>
  <div class="box mnemonic"><span class="box-t">Memory trick</span> mnemonic(s).</div>
  <div class="box exam-tip"><span class="box-t">How to write this in the exam</span> time plan, order of headings, which diagram to draw first, marks-winning phrases.</div>
  <div class="box pitfall"><span class="box-t">Mistakes that cost marks</span> ...</div>

  <div class="selftest"><div class="st-t">Quick self-test — cover the right column</div>
    <table><tr><th>Question</th><th>Answer</th></tr>
      <tr><td>...</td><td class="ans">...</td></tr>  (3–5 rows)
    </table></div>
  <div class="related">Related: <a href="#q15">Q15 Scalp &amp; bleeding</a> · <a href="#q21">Q21</a></div>
</section>
```

Optional boxes: `box clinical` (clinical correlate), `kw` span for keywords: `<span class="kw">Circle of Willis</span>`.
HTML flowchart helper: `<div class="flow"><span class="step">Receptor</span><span class="arr">→</span><span class="step">Dorsal root ganglion</span></div>` (add class `v` for vertical).

## Rules
1. EVERY question in your range gets its own `<section class="q" id="qN">` with the EXACT number N from the question bank and the exact wording, plus its year/paper tag (e.g. `[MK2010]`, `2017`, `Paper 2 · 18/3/2026`, `3rd In-course · 27/10/2025`). For questions without a year use the paper name. MK = Main/MBBS exam key, RT = resit — keep the code as given.
2. Answers are written the way a distinction student writes in the exam: headings, numbered points, definitions first, tables for comparisons, clinical notes, conclusion. Full depth for essays; short-note questions get crisp, complete short notes.
3. DIAGRAMS: every question where a diagram earns marks MUST have at least one clean, labelled inline SVG
   (anatomy schematics, cross-sections, pathways, flowcharts, cycles, graphs, tables-as-figures).
   SVG rules: set `viewBox`, width ≤ 680, use font-family="Inter, sans-serif", font-size 10–12,
   stroke colours from: #0b5cad blue, #0f8a7e teal, #c2410c orange, #b42318 red, #15803d green, #6d28d9 purple, #1b2330 ink;
   soft fills (#eef5fc, #edfaf7, #fff4ec, #fff1f0, #f5f0ff, #fff7e0). Leader lines from labels to structures.
   Make labels never overlap. Keep it schematic and correct — the kind he can reproduce by hand in 2–4 minutes.
   Add arrowhead markers via <defs><marker id="UNIQUE-ID">… — marker/gradient IDs MUST be unique across the whole book: prefix them with your question number, e.g. `id="a8"`, `id="q8-arr"`.
4. REPEATED questions (same topic asked again in another year): still give the question its own section with its own tag,
   but you may give a focused answer tailored to the exact wording and start with
   `<div class="box repeat"><span class="box-t">Asked before</span> This topic is also asked in <a href="#q8">Q8</a> — full diagrams there. Below is the answer tailored to THIS wording.</div>`.
   The tailored answer must still be complete enough to score well on its own. Link only to question numbers that exist (1–402) — prefer ones in your own range; cross-range links are fine if you are sure of the number.
5. Escape `&` as `&amp;`, `<` as `&lt;` in text. Valid, well-formed HTML. No `<style>` or `<script>` tags. No inline `style` beyond small tweaks.
6. Keep the voice warm and confident; this book is for Kris — you may occasionally address him ("Kris, ...") in the Understand/exam-tip boxes, sparingly.
7. Do not invent past-question years. Do not add questions that are not in your range.

## Question bank numbering
See the full question list file you are given. Use those numbers verbatim.
