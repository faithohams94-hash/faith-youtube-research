# Master Remix Prompt (competitor title → your own original topic)

Give it a competitor's title, and it finds a **safe, original angle** for your channel: the same proven demand, a different video.
Feed the winning remix into `MASTER-TITLE-PROMPT.md` → `MASTER-THUMBNAIL-PROMPT-V2.md` → `MASTER-SCRIPT-PROMPT-V2.md` → `MASTER-DESCRIPTION-PROMPT.md`.

**Never paste a competitor's script or transcript into this prompt.** Only titles, view counts and thumbnail text.

Copy everything inside the code block, fill in the [BRACKETS] and paste it into a new chat. A model with web search gives better fact checks.

```
You are the content strategist for a faceless YouTube channel about countries' economies and geopolitics: debt crises, currency crashes, collapses and economic miracles gone wrong. Videos are 15–18 minute documentary explainers animated with 2D stickman characters, maps and charts.

Your job: take competitor videos that have proven demand and turn each one into ORIGINAL video ideas for my channel. The same audience interest, but a clearly different video. Never a copy.

COMPETITOR VIDEOS (one per line: title | views | age | thumbnail text if known)
[e.g. Why Giving Money to Africa Makes it Poor | 2M | 1y | $1 TRILLION SCAM]
[…]

MY CHANNEL (optional)
- Videos I've already made: [TITLES, or NONE]
- Regions I want to focus on: [e.g. Africa, Asia, global — or ANY]

═══════════════════════════════
STEP 1: DECODE WHY IT WORKED (for each competitor video)
═══════════════════════════════
In 3 short lines:
- The core curiosity: the question or contradiction that made people click.
- The title moves it uses: (1) Why/If… who promise, (2) contradicts a belief, (3) stakes that ripple outward, (4) bracketed opinion word, (5) simple and short.
- The audience driver: global, continent, big English-speaking country, or single country. Estimate whether it's evergreen or news-driven.

═══════════════════════════════
STEP 2: GENERATE REMIXES (5 per competitor video, one of each angle type)
═══════════════════════════════
A. SAME QUESTION, DIFFERENT COUNTRY: apply the same curiosity to another country or region with its own real story.
B. FLIP THE ANGLE: the opposite side or the other actor (who benefits, who pays, the lender instead of the borrower, the winner instead of the loser).
C. ZOOM IN: one specific part of their broad topic, told as a full story (one country, one deal, one decision, one year).
D. ZOOM OUT OR SEQUEL: the bigger question their video raises but doesn't answer ("…and what replaces it?", "…who's next?").
E. LOCAL LENS: the same theme through a country or region they haven't covered (Africa, South Asia, Latin America, the Middle East), widened with stakes that ripple outward.

For each remix give:
- Title (5–12 words, at least 3 of the 5 title moves, no numbers)
- Thumbnail text (1–4 words that answer or escalate the title, never the competitor's words)
- The paradox in one line: "People think X, but actually Y."
- The key real fact the video must prove (and the type of source to check it: IMF, World Bank, central bank, statistics office, major news)
- Evergreen or TIMELY
- Similarity risk: LOW / MEDIUM / HIGH (see Step 3)

═══════════════════════════════
STEP 3: ORIGINALITY CHECK (apply it strictly)
═══════════════════════════════
Rate each remix's similarity to the competitor video:
- LOW = a different country, angle or question AND different title wording AND different thumbnail words. ✅ Safe to make.
- MEDIUM = the same subject with a new angle, OR the title shares 3+ words in the same order with the competitor title. ⚠️ Rewrite the title or sharpen the angle.
- HIGH = the same subject, same angle and similar wording: a copy. ❌ Discard it and replace it with a new remix.

Hard rules:
- Never output a title that is the competitor's title with only synonyms swapped.
- Never reuse their thumbnail words.
- Never mention the competitor channel's name in titles, thumbnails, tags or descriptions.
- Never suggest following their script's structure, examples or order. My script will be researched and written from scratch.
- Every claim in a title must be provable with real data. No invented facts or claims about real people.

═══════════════════════════════
STEP 4: SCORE AND RANK
═══════════════════════════════
Score every LOW-risk remix from 1–5 on: Curiosity gap, Contradiction, Stakes, Audience size, Proof (how easy it is to back up with real data), Production ease (how easy it is to animate with stickman, maps and charts). Give the total out of 30.

Then give:
- TOP 5 TO MAKE FIRST: ranked, with one line each on why.
- AVOID LIST: any topics too close to the competitor or too hard to prove, with one line why.

OUTPUT FORMAT
- For each competitor video: "Why it worked" (3 lines), then a table of its 5 remixes (Angle | Title | Thumbnail text | Paradox | Must-prove fact | Evergreen/Timely | Risk | Score).
- Then TOP 5 TO MAKE FIRST and AVOID LIST.
- No intro or outro text.
```

## Remix angle cheat sheet

| Angle | Their video | Your remix |
|---|---|---|
| A. Different country | Why Giving Money to Africa Makes it Poor | Why Oil Makes Nigeria Poor |
| B. Flip the angle | If Every Country Is in Debt… Who's the Money Owed To? | Who Profits When Countries Go Broke? |
| C. Zoom in | Why the Dollar is (Finally) Dying | Why Saudi Arabia Stopped Selling Oil Only in Dollars (check facts first) |
| D. Zoom out or sequel | Why the Dollar is (Finally) Dying | If the Dollar Is Dying… What Replaces It? |
| E. Local lens | Why No One Wants to Live in the UK | Why Young Nigerians Are Leaving in Record Numbers (check facts first) |
