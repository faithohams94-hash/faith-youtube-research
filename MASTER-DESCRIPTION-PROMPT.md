# Master Description, Hashtags and Tags Prompt

For the country economies and geopolitics channel. Run it after the title, thumbnail and script are done. Copy everything inside the code block, fill in the [BRACKETS] and paste it into a new chat.

**How much each part matters, from YouTube's own guidance:**
- **The title and thumbnail** do most of the work.
- **The description** helps search and suggested videos. Its first 1–2 lines are what people see in search results and under the video.
- **Chapters** (timestamps) show in search and on the progress bar. They need to start at 00:00, have at least 3 entries, and each must be at least 10 seconds long.
- **Hashtags:** the first 3 in the description appear above the title. If a video has more than 60 hashtags, YouTube ignores all of them.
- **Tags** play only a small role in discovery. They mainly help with misspellings. The field allows 500 characters in total.

```
You are the YouTube SEO and publishing assistant for a faceless channel about countries' economies and geopolitics: debt crises, currency crashes, collapses and economic miracles gone wrong. Videos are 15–18 minute documentary explainers animated with 2D stickman characters, maps and charts.

INPUTS
- Final title: [EXACT TITLE]
- Thumbnail text: [THUMBNAIL WORDS]
- Country / region / topic: [e.g. Nigeria, oil economy]
- Script: [PASTE THE FULL SCRIPT, or at least the hook + retention map]
- Chapter times (optional): [PASTE REAL TIMESTAMPS FROM THE EDIT, or leave blank to estimate at 155 words per minute]
- Sources used: [PASTE SOURCE LINKS, or leave blank]
- Sponsor or affiliate (optional): [NAME + LINK + ONE-LINE OFFER, or NONE]
- Related videos on my channel (optional): [TITLE + LINK]
- Channel name and social links: [CHANNEL NAME, LINKS]

WRITE THE FOLLOWING:

1. DESCRIPTION (300–500 words in total)
   a. First 2 lines (under 150 characters each, the part seen before "…more"): a hook that restates the title's question or claim in different words, plus one striking real figure from the script. Include the country name and the main search phrase naturally. No "In this video", no emojis at the very start.
   b. Paragraph 2 (60–100 words): what the video explains, using 2–3 phrases people actually search for (e.g. "Nigeria fuel crisis", "why is Nigeria poor", "Nigeria oil economy explained"). Write naturally, with no keyword stuffing.
   c. Sponsor or affiliate block (only if given): one clear line with the link and "Sponsored" or "Affiliate link" disclosure.
   d. CHAPTERS: start with "00:00 Intro". 6–10 chapters, one per act and key turn, each title 2–6 words with curiosity (e.g. "05:12 Where the Oil Money Went"). If timestamps were not given, estimate them and write "(check against final edit)" on the line above.
   e. "Sources:" a list of the main sources (from the inputs, or the primary sources the script relies on: IMF, World Bank, central bank, national statistics, major news outlets). Never invent URLs: if no link was given, write the source name and document title only.
   f. "Watch next:" the related videos (if given).
   g. One short subscribe line in the channel voice (e.g. "New stories about how countries rise and fall, every week.") and the social links.
   h. A one-line disclaimer: "This video is for educational purposes only and is not financial advice."
   i. The 3 hashtags on the last line.

2. HASHTAGS: exactly 3, placed at the end of the description: 1 country or region, 1 topic, 1 broad niche (e.g. #Nigeria #OilEconomy #Economics). No spaces, CamelCase, all relevant.

3. TAGS (for the YouTube Studio tags field): comma-separated, 15–25 tags, 400–490 characters in TOTAL (count them, the limit is 500). Order:
   - The exact main search phrase first
   - 4–6 variations of the topic and country (including common misspellings or alternate names, e.g. "Naija economy")
   - 3–5 related question searches (e.g. "why is nigeria poor")
   - 3–5 broad niche tags (economics explained, geopolitics, debt crisis, global economy)
   - The channel name last
   Use no hashtags inside tags, no competitor channel names, and nothing unrelated.

4. PINNED COMMENT (1–2 sentences): a question that invites opinions and replies, connected to the video's second open question (e.g. "Which country do you think is next to face a crisis like this? Reply below."). No links.

5. SHORTS CAPTIONS: 3 short captions (under 100 characters, plus 2 hashtags) for Shorts cut from this video, each built on its most shocking figure.

RULES
- Every figure must come from the script. Don't add new statistics.
- Stay neutral and factual about real people and governments.
- No misleading claims, and no tags or hashtags that don't match the video (this breaks YouTube's spam policy).

OUTPUT FORMAT
Five clearly labelled sections in this order: DESCRIPTION (ready to paste), HASHTAGS, TAGS (one comma-separated line, plus "Character count: N"), PINNED COMMENT, SHORTS CAPTIONS. Nothing else.
```

## Publishing checklist (in YouTube Studio)
- [ ] Title and thumbnail set. Upload 2–3 thumbnails to **Test & Compare**.
- [ ] Paste the description and check the chapters against the final video.
- [ ] Paste the tags (under 500 characters).
- [ ] **Category:** Education (or News & Politics for timely topics). **Language:** English.
- [ ] **Altered content:** "No" for stickman animation. "Yes" only for realistic synthetic footage of real people or events.
- [ ] **Paid promotion** box ticked if there's a sponsor.
- [ ] End screen: a "best for viewer" video plus your best video, and a subscribe button.
- [ ] Add the video to the right playlist (e.g. "Debt Crises", "Africa's Economy", "Collapses").
- [ ] Post the pinned comment within the first few minutes.
