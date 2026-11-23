# Episode 1 · ON SCREEN cards

20 animated info cards (MP4 videos, 1920×1080, 30 fps, no sound) in the style of Beanie Survives' data cards. The `.jpg` files are only still previews; use the `.mp4` files.

## Where each card goes

Every card goes **after** a clip, never on top of it. Put it **between** the two clips listed, right after the voice finishes the line shown.

**Example:** `c01-clock-947.mp4` goes after **clip 004** ("He just doesn't know who he's begging.") and before **clip 005**.

## How to do it in CapCut

1. Find the end of the "after" clip on your timeline (the timecode below is approximate until your voiceover is recorded; go by the line).
2. Insert the card on the **main video track** at that point.
3. **Keep the voiceover running.** The card plays while the voice moves on to the next line.
4. So the timing doesn't drift, **trim the start of the next clip** by the card's length (for example, cut the first 3.6 seconds off clip 005). The card replaces the beginning of that clip's picture, not its sound.
5. Add the sound effect for the card (listed in section 2 of the prompt book).

| # | Card file | Length | Put it AFTER clip | and BEFORE clip | Around | The voice has just said |
|---|---|---|---|---|---|---|
| 1 | `c01-clock-947.mp4` | 3.6s | **004** | **005** | 0:15 | "He just doesn't know who he's begging." |
| 2 | `c02-lease-stamp.mp4` | 4.2s | **007** | **008** | 0:30 | "… folder with a red tab. One line stamped across the front." |
| 3 | `c03-clock-952.mp4` | 3.6s | **013** | **014** | 0:50 | "Then it starts climbing again." |
| 4 | `c04-year-1.mp4` | 4.6s | **028** | **029** | 2:07 | "…f the desk, you need to go back to the Tuesday it started." |
| 5 | `c05-week-of-lunches.mp4` | 6.1s | **039** | **040** | 3:13 | "Ten containers lined up on the counter like soldiers." |
| 6 | `c06-the-rules.mp4` | 7.6s | **040** | **041** | 3:21 | "…I wrote the night I got the job. Four rules. Black marker." |
| 7 | `c07-lunch-math.mp4` | 6.1s | **059** | **060** | 4:53 | "…ch. Five for coffee. Five days a week, fifty weeks a year." |
| 8 | `c08-marcus-stats.mp4` | 6.6s | **066** | **067** | 5:27 | "…nds at a cocktail lounge, so everybody knows who's buying." |
| 9 | `c09-my-stats.mp4` | 6.6s | **073** | **074** | 6:02 | "… every bonus and every tax refund, moves the day it lands." |
| 10 | `c10-year-2.mp4` | 4.6s | **076** | **077** | 6:20 | "…r sliver of the five hundred biggest companies in America." |
| 11 | `c11-net-worth-62k.mp4` | 6.1s | **085** | **086** | 7:10 | "… boring little account crosses sixty-two thousand dollars." |
| 12 | `c12-year-3.mp4` | 5.1s | **088** | **089** | 7:29 | "…have to stop being the customer and start being the owner." |
| 13 | `c13-net-worth-94k.mp4` | 5.6s | **102** | **103** | 8:38 | "I have ninety-four thousand dollars ready." |
| 14 | `c14-refinance.mp4` | 6.6s | **111** | **112** | 9:25 | "Fourteen months later, every unit is full, and we refinance." |
| 15 | `c15-year-5.mp4` | 5.1s | **121** | **122** | 10:14 | "…arcus sees me, he's going to be carrying one just like it." |
| 16 | `c16-the-building.mp4` | 6.1s | **126** | **127** | 10:37 | "Price: two point four million dollars." |
| 17 | `c17-clock-1000.mp4` | 3.6s | **138** | **139** | 11:22 | "Which brings us back to this morning." |
| 18 | `c18-the-choice.mp4` | 7.1s | **160** | **161** | 13:16 | "… is the moment I didn't let myself imagine for five years." |
| 19 | `c19-rule-4.mp4` | 4.6s | **175** | **176** | 14:37 | "…my kitchen cabinet. Five years old. The corners gone soft." |
| 20 | `c20-episode-2.mp4` | 5.6s | **182** | (end of video) | 15:06 | "… and Arthur is calling. The east side building is on fire." |

Card 20 is the last thing in the video: put it after the final clip, as the closing teaser.

Source: `../cards-src/` (`node render.js ../cards 30` re-renders them).