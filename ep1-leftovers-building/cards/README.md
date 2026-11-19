# Episode 1 · ON SCREEN cards

20 animated info cards in the style of Beanie Survives' data cards: the **EPISODE 1** header on top, a cream panel across the middle with the characters in that scene, and the bottom kept clear for your captions.

**Format:** MP4, 1920×1080, 30 fps, no sound. Each card holds on its last frame for 0.6 seconds at the end.

## How to use them in CapCut

1. Find the shot number in the table below (it matches the prompt book).
2. At that point in your timeline, **split the clip and insert the card on the main track** as a short cutaway, the way Beanie cuts to the WATER card. Keep your narration running underneath.
3. Trim or slow the card to fit the line it covers.
4. Add the sound effect listed in section 2 of the prompt book (tick, stamp thud, cha-ching and so on).

| Card file | Length | Goes at | Script line |
|---|---|---|---|
| `c01-clock-947.mp4` | 3.6s | Shot 004 · 0:12 | "He just doesn't know who he's begging.…" |
| `c02-lease-stamp.mp4` | 4.2s | Shot 007 · 0:25 | "Next to it, a folder with a red tab. One line stamped across the front…" |
| `c03-clock-952.mp4` | 3.6s | Shot 014 · 0:50 | "My property manager knocks once and leans in. They're early, she says.…" |
| `c04-year-1.mp4` | 4.6s | Shot 029 · 2:07 | "Five years ago, I'm twenty-nine. Operations analyst at a logistics fir…" |
| `c05-week-of-lunches.mp4` | 6.1s | Shot 039 · 3:10 | "Ten containers lined up on the counter like soldiers.…" |
| `c06-the-rules.mp4` | 7.6s | Shot 041 · 3:21 | "I read it every Sunday while the rice cooks.…" |
| `c07-lunch-math.mp4` | 6.1s | Shot 059 · 4:47 | "Twenty-two dollars for lunch. Five for coffee. Five days a week, fifty…" |
| `c08-marcus-stats.mp4` | 6.6s | Shot 067 · 5:27 | "Between the car loan and the credit card from his last vacation, his n…" |
| `c09-my-stats.mp4` | 6.6s | Shot 073 · 5:55 | "Everything left over, about nineteen hundred, plus every bonus and eve…" |
| `c10-year-2.mp4` | 4.6s | Shot 077 · 6:20 | "December. The company holiday party. Marcus is running the Secret Sant…" |
| `c11-net-worth-62k.mp4` | 6.1s | Shot 085 · 7:06 | "That same month, my boring little account crosses sixty-two thousand d…" |
| `c12-year-3.mp4` | 5.1s | Shot 089 · 7:29 | "Year three, Marcus gets promoted again. Now he's my manager.…" |
| `c13-net-worth-94k.mp4` | 5.6s | Shot 102 · 8:36 | "I have ninety-four thousand dollars ready.…" |
| `c14-refinance.mp4` | 6.6s | Shot 112 · 9:25 | "My seventy-five thousand comes back to me in cash.…" |
| `c15-year-5.mp4` | 5.1s | Shot 122 · 10:14 | "Over the next two years, Arthur and I roll the cash flow into two more…" |
| `c16-the-building.mp4` | 6.1s | Shot 126 · 10:35 | "Price: two point four million dollars.…" |
| `c17-clock-1000.mp4` | 3.6s | Shot 138 · 11:19 | "Which brings us back to this morning.…" |
| `c18-the-choice.mp4` | 7.1s | Shot 160 · 13:12 | "This is the moment I didn't let myself imagine for five years.…" |
| `c19-rule-4.mp4` | 4.6s | Shot 176 · 14:37 | "Rule four.…" |
| `c20-episode-2.mp4` | 5.6s | Shot 182 · 14:58 | "Next time on Somber Journal: it's 2:14 in the morning, and Arthur is c…" |

`*.jpg` files are the finished last frame of each card, for a quick look.

Source: `../cards-src/` (`art.js` draws the characters and icons, `cards.js` lays out the cards, `render.js` renders them; run `node render.js ../cards 30`).