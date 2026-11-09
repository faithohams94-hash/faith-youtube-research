# Why the POV channel isn't getting views: an audit

*Researched 2026-11-09. Based on everything in this repo (4 scripts, the master prompts, thumbnail sets, voiceover timings) plus web research on the niche and YouTube policy. I have not seen the live channel or YouTube Studio data. Section 6 lists what to pull so the diagnosis can be confirmed.*

---

## TL;DR: the 7 most likely causes, ranked

| # | Problem | Evidence in the repo | Fix effort |
|---|---------|----------------------|-----------|
| 1 | **The hook arrives too late.** The premise ("Here's what nobody tells you…") lands 80–120 seconds in. | Brother: word 250 (~1:36). Parents: word 315 (~2:01). Divorce: word 209 (~1:20). | Low |
| 2 | **Titles and thumbnails hide the twist.** They sell the misery ("still at mom's", "work for your brother") and leave out the payoff (secretly owns 24%, paid in full). | `brother-company/book-config.json` puts "Nobody knows you own 24%" in a *subtitle*, not the title. Parents thumbnails v4 deliberately "sell the pain". | Low |
| 3 | **There's no clear channel identity.** Four videos use two formats (LADDER/ARC) and four different audiences (a 20s money tour, a 30-year-old at home, a 40-year-old employee, a 55-year-old divorcé). | Locked protagonist is a "young man… oversized head", even when the story says he is 40 or 55. | Medium |
| 4 | **The videos are too long and slow for a brand-new channel.** | Parents 25:16, divorce 16:31, brother 15:48. Narration runs ~2.4 words/sec, slow for second-person drama. | Low–Medium |
| 5 | **Dark, desaturated thumbnails** that disappear in a mobile feed. | Parents v4: "moody desaturated slate-blue palette with deep shadows". This contradicts your own master prompt ("bright, saturated"). | Low |
| 6 | **"Inauthentic / templated content" risk.** A locked formula, AI stills on 5-second beats and a likely TTS voice match the profile YouTube says it is tightening against. | One master prompt generates every script. "Quiet Equity" style is locked. Video prompts animate only 20 beats of hospitals. | Medium |
| 7 | **Inconsistent upload cadence, and a crowded title pattern.** | Commits: 4 scripts in 3 weeks (Oct 3–22), none since. "How X Treats You at Every Level of Wealth" is a heavily copied title pattern. | Medium |

If you only do three things, fix #1, #2 and #5 on the next upload. They're cheap, and they affect the two numbers that decide whether YouTube keeps showing a video: CTR and first-30-second retention.

---

## 1. The hook problem (biggest retention leak)

On a new channel, YouTube gives each video a small test audience. If most of them leave in the first 30 seconds, it stops showing the video. Most "no views" channels fail here.

Your ARC scripts open with a slow, literary scene and *then* state the premise:

| Script | Words before the premise | Time before the premise |
|--------|---------------------------|--------------------------|
| second-pov (divorce at 55) | 209 | ~1:20 |
| brother-company | 250 | ~1:36 |
| parents-at-30 | 315 | ~2:01 |
| hospitals (LADDER) | n/a: "Level one, zero dollars" is a hook in line 1 | ✅ |

The writing is good. The problem is that a click from a cold viewer is a bet. By second 10 they need to know **what they'll get by staying**, and right now they don't.

**Fix: a 15-second cold-open "promise" before the scene.** For example, in brother-company:

> "You own twenty-four percent of your little brother's company. He tells two hundred people he built it alone. Nobody knows about the check in your wallet. Not his wife. Not your father. Tonight, that changes."

*Then* "It's 8:15 on a Monday morning…" Move the "Here's what nobody tells you" paragraph up to roughly 0:20–0:30.

Add a rule to `MASTER-SCRIPT-PROMPT.md` (ARC section): *"The first 3 sentences state the secret, the injustice and the stakes. The full premise must land before word 75."*

## 2. Packaging: titles and thumbnails don't sell the payoff

People click on **curiosity plus a payoff**. They don't click on misery alone.

| Current | Problem | Stronger direction |
|---------|---------|--------------------|
| *POV: You Work for Your Younger Brother* | Sounds like a sad workplace vlog. The 24% secret is hidden. | **POV: Your Brother Says He Built It Alone (You Secretly Own 24%)** |
| *POV: You Still Live With Your Parents at 30* | Reads as pity. The "paid in full" twist is invisible. | **POV: Everyone Pities You for Living at Home (You Paid Off the House)** |
| second-pov (divorce): **no title in the repo** | Title written as an afterthought? | **POV: She Took Half in the Divorce. She Didn't Know About the Envelope.** |
| *How Hospitals Treat You at Every Level of Wealth* | Fine, but it's a crowded copy-pattern, so you're up against established channels on the same search. | Keep the format, but add a sharper angle: **"I Got the Same Surgery at $0 and $50M"** |

**Thumbnail rule:** show the **contrast**. Your master prompt already says this ("CALM VS CHAOS", "status reversal"), but parents-at-30 v4 dropped it for "the dark side". A thumbnail of a sad man at a dinner table answers its own question, so there's nothing left to click for. Show the moment *just before* the reveal instead: the folded check, the "PAID IN FULL" text on his phone, the family's smug faces.

Also:
- Parents thumbnail text "AT 30?" repeats the title, which breaks your own rule #6.
- AI image models often garble text. Add overlay text afterwards in Canva/Photoshop, not in the prompt.
- Test at phone size: shrink to 160×90 px. If you can't tell what's happening, it fails.
- Use YouTube's **Test & Compare** (thumbnail A/B testing in Studio) on every upload.

## 3. Channel identity: who is this channel for?

Right now a viewer who liked one video gets no strong signal that the next video is for them:

- **Hospitals** = a "wealth levels" explainer (young, finance-curious audience)
- **Parents at 30** = a quiet-millionaire arc (20s–30s)
- **Brother company** = a sibling and family-business drama (30s–50s)
- **Divorce at 55** = a midlife-comeback revenge story (45–65, the most proven audience for "underestimated, secretly rich" stories)

Your strongest, most original asset is the **"underestimated person with a secret money advantage"** arc. Three of your four scripts are already that. Commit to it:

1. **Pick the one format** (ARC: "everyone underestimates you, you have a secret") and make the next 8–10 videos in it. Put the LADDER videos on hold, or make them a clearly labeled series.
2. **Fix the protagonist mismatch.** A chibi "young man" narrating "you are fifty-five" breaks immersion, and viewers comment on it. Either age the design per story (gray streaks, same glasses and hoodie silhouette), or make the channel about one consistent age band.
3. Write the identity into the channel banner and the "About" text, e.g. *"POV stories about the people everyone underestimates."*

## 4. Length and pacing

- 25 minutes (parents-at-30) is very long for an unknown channel. Long videos are fine *once* people trust you; for a new channel, **10–14 minutes** is the sweet spot for this genre.
- Narration runs ~2.4 words/sec (from the SRT timings). Try **2.7–2.9 w/s**. The `parents-at-30/voiceover/` folder has both "slow" and "normal" versions, so pick the faster one.
- Your script prompt already targets 2,300–2,500 words for 15 minutes. Cut to **~1,800–2,000 words** until average view duration (AVD) data shows people stay.
- Add a **re-hook every 60–90 seconds** ("And that's when the email came."). Add a mid-video tease of the payoff around 40% of the way through, where most retention graphs dip.

## 5. "Inauthentic content" and AI-slop risk

YouTube renamed its "repetitious content" rule to **"inauthentic content"** (July 2025) and clarified it again in **July 2026**: generic or repetitive mass-produced videos aren't monetizable. Reports say whole channels are now evaluated together. AI use itself is allowed. The problem is videos that *feel* templated. Even before monetization, viewers bounce fast from slideshow-style AI videos with a robotic voice, and that hurts reach.

Your pipeline has several of those signals:
- One master prompt writes every script, with locked phrases ("Here's what nobody tells you", "Not X. Just Y.", "Somewhere right now, someone…"). After a few videos these become a noticeable tic.
- Still images every ~5 seconds with subtle motion; only ~20 beats animated per video.
- Narration appears to be generated (the voiceover `.mp3`s are git-ignored build output). If it's TTS, it's probably the #1 reason people leave in the first 10 seconds.

**Mitigations:**
- **Use a real human voice** (your own, or a hired narrator on Fiverr/Voices). This is probably the single highest-value change for this genre.
- Vary the sentence-level phrasing per video. Take the stock phrases out of the master prompt and add a rule: "never reuse a signature phrase in consecutive videos".
- Add editing that a template can't: sound design (fluorescent hum, courtroom murmur), music swells at reveals, on-screen text for numbers, occasional zooms or cuts tied to the narration.
- Disclose altered/synthetic content where YouTube asks for it.

## 6. Consistency and competition

- Your commit history shows 4 scripts between Oct 3 and Oct 22 and nothing since. If uploads are that irregular too, the algorithm and early subscribers lose track of you. **Aim for 1 video per week, same day**, and keep 2 finished videos in reserve.
- "How [X] Treats You at Every Level of Wealth" and "Every Level of Wealth in N Minutes" are among the most-copied title patterns on YouTube. You're competing with established channels on a template. The ARC stories are **more original**, which is another reason to lean into them.
- **Shorts:** cut a 30–50-second vertical teaser from each video: the reveal moment, with a hook in the first line. It's the cheapest discovery channel for a new account, and it can pull viewers to the long version.

---

## 7. What to pull from YouTube Studio to confirm the diagnosis

Open **YouTube Studio → Analytics → Advanced mode** and note these numbers for each video:

| Metric | Where | What it tells you |
|--------|-------|-------------------|
| **Impressions** | Reach tab | Under ~1,000 means YouTube isn't testing the video. Packaging or niche signal is the problem (sections 2–3). |
| **Impressions CTR** | Reach tab | Under ~3% means the title or thumbnail is the problem (section 2). YouTube says half of all channels sit between 2% and 10%. |
| **Retention at 0:30** | Engagement → Audience retention | Under ~60% means the hook is the problem (section 1). |
| **Average view duration (and %)** | Engagement | Under ~30% means pacing or length is the problem (section 4). |
| **Traffic sources** | Reach | Browse/Suggested ≈ 0 means the algorithm isn't picking it up yet. |
| **Monetization / policy notices** | Earn tab, email | Any "inauthentic content" flag (section 5). |

How to read it:
- **Low impressions, decent CTR**: a niche or identity problem → section 3.
- **Healthy impressions, low CTR**: packaging → section 2.
- **Healthy CTR, retention collapses early**: hook or voice → sections 1 and 5.
- **Good early retention, low AVD**: length or pacing → section 4.

---

## 8. Action plan for the next upload

1. Pick the strongest finished script (brother-company). Rewrite the first 30 seconds so they state the secret and the stakes, and cut it to ~12 minutes.
2. Re-record with a human voice, or at least a better voice at ~2.8 words/sec.
3. Retitle it: **"POV: Your Brother Says He Built It Alone (You Secretly Own 24%)"**.
4. Make 3 bright, high-contrast thumbnails using the CALM-vs-CHAOS rule: the smug brother on stage, the deadpan protagonist in front, the check stub with a red arrow. A/B test them with Test & Compare.
5. Post a 40-second Short of the reveal the same day.
6. After 7 days, record the metrics in section 7 and compare with the older videos.
7. Update `MASTER-SCRIPT-PROMPT.md` and `MASTER-THUMBNAIL-PROMPT.md` with the new rules (premise before word 75, payoff visible in thumbnail, no repeated signature phrases, 1,800–2,000 words).

---

### Sources
- [Tubefilter: YouTube inauthentic content monetization policy update (Jul 2026)](https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/)
- [Metricool: YouTube clarifies its AI content rules](https://metricool.com/youtube-ai-content-rules-monetization/)
- [TechRepublic: YouTube tightens monetization rules for AI-generated and low-quality content](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)
- [vidIQ: Can you monetize AI-generated videos in 2026?](https://vidiq.com/blog/post/youtube-ai-monetization/)
- [OutlierKit: Why faceless channels get demonetized](https://outlierkit.com/resources/faceless-youtube-channel-demonetized/)
- [AIR Media-Tech: YouTube monetization policy changes 2026 timeline](https://air.io/en/monetization/youtube-monetization-policy-changes-2026-a-complete-dated-timeline)
- [Subscribr: Why your YouTube videos get no views](https://subscribr.ai/youtube-strategy/youtube-videos-no-views-fix)
- [Subscribr: YouTube analytics for newbies](https://subscribr.ai/youtube-strategy/youtube-analytics-for-newbies)
- [Yoola: Why your YouTube videos are not getting views in 2026](https://yoola.com/blog/why-your-youtube-videos-are-not-getting-views-in-2026)
- [OutlierKit: Faceless YouTube growth strategy 2026](https://alpha.outlierkit.com/resources/faceless-youtube-growth-strategy/)
- [Gary Wu: Faceless channel playbook](https://garywu.github.io/posts/faceless-channel-playbook)

*Note: most third-party sources are creator-tool blogs. Treat their benchmarks (CTR %, retention thresholds) as rough heuristics, not YouTube-official numbers.*
