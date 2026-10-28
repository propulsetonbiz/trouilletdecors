const header=document.querySelector('header');
const onScroll=()=>header.classList.toggle('scrolled',scrollY>40);
addEventListener('scroll',onScroll,{passive:true});onScroll();

const burger=document.getElementById('burger'),menu=document.getElementById('menu');
burger.onclick=()=>{const o=menu.classList.toggle('open');burger.classList.toggle('open',o);document.body.style.overflow=o?'hidden':''};
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{burger.classList.remove('open');menu.classList.remove('open');document.body.style.overflow=''}));

// Éléments animés en « rideau » (ajoutés avant l'observation)
// (un élément entièrement masqué n'est pas détecté à l'écran : on surveille donc son conteneur)
const wipeIO=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;wipeIO.unobserve(e.target);
  e.target.querySelectorAll('.wipe').forEach((w,k)=>setTimeout(()=>w.classList.add('in'),k*110));
}),{threshold:.15});
document.querySelectorAll('.concept-img img,.projets-home .proj,.cat').forEach(el=>el.classList.add('wipe'));
new Set([...document.querySelectorAll('.wipe')].map(w=>w.parentElement)).forEach(p=>wipeIO.observe(p));
document.querySelectorAll('.steps').forEach(el=>el.classList.add('rv-line'));

const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
const reveal=root=>root.querySelectorAll('.rv:not(.in),.rv-line:not(.in)').forEach(el=>io.observe(el));
reveal(document);

const y=document.getElementById('y');if(y)y.textContent=new Date().getFullYear();

// Formulaire : envoi direct vers la boîte mail via FormSubmit (https://formsubmit.co)
const CONTACT_EMAIL='trouilletdecors@gmail.com';
const form=document.getElementById('form');
if(form)form.addEventListener('submit',async e=>{
  e.preventDefault();
  const v=id=>form.querySelector('#'+id).value.trim();
  const status=document.getElementById('form-status');
  const btn=form.querySelector('button[type=submit]');
  const travaux=[...form.querySelectorAll('.chips input:checked')].map(c=>c.value).join(', ')||'—';
  const data={
    _subject:`Demande de devis — ${v('nom')}`,
    _template:'table',
    _replyto:v('email'),
    _honey:form.querySelector('[name=_honey]').value,
    'Nom':v('nom'),'Téléphone':v('tel'),'E-mail':v('email'),'Profil':v('type'),
    'Travaux envisagés':travaux,'Ville du chantier':v('ville')||'—','Message':v('msg')||'—'
  };
  const show=(msg,ok)=>{status.hidden=false;status.className='form-status '+(ok?'ok':'err');status.innerHTML=msg};
  btn.disabled=true;btn.firstChild.textContent='Envoi en cours…';
  try{
    const r=await fetch('https://formsubmit.co/ajax/'+CONTACT_EMAIL,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
    const j=await r.json().catch(()=>({}));
    if(!r.ok||j.success===false||j.success==='false')throw new Error(j.message||r.status);
    form.reset();
    show('Merci, votre demande a bien été envoyée. Nous revenons vers vous sous 48h.',true);
  }catch(err){
    show(`L'envoi n'a pas abouti. Contactez-nous directement au <a href="tel:+33625516784">06 25 51 67 84</a> ou à <a href="mailto:${CONTACT_EMAIL}">${CONTACT_EMAIL}</a>.`,false);
  }finally{
    btn.disabled=false;btn.firstChild.textContent='Envoyer ma demande';
  }
});

/* ---------- Visionneuse plein écran ---------- */
const Lightbox=(()=>{
  let items=[],idx=0,title='',el;
  function build(){
    el=document.createElement('div');el.className='lb';el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');
    el.innerHTML=`<div class="lb-top"><span class="lb-title"></span><span class="lb-count"></span><button class="lb-close" aria-label="Fermer">&times;</button></div>
      <button class="lb-nav lb-prev" aria-label="Photo précédente">&#8249;</button>
      <figure class="lb-stage"><img alt=""></figure>
      <div class="lb-cap"><span class="lb-stage-tag"></span><p></p></div>
      <button class="lb-nav lb-next" aria-label="Photo suivante">&#8250;</button>`;
    document.body.appendChild(el);
    el.querySelector('.lb-close').onclick=close;
    el.querySelector('.lb-prev').onclick=()=>go(-1);
    el.querySelector('.lb-next').onclick=()=>go(1);
    el.addEventListener('click',e=>{if(e.target===el||e.target.classList.contains('lb-stage'))close()});
    let x0=null;
    el.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});
    el.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)go(dx<0?1:-1);x0=null});
    addEventListener('keydown',e=>{if(!el.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')go(-1);if(e.key==='ArrowRight')go(1)});
  }
  function render(){
    const img=el.querySelector('img');img.classList.remove('ready');
    img.onload=()=>img.classList.add('ready');
    const it=items[idx];
    img.src=it.src;img.alt=it.alt||it.cap||'';
    el.querySelector('.lb-cap p').textContent='';
    el.querySelector('.lb-stage-tag').textContent=it.stage||'';
    el.querySelector('.lb-cap').hidden=!it.stage;
    el.querySelector('.lb-title').textContent=title;
    el.querySelector('.lb-count').textContent=`${idx+1} / ${items.length}`;
    [-1,1].forEach(d=>{const n=items[(idx+d+items.length)%items.length];if(n)new Image().src=n.src});
  }
  function go(d){idx=(idx+d+items.length)%items.length;render()}
  function open(list,i,t){if(!el)build();items=list.map(x=>typeof x==='string'?{src:x}:x);idx=i||0;title=t||'';el.classList.add('open');document.body.style.overflow='hidden';render()}
  function close(){el.classList.remove('open');document.body.style.overflow=''}
  return{open};
})();

// Projets phares (accueil et page réalisations) : clic = ouverture du diaporama du projet
document.querySelectorAll('[data-project]').forEach(card=>card.addEventListener('click',e=>{
  if(!window.PHOTOS)return;
  e.preventDefault();
  const p=PHOTOS.projects.find(p=>p.id===card.dataset.project);
  openProject(p,0);
}));
// Diaporama d'un projet ; s'il contient des photos « avant », les étapes sont libellées Avant / Pendant / Après
function openProject(p,i){
  const ba=p.photos.some(x=>x[5]==='avant');
  const STAGE=ba?{avant:'Avant',chantier:'Pendant les travaux',resultat:'Après'}:{resultat:'Résultat',chantier:'En cours de chantier'};
  Lightbox.open(p.photos.map(([f,,,alt,,st])=>({src:`images/${p.id}/full/${f}`,alt,stage:STAGE[st]})),i||0,p.title);
}

/* ---------- Animations ---------- */
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

// Intro avec le logo : une seule fois par session, puis lancement du titre
(()=>{
  const intro=document.querySelector('.intro'),title=document.querySelector('.hero-title');
  const start=()=>title&&title.classList.add('go');
  if(!intro){start();return}
  let seen=false;try{seen=sessionStorage.getItem('td-intro')==='1';sessionStorage.setItem('td-intro','1')}catch(e){}
  if(seen||reduce){intro.classList.add('skip');start();return}
  document.body.style.overflow='hidden';
  const end=()=>{intro.classList.add('done');document.body.style.overflow='';setTimeout(start,250)};
  const t0=performance.now();
  const go=()=>setTimeout(end,Math.max(0,1300-(performance.now()-t0)));
  document.readyState==='complete'?go():addEventListener('load',go,{once:true});
  setTimeout(end,3000); // sécurité si une image tarde
})();

// Compteurs des chiffres clés
const countIO=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;countIO.unobserve(e.target);
  const el=e.target,to=+el.dataset.count,suf=el.dataset.suffix||'',t0=performance.now(),dur=1600;
  if(reduce){el.textContent=to+suf;return}
  const step=t=>{const k=Math.min(1,(t-t0)/dur),v=Math.round(to*(1-Math.pow(1-k,3)));el.textContent=v+suf;if(k<1)requestAnimationFrame(step)};
  requestAnimationFrame(step);
}),{threshold:.6});
document.querySelectorAll('[data-count]').forEach(el=>countIO.observe(el));

// Barre de progression + léger parallaxe du héro
const bar=document.querySelector('.progress'),heroMedia=document.querySelector('.hero-media');
let ticking=false;
addEventListener('scroll',()=>{
  if(ticking)return;ticking=true;
  requestAnimationFrame(()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    if(bar)bar.style.transform=`scaleX(${max>0?scrollY/max:0})`;
    if(heroMedia&&!reduce&&scrollY<innerHeight*1.2)heroMedia.style.transform=`translate3d(0,${scrollY*.18}px,0)`;
    ticking=false;
  });
},{passive:true});

// Bouton d'appel : sur téléphone il lance l'appel ; sur ordinateur (pas de téléphonie) il affiche le numéro
(()=>{
  const btn=document.querySelector('.float-call');if(!btn)return;
  const isPhone=matchMedia('(pointer:coarse)').matches||/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if(isPhone)return;
  const num='06 25 51 67 84';
  const pop=document.createElement('div');pop.className='call-pop';pop.setAttribute('role','dialog');pop.setAttribute('aria-label','Nous appeler');
  pop.innerHTML=`<small>Appelez-nous</small><b>${num}</b><div class="call-pop-actions"><button type="button" class="cp-copy">Copier le numéro</button><a href="index.html#contact" class="cp-form">Formulaire</a></div>`;
  document.body.appendChild(pop);
  const toggle=o=>pop.classList.toggle('open',o);
  btn.addEventListener('click',e=>{e.preventDefault();toggle(!pop.classList.contains('open'))});
  pop.querySelector('.cp-form').addEventListener('click',()=>toggle(false));
  pop.querySelector('.cp-copy').addEventListener('click',async e=>{
    const b=e.currentTarget;
    try{await navigator.clipboard.writeText(num.replace(/\s/g,''));b.textContent='Numéro copié ✓'}catch(_){b.textContent=num}
    setTimeout(()=>b.textContent='Copier le numéro',2000);
  });
  addEventListener('click',e=>{if(!pop.contains(e.target)&&!btn.contains(e.target))toggle(false)});
  addEventListener('keydown',e=>{if(e.key==='Escape')toggle(false)});
})();

// Pages savoir-faire (générées) : rubriques, filtre Résultats / En chantier, visionneuse légendée
document.querySelectorAll('.svc-gallery').forEach(g=>{
  g.querySelectorAll('[data-jump]').forEach(a=>a.addEventListener('click',e=>{
    e.preventDefault();const t=document.getElementById(a.dataset.jump);
    scrollTo({top:t.getBoundingClientRect().top+scrollY-(innerWidth<=860?130:160),behavior:'smooth'});
  }));
  g.querySelectorAll('.stage-toggle button').forEach(b=>b.addEventListener('click',()=>{
    g.querySelectorAll('.stage-toggle button').forEach(x=>x.classList.toggle('on',x===b));
    const s=b.dataset.stage;
    g.querySelectorAll('.pc').forEach(f=>f.hidden=!!s&&f.dataset.stage!==s);
    g.querySelectorAll('.sub').forEach(sec=>sec.hidden=!sec.querySelector('.pc:not([hidden])'));
  }));
  g.addEventListener('click',e=>{
    const f=e.target.closest('.pc');if(!f)return;
    const vis=[...g.querySelectorAll('.pc:not([hidden])')];
    const title=(document.querySelector('.svc-hero h1')||{}).textContent||'';
    Lightbox.open(vis.map(v=>({src:v.dataset.full,alt:v.querySelector('img').alt,stage:v.dataset.stageLabel})),vis.indexOf(f),title.replace(/ à Aix-en-Provence\.?$/,''));
  });
});

/* ---------- Garanties, labels & avis clients (contenu dans confiance.js) ---------- */
(()=>{
  const C=window.CONFIANCE;if(!C)return;
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const star='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z" fill="currentColor"/></svg>';
  const stars=n=>`<span class="stars" aria-label="${n} sur 5">${star.repeat(Math.round(n))}</span>`;

  const g=document.getElementById('garanties');
  if(g&&(C.garanties||[]).length){
    g.hidden=false;
    g.innerHTML=`<div class="wrap"><div class="gar-row">${C.garanties.map((x,i)=>`
      <div class="gar rv${i?' d'+Math.min(i,3):''}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>
      <div><b>${esc(x.titre)}</b><span>${esc(x.texte||'')}</span></div></div>`).join('')}</div>
      ${(C.labels||[]).length?`<div class="labels">${C.labels.map(l=>`<img src="${esc(l.logo)}" alt="${esc(l.nom)}" title="${esc(l.nom)}">`).join('')}</div>`:''}</div>`;
    reveal(g);
  }

  const a=document.getElementById('avis');
  if(a){
    const list=C.avis||[];
    const lienAvis=C.lienAvis||`mailto:trouilletdecors@gmail.com?subject=${encodeURIComponent('Mon avis sur Trouillet Décors')}`;
    const note=C.note?`<div class="avis-note rv d2"><b class="gold">${String(C.note).replace('.',',')}</b><div>${stars(C.note)}<small>${C.nombreAvis?C.nombreAvis+' avis Google':'Avis Google'}</small></div></div>`:'';
    a.hidden=false;
    a.innerHTML=`<div class="wrap">
      <div class="sec-head"><div><span class="eyebrow rv">Avis clients</span><h2 class="rv d1">${list.length?'Ils nous ont <em class="gold">fait confiance.</em>':'Votre avis <em class="gold">compte.</em>'}</h2></div>${note}</div>
      ${list.length?`<div class="avis-grid">${list.map((r,i)=>`
        <figure class="avis-card rv${i%3?' d'+(i%3):''}">${stars(r.note||5)}
          <blockquote>« ${esc(r.texte)} »</blockquote>
          <figcaption><b>${esc(r.nom)}</b>${r.projet?`<span>${esc(r.projet)}</span>`:''}${r.date?`<small>${esc(r.date)}</small>`:''}</figcaption></figure>`).join('')}</div>`:''}
      <div class="avis-cta rv">
        <p>${list.length?'Vous aussi, vous avez fait appel à nous ?':'Vous avez fait appel à Trouillet Décors ?'} Votre avis aide d'autres familles de la région à nous trouver.</p>
        <div class="avis-btns">
          <a class="btn btn-gold" href="${esc(lienAvis)}" ${C.lienAvis?'target="_blank" rel="noopener"':''}>${C.lienAvis?'Laisser un avis Google':'Nous envoyer votre avis'}</a>
          ${C.lienGoogle?`<a class="btn btn-ghost" href="${esc(C.lienGoogle)}" target="_blank" rel="noopener">Voir tous nos avis</a>`:''}
        </div>
      </div></div>`;
    reveal(a);
  }
})();
