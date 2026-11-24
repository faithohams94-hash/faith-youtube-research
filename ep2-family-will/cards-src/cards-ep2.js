// Episode 2 ON SCREEN cards. Uses the shared card engine and character art from Episode 1:
//   ../../ep1-leftovers-building/cards-src/  (art.js, cards.js, render.js)
// Render: CARDS_MODULE=$PWD/cards-ep2.js node ../../ep1-leftovers-building/cards-src/render.js ../cards 30
const path = require("path");
const ENGINE = path.join(__dirname, "../../ep1-leftovers-building/cards-src/cards.js");
const E = require(ENGINE);
const { at, people, count, icon, clock } = E;

const EP = "EPISODE 2";
const MAX_NW = 2000000; // every net-worth bar is drawn on the same $2M scale, so the climb is visible card to card

// ---------------------------------------------------------------- small building blocks
const heart = `<svg viewBox="0 0 24 24" width="40" height="40" style="vertical-align:-6px"><path d="M12 21s-7-4.5-9.5-9C.8 8.6 3 5 6.5 5c2 0 3.6 1.1 5.5 3 1.9-1.9 3.5-3 5.5-3C21 5 23.2 8.6 21.5 12 19 16.5 12 21 12 21z" fill="#e5484d" stroke="#151a17" stroke-width="1.5"/></svg>`;
const money = (n) => "$" + n.toLocaleString("en-US");

function yearCard(id, key, year, age, nw, chars, sub, line) {
  return { id, key, dur: 4.5, sub,
    body: people(chars) + `<div class="content">
      <div class="yrrow"><div class="year" ${at("pop", 0.3, 0.4)}>YEAR ${year}</div><div class="age" ${at("up", 0.6)}>AGE ${age}</div></div>
      <div class="nwrow" ${at("up", 0.8)}><span class="label">NET WORTH</span><span class="big green">${count(nw, 0.9, 1.2, { pre: "$" })}</span></div>
      <div class="bar" ${at("fade", 0.8)}><div class="fill green" ${at("fill", 0.9, 1.2)} data-to="${Math.max(0.6, (nw / MAX_NW) * 100).toFixed(1)}"></div><span class="bmax">$2M</span></div>
      ${line ? `<div class="line" ${at("up", 2.0)}>${line}</div>` : ""}</div>` };
}
function clockCard(id, key, day, time, chars, sub, line) {
  return { id, key, dur: 3.2, sub,
    body: people(chars) + `<div class="content center"><div class="day" ${at("fade", 0.15)}>${day}</div>${clock(time, 0.3)}
      ${line ? `<div class="line" ${at("up", 1.1)}>${line}</div>` : ""}</div>` };
}
function choiceCard(id, key, a, b, pick, chars, sub) {
  return { id, key, dur: 6.0, sub,
    body: people(chars) + `<div class="content center">
      <div class="pill white" ${at("pulse", 0.8, 0.4)} ${pick === "a" ? 'data-glow="4.2"' : 'data-dim="4.2"'}>${a}<span class="check">✓</span></div>
      <div class="or" ${at("fade", 1.1)}>or</div>
      <div class="pill red" ${at("pulse", 1.3, 0.4)} ${pick === "b" ? 'data-glow="4.2"' : 'data-dim="4.2"'}>${b}<span class="check">✓</span></div></div>` };
}
const phone = (inner, t = 0.2, fx = "up") => `<div class="ph" ${at(fx, t)}><div class="phs">${inner}</div></div>`;

// ---------------------------------------------------------------- the 41 cards, in script order
const CARDS = [
  clockCard("e01-tuesday-604", "TUESDAY · 6:04 PM", "TUESDAY", "6:04 PM", [["me_now", 0.1]], "THE PHONE THAT NEVER RINGS", "Your phone hasn't rung on a Tuesday in 8 years"),

  { id: "e02-seven-missed-calls", key: "7 MISSED CALLS · DANNY", dur: 4.5, sub: "IT WON'T STOP",
    body: people([["danny", 0.1]]) + `<div class="content row">${phone(`<div class="pt">Missed calls</div>
      ${[0, 1, 2, 3].map((i) => `<div class="mc" ${at("left", 0.5 + i * 0.25)}><span class="mcn">Danny</span><span class="mct">6:0${4 - i} PM</span></div>`).join("")}`, 0.15, "buzz")}
      <div class="stack"><div class="big red">${count(7, 0.5, 1.4)}</div><div class="line">MISSED CALLS FROM DANNY</div>
      <div class="expl" ${at("up", 2.0)}>He hasn't called since you were 29.</div></div></div>` },

  { id: "e03-birthday-text", key: '"hbd hope ur good"', dur: 4.2, sub: "EVERY BIRTHDAY · ONE LINE",
    body: people([["me_sad", 0.1]]) + `<div class="content row">${phone(`<div class="pt">Danny</div><div class="ts">March · 11:52 PM</div>
      <div class="bub" ${at("pop", 0.7, 0.35)}><span ${at("type", 0.9, 0.8)} data-text="hbd hope ur good"></span></div>`)}
      <div class="stack"><div class="line" ${at("up", 1.8)}>Sent 8 minutes before your birthday ended.</div></div></div>` },

  { id: "e04-mom-added-you", key: 'Mom added you to "THE FAMILY ❤️"', dur: 4.5, sub: "AFTER EIGHT YEARS",
    body: people([["mom", 0.1]]) + `<div class="content center">
      <div class="notif" ${at("up", 0.3)}><div class="nic">💬</div><div><div class="nt">THE FAMILY ${heart}</div><div class="nm">Mom added you to the group</div></div><div class="nw">now</div></div>
      <div class="line" ${at("up", 1.6)}>8 years after they took you out</div></div>` },

  { id: "e05-total-assets", key: "TOTAL ASSETS · $1,840,000", dur: 5.0, sub: "THE WRONG EMAIL · 9:12 AM",
    body: people([["danny_shock", 0.1]]) + `<div class="content row"><div class="doc" ${at("up", 0.15)}><div class="dh">TRUST · SCHEDULE OF ASSETS · PAGE 2</div>
      <div class="dl"><span>Index funds</span><span>$1,120,000</span></div><div class="dl"><span>Treasury bills</span><span>$160,000</span></div>
      <div class="dl"><span>Real estate equity</span><span>$560,000</span></div>
      <div class="dt" ${at("pop", 1.0, 0.4)}><span>TOTAL ASSETS</span><span class="green">${count(1840000, 1.1, 1.4, { pre: "$" })}</span></div></div>
      <div class="stack"><div class="label" ${at("up", 2.6)}>CC: danny@…</div><div class="expl" ${at("up", 2.9)}>One wrong address. One click.</div></div></div>` },

  choiceCard("e06-let-it-ring", "ANSWER · or · LET IT RING", "ANSWER", "LET IT RING", "b", [["me_now", 0.1], ["danny", 0.2, 0.85]], "CALL NUMBER EIGHT"),

  yearCard("e07-year-1", "YEAR 1 · AGE 22 · NET WORTH: $0", 1, 22, 0, [["me_past", 0.1]], "THE RESPONSIBLE ONE", "Supply chain coordinator · $58,000 a year"),

  { id: "e08-the-rule", key: '"Never spend money before it clears. Always keep a wall between you and desperation."', dur: 6.0, sub: "BEHIND THE PAY STUB IN YOUR WALLET",
    body: people([["me_past", 0.1]]) + `<div class="content center"><div class="stub" ${at("up", 0.15)}><div class="sh">PAY STUB · BACK</div>
      <div class="hand"><span ${at("type", 0.5, 1.6)} data-text="Never spend money before it clears."></span></div>
      <div class="hand red"><span ${at("type", 2.3, 1.8)} data-text="Always keep a wall between you and desperation."></span></div></div></div>` },

  { id: "e09-first-budget", key: "SALARY $58,000 · RENT $920 · CAR PAID IN CASH · SAVING $900 A MONTH", dur: 5.5, sub: "THE ONE-BEDROOM ABOVE THE DRY CLEANER",
    body: people([["me_past", 0.1]]) + `<div class="content"><div class="panel greenp" ${at("left", 0.2)}>
      <div class="phead"><span>YOU · AGE 22</span><span>SALARY <b>$58,000</b></span></div>
      <div class="prow" ${at("left", 0.6)}>${E.ICONS.studio}<span>Rent, above a dry cleaner</span><b>$920/mo</b></div>
      <div class="prow" ${at("left", 0.9)}>${E.ICONS.car("#8a96a3")}<span>Used hatchback</span><b>PAID IN CASH</b></div>
      <div class="pfoot" ${at("up", 1.4)}><span>SAVING</span><b class="green">${count(900, 1.5, 1.0, { pre: "$" })}<small> / MONTH</small></b></div></div></div>` },

  yearCard("e10-year-2", "YEAR 2 · AGE 23 · NET WORTH: $11,400", 2, 23, 11400, [["me_past", 0.1], ["danny_worried", 0.25]], "THE FIRST CALL", "Danny: \"We'll pay you back next month.\""),

  { id: "e11-the-family-tab", key: "THE FAMILY TAB", dur: 4.5, sub: "THE FIRST THREE \"LOANS\"",
    body: people([["danny", 0.1, 0.85], ["mom", 0.2, 0.85]]) + `<div class="content"><div class="ledger" ${at("up", 0.15)}><div class="lh">THE FAMILY TAB</div>
      ${[["Danny · electric bill", 312, 0.6], ["Mom · water heater", 600, 1.0], ["Tasha · flight home", 420, 1.4]].map(([n, v, t]) => `<div class="lr" ${at("left", t)}><span>${n}</span><b>${money(v)}</b></div>`).join("")}
      <div class="lr dots" ${at("fade", 1.9)}><span>…</span><b></b></div></div></div>` },

  { id: "e12-the-full-tab", key: "ELECTRIC BILL $312 · WATER HEATER $600 · FLIGHT $420 · TRANSMISSION $1,100 · PROPERTY TAX $800 · WEDDING RING $2,000 · …", dur: 6.0, sub: "\"WE'LL PAY YOU BACK NEXT MONTH\"",
    body: people([["danny", 0.1, 0.85], ["mom", 0.2, 0.85], ["dad", 0.3, 0.85]]) + `<div class="content"><div class="ledger wide" ${at("up", 0.15)}><div class="lh">THE FAMILY TAB</div>
      <div class="lgrid">${[["Electric bill", 312], ["Water heater", 600], ["Flight home", 420], ["Transmission", 1100], ["Property tax", 800], ["Wedding ring", 2000]].map(([n, v], i) => `<div class="lr" ${at("pop", 0.5 + i * 0.35, 0.3)}><span>${n}</span><b>${money(v)}</b></div>`).join("")}</div>
      <div class="lr dots" ${at("fade", 2.8)}><span>… and more, every month</span><b></b></div></div></div>` },

  { id: "e13-lent-vs-paid", key: "LENT: $11,400 · PAID BACK: $0", dur: 4.5, sub: "BY AGE 28",
    body: people([["me_past", 0.1]]) + `<div class="content"><div class="vs2">
      <div class="vcol" ${at("up", 0.3)}><div class="label">YOU LENT</div><div class="big">${count(11400, 0.5, 1.2, { pre: "$" })}</div></div>
      <div class="vcol" ${at("up", 1.0)}><div class="label">PAID BACK</div><div class="big red">$0</div></div></div>
      <div class="expl" ${at("up", 2.0)}>Nobody ever asked how you were doing.</div></div>` },

  yearCard("e14-year-6", "YEAR 6 · AGE 27 · NET WORTH: $100,000", 6, 27, 100000, [["me_past", 0.1]], "A TUESDAY IN OCTOBER", "You cried in the parking lot. You told no one."),
  yearCard("e15-year-8", "YEAR 8 · AGE 29 · NET WORTH: $132,000", 8, 29, 132000, [["me_past", 0.1], ["danny", 0.25]], "ROSIE'S DINER · ROUTE 9", "A rainy Sunday in November"),

  { id: "e16-shine-squad", key: '"SHINE SQUAD MOBILE DETAILING · INVESTOR PRESENTATION"', dur: 5.0, sub: "DANNY'S PITCH DECK",
    body: people([["danny", 0.1]]) + `<div class="content row"><div class="deck" ${at("up", 0.15)}><div class="dk1">SHINE SQUAD</div><div class="dk2">MOBILE DETAILING</div>
      <div class="van" ${at("pop", 0.8, 0.4)}>🚐</div><div class="dk3">INVESTOR PRESENTATION</div></div>
      <div class="stack"><div class="label" ${at("up", 1.4)}>DANNY'S ASK</div><div class="big red">${count(15000, 1.5, 1.0, { pre: "$" })}</div>
      <div class="expl" ${at("up", 2.6)}>His own money in: <b>$0</b></div></div></div>` },

  { id: "e17-asked-vs-had", key: "WHAT DANNY ASKED FOR: $15,000 · WHAT YOU ACTUALLY HAD: $132,000", dur: 5.5, sub: "THE DINER",
    body: people([["danny", 0.1], ["me_past", 0.2]]) + `<div class="content"><div class="hbars">
      <div class="hb" ${at("up", 0.3)}><span class="hl">DANNY ASKED FOR</span><div class="hbar"><div class="fill red" ${at("fill", 0.5, 0.8)} data-to="11"></div></div><b>$15,000</b></div>
      <div class="hb" ${at("up", 1.2)}><span class="hl">YOU ACTUALLY HAD</span><div class="hbar"><div class="fill green" ${at("fill", 1.4, 1.2)} data-to="100"></div></div><b class="green">$132,000</b></div></div>
      <div class="expl" ${at("up", 2.8)}>You said: <b>"I'm tapped out."</b></div></div>` },

  { id: "e18-balance-that-night", key: "YOUR BALANCE THAT NIGHT: $132,000", dur: 5.0, sub: "\"IS IT GAMBLING, BABY?\"",
    body: people([["mom_sad", 0.1], ["me_past", 0.2]]) + `<div class="content row">${phone(`<div class="pt">Balance</div><div class="bal">${count(132000, 0.7, 1.2, { pre: "$" })}</div><div class="ts">Available</div>`)}
      <div class="stack"><div class="line" ${at("up", 1.6)}>One screenshot would have ended it.</div><div class="expl" ${at("up", 2.4)}>You said: "Things are tight right now, Mom."</div></div></div>` },

  { id: "e19-danny-removed-you", key: '"Danny removed you from THE FAMILY ❤️"', dur: 4.2, sub: "ONE NIGHT IN DECEMBER",
    body: people([["me_sad", 0.1]]) + `<div class="content center"><div class="chat" ${at("up", 0.2)}><div class="ch">THE FAMILY ${heart}</div>
      <div class="cb" ${at("fade", 0.5)}>Kayla: 📸 Christmas plans!!</div><div class="sys" ${at("pop", 1.2, 0.4)}>Danny removed you</div></div>
      <div class="expl" ${at("up", 2.2)}>No message. No argument.</div></div>` },

  yearCard("e20-year-9", "YEAR 9 · AGE 30 · NET WORTH: $168,000", 9, 30, 168000, [["me_home", 0.1]], "THE SILENT YEARS", "No calls. No emergencies. No leaks."),

  { id: "e21-salary-climb", key: "SALARY: $58,000 → $96,000 → $118,000", dur: 5.0, sub: "NIGHT CLASSES · PROMOTIONS",
    body: people([["me_past", 0.1]]) + `<div class="content"><div class="ttl" ${at("up", 0.2)}>YOUR SALARY</div><div class="steps">
      ${[[58000, 30, 0.5], [96000, 55, 1.0], [118000, 70, 1.5]].map(([v, h, t]) => `<div class="stp" ${at("up", t)}><div class="sb" style="height:${h * 3}px"></div><b>${money(v)}</b></div>`).join("")}</div>
      <div class="expl" ${at("up", 2.3)}>Every raise, you pretended you didn't get it.</div></div>` },

  { id: "e22-investing-4500", key: "INVESTING $4,500 A MONTH · EVERY MONTH · NO EXCEPTIONS", dur: 5.5, sub: "AUTOMATIC · EVERY TWO WEEKS",
    body: people([["me_home", 0.1]]) + `<div class="content"><div class="nwrow" ${at("up", 0.2)}><span class="label">INVESTING</span><span class="big green">$4,500</span><span class="per">/ MONTH</span></div>
      <div class="cal">${"JFMAMJJASOND".split("").map((m, i) => `<div class="cm" ${at("pop", 0.7 + i * 0.12, 0.25)}><span>${m}</span><i>✓</i></div>`).join("")}</div>
      <div class="expl" ${at("up", 2.6)}>Every month. No exceptions.</div></div>` },

  { id: "e23-birthday-text-2", key: 'DANNY · "hbd hope ur good"', dur: 4.0, sub: "YOUR BIRTHDAY · AGAIN",
    body: people([["me_home", 0.1]]) + `<div class="content row">${phone(`<div class="pt">Danny</div><div class="ts">March · 11:52 PM</div>
      <div class="bub" ${at("pop", 0.6, 0.35)}>hbd hope ur good</div><div class="read" ${at("fade", 1.6)}>Read 11:53 PM</div>`)}
      <div class="stack"><div class="line" ${at("up", 2.0)}>Same text. Same minute.</div></div></div>` },

  yearCard("e24-year-10", "YEAR 10 · AGE 31 · NET WORTH: $412,000", 10, 31, 412000, [["me_home", 0.1]], "THE LAKE CABIN PHOTOS", "They chipped in $400 each. They didn't invite you."),

  { id: "e25-two-duplexes", key: "2 DUPLEXES · 4 UNITS · $180,000 DOWN", dur: 5.5, sub: "30 MINUTES OUTSIDE THE CITY",
    body: people([["me_home", 0.1], ["gloria", 0.25]]) + `<div class="content"><div class="ttl" ${at("up", 0.2)}>2 DUPLEXES · 4 UNITS</div>
      <div class="blds">${[0.6, 0.9].map((t) => `<div class="bld" ${at("pop", t, 0.35)}>${E.ICONS.building("#b5654a")}</div>`).join("")}
      <div class="stack"><div class="label" ${at("up", 1.3)}>DOWN PAYMENT</div><div class="big">${count(180000, 1.4, 1.0, { pre: "$" })}</div></div></div>
      <div class="expl" ${at("up", 2.6)}>Gloria's Christmas card: the only one you got that year.</div></div>` },

  yearCard("e26-year-11", "YEAR 11 · AGE 32 · NET WORTH: $590,000", 11, 32, 590000, [["me_home", 0.1], ["dad_sad", 0.25]], "DAD'S HEART ATTACK", "Mercy General · parking garage, level 3"),

  { id: "e27-hospital-bill", key: "MERCY GENERAL · BALANCE DUE: $31,400", dur: 5.0, sub: "AFTER INSURANCE",
    body: people([["mom_sad", 0.1], ["dad_sad", 0.2]]) + `<div class="content row"><div class="bill" ${at("up", 0.15)}><div class="bh">MERCY GENERAL HOSPITAL</div>
      <div class="bl"><span>Patient</span><span>Raymond</span></div><div class="bl"><span>Procedure</span><span>2 cardiac stents</span></div>
      <div class="bt" ${at("pop", 1.0, 0.4)}><span>BALANCE DUE</span><b class="red">${count(31400, 1.1, 1.2, { pre: "$" })}</b></div></div>
      <div class="stack"><div class="line" ${at("up", 2.4)}>Their savings: $0</div></div></div>` },

  { id: "e28-fundraiser", key: "FUNDRAISER · RAISED: $2,140 OF $31,400", dur: 5.0, sub: "DANNY'S POST: \"FAMILY CARRIES FAMILY\"",
    body: people([["danny", 0.1], ["kayla", 0.2]]) + `<div class="content"><div class="ttl" ${at("up", 0.2)}>HELP DAD HEAL ${heart}</div>
      <div class="bar" ${at("fade", 0.6)}><div class="fill green" ${at("fill", 0.8, 1.2)} data-to="6.8"></div><span class="bmax">$31,400</span></div>
      <div class="nwrow" ${at("up", 1.2)}><span class="big sm green">${count(2140, 1.2, 1.0, { pre: "$" })}</span><span class="label">raised after 3 weeks</span></div></div>` },

  { id: "e29-paid-in-full", key: "BALANCE DUE: $0 · PAID IN FULL", dur: 5.0, sub: "ONE PHONE CALL · ANONYMOUS",
    body: people([["me_home", 0.1]]) + `<div class="content row"><div class="bill" ${at("up", 0.15)}><div class="bh">MERCY GENERAL HOSPITAL</div>
      <div class="bl"><span>Paid by</span><span>Anonymous</span></div><div class="bt"><span>BALANCE DUE</span><b class="green">$0</b></div>
      <div class="stamp pif" ${at("stamp", 0.8, 0.22)}>PAID IN FULL</div></div>
      <div class="stack"><div class="big green">${count(31400, 1.6, 1.0, { pre: "$" })}</div><div class="line" ${at("up", 2.4)}>You never told anyone.</div></div></div>`, shake: 1.02 },

  yearCard("e30-year-13", "YEAR 13 · AGE 34 · NET WORTH: $1,000,000", 13, 34, 1000000, [["me_now", 0.1]], "A SUNDAY IN A LAUNDROMAT", "Nobody clapped."),

  { id: "e31-the-breakdown", key: "YEAR 16 · AGE 37 · INDEX FUNDS $1,120,000 · TREASURY BILLS $160,000 · DUPLEX EQUITY $560,000", dur: 6.0, sub: "YEAR 16 · AGE 37",
    body: people([["me_now", 0.1], ["okafor", 0.25]]) + `<div class="content"><div class="ledger" ${at("up", 0.15)}><div class="lh">WHAT YOU OWN</div>
      ${[["Index funds", 1120000, 0.6], ["Treasury bills", 160000, 1.0], ["Duplex equity", 560000, 1.4]].map(([n, v, t]) => `<div class="lr" ${at("left", t)}><span>${n}</span><b>${money(v)}</b></div>`).join("")}
      <div class="lr tot" ${at("pop", 2.0, 0.35)}><span>TOTAL</span><b class="green">${count(1840000, 2.1, 1.2, { pre: "$" })}</b></div></div></div>` },

  { id: "e32-eighty-percent", key: "80% · SCHOLARSHIPS + ANIMAL SHELTER", dur: 5.0, sub: "THE TRUST",
    body: people([["okafor", 0.1]]) + `<div class="content"><div class="pct" ${at("pop", 0.3, 0.4)}>80%</div>
      <div class="statrow left"><div class="tag2" ${at("up", 0.9)}>🎓 Scholarships for kids who work after school</div></div>
      <div class="statrow left"><div class="tag2" ${at("up", 1.4)}>🐾 The shelter where you adopted Biscuit</div></div></div>` },

  { id: "e33-twenty-percent", key: "20% · MEDICAL TRUST FOR MOM & DAD · NOBODY ELSE CAN TOUCH IT", dur: 5.0, sub: "THE TRUST",
    body: people([["mom", 0.1], ["dad", 0.2]]) + `<div class="content"><div class="pct" ${at("pop", 0.3, 0.4)}>20%</div>
      <div class="line" ${at("up", 0.9)}>🔒 Medical care for Mom &amp; Dad, for life</div>
      <div class="expl" ${at("up", 1.6)}>Nobody else can touch it. Not for a van. Not for an SUV.</div></div>` },

  { id: "e34-page-31", key: "PAGE 31 · PRIOR GIFTS · MERCY GENERAL HOSPITAL · $31,400 · PAID ON BEHALF OF RAYMOND", dur: 6.0, sub: "THE PAGE MOM KEPT SCROLLING TO",
    body: people([["mom_sad", 0.1]]) + `<div class="content"><div class="doc wide" ${at("up", 0.15)}><div class="dh">TRUST · PAGE 31 · PRIOR GIFTS</div>
      <div class="dl"><span>Recipient</span><span>Mercy General Hospital</span></div><div class="dl"><span>On behalf of</span><span>Raymond (father)</span></div>
      <div class="dl hil" ${at("pop", 1.2, 0.35)}><span>Amount</span><span>$31,400 · paid in full</span></div></div>
      <div class="line" ${at("up", 2.4)}>"It was you. The hospital. It was you."</div></div>` },

  clockCard("e35-tuesday-658", "TUESDAY · 6:58 PM", "TUESDAY", "6:58 PM", [["me_now", 0.1]], "BACK TO TONIGHT", "You finally turn the phone over"),

  { id: "e36-fourteen-missed", key: "14 MISSED CALLS · 9 FROM DANNY", dur: 5.0, sub: "IN NINE HOURS",
    body: people([["danny_worried", 0.1, 0.85], ["kayla", 0.2, 0.85]]) + `<div class="content row"><div class="stack"><div class="big red">${count(14, 0.3, 1.2)}</div><div class="line">MISSED CALLS</div></div>
      <div class="ledger" ${at("up", 0.5)}>${[["Danny", 9], ["Kayla", 2], ["Tasha", 1], ["Uncle", 1], ["Dad", 1]].map(([n, v], i) => `<div class="lr" ${at("left", 0.8 + i * 0.2)}><span>${n}</span><b>${v}</b></div>`).join("")}</div></div>` },

  { id: "e37-moms-voice-note", key: "VOICE NOTE · MOM · 0:41", dur: 5.0, sub: "41 SECONDS",
    body: people([["mom_sad", 0.1]]) + `<div class="content center"><div class="vn" ${at("up", 0.2)}><div class="play">▶</div>
      <div class="wave">${Array.from({ length: 34 }, (_, i) => `<i style="height:${20 + ((i * 37) % 60)}px" ${at("pop", 0.5 + i * 0.03, 0.2)}></i>`).join("")}</div><div class="vt">0:41</div></div>
      <div class="line" ${at("up", 1.8)}>"Baby… on page thirty-one…"</div></div>` },

  choiceCard("e38-call-mom", "ANSWER DANNY · or · CALL MOM", "ANSWER DANNY", "CALL MOM", "b", [["danny", 0.1, 0.8], ["me_now", 0.2, 0.8], ["mom_sad", 0.3, 0.8]], "CALL NUMBER FIFTEEN"),

  clockCard("e39-wednesday-801", "WEDNESDAY · 8:01 AM", "WEDNESDAY", "8:01 AM", [["danny", 0.1], ["me_now_calm", 0.2]], "THIS TIME, YOU ANSWER", "\"Hey! Little brother!\""),

  { id: "e40-next-of-kin", key: "NEXT OF KIN: DANNY → INDEPENDENT TRUSTEE", dur: 5.0, sub: "THAT AFTERNOON",
    body: people([["okafor", 0.1], ["me_now_calm", 0.2]]) + `<div class="content"><div class="doc wide" ${at("up", 0.15)}><div class="dh">TRUST · AMENDMENT</div>
      <div class="dl"><span>Next of kin / contact</span><span class="strk">Danny<i ${at("fill", 0.8, 0.5)} data-to="100"></i></span></div>
      <div class="dl"><span>Replaced with</span><span class="green"><span ${at("type", 1.5, 1.0)} data-text="Independent trustee"></span></span></div></div>
      <div class="expl" ${at("up", 2.8)}>Corrected copy sent to your email. Just yours.</div></div>` },

  { id: "e41-episode-3", key: "EPISODE 3 · COMING SOON", dur: 5.0, sub: "NEXT TIME ON SOMBER JOURNAL", dark: true,
    body: people([["me_now", 0.1]]) + `<div class="content row"><div class="doc dk" ${at("up", 0.3)}><div class="dh">MORTGAGE APPLICATION</div><div class="dl"><span>Co-signer</span><span class="red">DECLINED</span></div></div>
      <div class="stack"><div class="ep2" style="font-size:140px;white-space:nowrap" ${at("pop", 1.2, 0.45)}>EPISODE 3</div><div class="soon" ${at("fade", 1.7)}>COMING SOON</div>
        <div class="line light" ${at("up", 2.2)}>Five years later, he's your landlord.</div></div></div>` },
];
CARDS.forEach((c) => (c.ep = EP));

const CSS2 = `
.yrrow{display:flex;align-items:baseline;gap:30px}.age{font-family:Bebas;font-size:70px;color:#6b726e;letter-spacing:3px}
.day{font-family:Bebas;font-size:70px;letter-spacing:6px;color:#6b726e;margin-bottom:-10px}
.ph{width:330px;height:500px;background:#111;border-radius:46px;border:8px solid #333;padding:16px;flex:0 0 auto}
.phs{height:100%;border-radius:30px;background:#f6f6f6;padding:26px 20px;display:flex;flex-direction:column;gap:12px;overflow:hidden}
.pt{font-family:Inter;font-weight:800;font-size:34px;text-align:center}.ts{font-size:22px;color:#888;text-align:center}
.mc{display:flex;justify-content:space-between;border-bottom:2px solid #e3e3e3;padding:8px 4px;font-size:26px}.mcn{color:#d63b3f;font-weight:800}.mct{color:#888}
.bub{background:#e5e5ea;border-radius:26px;padding:16px 22px;font-size:32px;align-self:flex-start;min-height:70px}
.read{font-size:20px;color:#999;align-self:flex-start;margin-left:10px}
.bal{font-family:Anton;font-size:66px;text-align:center;color:#1f9d55;margin-top:60px}
.notif{display:flex;align-items:center;gap:26px;background:#fff;border-radius:34px;padding:26px 40px;box-shadow:0 10px 30px rgba(0,0,0,.18);width:1000px}
.nic{font-size:60px;background:#2fbf71;border-radius:18px;width:90px;height:90px;display:flex;align-items:center;justify-content:center}
.nt{font-family:Inter;font-weight:800;font-size:42px}.nm{font-size:34px;color:#444}.nw{margin-left:auto;font-size:26px;color:#999}
.doc{flex:0 0 auto;background:#fff;border:5px solid #151a17;border-radius:8px;padding:26px 34px;width:620px;box-shadow:0 10px 24px rgba(0,0,0,.18)}
.doc.wide{width:900px}.doc.dk{background:#1f1a16;color:#f2e6d6;border-color:#E3B341}
.dh{font-family:Bebas;font-size:40px;letter-spacing:2px;border-bottom:3px solid #ddd;padding-bottom:6px;margin-bottom:10px}
.dl{position:relative;display:flex;justify-content:space-between;gap:30px;font-size:32px;padding:6px 10px;border-bottom:1px dashed #ddd;white-space:nowrap;isolation:isolate}
.dt{display:flex;justify-content:space-between;align-items:baseline;font-family:Bebas;font-size:44px;margin-top:10px}.dt span:last-child{font-family:Anton;font-size:64px}
.dl.hil{font-weight:800;background:#ffe08a;border-radius:8px;margin-top:6px}.hlbar{position:absolute;left:0;top:4px;bottom:4px;width:0;background:rgba(255,216,102,.55);z-index:-1;border-radius:6px}
.strk{position:relative}.strk i{position:absolute;left:-6px;top:50%;height:6px;width:0;background:#d63b3f;border-radius:3px}
.stub{background:#f7f2e4;border:4px dashed #b9a982;border-radius:10px;padding:30px 50px;width:1100px;transform:rotate(-1.5deg)}
.sh{font-family:Bebas;font-size:34px;color:#9b8c6a;letter-spacing:3px}.hand{font-family:Marker;font-size:52px;color:#1f2b55;min-height:70px}.hand.red{color:#b3262b}
.ledger{background:#fff;border:5px solid #151a17;border-radius:12px;padding:18px 34px;min-width:640px}.ledger.wide{min-width:1000px}
.lh{font-family:Bebas;font-size:48px;letter-spacing:3px;border-bottom:3px solid #ddd;margin-bottom:6px}
.lr{display:flex;justify-content:space-between;font-size:34px;font-weight:600;padding:5px 0}.lr b{font-weight:800}
.lr.tot{border-top:3px solid #ddd;margin-top:6px;padding-top:10px;font-family:Bebas;font-size:48px}.lr.tot b{font-family:Anton;font-size:64px}
.lgrid{display:grid;grid-template-columns:1fr 1fr;column-gap:60px}.lr.dots{color:#888;font-style:italic}
.vs2{display:flex;gap:120px}.vcol{display:flex;flex-direction:column;gap:6px}
.hbars{display:flex;flex-direction:column;gap:26px}.hb{display:flex;align-items:center;gap:26px}.hl{font-family:Bebas;font-size:44px;width:330px;letter-spacing:2px}
.hbar{position:relative;flex:1;height:60px;background:#ddd5c4;border:5px solid #151a17;border-radius:30px;overflow:hidden;min-width:420px}.hb b{font-family:Anton;font-size:64px;width:270px}
.fill.red{background:#e5484d}
.deck{width:560px;height:400px;background:linear-gradient(160deg,#1f8a8a,#0f4f4f);border:6px solid #151a17;border-radius:14px;color:#fff;padding:30px;display:flex;flex-direction:column;align-items:center}
.dk1{font-family:Anton;font-size:76px;letter-spacing:3px}.dk2{font-family:Bebas;font-size:42px;letter-spacing:5px;color:#E3B341}.van{font-size:120px}.dk3{font-family:Bebas;font-size:30px;letter-spacing:3px;margin-top:auto}
.chat{width:900px;background:#fff;border-radius:24px;padding:24px 34px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.ch{font-family:Inter;font-weight:800;font-size:40px;text-align:center;border-bottom:2px solid #eee;padding-bottom:10px}
.cb{background:#e5e5ea;border-radius:22px;padding:14px 20px;font-size:30px;margin:16px 0;display:inline-block}
.sys{text-align:center;color:#888;font-size:34px;font-style:italic;margin-top:10px}
.steps{display:flex;align-items:flex-end;gap:60px;height:260px}.stp{display:flex;flex-direction:column;align-items:center;gap:8px}
.sb{width:150px;background:#2fbf71;border:5px solid #151a17;border-radius:10px 10px 0 0}.stp b{font-family:Anton;font-size:46px}
.cal{display:grid;grid-template-columns:repeat(12,1fr);gap:10px}.cm{background:#fff;border:4px solid #151a17;border-radius:10px;height:90px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.cm span{font-family:Bebas;font-size:30px}.cm i{font-style:normal;color:#1f9d55;font-weight:800;font-size:34px}
.bill{flex:0 0 auto;position:relative;background:#fff;border:5px solid #151a17;border-radius:8px;padding:26px 34px;width:620px}
.bh{font-family:Bebas;font-size:40px;letter-spacing:2px;color:#2c5a8a;border-bottom:3px solid #ddd;padding-bottom:6px;margin-bottom:8px}
.bl{display:flex;justify-content:space-between;font-size:30px;padding:5px 0}
.bt{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px;font-family:Bebas;font-size:44px}.bt b{font-family:Anton;font-size:62px}
.stamp.pif{left:auto;right:-60px;top:-50px;border-color:#1f9d55;color:#1f9d55;font-size:50px;padding:8px 20px;background:rgba(255,255,255,.85)}
.pct{font-family:Anton;font-size:200px;line-height:1;color:#0B1410}
.tag2{font-size:40px;font-weight:700;background:#fff;border:4px solid #151a17;border-radius:16px;padding:12px 24px}
.vn{display:flex;align-items:center;gap:26px;background:#fff;border-radius:60px;padding:24px 40px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.play{width:80px;height:80px;border-radius:50%;background:#2fbf71;color:#fff;font-size:40px;display:flex;align-items:center;justify-content:center}
.wave{display:flex;align-items:center;gap:7px;height:90px}.wave i{width:10px;background:#2c3a33;border-radius:5px;display:block}
.vt{font-family:Mono;font-size:44px;color:#555}
`;

module.exports = { CARDS, page: (c) => E.page(c, CSS2) };
