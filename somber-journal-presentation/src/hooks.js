
  // ---- helpers ----
  const fmt=v=>v<1000?String(v):v<10000?(Math.floor(v/100)/10)+'K':Math.floor(v/1000)+'K';
  function ease(p){return p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;}
  // exponential count: flies through the small numbers and lands on big ones
  function countExp(from,to,ms,onTick,done){
    if(reduce){onTick(to,1);done&&done();return;}
    const t0=performance.now(),me=cur,lf=Math.log(Math.max(from,1)),lt=Math.log(to);
    (function f(t){
      if(cur!==me)return;
      const p=Math.min(1,(t-t0)/ms),v=p>=1?to:Math.round(Math.exp(lf+(lt-lf)*ease(p)));
      onTick(v,p);
      if(p<1)requestAnimationFrame(f);else done&&done();
    })(t0);
  }
  function countLin(from,to,ms,onTick,done){
    if(reduce){onTick(to,1);done&&done();return;}
    const t0=performance.now(),me=cur;
    (function f(t){
      if(cur!==me)return;
      const p=Math.min(1,(t-t0)/ms);onTick(Math.round(from+(to-from)*ease(p)),p);
      if(p<1)requestAnimationFrame(f);else done&&done();
    })(t0);
  }
  function popPlus(host,x,y,txt,cls){
    if(reduce)return;const el=document.createElement('span');
    el.className='plus'+(cls?' '+cls:'');el.textContent=txt;el.style.left=x+'px';el.style.top=y+'px';
    host.appendChild(el);setTimeout(()=>el.remove(),1200);
  }
  function confetti(canvas,n){
    if(reduce||!canvas)return;const c=canvas.getContext('2d'),W=canvas.width,H=canvas.height;
    const cols=['#ff8a1e','#f5f6f8','#37d67a','#ffc285'];
    const ps=Array.from({length:n},()=>({x:W/2,y:H/2,vx:(Math.random()-.5)*20,vy:(Math.random()-.8)*18,r:Math.random()*6+3,c:cols[Math.random()*4|0],a:Math.random()*6,life:1}));
    (function f(){c.clearRect(0,0,W,H);let alive=0;ps.forEach(p=>{p.vy+=.4;p.x+=p.vx;p.y+=p.vy;p.a+=.2;p.life-=.011;if(p.life>0){alive++;c.globalAlpha=p.life;c.fillStyle=p.c;c.save();c.translate(p.x,p.y);c.rotate(p.a);c.fillRect(-p.r,-p.r/2,p.r*2,p.r);c.restore();}});c.globalAlpha=1;if(alive)requestAnimationFrame(f);else c.clearRect(0,0,W,H);})();
  }
  function resetSlide(sl,cls){sl.classList.add('notrans');sl.classList.remove(...cls);void sl.offsetWidth;sl.classList.remove('notrans');}

  const START=[7,20,17,70,40],END=[50000,38000,41000,120000,64000];
  function setRec(cam,views,subs){
    cam.querySelectorAll('.rviews').forEach((e,k)=>{e.textContent=fmt(views[k]);});
    cam.querySelector('.rsubs').textContent=subs>=1000&&subs%1000===0?fmt(subs):subs.toLocaleString('en-US');
  }
  // generic: any [data-to] number on a slide counts up when the slide opens
  function countAll(s){
    s.querySelectorAll('[data-to]').forEach((el,k)=>{
      const to=+el.dataset.to,from=+(el.dataset.from||el.textContent.replace(/\D/g,'')||1);
      timers.push(setTimeout(()=>countExp(Math.max(from,1),to,1700,v=>{el.textContent=fmt(v);}),900+k*150));
    });
  }

  const enter={
    intro(){
      const sl=document.getElementById('intro'),cam=document.getElementById('introCam');
      resetSlide(sl,['dive','zoomv','counting','done','stamped']);
      setRec(cam,START,15);
      const hot=cam.querySelectorAll('.rviews');hot.forEach(e=>e.classList.remove('hot'));hot[0].classList.add('hot');
      if(reduce){sl.classList.add('dive','done');setRec(cam,END,1000);return;}
      timers.push(setTimeout(()=>sl.classList.add('dive'),500));
      timers.push(setTimeout(()=>sl.classList.add('zoomv'),1800));
      timers.push(setTimeout(()=>{
        sl.classList.add('counting');let last=0;
        countExp(7,50000,1500,(v,p)=>{hot[0].textContent=fmt(v);const n=performance.now();if(n-last>90){last=n;popPlus(sl,560+Math.random()*420,560+Math.random()*120,'+'+fmt(Math.max(1,Math.round(v*.04)))+' views');}});
      },2500));
      timers.push(setTimeout(()=>{
        sl.classList.remove('zoomv');hot.forEach(e=>e.classList.add('hot'));
        const views=[50000,20,17,70,40];
        [1,2,3,4].forEach(k=>countExp(START[k],END[k],1300,v=>{views[k]=v;hot[k].textContent=fmt(v);}));
        const subsEl=cam.querySelector('.rsubs');
        countLin(15,1000,1400,v=>{subsEl.textContent=v.toLocaleString('en-US');},()=>{subsEl.textContent='1K';});
        let last=0;const t0=performance.now();
        (function pp(){if(cur!==0||performance.now()-t0>1400)return;const n=performance.now();if(n-last>110){last=n;popPlus(sl,150+Math.random()*1300,520+Math.random()*140,Math.random()<.5?'+1 subscriber':'+'+(1+Math.random()*9|0)+'K views',Math.random()<.4?'o':'');}requestAnimationFrame(pp);})();
      },4200));
      timers.push(setTimeout(()=>{sl.classList.remove('counting');sl.classList.add('done');confetti(document.getElementById('cf0'),260);},5800));
    },
    score(){
      const s=slides[cur];s.querySelectorAll('.sc').forEach(e=>e.classList.remove('on'));
      s.querySelectorAll('.sc').forEach((e,k)=>timers.push(setTimeout(()=>e.classList.add('on'),900+k*230)));
    },
    titles(){
      const rws=slides[cur].querySelectorAll('.rw');
      rws.forEach((rw,k)=>{
        const sp=rw.querySelector('.new > span'),txt=sp.dataset.title,cc=rw.querySelector('.cc'),b=cc.querySelector('b'),bar=cc.querySelector('i');
        sp.textContent='';b.textContent='0';bar.style.setProperty('--w','0%');
        const dash=txt.indexOf('—');
        const ant=sp.dataset.ant||'';const esc=x=>x.replace(/&/g,'&amp;').replace(/</g,'&lt;');const paint=n=>{const t=esc(txt.slice(0,n));let h=t;const ai=t.indexOf(ant);if(ant&&ai>=0)h=t.slice(0,ai)+'<span class="ant">'+ant+'</span>'+t.slice(ai+ant.length);else if(ant&&n<5+ant.length)h=t.replace(/^(POV: )(.*)$/,'$1<span class="ant">$2</span>');sp.innerHTML=h.replace(/(— .*)$/,'<span class="tw">$1</span>');b.textContent=n;bar.style.setProperty('--w',(n/70*100)+'%');};
        if(reduce){paint(txt.length);return;}
        let n=0;const tick=()=>{paint(++n);if(n<txt.length)timers.push(setTimeout(tick,22));};
        timers.push(setTimeout(tick,600+k*800));
      });
    },
    char(){
      const s=slides[cur];s.classList.remove('s-char-on');void s.offsetWidth;
      timers.push(setTimeout(()=>s.classList.add('s-char-on'),reduce?0:1500));
    },
    road(){
      const h=document.getElementById('mHours');h.textContent='0';
      timers.push(setTimeout(()=>countLin(0,4800,1800,v=>{h.textContent=v.toLocaleString('en-US');}),reduce?0:2000));
    },
    close(){playClose();}
  };
  function playClose(){
    clearTimers();
    const sl=document.getElementById('close'),cam=document.getElementById('closeCam');
    resetSlide(sl,['counting','done','stamped']);
    setRec(cam,START,15);
    const hot=cam.querySelectorAll('.rviews');hot.forEach(e=>e.classList.add('hot'));
    if(reduce){setRec(cam,END,1000);sl.classList.add('done','stamped');return;}
    timers.push(setTimeout(()=>{
      sl.classList.add('counting');
      [0,1,2,3,4].forEach(k=>countExp(START[k],END[k],1800,v=>{hot[k].textContent=fmt(v);}));
      const subsEl=cam.querySelector('.rsubs');
      countLin(15,1000,1900,v=>{subsEl.textContent=v.toLocaleString('en-US');},()=>{subsEl.textContent='1K';});
      let last=0;const t0=performance.now(),me=cur;
      (function pp(){if(cur!==me||performance.now()-t0>1900)return;const n=performance.now();if(n-last>100){last=n;popPlus(sl,150+Math.random()*1300,500+Math.random()*160,Math.random()<.5?'+1 subscriber':'+'+(1+Math.random()*9|0)+'K views',Math.random()<.4?'o':'');}requestAnimationFrame(pp);})();
    },1200));
    timers.push(setTimeout(()=>{sl.classList.add('stamped');confetti(document.getElementById('cf1'),300);},3300));
    timers.push(setTimeout(()=>{sl.classList.remove('counting');sl.classList.add('done');},4100));
  }
  document.getElementById('replay').addEventListener('click',playClose);

  // controls
  document.getElementById('prev').onclick=()=>go(cur-1);
  document.getElementById('next').onclick=()=>go(cur+1);
  document.getElementById('fs').onclick=()=>{try{const p=document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();p&&p.catch&&p.catch(()=>{});}catch(e){}};
  addEventListener('keydown',e=>{
    if(e.target.tagName==='INPUT')return;
    if(!splash.classList.contains('gone')){if(['ArrowRight',' ','Enter','PageDown'].includes(e.key)){e.preventDefault();closeSplash();}return;}
    if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(cur+1);}
    else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(cur-1);}
    else if(e.key==='Home')go(0);else if(e.key==='End')go(slides.length-1);
    else if(e.key==='f'||e.key==='F')document.getElementById('fs').click();
  });
  let tx=null;
  vp.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;},{passive:true});
  vp.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(cur+(dx<0?1:-1));tx=null;});

  // splash
  const splash=document.getElementById('splash');
  const hi=document.getElementById('hi');hi.innerHTML=[...hi.textContent].map((ch,k)=>`<span style="animation-delay:${3.1+k*.07}s">${ch}</span>`).join('');
  const cd=document.getElementById('cd');[2,1].forEach((n,k)=>setTimeout(()=>{cd.textContent=n;},900*(k+1)));
  setTimeout(()=>{if(reduce)return;for(let k=0;k<28;k++){const s=document.createElement('i');s.className='spark';const a=Math.random()*Math.PI*2,d=160+Math.random()*260;s.style.cssText=`left:50%;top:50%;--x:${Math.cos(a)*d}px;--y:${Math.sin(a)*d}px;animation-delay:${Math.random()*.2}s`;splash.appendChild(s);}},3000);
  function closeSplash(){if(closed)return;closed=true;splash.classList.add('gone');const start=slides[cur];restore(start);start.classList.remove('active');void start.offsetWidth;start.classList.add('active');runEnter(start);}
  splash.addEventListener('click',closeSplash);
  setTimeout(closeSplash,12000);

  const m=/^#slide-(\d+)$/.exec(location.hash);
  go(m?(+m[1]-1):0);
  if(m||reduce)closeSplash();
  addEventListener('hashchange',()=>{const h=/^#slide-(\d+)$/.exec(location.hash);if(h)go(+h[1]-1);});
})();
