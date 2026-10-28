"""Builds the Movie Recap Course deck as HTML (one 16:9 slide per page).

Run:  python3 build/build_pdf.py   (from movie-recap-course/)
"""

MODULES = [
    ("m1", "What Is the Movie Recap Niche?"),
    ("m2", "Is It Profitable?"),
    ("m3", "Tools You Need"),
    ("m4", "Where to Find Movie Ideas"),
    ("m5", "Where to Download Movies"),
    ("m6", "Writing Your Script"),
    ("m7", "Generating Voiceover"),
    ("m8", "Editing & Avoiding Copyright"),
    ("m9", "Uploading Your Videos"),
    ("m10", "Tips & Hacks"),
]

slides = []  # (id, module_index or None, html)


def nav(sid, mod):
    idx = [s[0] for s in slides].index(sid)
    prev_id = slides[idx - 1][0] if idx > 0 else None
    next_id = f"__NEXT_{idx}__"
    dots = "".join(
        f'<a class="dot{" on" if mod == i else ""}" href="#{m}">{i + 1}</a>'
        for i, (m, _) in enumerate(MODULES)
    )
    prev = f'<a class="nb" href="#{prev_id}">&#9664; Prev</a>' if prev_id else '<span class="nb off">&#9664; Prev</span>'
    return f'''<div class="nav">
      {prev}<a class="nb home" href="#roadmap">&#9776; Roadmap</a><a class="nb" href="#{next_id}">Next &#9654;</a>
      <div class="dots">{dots}</div>
      <div class="pg">{idx + 1}</div>
    </div>'''


def slide(sid, mod, body, cls=""):
    slides.append((sid, mod, body, cls))


def header(mod, kicker=None):
    num = f"{mod + 1:02d}"
    title = MODULES[mod][1]
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f'<div class="hdr"><div class="mnum">MODULE {num}</div><h2>{title}</h2>{k}</div>'


# ---------------------------------------------------------------- COVER
slide("cover", None, '''
<div class="cover">
  <div class="strip top"></div>
  <div class="cv-inner">
    <div class="badge">&#9654; FULL COURSE</div>
    <h1>MOVIE<br><span>RECAP</span><br>COURSE</h1>
    <p class="sub">From zero to a monetised YouTube movie recap channel. Ideas, scripts, voiceover, editing, uploads and growth.</p>
    <a class="cta" href="#roadmap">START THE COURSE &#9654;</a>
  </div>
  <div class="reel">
    <div class="r1"></div><div class="r2"></div>
    <div class="play">&#9654;</div>
  </div>
  <div class="strip bot"></div>
</div>''', "dark")

# ---------------------------------------------------------------- ROADMAP
cards = "".join(
    f'<a class="rm" href="#{m}"><b>{i + 1:02d}</b><span>{t}</span><i>&#9654;</i></a>'
    for i, (m, t) in enumerate(MODULES)
)
slide("roadmap", None, f'''
<div class="hdr"><div class="mnum">COURSE ROADMAP</div><h2>10 modules. Tap any one to jump in.</h2></div>
<div class="rmgrid">{cards}</div>
<div class="hint">&#128073; Every page has <b>Prev / Roadmap / Next</b> buttons and numbered dots at the bottom. They're all clickable.</div>
''')

# ---------------------------------------------------------------- M1
slide("m1", 0, header(0, "The niche in one sentence") + '''
<div class="big-quote">A movie recap channel <span class="hl">tells the story of a full movie in 10 to 30 minutes</span>, so busy viewers get the whole idea without spending 2+ hours watching it.</div>
<div class="row3">
  <div class="card"><div class="ic">&#9203;</div><h4>People are busy</h4><p>They see a trailer and want the story, but they don't have time to sit through the full movie.</p></div>
  <div class="card"><div class="ic">&#127916;</div><h4>Recaps fill the gap</h4><p>A recap gives them the plot, the twists and the ending in a fraction of the time.</p></div>
  <div class="card"><div class="ic">&#128100;</div><h4>Faceless</h4><p>You never show your face. Movie clips, a voiceover and good editing carry the whole video.</p></div>
</div>
<div class="flow"><span>Watch the movie</span><em>&#10140;</em><span>Summarise</span><em>&#10140;</em><span>Script</span><em>&#10140;</em><span>Voiceover</span><em>&#10140;</em><span>Edit</span><em>&#10140;</em><span>Upload</span></div>
''')

# ---------------------------------------------------------------- M2 (a)
slide("m2", 1, header(1, "Short answer: YES. Very, very profitable.") + '''
<div class="row2">
  <div>
    <ul class="ticks">
      <li><b>Endless demand.</b> People always want to watch movies, and new ones come out every week.</li>
      <li><b>Endless content.</b> Every movie ever made is a possible video. You'll never run out of ideas.</li>
      <li><b>Long watch time.</b> Recaps run 10 to 30 minutes, so you get more ad breaks and more money per view.</li>
      <li><b>Global audience.</b> Recaps work in English, Hindi, Swahili, Spanish and more. You can even run more than one channel.</li>
      <li><b>Faceless and repeatable.</b> Once you have your system, every video follows the same steps.</li>
    </ul>
  </div>
  <div class="money">
    <div class="m-lbl">HOW YOU GET PAID</div>
    <div class="m-row"><span>&#128176;</span><div><b>YouTube AdSense</b><br>Join the Partner Program (1,000 subs + 4,000 watch hours)</div></div>
    <div class="m-row"><span>&#129309;</span><div><b>Sponsorships</b><br>Apps and brands pay for mentions</div></div>
    <div class="m-row"><span>&#128279;</span><div><b>Affiliate links</b><br>Tools you use, in your description</div></div>
    <div class="m-row"><span>&#128200;</span><div><b>Multiple channels</b><br>Same skill, different languages or genres</div></div>
  </div>
</div>
<a class="jump" href="#m2b">See real channels making money &#9654;</a>
''')

# ---------------------------------------------------------------- M2 (b) channels
CH = [
    ("Movie Recaps", "@movierecapsofficial", "2.77M", "~$17.1K", "/ month", "vidIQ", "https://vidiq.com/youtube-stats/channel/@movierecapsofficial/", 100),
    ("Movie Recaps PK", "@movierecaps-d1p", "1.17M", "4.39M", "views / 30 days", "vidIQ", "https://vidiq.com/youtube-stats/channel/@movierecaps-d1p/", 42),
    ("Movie Recap Swahili", "@movierecapswahili1", "361K", "~$1.3K", "/ month", "vidIQ", "https://vidiq.com/youtube-stats/channel/@movierecapswahili1/", 13),
    ("XYZ Movie Recaps", "", "53K", "$820 to $2.3K", "/ month", "Social Blade-style tracker", "https://socialblade.com/", 2),
    ("Movie Recap 4U", "", "81K", "$258 to $737", "/ month", "Social Blade-style tracker", "https://socialblade.com/", 3),
]
rows = "".join(f'''
  <a class="ch" href="{u}">
    <div class="ch-av">{n[0]}</div>
    <div class="ch-n"><b>{n}</b><small>{h or "&nbsp;"}</small></div>
    <div class="ch-bar"><div style="width:{w}%"></div><span>{s} subs</span></div>
    <div class="ch-e"><b>{e}</b><small>{per}</small></div>
    <div class="ch-src">{src} &#8599;</div>
  </a>''' for n, h, s, e, per, src, u, w in CH)
slide("m2b", 1, header(1, "5 movie recap channels making money right now") + f'''
<div class="chs">{rows}</div>
<div class="note">Estimated AdSense only (no sponsors), from vidIQ and Social Blade-style trackers, Jul to Oct 2026. Tap a row to open live stats. Even the <b>smaller</b> channels earn every month.</div>
''')

# ---------------------------------------------------------------- M2 (c) math
slide("m2c", 1, header(1, "The money math: what ONE video can earn") + '''
<div class="formula"><span>VIEWS</span><em>&divide; 1,000</em><em>&times;</em><span>RPM</span><em>=</em><span class="g">YOUR PAY</span></div>
<p class="center dim">RPM = what you earn per 1,000 views. For long movie recaps, roughly <b>$1 to $5</b> depending on your audience's country.</p>
<div class="row3 calc">
  <div class="card"><div class="v">50K views</div><div class="pay">$50 to $250</div><p>A small but solid video</p></div>
  <div class="card hot"><div class="v">500K views</div><div class="pay">$500 to $2,500</div><p>One good video that takes off</p></div>
  <div class="card"><div class="v">2M views</div><div class="pay">$2,000 to $10,000</div><p>A viral recap. It happens in this niche.</p></div>
</div>
<div class="hint">&#128161; Do this live in class: open any recap channel on Social Blade or vidIQ and work out the earnings together.</div>
''')

# ---------------------------------------------------------------- M3 tools
TOOLS = [
    ("CapCut", "Editing", "Cut clips, add effects, zoom, blur, subtitles and export. Free on phone and PC.", "https://www.capcut.com", "&#9986;"),
    ("ChatGPT / Gemini", "Script writing", "Turn your movie summary into a full recap script with one prompt. Use whichever you like.", "https://chat.openai.com", "&#9998;"),
    ("Google Flow", "Thumbnails", "Generate eye-catching thumbnail images from a prompt.", "https://labs.google/flow", "&#127912;"),
    ("ElevenLabs", "Voiceover", "Realistic AI voices that sound human. Free tier, paid plans for more.", "https://elevenlabs.io", "&#127908;"),
    ("MovieBox", "Movies", "Watch and download the movies you will recap (Module 05).", "#m5", "&#127871;"),
]
tc = "".join(f'''<a class="tool" href="{u}"><div class="t-ic">{ic}</div><div class="t-tag">{tag}</div><h4>{n}</h4><p>{d}</p><div class="t-go">Open &#8599;</div></a>'''
             for n, tag, d, u, ic in TOOLS)
slide("m3", 2, header(2, "Your whole studio. Most of it is free.") + f'''
<div class="tools">{tc}</div>
<div class="kit"><b>Starter kit:</b> phone or laptop &middot; internet &middot; CapCut &middot; one AI chatbot &middot; one voice tool. That's it.</div>
''')

# ---------------------------------------------------------------- M4 ideas
slide("m4", 3, header(3, "Never run out of movies to recap") + '''
<div class="row2">
  <div>
    <h3 class="sec">Where to look</h3>
    <div class="src-grid">
      <div class="src"><b>MovieBox</b><span>Trending and new releases</span></div>
      <div class="src"><b>Netflix</b><span>"Top 10 today" list</span></div>
      <div class="src"><b>Showbox</b><span>Big library to browse</span></div>
      <div class="src"><b>Downloader app</b><span>Android, for app links</span></div>
      <div class="src"><b>YouTube</b><span>What other recap channels upload</span></div>
      <div class="src"><b>Trailers</b><span>Upcoming and hyped movies</span></div>
    </div>
  </div>
  <div>
    <h3 class="sec">What makes a GOOD pick</h3>
    <ul class="ticks">
      <li>A <b>strong story</b> with a twist, mystery or shocking ending</li>
      <li><b>Trending or newly released</b>, so people are already searching for it</li>
      <li>Genres that do well: <b>thriller, horror, sci-fi, survival, K-drama, crime</b></li>
      <li>Already <b>doing well on other recap channels</b>, which proves people want it</li>
    </ul>
    <div class="tip">&#127919; Keep a running list of 20+ movie ideas so you're never stuck.</div>
  </div>
</div>
''')

# ---------------------------------------------------------------- M5 download
slide("m5", 4, header(4, "Get the movie onto your device") + '''
<div class="row2">
  <div class="hero-tool">
    <div class="ht-ic">&#127871;</div>
    <h3>MovieBox</h3>
    <p>The main app we use. Search the movie, download it in good quality, and it's saved on your device ready to edit.</p>
    <ol class="steps">
      <li>Install MovieBox</li>
      <li>Search for your movie</li>
      <li>Choose the <b>highest quality</b> (720p or 1080p)</li>
      <li>Download, then move it to your editing folder</li>
    </ol>
  </div>
  <div>
    <h3 class="sec">Other options</h3>
    <div class="src-grid one">
      <div class="src"><b>Downloader app (Android)</b><span>Paste a link to install apps or download files</span></div>
      <div class="src"><b>Showbox</b><span>Another big movie library</span></div>
      <div class="src"><b>Bought or rented digital copies</b><span>The safest option for clean, high-quality files</span></div>
    </div>
    <div class="tip">&#128193; Make one folder for each video: <b>movie, script, voiceover, images, thumbnail</b>.</div>
  </div>
</div>
''')

# ---------------------------------------------------------------- M6 script
slide("m6", 5, header(5, "Explain the movie. Don't retell every scene.") + '''
<div class="row2">
  <div>
    <h3 class="sec">The golden rules</h3>
    <ul class="ticks">
      <li><b>Watch the movie fully</b> and understand it before you write a word</li>
      <li>Your goal is to make viewers <b>understand</b> the movie, not to describe every detail</li>
      <li>Keep <b>only the most important parts</b>: the setup, the main conflict, the twists, the ending</li>
      <li><b>Hook in the first 10 seconds.</b> Start with the most shocking moment or question.</li>
      <li>Write the way people talk, in simple and dramatic language</li>
    </ul>
  </div>
  <div class="dont">
    <div class="dd do"><b>&#10004; DO</b><p>"A man wakes up in a locked room with no memory and a note that says <i>don't trust her</i>..."</p></div>
    <div class="dd no"><b>&#10008; DON'T</b><p>"So first he wakes up, then he looks around, then he walks to the door, then he..."</p></div>
  </div>
</div>
<a class="jump" href="#m6b">The time-saving prompt method &#9654;</a>
''')

slide("m6b", 5, header(5, "The shortcut: Summary &#10140; Prompt &#10140; Script") + '''
<div class="pipe">
  <div class="p"><b>1</b><h4>Watch</h4><p>Watch the movie and note the key moments</p></div>
  <em>&#10140;</em>
  <div class="p"><b>2</b><h4>Summarise</h4><p>Write a short summary in your own words, 10 to 20 bullet points</p></div>
  <em>&#10140;</em>
  <div class="p"><b>3</b><h4>Prompt</h4><p>Paste the summary into ChatGPT or Gemini with your master prompt</p></div>
  <em>&#10140;</em>
  <div class="p g"><b>4</b><h4>Script</h4><p>Get a full recap script, then read it and fix anything wrong</p></div>
</div>
<div class="prompt">
  <div class="p-lbl">SAMPLE MASTER PROMPT (we'll build yours in class)</div>
  <code>You are a scriptwriter for a YouTube movie recap channel. Using the summary below, write a [10–15] minute recap script. Open with a powerful hook, tell the story in present tense, keep only the key moments, build suspense before each twist, and end with a question for the comments. Simple, dramatic, conversational English. No scene directions.<br><br>MOVIE: [TITLE]<br>SUMMARY: [PASTE YOUR BULLET POINTS]</code>
</div>
''')

# ---------------------------------------------------------------- M7 voice
slide("m7", 6, header(6, "Give your script a voice") + '''
<div class="row2 vo">
  <div class="tier">
    <div class="t-h free">FREE / LOW BUDGET</div>
    <h3>CapCut text-to-speech</h3>
    <p>Built into CapCut. Paste the script, pick a voice, done. Good for starting out.</p>
  </div>
  <div class="tier pro">
    <div class="t-h">BEST QUALITY</div>
    <h3>ElevenLabs</h3>
    <p>The most human-sounding AI voices. Free tier to test, paid plans as you grow.</p>
  </div>
</div>
<h3 class="sec">Voiceover checklist</h3>
<div class="chips">
  <span>Pick ONE voice and keep it, it becomes your brand</span>
  <span>Calm, storytelling pace</span>
  <span>Split long scripts into parts</span>
  <span>Listen back and fix mispronounced names</span>
  <span>Export as MP3 or WAV</span>
</div>
<div class="tip">&#127911; Choose based on your budget. Start free, upgrade when the channel starts paying.</div>
''')

# ---------------------------------------------------------------- M8 editing
STEPS = [
    ("Gather", "Voiceover, movie, images all ready"),
    ("Import", "Bring everything into the CapCut timeline"),
    ("Cut", "Trim the clips down to the key scenes"),
    ("Transform", "Mirror, zoom and crop the clips"),
    ("Effects", "Add effects, plus blur where needed"),
    ("Subtitles", "Auto captions, then check them"),
    ("Voiceover", "Drop in the VO and sync the clips"),
    ("Brand", "Channel logo in the corner"),
]
st = "".join(f'<div class="st"><b>{i + 1}</b><h4>{a}</h4><p>{b}</p></div>' for i, (a, b) in enumerate(STEPS))
slide("m8", 7, header(7, "The editing workflow in CapCut") + f'''
<div class="timeline">{st}</div>
<div class="track">
  <div class="tr"><label>VIDEO</label><div class="clips"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="tr"><label>TEXT</label><div class="clips sub"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="tr"><label>AUDIO</label><div class="clips aud"><i></i></div></div>
</div>
<div class="tip">&#127909; I'll show every step live. Get your files ready before you open CapCut.</div>
''')

slide("m8b", 7, header(7, "Avoiding copyright claims (this happens while you edit)") + '''
<div class="shield">
  <div class="sh-c">&#128737;&#65039;</div>
  <div class="sh-grid">
    <div class="sh"><b>Mirror / flip</b><p>Flip clips horizontally</p></div>
    <div class="sh"><b>Zoom &amp; crop</b><p>Zoom 110 to 130%, reframe the shot</p></div>
    <div class="sh"><b>Short clips</b><p>Don't play long scenes. Cut every few seconds.</p></div>
    <div class="sh"><b>Mute original audio</b><p>Your voiceover only, no movie soundtrack</p></div>
    <div class="sh"><b>Add effects</b><p>Filters, borders, speed tweaks, overlays</p></div>
    <div class="sh"><b>Blur</b><p>Blur logos, watermarks and nudity</p></div>
    <div class="sh"><b>Your commentary</b><p>Your own words and storytelling add value</p></div>
    <div class="sh"><b>Logo + subtitles</b><p>Make the video clearly yours</p></div>
  </div>
</div>
<div class="note">No method is 100% guaranteed. Some studios claim aggressively. Check the Copyright tab in YouTube Studio's upload checks before you publish.</div>
''')

# ---------------------------------------------------------------- M9 upload
slide("m9", 8, header(8, "Title + Thumbnail + Description") + '''
<div class="row3 up">
  <div class="card"><div class="ic">&#128221;</div><h4>Title</h4><p>Don't just use the movie's name. Write a <b>curiosity hook</b> that pulls viewers in.</p></div>
  <div class="card"><div class="ic">&#128444;</div><h4>Thumbnail</h4><p>Made in <b>Google Flow</b> from a prompt. Bold, clear and readable on a small phone screen.</p></div>
  <div class="card"><div class="ic">&#128196;</div><h4>Description</h4><p>A short summary, keywords, the movie name, a disclaimer and hashtags.</p></div>
</div>
<div class="titles">
  <div class="tt bad"><b>&#10008; BORING</b><span>"Inception (2010) Movie Recap"</span></div>
  <div class="tt good"><b>&#10004; CAPTIVATING</b><span>"He Steals Secrets From People's DREAMS, But One Dream Traps Him Forever"</span></div>
</div>
<div class="prompt sm">
  <div class="p-lbl">THUMBNAIL PROMPT STARTER (Google Flow)</div>
  <code>YouTube thumbnail, 16:9, cinematic, [MAIN CHARACTER] with a shocked expression in the foreground, [KEY SCENE] behind, high contrast, bold colors, dramatic lighting, sharp and readable at small size.</code>
</div>
''')

CHECK = [
    "Captivating title (not just the movie name)",
    "Thumbnail made and checked at phone size",
    "Description with summary, keywords and hashtags",
    "Tags added (movie name, actors, genre, 'movie recap')",
    "Logo and subtitles in the video",
    "Copyright check passed in YouTube Studio",
    "End screen and cards added",
    "Scheduled for your best posting time",
]
chk = "".join(f'<div class="cb" data-cb="up{i}"><span class="box"></span>{c}</div>' for i, c in enumerate(CHECK))
slide("m9b", 8, header(8, "Pre-upload checklist (tick the boxes, they're clickable)") + f'''
<div class="cbs">{chk}</div>
<div class="tip">&#9989; Run through this list before every upload. Skipping a step costs you views.</div>
''')

# ---------------------------------------------------------------- M10 tips
TIPS = [
    ("&#9889;", "Hook in 5 seconds", "Open with the craziest moment, not 'Hello guys'."),
    ("&#128197;", "Be consistent", "Post on a schedule, for example 3 to 4 videos a week."),
    ("&#128293;", "Ride the trends", "Recap new and trending movies while people are searching for them."),
    ("&#128257;", "Copy what works", "Study the best videos on top recap channels and make your version."),
    ("&#127941;", "Series and playlists", "Recap whole franchises so viewers binge-watch your channel."),
    ("&#128172;", "End with a question", "Comments boost the algorithm. Ask what they'd do."),
    ("&#127916;", "Post Shorts", "Cut 30 to 60 second teasers from each recap to bring in new viewers."),
    ("&#128202;", "Read analytics", "Watch CTR and retention. Improve thumbnails and hooks."),
]
tp = "".join(f'<div class="tp"><div class="tp-i">{i}</div><div><h4>{a}</h4><p>{b}</p></div></div>' for i, a, b in TIPS)
slide("m10", 9, header(9, "Get more views and grow faster") + f'<div class="tips">{tp}</div>')

# ---------------------------------------------------------------- CLOSE
plan = "".join(f'<div class="cb" data-cb="go{i}"><span class="box"></span>{c}</div>' for i, c in enumerate([
    "Create my channel, name and logo",
    "Pick my first 5 movies",
    "Write my master script prompt",
    "Choose my voice",
    "Edit and upload video #1 this week",
]))
slide("close", None, '''
<div class="hdr"><div class="mnum">YOUR ACTION PLAN</div><h2>Now it's your turn. Lights, camera, recap.</h2></div>
<div class="row2">
  <div><div class="cbs one">''' + plan + '''</div></div>
  <div class="notes"><div class="p-lbl">MY NOTES (type here)</div><div class="notebox" data-notes="1"></div></div>
</div>
<a class="jump" href="#roadmap">&#9776; Back to the roadmap</a>
''')


def render():
    from pathlib import Path
    css = (Path(__file__).parent / "style.css").read_text()
    pages = []
    for i, (sid, mod, body, cls) in enumerate(slides):
        n = nav(sid, mod).replace(f"__NEXT_{i}__", slides[min(i + 1, len(slides) - 1)][0])
        if i == len(slides) - 1:
            n = n.replace('<a class="nb" href="#close">Next &#9654;</a>', '<span class="nb off">Next &#9654;</span>')
        pages.append(f'<section class="slide {cls}" id="{sid}"><div class="body">{body}</div>{n}</section>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>Movie Recap Course</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{"".join(pages)}</body></html>'''
