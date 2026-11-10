
(function(){
  const stage=document.getElementById('stage'),vp=document.getElementById('vp');
  const slides=[...stage.querySelectorAll('.slide')];
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cur=-1;

  function fit(){const s=Math.min(vp.clientWidth/1600,vp.clientHeight/900);stage.style.transform=`translate(-50%,-50%) scale(${s})`;}
  addEventListener('resize',fit);fit();

  // dots
  const dots=document.getElementById('dots');
  slides.forEach((s,i)=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Go to slide '+(i+1)+': '+(s.dataset.name||''));b.onclick=()=>go(i);dots.appendChild(b);});

  const timers=[];
  function clearTimers(){while(timers.length)clearTimeout(timers.pop());}

  function restore(sl){sl.querySelectorAll('[data-mt]').forEach(e=>{e.style.animation='';e.style.transition='';e.style.transform='';e.style.transformOrigin='';e.removeAttribute('data-mt');});}
  // Morph: the new slide's object starts at the old object's box and glides home along a slight arc,
  // while a ghost copy of the old object travels with it and dissolves (a true cross-morph).
  function morph(old,s){
    const sr=stage.getBoundingClientRect(),sc=sr.width/1600;
    const ez='cubic-bezier(.76,0,.14,1)';
    s.querySelectorAll('[data-morph]').forEach(el=>{
      const src=old.querySelector('[data-morph="'+el.dataset.morph+'"]');if(!src)return;
      const o=src.getBoundingClientRect();if(!o.width||!o.height)return;
      for(let p=el;p&&p!==s;p=p.parentElement){p.style.animation='none';p.setAttribute('data-mt','');}
      const n=el.getBoundingClientRect();if(!n.width||!n.height)return;
      const dx=(o.left-n.left)/sc,dy=(o.top-n.top)/sc,sx=o.width/n.width,sy=o.height/n.height;
      const lift=-Math.min(90,Math.hypot(dx,dy)*.12);
      const ghost=src.cloneNode(true);ghost.removeAttribute('id');ghost.querySelectorAll('[id]').forEach(e=>e.removeAttribute('id'));
      ghost.removeAttribute('data-morph');
      Object.assign(ghost.style,{position:'absolute',left:(o.left-sr.left)/sc+'px',top:(o.top-sr.top)/sc+'px',width:o.width/sc+'px',height:o.height/sc+'px',margin:'0',right:'auto',bottom:'auto',zIndex:'40',pointerEvents:'none',transformOrigin:'0 0',animation:'none',opacity:'1',flex:'none'});
      stage.appendChild(ghost);
      src.style.opacity='0';
      el.style.transformOrigin='0 0';
      const mid=(a,f)=>a+(1-a)*f;
      el.animate([
        {transform:'translate('+dx+'px,'+dy+'px) scale('+sx+','+sy+')',opacity:0,filter:'blur(6px) brightness(1.4)'},
        {offset:.5,transform:'translate('+dx*.45+'px,'+(dy*.45+lift)+'px) scale('+mid(sx,.55)*1.04+','+mid(sy,.55)*1.04+')',opacity:.85,filter:'blur(2px) brightness(1.15)'},
        {transform:'none',opacity:1,filter:'blur(0) brightness(1)'}
      ],{duration:1350,easing:ez,fill:'backwards'});
      ghost.animate([
        {transform:'none',opacity:1,filter:'blur(0)'},
        {offset:.5,transform:'translate('+(-dx*.55)+'px,'+(-dy*.55+lift)+'px) scale('+mid(1/sx,.55)*1.04+','+mid(1/sy,.55)*1.04+')',opacity:.5,filter:'blur(3px)'},
        {transform:'translate('+(-dx)+'px,'+(-dy)+'px) scale('+(1/sx)+','+(1/sy)+')',opacity:0,filter:'blur(8px)'}
      ],{duration:1350,easing:ez,fill:'forwards'}).onfinish=()=>ghost.remove();
    });
  }
  let closed=false;
  const TRANS=['push','cube','flip','iris','split','wipe','vortex'];
  function clearT(el){TRANS.forEach(t=>el.classList.remove('in-'+t,'out-'+t));el.classList.remove('nochild');}
  function go(i){
    i=Math.max(0,Math.min(slides.length-1,i));
    if(i===cur)return;
    clearTimers();
    const dir=cur<0||i>cur?1:-1;
    stage.style.setProperty('--dir',dir);
    const old=cur>=0?slides[cur]:null,s=slides[i];
    const t=reduce||!old?'none':(s.dataset.t||'morph');
    cur=i;
    document.getElementById('prog').style.width=((i+1)/slides.length*100)+'%';
    document.getElementById('count').textContent=(i+1)+' / '+slides.length;
    [...dots.children].forEach((d,k)=>d.setAttribute('aria-current',k===i?'true':'false'));
    try{history.replaceState(null,'','#slide-'+(i+1));}catch(e){}
    const swap=(tt)=>{
      if(old){restore(old);clearT(old);old.classList.remove('active');old.classList.add('leaving');
        if(TRANS.includes(tt)){old.classList.add('out-'+tt,'nochild');}
        clearTimeout(old._t);old._t=setTimeout(()=>{old.classList.remove('leaving');clearT(old);old.querySelectorAll('[data-morph]').forEach(e=>e.style.opacity='');},TRANS.includes(tt)?1300:650);}
      clearTimeout(s._t);s.classList.remove('leaving');clearT(s);s.querySelectorAll('[data-morph]').forEach(e=>e.style.opacity='');
      void s.offsetWidth;
      if(TRANS.includes(tt)){s.classList.add('in-'+tt);s._t=setTimeout(()=>clearT(s),1400);}
      s.classList.add('active');
      if(old&&tt==='morph')morph(old,s);
      const fn=enter[s.dataset.enter];if(fn&&closed)fn();
    };
    if(t==='curtain'){
      const c=document.getElementById('curtains');c.classList.remove('run');void c.offsetWidth;c.classList.add('run');
      timers.push(setTimeout(()=>swap('none'),800));
    } else swap(t);
  }

