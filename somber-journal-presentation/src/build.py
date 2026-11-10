"""Assemble the Somber Journal deck from src/ parts plus the shared engine.
Run: python3 -I src/build.py <engine-css> <engine-js>"""
import sys,re,os
here=os.path.dirname(os.path.abspath(__file__)); root=os.path.dirname(here)
base_css=open(sys.argv[1]).read(); engine=open(sys.argv[2]).read()
slides=open(os.path.join(here,'slides.html')).read()
css=open(os.path.join(here,'slides.css')).read()
hooks=open(os.path.join(here,'hooks.js')).read()
V=[('sj-v1.jpg','17:12','POV: What Your Family Stops Telling You at Every Level of Wealth from -$412 to $60…','3 days ago'),
   ('sj-v2.jpg','17:54','POV: What Getting Sick Costs You at Every Level of Wealth From $0 to $1 Billion','10 days ago'),
   ('sj-v3.jpg','15:23','POV: You are 40 and You Still Work for your Younger Brother','13 days ago'),
   ('sj-v4.jpg','16:52','POV: Divorced at 55, had $0, then At 56, $1.4M','2 weeks ago'),
   ('sj-v5.jpg','25:17','POV: You Still Live with Your Parents at 30','3 weeks ago')]
def rec(p):
    morph=' data-morph="hero"' if p=='intro' else ''
    cards=''.join(f'<div class="rv"><div class="rt"><img src="img/{i}" alt=""><span class="dur">{d}</span></div><div class="rti">{t}</div><div class="rme"><span class="rviews">0</span> views · {a}</div></div>' for i,d,t,a in V)
    return (f'<div class="rec"><div class="rbar"><div class="rsearch">Search</div></div>'
            f'<div class="rbanner"><img src="img/sj-banner.jpg" alt="Somber Journal banner: The money stories nobody tells you"></div>'
            f'<div class="ravatar"{morph}><div class="disc"><img src="img/sj-avatar.jpg" alt="Somber Journal avatar"></div></div>'
            f'<div class="rname">Somber Journal</div>'
            f'<div class="rstats"><b>@somberjournal</b> · <span class="rsubs">15</span> subscribers · 5 videos</div>'
            f'<div class="rdesc">POV: The Money Stories nobody tells you <b>...more</b></div>'
            f'<div class="rtabs"><span>Home</span><span class="on">Videos</span></div>'
            f'<div class="rgrid">{cards}</div></div>')
slides=slides.replace('%%REC:intro%%',rec('intro')).replace('%%REC:close%%',rec('close'))
slides=slides.replace('<section class="slide" data-name="Title" data-t="cube" data-enter="titles">','<section class="slide" data-name="Titles" data-t="cube" data-enter="titles">')
k=iter(range(100))
slides=re.sub(r'<b class="beat" style="left:([\d.]+)%">',lambda m:f'<b class="beat" style="left:{m.group(1)}%;--i:{next(k)}">',slides)
slides=slides.replace('views per video, before vs. after the angle','worst video before → best video after')
engine=engine.replace("const fn=enter[s.dataset.enter];if(fn&&closed)fn();","if(closed)runEnter(s);")
hooks="  function runEnter(s){const fn=enter[s.dataset.enter];if(fn)fn();countAll(s);}\n"+hooks
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Somber Journal Angle Plan</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Fraunces:ital,opsz,wght@1,9..144,500;1,9..144,700&family=Manrope:wght@400;500;600;700;800&family=Roboto:wght@400;500;700&display=swap">
<style>*,*::before,*::after{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}
'''
out=head+base_css+css+'</style>\n</head>\n<body>\n'+slides+'\n<script>'+engine+hooks+'</script>\n</body>\n</html>\n'
open(os.path.join(root,'index.html'),'w').write(out)
print('slides',slides.count('<section class="slide'),'bytes',len(out))
