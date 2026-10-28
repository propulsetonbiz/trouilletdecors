// Page Réalisations : vue d'ensemble + une vue dédiée par catégorie, générées depuis photos.js
(()=>{
  const {categories}=window.PHOTOS;
  const $=s=>document.querySelector(s);
  const filters=$('#filters'),overview=$('#overview'),viewAll=$('#view-all'),viewCat=$('#view-cat');
  const total=categories.reduce((n,c)=>n+c.photos.length,0);
  const pad=n=>String(n).padStart(2,'0');
  const plural=(n,w)=>`${n} ${w}${n>1?'s':''}`;
  const groupsOf=c=>[...new Set(c.photos.map(p=>p[4]))];
  const STAGE={resultat:'Résultat',chantier:'En cours de chantier',illustration:'Illustration'};

  // Barre de filtres
  filters.innerHTML=[{id:'',title:'Vue d\'ensemble',n:total},...categories.map(c=>({id:c.id,title:c.title,n:c.photos.length}))]
    .map(t=>`<button data-f="${t.id}">${t.title}<sup>${t.n}</sup></button>`).join('');
  filters.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
    const page=(window.PAGES||{})[b.dataset.f];if(page){location.href=page;return}
    location.hash=b.dataset.f||'tout'});

  // Vue d'ensemble : une carte par savoir-faire
  overview.innerHTML=categories.map((c,i)=>`
    <a class="ov rv${['',' d1',' d2'][i%3]}" href="${(window.PAGES||{})[c.id]||'#'+c.id}">
      <div class="ov-img"><img src="images/${c.id}/thumb/${c.cover}" alt="${c.title}" loading="lazy"><span class="ov-n">${pad(i+1)}</span></div>
      <div class="ov-body">
        <h3>${c.title}</h3>
        <p>${c.desc}</p>
        <div class="ov-tags">${groupsOf(c).map(g=>`<span>${g}</span>`).join('')}</div>
        <div class="ov-foot"><span>${plural(c.photos.length,'photo')}</span><span class="ov-go">Découvrir &rarr;</span></div>
      </div>
    </a>`).join('');
  reveal(overview);

  // Projets avec photos « avant » : déroulé Avant -> Pendant -> Après
  const baWrap=document.getElementById('avant-apres');
  if(baWrap){
    const steps=[['avant','Avant','L\'état d\'origine'],['chantier','Pendant','Les travaux'],['resultat','Après','Le résultat']];
    baWrap.innerHTML=window.PHOTOS.projects.filter(p=>p.photos.some(x=>x[5]==='avant')).map(p=>`
      <section class="cat-block ba" data-ba="${p.id}">
        <div class="wrap">
          <div class="cat-head rv">
            <div><span class="eyebrow">Avant / après · ${p.place}</span><h2>${p.title}</h2></div>
            <p>${p.desc} Cliquez sur une photo pour suivre le chantier étape par étape.</p>
          </div>
          <div class="ba-steps">${steps.map(([st,label,sub],k)=>{
            const ph=p.photos.map((x,i)=>[x,i]).filter(([x])=>x[5]===st);
            if(!ph.length)return'';
            return`<div class="ba-step ba-${st} rv${k?' d'+k:''}">
              <div class="ba-label"><span class="ba-n">${String(k+1).padStart(2,'0')}</span><b>${label}</b><small>${sub} · ${ph.length} photo${ph.length>1?'s':''}</small></div>
              <div class="ba-photos">${ph.map(([x,i])=>`<figure class="ba-ph" data-i="${i}"><img src="images/${p.id}/thumb/${x[0]}" alt="${x[3]}" loading="lazy"></figure>`).join('')}</div>
            </div>`}).join('<span class="ba-arrow" aria-hidden="true">&rarr;</span>')}
          </div>
        </div>
      </section>`).join('');
    baWrap.addEventListener('click',e=>{
      const f=e.target.closest('.ba-ph');if(!f)return;
      openProject(window.PHOTOS.projects.find(p=>p.id===f.closest('[data-ba]').dataset.ba),+f.dataset.i);
    });
    reveal(baWrap);
  }

  // Vue dédiée à une catégorie
  function renderCat(c){
    const i=categories.indexOf(c),groups=groupsOf(c);
    const prev=categories[(i-1+categories.length)%categories.length],next=categories[(i+1)%categories.length];
    const nRes=c.photos.filter(p=>p[5]==='resultat').length,nCh=c.photos.length-nRes;
    viewCat.innerHTML=`
      <section class="cat-intro">
        <div class="wrap">
          <div class="cat-intro-grid">
            <div>
              <span class="eyebrow">Savoir-faire ${pad(i+1)} / ${pad(categories.length)}</span>
              <h2>${c.title}</h2>
              <p class="lead">${c.desc}</p>
            </div>
            <ul class="cat-stats">
              <li><b class="gold">${c.photos.length}</b><span>Photos</span></li>
              <li><b class="gold">${nRes}</b><span>Résultats</span></li>
              <li><b class="gold">${nCh}</b><span>En chantier</span></li>
            </ul>
          </div>
          <div class="cat-tools">
            ${groups.length>1?`<div class="jump"><small>Rubriques</small>${groups.map((g,k)=>`<a href="#${c.id}" data-jump="g${k}">${g} <sup>${c.photos.filter(p=>p[4]===g).length}</sup></a>`).join('')}</div>`:''}
            ${nRes&&nCh?`<div class="stage-toggle" role="group" aria-label="Afficher">
              <button class="on" data-stage="">Tout</button><button data-stage="resultat">Résultats</button><button data-stage="chantier">En chantier</button>
            </div>`:''}
          </div>
        </div>
      </section>
      ${groups.map((g,k)=>{const ph=c.photos.filter(p=>p[4]===g);return`
      <section class="sub" id="g${k}">
        <div class="wrap">
          <div class="sub-head"><span class="sub-n">${pad(k+1)}</span><h3>${g||c.title}</h3><span class="sub-count">${plural(ph.length,'photo')}</span></div>
          <div class="pgrid">${ph.map(p=>{const idx=c.photos.indexOf(p);return`
            <figure class="pc" data-i="${idx}" data-stage="${p[5]}" style="--d:${ph.indexOf(p)%8}">
              <div class="pc-img"><img src="images/${c.id}/thumb/${p[0]}" alt="${p[3]}" loading="lazy"><span class="stage stage-${p[5]}">${STAGE[p[5]]}</span></div>
            </figure>`}).join('')}
          </div>
        </div>
      </section>`}).join('')}
      <nav class="cat-nav">
        <div class="wrap">
          <a href="#${prev.id}"><small>&larr; Savoir-faire précédent</small><b>${prev.title}</b></a>
          <a href="#tout" class="cat-nav-all">Tous les savoir-faire</a>
          <a href="#${next.id}" class="r"><small>Savoir-faire suivant &rarr;</small><b>${next.title}</b></a>
        </div>
      </nav>`;

    viewCat.querySelectorAll('[data-jump]').forEach(a=>a.addEventListener('click',e=>{
      e.preventDefault();
      const t=document.getElementById(a.dataset.jump);
      scrollTo({top:t.getBoundingClientRect().top+scrollY-(innerWidth<=860?130:160),behavior:'smooth'});
    }));
    viewCat.querySelectorAll('[data-stage]').forEach(b=>b.tagName==='BUTTON'&&b.addEventListener('click',()=>{
      viewCat.querySelectorAll('.stage-toggle button').forEach(x=>x.classList.toggle('on',x===b));
      const s=b.dataset.stage;
      viewCat.querySelectorAll('.pc').forEach(f=>f.hidden=!!s&&f.dataset.stage!==s);
      viewCat.querySelectorAll('.sub').forEach(sec=>sec.hidden=!sec.querySelector('.pc:not([hidden])'));
    }));
    viewCat.querySelectorAll('.pc').forEach(f=>f.addEventListener('click',()=>{
      // le diaporama suit les photos actuellement visibles
      const vis=[...viewCat.querySelectorAll('.pc:not([hidden])')];
      const list=vis.map(v=>{const p=c.photos[+v.dataset.i];return{src:`images/${c.id}/full/${p[0]}`,alt:p[3],stage:STAGE[p[5]]}});
      Lightbox.open(list,vis.indexOf(f),c.title);
    }));
  }

  function apply(){
    const id=decodeURIComponent(location.hash.slice(1));
    if(window.PAGES&&window.PAGES[id]){location.replace(window.PAGES[id]);return}
    const c=categories.find(c=>c.id===id);
    filters.querySelectorAll('button').forEach(b=>{
      const on=b.dataset.f===(c?c.id:'');b.classList.toggle('on',on);
      if(on)b.scrollIntoView({block:'nearest',inline:'center'});
    });
    viewAll.hidden=!!c;viewCat.hidden=!c;
    if(c)renderCat(c);
    document.title=(c?c.title+' — ':'')+'Réalisations — Trouillet Décors';
    // haut de la zone de contenu (la barre de filtres est « sticky », on se base sur la fin du bandeau)
    const hero=document.querySelector('.page-hero');
    const H=innerWidth<=860?64:74; // hauteur de l'en-tête réduit
    const top=hero.offsetTop+hero.offsetHeight-H;
    if(id==='projets'){const p=$('#projets');scrollTo({top:p.getBoundingClientRect().top+scrollY-H-70,behavior:'instant'})}
    else if(c||scrollY>top)scrollTo({top,behavior:'instant'});
  }
  addEventListener('hashchange',apply);
  apply();
})();
