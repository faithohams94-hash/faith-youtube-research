// The 20 ON SCREEN info cards for Episode 1, in the style of Beanie Survives' data cards:
// series header on top, a cream panel across the middle, the bottom kept clear for captions.
// Every animated element carries data-fx / data-in (seconds) and is driven by render(t).
const path = require("path");
const { bust, PEOPLE, ICONS } = require("./art");

const FONTS = path.join(__dirname, "fonts");

// ---------------------------------------------------------------- building blocks
const at = (fx, t, d) => `data-fx="${fx}" data-in="${t}"${d ? ` data-d="${d}"` : ""}`;
const person = (k, t, size = 1) =>
  `<div class="person" style="--s:${size}" ${at("up", t)}>${bust(PEOPLE[k])}<div class="tag">${PEOPLE[k].label}</div></div>`;
const people = (list) => `<div class="people">${list.map(([k, t, s]) => person(k, t, s)).join("")}</div>`;
const count = (to, t, d, opts = {}) =>
  `<span ${at("count", t, d)} data-to="${to}" data-from="${opts.from || 0}" data-pre="${opts.pre || ""}" data-suf="${opts.suf || ""}" data-dec="${opts.dec || 0}">${opts.pre || ""}0</span>`;
const icon = (svg, t, cls = "ic") => `<div class="${cls}" ${at("pop", t, 0.35)}>${svg}</div>`;
const clock = (time, t) => `<div class="clock" ${at("flicker", t)}>${time.replace(/ (AM|PM)/, '<span class="ampm"> $1</span>')}</div>`;

const CARDS = [
  { id: "c01-clock-947", key: "clock947", dur: 3.0, sub: "THE OWNER'S OFFICE · TUESDAY",
    body: people([["me_owner", 0.1]]) + `<div class="content center">${clock("9:47 AM", 0.25)}
      <div class="line" ${at("up", 1.0)}>13 MINUTES UNTIL THE MEETING</div></div>` },

  { id: "c02-lease-stamp", key: "leasestamp", dur: 3.6, sub: "THE THIRD-FLOOR TENANT",
    body: people([["me_owner", 0.1]]) + `<div class="content row">
      <div class="folder" ${at("up", 0.15)}><div class="ftab"></div><div class="fline w80"></div><div class="fline w60"></div><div class="fline w70"></div>
        <div class="stamp" ${at("stamp", 0.55, 0.22)}>LEASE RENEWAL<br>DEADLINE MISSED</div></div>
      <div class="stack"><div class="label" ${at("up", 1.2)}>PAST DUE</div>
        <div class="big red" ${at("fade", 1.3, 0.1)}>${count(40800, 1.3, 1.0, { pre: "$" })}</div>
        <div class="line" ${at("up", 1.7)}>3 months of unpaid rent</div></div></div>`, shake: 0.77 },

  { id: "c03-clock-952", key: "clock952", dur: 3.0, sub: "THEY'RE EARLY",
    body: people([["pm", 0.1]]) + `<div class="content center">${clock("9:52 AM", 0.25)}
      <div class="line" ${at("up", 1.0)}>THE DIRECTOR AND 2 STAFF ARE ON THEIR WAY UP</div></div>` },

  { id: "c04-year-1", key: "year1", dur: 4.0, sub: "FIVE YEARS EARLIER",
    body: people([["me_past", 0.1]]) + `<div class="content">
      <div class="year" ${at("pop", 0.3, 0.4)}>YEAR 1</div>
      <div class="nwrow" ${at("up", 0.8)}><span class="label">NET WORTH</span><span class="big">$0</span></div>
      <div class="bar" ${at("fade", 0.9)}><div class="fill green" ${at("fill", 1.0, 0.6)} data-to="1"></div><span class="bmax">$100K</span></div>
      <div class="line" ${at("up", 1.4)}>Operations analyst · $68,000 a year</div></div>` },

  { id: "c05-week-of-lunches", key: "weeklunch", dur: 5.5, sub: "SUNDAY MEAL PREP",
    body: people([["me_home", 0.1]]) + `<div class="content">
      <div class="ttl" ${at("up", 0.2)}>A WEEK OF LUNCHES</div>
      <div class="statrow"><div><div class="label" ${at("fade", 0.4)}>Cooked on Sunday</div>
        <div class="icons">${Array.from({ length: 10 }, (_, i) => icon(ICONS.container, 0.6 + i * 0.12)).join("")}</div></div>
        <div class="big" ${at("fade", 1.0, 0.1)}>${count(38, 1.0, 1.0, { pre: "$" })}</div></div>
      <div class="expl" ${at("up", 2.2)}>1 container = 1 meal = $3.80</div></div>` },

  { id: "c06-the-rules", key: "rules", dur: 7.0, sub: "TAPED INSIDE THE KITCHEN CABINET",
    body: people([["me_home", 0.1]]) + `<div class="content center"><div class="index" ${at("up", 0.15)}><div class="tape t1"></div><div class="tape t2"></div>
      <div class="rtitle"><span ${at("type", 0.4, 0.5)} data-text="THE RULES"></span></div>
      <div class="rule"><span ${at("type", 1.0, 0.8)} data-text="1. Lunch costs $4."></span></div>
      <div class="rule"><span ${at("type", 2.2, 1.0)} data-text="2. The car stays paid off."></span></div>
      <div class="rule"><span ${at("type", 3.5, 1.0)} data-text="3. Every raise gets invested."></span></div>
      <div class="rule r4"><span ${at("type", 4.9, 1.0)} data-text="4. Nobody needs to know."></span></div></div></div>` },

  { id: "c07-lunch-math", key: "math27", dur: 5.5, sub: "THE MATH NOBODY CHECKED",
    body: people([["marcus_past", 0.1]]) + `<div class="content">
      <div class="ttl" ${at("up", 0.2)}>LUNCH + COFFEE</div>
      <div class="statrow"><div class="icons big-ic">${icon(ICONS.salad, 0.5)}<div class="plus" ${at("pop", 0.7)}>+</div>${icon(ICONS.coffee, 0.8)}
        <div class="line inl" ${at("up", 1.1)}>$22 + $5 = <b>$27 a day</b></div></div>
        <div class="bigwrap" ${at("fade", 1.5, 0.1)}><span class="big">${count(6750, 1.5, 1.1, { pre: "$" })}</span><span class="per">/ YEAR</span></div></div>
      <div class="expl" ${at("up", 2.8)}>$27 × 250 work days · <b>$33,750</b> over five years</div></div>` },

  { id: "c08-marcus-stats", key: "marcuscard", dur: 6.0, sub: "MARCUS · SENIOR ACCOUNT DIRECTOR",
    body: people([["marcus_past", 0.1]]) + `<div class="content"><div class="panel redp" ${at("right", 0.2)}>
      <div class="phead"><span>MARCUS</span><span>SALARY <b>$115,000</b></span></div>
      <div class="prow" ${at("right", 0.6)}>${ICONS.highrise}<span>Luxury apartment</span><b>$3,200/mo</b></div>
      <div class="prow" ${at("right", 0.9)}>${ICONS.car("#1d1d1d")}<span>BMW + insurance + parking</span><b>$1,080/mo</b></div>
      <div class="prow" ${at("right", 1.2)}>${ICONS.cocktail}<span>Friday-night rounds</span><b>$800/mo</b></div>
      <div class="pfoot" ${at("up", 1.7)}><span>NET WORTH</span><b class="red">▼ ${count(-14000, 1.8, 1.2, { pre: "$" })}</b></div></div></div>` },

  { id: "c09-my-stats", key: "mecard", dur: 6.0, sub: "ME · OPERATIONS ANALYST",
    body: people([["me_past", 0.1]]) + `<div class="content"><div class="panel greenp" ${at("left", 0.2)}>
      <div class="phead"><span>ME</span><span>SALARY <b>$68,000</b></span></div>
      <div class="prow" ${at("left", 0.6)}>${ICONS.studio}<span>Studio, 25 minutes out</span><b>$1,100/mo</b></div>
      <div class="prow" ${at("left", 0.9)}>${ICONS.car("#b9c0c7")}<span>11-year-old Corolla</span><b>PAID OFF</b></div>
      <div class="prow" ${at("left", 1.2)}>${ICONS.container}<span>Homemade lunch</span><b>$3.80/day</b></div>
      <div class="pfoot" ${at("up", 1.7)}><span>INVESTING</span><b class="green">▲ ${count(1900, 1.8, 1.0, { pre: "$" })}<small> / MONTH</small></b></div></div></div>` },

  { id: "c10-year-2", key: "year2", dur: 4.0, sub: "THE HOLIDAY PARTY",
    body: people([["marcus_santa", 0.1], ["me_past", 0.25]]) + `<div class="content">
      <div class="year" ${at("pop", 0.4, 0.4)}>YEAR 2</div>
      <div class="statrow left">${icon(ICONS.lunchbox, 1.0, "ic xl")}<div class="line" ${at("up", 1.3)}>Secret Santa gift:<br><b>a $12 lunchbox</b></div></div></div>` },

  { id: "c11-net-worth-62k", key: "nw62", dur: 5.5, sub: "DECEMBER · YEAR 2",
    body: people([["marcus_broke", 0.1], ["me_past", 0.25]]) + `<div class="content">
      <div class="vrow" ${at("up", 0.5)}><span class="who">MARCUS</span><div class="stamp small" ${at("stamp", 0.9, 0.22)}>PAYROLL ADVANCE REQUESTED</div></div>
      <div class="vrow" ${at("up", 1.5)}><span class="who">ME</span><div class="bar"><div class="fill green" ${at("fill", 1.7, 1.1)} data-to="62"></div><span class="bmax">$100K</span></div>
        <span class="big sm green">${count(62000, 1.7, 1.1, { pre: "$" })}</span></div>
      <div class="expl" ${at("up", 3.0)}>Same month. Same office. Different math.</div></div>`, shake: 1.12 },

  { id: "c12-year-3", key: "year3", dur: 4.5, sub: "MARCUS IS NOW MY MANAGER",
    body: people([["marcus_past", 0.1], ["me_past", 0.25]]) + `<div class="content">
      <div class="year" ${at("pop", 0.4, 0.4)}>YEAR 3</div>
      <div class="nwrow" ${at("up", 0.9)}><span class="label">MY RAISE</span><span class="big red">${count(2, 1.0, 0.6, { suf: "%" })}</span></div>
      <div class="statrow left">${icon(ICONS.watch, 1.6, "ic lg")}<div class="quote" ${at("up", 1.8)}>“Invest in your image. Get a real watch.”</div></div></div>` },

  { id: "c13-net-worth-94k", key: "nw94", dur: 5.0, sub: "THE CHURCH BASEMENT MEETUP",
    body: people([["me_past", 0.1], ["arthur", 0.25]]) + `<div class="content">
      <div class="year sm" ${at("pop", 0.4, 0.4)}>YEAR 3</div>
      <div class="nwrow" ${at("up", 0.8)}><span class="label">NET WORTH</span><span class="big green">${count(94000, 0.9, 1.1, { pre: "$" })}</span></div>
      <div class="bar" ${at("fade", 0.8)}><div class="fill green" ${at("fill", 0.9, 1.1)} data-to="94"></div><span class="bmax">$100K</span></div>
      <div class="line" ${at("up", 2.2)}>Enough to sit at Arthur's table</div></div>` },

  { id: "c14-refinance", key: "refi", dur: 6.0, sub: "THE EAST SIDE BUILDING",
    body: people([["me_past", 0.1], ["arthur", 0.25]]) + `<div class="content">
      <div class="ttl" ${at("up", 0.3)}>8 UNITS · ALL RENTED</div>
      <div class="statrow"><div class="icons units">${Array.from({ length: 8 }, (_, i) => `<div class="unitwrap" ${at("pop", 0.5 + i * 0.08, 0.3)}>${ICONS.unit(false)}<div class="lit" ${at("fade", 1.3 + i * 0.18, 0.2)}>${ICONS.unit(true)}</div></div>`).join("")}</div>
        <div class="bigwrap" ${at("fade", 2.8, 0.1)}><span class="big green">${count(2200, 2.8, 1.0, { pre: "$" })}</span><span class="per">/ MONTH</span></div></div>
      <div class="expl" ${at("up", 3.6)}>Refinance: <b>$75,000</b> back to me · I still own <b>30%</b></div></div>` },

  { id: "c15-year-5", key: "year5", dur: 4.5, sub: "TWO YEARS LATER",
    body: people([["me_owner", 0.1], ["arthur", 0.25]]) + `<div class="content">
      <div class="year" ${at("pop", 0.4, 0.4)}>YEAR 5</div>
      <div class="blds">${[["Medical offices", "#7fa7c9", 1.0], ["Accounting firm", "#c9a76a", 1.2], ["Logistics suites", "#b5654a", 1.4]].map(([n, c, t]) => `<div class="bld" ${at("pop", t, 0.35)}>${ICONS.building(c)}<span>${n}</span></div>`).join("")}</div>
      <div class="line" ${at("up", 2.0)}>Every unit rented</div></div>` },

  { id: "c16-the-building", key: "building", dur: 5.5, sub: "THE OFF-MARKET DEAL",
    body: people([["me_owner", 0.1]]) + `<div class="content row">
      <div class="tower" ${at("up", 0.2)}>${[4, 3, 2, 1].map((f) => `<div class="floor${f === 3 ? " f3" : ""}"><span>FLOOR ${f}</span>${f === 3 ? `<em ${at("pop", 1.8, 0.3)}>MY OLD EMPLOYER</em>` : ""}</div>`).join("")}<div class="door"></div></div>
      <div class="stack"><div class="label" ${at("up", 0.7)}>4-STORY OFFICE BUILDING</div>
        <div class="big" ${at("fade", 0.8, 0.1)}>${count(2400000, 0.8, 1.2, { pre: "$" })}</div>
        <div class="line" ${at("up", 2.4)}>20% down · floor 3 lease ends in 4 months</div></div></div>` },

  { id: "c17-clock-1000", key: "clock1000", dur: 3.0, sub: "THEY'RE HERE",
    body: people([["marcus_now", 0.1], ["dana_now", 0.2, 0.85], ["staffer", 0.3, 0.85]]) + `<div class="content center">${clock("10:00 AM", 0.25)}
      <div class="line" ${at("up", 1.0)}>THE MEETING STARTS NOW</div></div>` },

  { id: "c18-the-choice", key: "choice", dur: 6.5, sub: "THE DECISION",
    body: people([["marcus_now", 0.1, 0.85], ["me_owner", 0.2, 0.85], ["dana_now", 0.3, 0.85]]) + `<div class="content center">
      <div class="pill white" ${at("pulse", 0.8, 0.4)} data-glow="4.6">EXTEND THE LEASE<span class="check">✓</span></div>
      <div class="or" ${at("fade", 1.1)}>or</div>
      <div class="pill red" ${at("pulse", 1.3, 0.4)} data-dim="4.6">LET THEM GO</div></div>` },

  { id: "c19-rule-4", key: "rule4", dur: 4.0, sub: "BEHIND MY LICENSE",
    body: people([["me_owner", 0.1]]) + `<div class="content center"><div class="index worn" ${at("up", 0.15)}><div class="crease"></div><div class="crease v"></div>
      <div class="rule r4 big4"><span ${at("type", 0.5, 1.4)} data-text="4. Nobody needs to know."></span></div></div>
      <div class="line" ${at("fade", 2.4)}>For five years, nobody did.</div></div>` },

  { id: "c20-episode-2", key: "ep2", dur: 5.0, sub: "NEXT TIME ON SOMBER JOURNAL", dark: true,
    body: people([["arthur_worried", 0.1]]) + `<div class="content row">
      <div class="phone" ${at("buzz", 0.4)}><div class="pscreen"><div class="pname">ARTHUR</div><div class="ptime">2:14 AM</div><div class="pinc">incoming call…</div>
        <div class="pbtns"><span class="pb r"></span><span class="pb g"></span></div></div></div>
      <div class="stack"><div class="ep2" ${at("pop", 1.4, 0.45)}>EPISODE 2</div><div class="soon" ${at("fade", 1.9)}>COMING SOON</div>
        <div class="line light" ${at("up", 2.4)}>The east side building is on fire.</div></div></div>` },
];

// ---------------------------------------------------------------- page
const CSS = `
@font-face{font-family:Anton;src:url('file://${FONTS}/anton-latin-400-normal.woff2')}
@font-face{font-family:Bebas;src:url('file://${FONTS}/bebas-neue-latin-400-normal.woff2')}
@font-face{font-family:Inter;font-weight:400;src:url('file://${FONTS}/inter-latin-400-normal.woff2')}
@font-face{font-family:Inter;font-weight:600;src:url('file://${FONTS}/inter-latin-600-normal.woff2')}
@font-face{font-family:Inter;font-weight:800;src:url('file://${FONTS}/inter-latin-800-normal.woff2')}
@font-face{font-family:Marker;src:url('file://${FONTS}/permanent-marker-latin-400-normal.woff2')}
@font-face{font-family:Mono;src:url('file://${FONTS}/share-tech-mono-latin-400-normal.woff2')}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;overflow:hidden}
body{background:radial-gradient(ellipse at 50% 40%,#22352b 0%,#0B1410 70%);font-family:Inter,sans-serif;color:#1b1f1d;position:relative}
.blob{position:absolute;border-radius:50%;filter:blur(70px);opacity:.55}
.hdr{position:absolute;top:70px;left:0;right:0;text-align:center}
.ep{font-family:Anton;font-size:104px;color:#fff;letter-spacing:3px;line-height:1;text-shadow:0 6px 24px rgba(0,0,0,.45)}
.sub{font-family:Bebas;font-size:56px;color:#E3B341;letter-spacing:4px;margin-top:10px}
.band{position:absolute;top:330px;left:0;right:0;height:560px;background:#F4EFE3;display:flex;align-items:center;padding:0 90px;gap:60px;box-shadow:0 20px 60px rgba(0,0,0,.45)}
.band.dark{background:radial-gradient(ellipse at 30% 60%,#5a2a10 0%,#1a1410 55%,#0e0c0b 100%);color:#fff}
.people{display:flex;align-items:flex-end;gap:10px;flex:0 0 auto;height:100%;padding-top:40px}
.person{width:calc(270px*var(--s));display:flex;flex-direction:column;align-items:center}
.person svg{width:100%;height:auto;display:block}
.tag{font-family:Bebas;font-size:34px;letter-spacing:2px;background:#0B1410;color:#E3B341;padding:4px 16px 0;border-radius:8px;margin:-6px 0 30px;white-space:nowrap}
.content{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;min-width:0}
.content.center{align-items:center;text-align:center}
.content.row{flex-direction:row;align-items:center;gap:60px}
.stack{display:flex;flex-direction:column;gap:14px}
.clock{font-family:Mono;font-size:230px;line-height:.9;color:#0B1410;letter-spacing:4px}
.clock .ampm{font-size:110px}
.line{font-family:Inter;font-weight:800;font-size:44px;color:#2c3a33;letter-spacing:.5px}
.line.inl{font-size:40px;margin-left:16px}.line.light{color:#f2e6d6;font-weight:600}
.label{font-family:Inter;font-weight:600;font-size:36px;color:#6b726e;letter-spacing:1px}
.ttl{font-family:Inter;font-weight:800;font-size:64px;color:#151a17;letter-spacing:1px}
.big{font-family:Anton;font-size:150px;line-height:1;color:#151a17}
.big.sm{font-size:96px}.big.red,.red{color:#d63b3f}.big.green,.green{color:#1f9d55}
.bigwrap{display:flex;align-items:baseline;gap:14px;white-space:nowrap;flex:0 0 auto}.per{font-family:Anton;font-size:56px;color:#6b726e}
.expl{font-family:Inter;font-weight:600;font-size:38px;color:#555c58}
.statrow{display:flex;align-items:center;justify-content:space-between;gap:40px}.statrow.left{justify-content:flex-start}
.icons{display:flex;gap:10px;align-items:center;margin-top:10px}
.ic{width:74px;height:74px}.ic svg,.big-ic .ic svg{width:100%;height:100%}
.big-ic .ic{width:120px;height:120px}.ic.lg{width:130px;height:130px}.ic.xl{width:190px;height:190px}
.plus{font-family:Anton;font-size:90px;color:#151a17}
.year{font-family:Anton;font-size:170px;line-height:1;color:#0B1410;letter-spacing:4px}.year.sm{font-size:120px}
.nwrow{display:flex;align-items:baseline;gap:30px}
.bar{position:relative;height:56px;flex:0 0 56px;width:100%;background:#ddd5c4;border-radius:28px;border:5px solid #151a17;overflow:hidden}.vrow .bar{flex:1 1 auto;width:auto;min-width:420px}
.fill{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:22px}.fill.green{background:#2fbf71}
.bmax{position:absolute;right:20px;top:4px;font-family:Bebas;font-size:40px;color:#6b726e}
.vrow{display:flex;align-items:center;gap:30px}.who{font-family:Bebas;font-size:56px;letter-spacing:2px;width:170px;color:#151a17}
.folder{position:relative;width:520px;height:360px;background:#e8c98f;border:6px solid #151a17;border-radius:10px;padding:70px 40px}
.ftab{position:absolute;top:-34px;left:30px;width:170px;height:40px;background:#d63b3f;border:6px solid #151a17;border-bottom:none;border-radius:10px 10px 0 0}
.fline{height:14px;background:#c5a46a;border-radius:7px;margin-bottom:26px}.w80{width:80%}.w60{width:60%}.w70{width:70%}
.stamp{position:absolute;left:40px;top:110px;border:10px solid #d63b3f;color:#d63b3f;font-family:Anton;font-size:58px;line-height:1.05;padding:14px 26px;text-align:center;background:rgba(244,239,227,.6);letter-spacing:2px}
.stamp.small{position:static;font-size:50px;border-width:8px;padding:8px 22px}
.index{position:relative;width:900px;background:#fff;border-radius:6px;padding:40px 60px 34px 110px;box-shadow:0 12px 30px rgba(0,0,0,.25);transform:rotate(-2deg);
  background-image:repeating-linear-gradient(#fff 0 66px,#a9c7e8 66px 69px);text-align:left}
.index:before{content:"";position:absolute;left:80px;top:0;bottom:0;width:4px;background:#e58a8a}
.tape{position:absolute;width:150px;height:46px;background:rgba(240,226,170,.85);top:-20px}.t1{left:40px;transform:rotate(-8deg)}.t2{right:40px;transform:rotate(7deg)}
.rtitle{font-family:Marker;font-size:66px;color:#151a17;height:76px}
.rule{font-family:Marker;font-size:52px;color:#1f2b55;height:69px;line-height:69px}.rule.r4{color:#b3262b}
.index.worn{background-color:#f3ead5;background-image:none;width:1000px;padding:70px 60px;transform:rotate(-1deg)}
.index.worn:before{display:none}.crease{position:absolute;left:0;right:0;top:50%;height:2px;background:rgba(0,0,0,.12)}.crease.v{top:0;bottom:0;left:50%;width:2px;height:auto}
.big4{font-size:76px;height:auto;line-height:1.2;text-align:center}
.panel{border:7px solid;border-radius:20px;padding:22px 34px;background:#fff;display:flex;flex-direction:column;gap:6px}
.redp{border-color:#d63b3f}.greenp{border-color:#1f9d55}
.phead{display:flex;justify-content:space-between;font-family:Bebas;font-size:54px;letter-spacing:2px;border-bottom:3px solid #e2dccf;padding-bottom:4px}
.prow{display:flex;align-items:center;gap:22px;font-size:38px;font-weight:600;padding:4px 0}.prow svg{width:62px;height:62px;flex:0 0 62px}.prow span{flex:1}.prow b{font-weight:800}
.pfoot{display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid #e2dccf;padding-top:8px;font-family:Bebas;font-size:54px;letter-spacing:2px}
.pfoot b{font-family:Anton;font-size:78px;letter-spacing:1px}.pfoot small{font-family:Bebas;font-size:40px;color:#6b726e}
.quote{font-family:Inter;font-style:italic;font-weight:600;font-size:46px;color:#2c3a33}
.units{gap:10px}.unitwrap{position:relative;width:64px;height:64px}.unitwrap svg{width:100%;height:100%}.lit{position:absolute;inset:0}
.blds{display:flex;gap:50px}.bld{display:flex;flex-direction:column;align-items:center;gap:8px;font-weight:800;font-size:34px}.bld svg{width:170px;height:170px}
.tower{position:relative;width:520px;border:7px solid #151a17;background:#b5654a;padding:16px;display:flex;flex-direction:column;gap:12px;border-radius:6px 6px 0 0}
.floor{position:relative;height:80px;background:#e9d9b6;border:5px solid #151a17;display:flex;align-items:center;padding-left:18px;font-family:Bebas;font-size:40px;letter-spacing:2px}
.floor.f3{background:#ffd3d3;border-color:#d63b3f}.floor em{position:absolute;right:10px;font-style:normal;background:#d63b3f;color:#fff;padding:4px 14px;border-radius:8px;font-size:34px;white-space:nowrap}
.door{height:30px;width:80px;background:#151a17;margin:0 auto}
.pill{white-space:nowrap;font-family:Anton;font-size:72px;letter-spacing:3px;padding:14px 70px;border-radius:80px;border:7px solid #151a17;position:relative;transition:none}
.pill.white{background:#fff;color:#151a17}.pill.red{background:#d63b3f;color:#fff}
.pill.white.glow{background:#E3B341;box-shadow:0 0 0 10px rgba(227,179,65,.35),0 0 60px rgba(227,179,65,.9)}
.pill .check{display:none;margin-left:24px}.pill.glow .check{display:inline}
.pill.dimmed{opacity:.35 !important}
.or{font-family:Bebas;font-size:60px;color:#6b726e;margin:8px 0}
.phone{width:300px;height:520px;background:#111;border-radius:44px;border:8px solid #333;padding:22px;box-shadow:0 0 80px rgba(255,140,40,.55)}
.pscreen{height:100%;border-radius:26px;background:linear-gradient(#2a1a10,#5a2a10);display:flex;flex-direction:column;align-items:center;padding-top:70px;color:#fff;gap:10px}
.pname{font-family:Bebas;font-size:64px;letter-spacing:3px}.ptime{font-family:Mono;font-size:56px;color:#ffb347}.pinc{font-size:26px;color:#e8cdb5}
.pbtns{margin-top:auto;margin-bottom:40px;display:flex;gap:70px}.pb{width:70px;height:70px;border-radius:50%}.pb.r{background:#d63b3f}.pb.g{background:#2fbf71}
.ep2{font-family:Anton;font-size:190px;line-height:1;color:#E3B341;letter-spacing:5px}.soon{font-family:Bebas;font-size:80px;letter-spacing:8px;color:#fff}
.band.dark .tag{background:#E3B341;color:#0B1410}
`;

const ENGINE = `
function ease(p){return 1-Math.pow(1-p,3)}
function back(p){const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)}
function money(v,dec){const s=v<0?'−':'';v=Math.abs(v);return s+v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec})}
window.render=function(t){
  document.querySelectorAll('[data-fx]').forEach(el=>{
    const fx=el.dataset.fx,tin=+el.dataset.in||0,d=+(el.dataset.d||0.45);
    const p=Math.min(1,Math.max(0,(t-tin)/d));let tr='',op=1;
    switch(fx){
      case 'fade':op=p;break;
      case 'up':op=p;tr='translateY('+((1-ease(p))*50)+'px)';break;
      case 'left':op=p;tr='translateX('+(-(1-ease(p))*160)+'px)';break;
      case 'right':op=p;tr='translateX('+((1-ease(p))*160)+'px)';break;
      case 'pop':op=Math.min(1,p*3);tr='scale('+(0.4+0.6*back(p))+')';break;
      case 'stamp':op=t<tin?0:1;tr='scale('+(2.3-1.3*ease(p))+') rotate(-7deg)';break;
      case 'flicker':{const k=Math.floor((t-tin)*30);op=t<tin?0:(k<8?[1,0,1,1,0,1,0,1][k]:1);break}
      case 'type':{const f=el.dataset.text;el.textContent=f.slice(0,Math.round(f.length*p));op=t<tin?0:1;break}
      case 'count':{const to=+el.dataset.to,fr=+el.dataset.from;const v=fr+(to-fr)*ease(p);el.textContent=(v<0?'−':'')+el.dataset.pre+money(Math.abs(v),+el.dataset.dec)+el.dataset.suf;break}
      case 'fill':el.style.width=(+el.dataset.to*ease(p))+'%';break;
      case 'pulse':{op=Math.min(1,p*2);const s=t>tin+d?1+0.045*Math.sin((t-tin-d)*2*Math.PI/0.9):0.4+0.6*back(p);tr='scale('+s+')';break}
      case 'buzz':{op=Math.min(1,p*2);const k=t-tin;tr=k>0?'translateX('+(Math.sin(k*70)*7*((Math.floor(k*1.6))%2===0?1:0))+'px) rotate('+(Math.sin(k*70)*1.5*((Math.floor(k*1.6))%2===0?1:0))+'deg)':'';break}
    }
    if(fx!=='fill'&&fx!=='count'){el.style.opacity=op;el.style.transform=tr}
  });
  const sh=document.body.dataset.shake;const band=document.querySelector('.band');
  if(sh){const dt=t-sh;band.style.transform=(dt>0&&dt<0.3)?'translate('+(Math.sin(dt*110)*10*(1-dt/0.3))+'px,'+(Math.cos(dt*90)*7*(1-dt/0.3))+'px)':''}
  document.querySelectorAll('[data-glow]').forEach(el=>el.classList.toggle('glow',t>=+el.dataset.glow));
  document.querySelectorAll('[data-dim]').forEach(el=>el.classList.toggle('dimmed',t>=+el.dataset.dim));
};`;

function page(c) {
  const blobs = c.dark
    ? `<div class="blob" style="left:-100px;top:-120px;width:700px;height:500px;background:#ff7a1a"></div><div class="blob" style="right:-120px;bottom:-140px;width:800px;height:500px;background:#8a2a10"></div>`
    : `<div class="blob" style="left:-120px;top:-140px;width:760px;height:520px;background:#3d6b4f"></div><div class="blob" style="right:-140px;top:-80px;width:700px;height:480px;background:#7a5a22"></div>
       <div class="blob" style="left:30%;bottom:-260px;width:900px;height:420px;background:#2c4a5a"></div>`;
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head>
  <body${c.shake ? ` data-shake="${c.shake}"` : ""}>${blobs}
  <div class="hdr"><div class="ep" ${at("fade", 0, 0.3)}>EPISODE 1</div><div class="sub" ${at("up", 0.05, 0.4)}>${c.sub}</div></div>
  <div class="band${c.dark ? " dark" : ""}">${c.body}</div>
  <script>${ENGINE}</script></body></html>`;
}

module.exports = { CARDS, page };
