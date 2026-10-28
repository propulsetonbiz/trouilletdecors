#!/usr/bin/env python3
"""Génère une page dédiée (optimisée pour Google) par savoir-faire, + sitemap.xml et robots.txt.

À relancer après generer-photos.py, ou après une modification de l'en-tête / du pied de page
(ils sont repris de entreprise.html).  ->  python3 tools/generer-pages.py
"""
import os, json, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Adresse définitive du site : à modifier si le nom de domaine est différent
DOMAINE = 'https://www.trouilletdecors.fr'
VILLES = "Aix-en-Provence, Le Tholonet, Puyricard, Éguilles, Venelles, Luynes, Meyreuil, Gardanne, Bouc-Bel-Air"

PHOTOS = json.loads(open('photos.js', encoding='utf-8').read().split('= ', 1)[1].rstrip(';\n'))
CATS = {c['id']: c for c in PHOTOS['categories']}

# Chaque page : sources de photos = [(catégorie, sous-rubrique ou None pour toutes)]
SERVICES = [
 dict(id='peinture', fichier='peinture-aix-en-provence.html', court='Peinture intérieure',
  h1='Peinture intérieure', titre='Peintre en bâtiment : peinture intérieure à Aix-en-Provence',
  meta="Peinture intérieure des murs, plafonds et boiseries, mise en teinte et peintures décoratives à Aix-en-Provence et en région PACA. Devis gratuit.",
  accroche="Des murs impeccables et des teintes justes, pour des pièces lumineuses et prêtes à vivre.",
  texte=["La peinture est la finition que l'on voit en premier : elle demande une préparation soignée des supports, des protections irréprochables et un œil juste pour les couleurs. Nous intervenons sur les murs, plafonds et boiseries, des beiges les plus doux aux teintes les plus profondes.",
         "Rebouchage, ponçage, sous-couche puis deux couches de finition : chaque étape compte pour obtenir un rendu uniforme et durable. Nous réalisons aussi des peintures décoratives, bicolores, damiers ou fresques graphiques."],
  prestations=["Peinture des murs et plafonds", "Mise en teinte et conseil couleurs", "Préparation des supports : rebouchage, ponçage, sous-couche", "Peinture des boiseries et des portes", "Pose et peinture de plinthes", "Peintures décoratives : bicolore, damier, fresques"],
  sources=[('peinture', None)]),
 dict(id='placo', fichier='placo-aix-en-provence.html', court='Placo & meubles en placo',
  h1='Plâtrerie & meubles en placo', titre='Plaquiste : cloisons, faux-plafonds & meubles en placo à Aix-en-Provence',
  meta="Cloisons, doublages, faux-plafonds, niches, bibliothèques et meubles maçonnés en placo à Aix-en-Provence. Plaquiste pour particuliers et professionnels.",
  accroche="Redistribuer les espaces, créer des rangements intégrés, dessiner des volumes sur mesure.",
  texte=["Le placo permet de transformer un intérieur sans gros œuvre : nouvelles cloisons, doublages isolants, faux-plafonds, soffites ou arches en plein cintre. Nous réalisons l'ossature, le passage des réseaux, la pose et les bandes jusqu'à une surface prête à peindre.",
         "C'est aussi un formidable outil de décoration : bibliothèques intégrées avec éclairage, murs TV avec niches, meubles vasques et plans maçonnés, placards encastrés. Des agencements qui font corps avec l'architecture de la pièce."],
  prestations=["Cloisons et doublages (isolation thermique et phonique)", "Faux-plafonds, caissons et soffites", "Arches et formes arrondies", "Bibliothèques et niches éclairées", "Murs TV et cheminées intégrées", "Meubles vasques et plans maçonnés"],
  sources=[('placo', None)]),
 dict(id='patines', fichier='beton-cire-enduit-chaux-aix-en-provence.html', court='Béton ciré & chaux',
  h1='Béton ciré & patines à la chaux', titre='Béton ciré & enduit à la chaux à Aix-en-Provence',
  meta="Béton ciré, microciment et enduits à la chaux pour murs, sols, salles de bains, douches et escaliers à Aix-en-Provence et dans toute la région PACA.",
  accroche="Des matières minérales, douces au toucher et sans joint, pour un intérieur intemporel.",
  texte=["Le béton ciré et les enduits à la chaux apportent cette profondeur de matière qui caractérise les intérieurs contemporains et les maisons de caractère. Appliqués à la main, ils créent des surfaces continues, nuancées et uniques.",
         "Nous les réalisons sur les murs, les sols, les douches à l'italienne, les meubles vasques maçonnés et jusqu'aux escaliers, avec une attention particulière à la préparation des supports et à la protection finale."],
  prestations=["Béton ciré et microciment sols et murs", "Douches à l'italienne et salles d'eau sans joint", "Meubles vasques et plans en béton ciré", "Habillage d'escaliers", "Patines et enduits à la chaux", "Teintes sur mesure"],
  sources=[('patines', None)]),
 dict(id='zelliges', fichier='zelliges-carrelage-aix-en-provence.html', court='Zelliges & carrelage décoratif',
  h1='Zelliges & carrelage décoratif', titre='Pose de zelliges & carreaux ciment à Aix-en-Provence',
  meta="Pose de zelliges, carreaux ciment et panneaux décoratifs pour salles de bains, douches, cuisines et crédences à Aix-en-Provence.",
  accroche="Le charme de l'artisanat dans vos salles de bains, cuisines et crédences.",
  texte=["Les zelliges, avec leurs nuances et leurs irrégularités, demandent une pose experte pour révéler tout leur éclat. Nous les posons en douche, en crédence ou en pan de mur, associés à une robinetterie laiton, à des plans en pierre ou à du bois.",
         "Nous posons aussi les carreaux ciment et les carreaux à motifs, en sol comme en mur, ainsi que les panneaux décoratifs grand format qui habillent une douche d'un seul tenant."],
  prestations=["Pose de zelliges en douche et en crédence", "Carreaux ciment et carreaux à motifs", "Panneaux décoratifs grand format", "Salles de bains complètes", "Crédences de cuisine", "WC et lave-mains"],
  sources=[('zelliges', None)]),
 dict(id='sols', fichier='pose-sols-aix-en-provence.html', court='Sols & escaliers',
  h1='Pose de sols & habillage d’escaliers', titre='Pose de parquet, LVT, carrelage & moquette à Aix-en-Provence',
  meta="Pose de parquet, lames LVT, carrelage grand format et moquette, habillage d'escaliers à Aix-en-Provence et dans toute la région PACA.",
  accroche="Le bon revêtement pour chaque pièce, posé avec précision jusqu'au dernier nez de marche.",
  texte=["Un beau sol commence par un support parfaitement préparé. Nous posons tous les revêtements : parquet, lames vinyle LVT, carrelage grand format, carreaux ciment et moquette, avec des raccords nets et des finitions soignées.",
         "Nous habillons aussi les escaliers, droits, quart tournant ou suspendus, en lames aspect bois ou en moquette, avec nez de marche assortis."],
  prestations=["Parquet et lames aspect bois", "Lames vinyle LVT", "Carrelage grand format", "Carreaux ciment", "Moquette", "Habillage d'escaliers et nez de marche"],
  sources=[('sols', None)]),
 dict(id='finitions', fichier='papier-peint-decoration-aix-en-provence.html', court='Finitions décoratives',
  h1='Papiers peints & finitions décoratives', titre='Pose de papier peint panoramique & décoration murale à Aix-en-Provence',
  meta="Pose de papiers peints panoramiques, claustras, tasseaux, panneaux acoustiques, bardage bois et feuille de pierre à Aix-en-Provence.",
  accroche="La touche qui signe un intérieur : panoramiques, claustras, bois et matières.",
  texte=["Un panoramique bien posé transforme une pièce entière : forêts, montagnes, jungles ou motifs graphiques, nous assurons des raccords parfaits sur les plus grands formats.",
         "Nous réalisons aussi les claustras et tasseaux en bois, les panneaux acoustiques, les têtes de lit, les bardages en chêne et les parements en feuille de pierre, pour donner relief et chaleur à vos murs."],
  prestations=["Papiers peints panoramiques", "Papiers peints à motifs", "Claustras et tasseaux bois", "Panneaux acoustiques", "Bardage bois et têtes de lit", "Feuille de pierre et parements"],
  sources=[('finitions', None)]),
 dict(id='agencement', fichier='agencement-sur-mesure-aix-en-provence.html', court='Agencement & mobilier',
  h1='Agencement sur mesure & montage de mobilier', titre='Agencement sur mesure, rangements & montage de mobilier à Aix-en-Provence',
  meta="Rangements sur mesure, placards, bibliothèques, meubles maçonnés et montage de mobilier et de cuisines à Aix-en-Provence.",
  accroche="Des rangements pensés pour vos volumes, et un montage soigné de votre mobilier.",
  texte=["Chaque centimètre compte : nous concevons et réalisons des rangements qui s'intègrent à l'architecture de la pièce, placards toute hauteur, bibliothèques, niches et meubles maçonnés.",
         "Nous assurons aussi le montage et l'ajustement de votre mobilier et de vos cuisines, pour les particuliers comme pour les bureaux et commerces."],
  prestations=["Placards et dressings sur mesure", "Bibliothèques et niches intégrées", "Meubles maçonnés", "Montage de cuisines", "Montage et ajustement de mobilier", "Aménagement de bureaux et commerces"],
  sources=[('agencement', None), ('placo', 'Meubles & niches en placo')]),
 dict(id='plomberie', fichier='plomberie-electricite-aix-en-provence.html', court='Plomberie & électricité',
  h1='Plomberie & électricité', titre='Plomberie & électricité pour vos rénovations à Aix-en-Provence',
  meta="Plomberie et électricité dans le cadre de vos travaux de rénovation à Aix-en-Provence : réseaux encastrés, salles de bains, raccordements et appareillages.",
  accroche="Les réseaux d'eau et d'électricité préparés en même temps que vos finitions, par la même équipe.",
  texte=["Une rénovation de salle de bains, de cuisine ou de pièce de vie passe presque toujours par la plomberie et l'électricité. En les intégrant à notre intervention, nous évitons les allers-retours entre corps de métier et garantissons des réseaux bien placés avant la fermeture des cloisons.",
         "Alimentations et évacuations, bâti-supports, douches à l'italienne, prises, interrupteurs, éclairages encastrés ou rubans LED : tout est pensé avec l'aménagement final, puis raccordé une fois les finitions terminées."],
  prestations=["Alimentations et évacuations d'eau", "Salles de bains et douches à l'italienne", "Pose de WC suspendus et de meubles vasques", "Prises, interrupteurs et circuits", "Éclairages encastrés et LED", "Réseaux encastrés avant fermeture des cloisons"],
  sources=[('plomberie', None)]),
 dict(id='preparation', fichier='renovation-interieure-aix-en-provence.html', court='Rénovation complète',
  h1='Rénovation intérieure clé en main', titre="Rénovation intérieure clé en main à Aix-en-Provence — un seul interlocuteur",
  meta="Rénovation intérieure complète à Aix-en-Provence : démolition, préparation, placo, sols, peinture et décoration coordonnés par un seul interlocuteur.",
  accroche="De la démolition à la décoration, un seul interlocuteur coordonne tout votre chantier.",
  texte=["Une rénovation réussie repose sur une préparation sérieuse : dépose, curage, protection des lieux, puis un enchaînement maîtrisé des corps de métier. C'est exactement ce que nous prenons en charge.",
         "Placo, sols, peinture, béton ciré, zelliges, papiers peints, agencement : tous nos savoir-faire sont réunis dans un seul devis et un seul planning, pour un appartement, une villa ou un local professionnel."],
  prestations=["Démolition et curage", "Protection des lieux", "Coordination de tous les corps de métier", "Rénovation d'appartements et de villas", "Rénovation de locaux professionnels", "Suivi de chantier jusqu'à la réception"],
  sources=[('preparation', None)], projets=True),
]

esc = html.escape
STAGE = {'resultat': 'Résultat', 'chantier': 'En cours de chantier', 'avant': 'Avant', 'illustration': 'Illustration'}

def photos_for(svc):
    groupes = []
    for cid, grp in svc['sources']:
        ph = [p for p in CATS[cid]['photos'] if grp is None or p[4] == grp]
        for g in dict.fromkeys(p[4] for p in ph):
            groupes.append((g or CATS[cid]['title'], cid, [p for p in ph if p[4] == g]))
    return groupes

ent = open('entreprise.html', encoding='utf-8').read()
HEAD = ent[:ent.index('<section class="page-hero')]
FOOT = ent[ent.index('<footer>'):]
HEAD = HEAD.replace(' aria-current="page"', '')

def page(svc, idx):
    groupes = photos_for(svc)
    allp = [p for _, _, ph in groupes for p in ph]
    cover = CATS[svc['id']]['cover']
    url = f"{DOMAINE}/{svc['fichier']}"
    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": svc['titre'], "serviceType": svc['h1'],
       "description": svc['meta'], "areaServed": [{"@type": "City", "name": "Aix-en-Provence"}, {"@type": "AdministrativeArea", "name": "Provence-Alpes-Côte d'Azur"}],
       "provider": {"@type": "HomeAndConstructionBusiness", "name": "Trouillet Décors", "telephone": "+33625516784",
                    "email": "contact@trouilletdecors.fr", "url": DOMAINE + "/",
                    "address": {"@type": "PostalAddress", "addressLocality": "Aix-en-Provence", "postalCode": "13100", "addressCountry": "FR"}},
       "url": url},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOMAINE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Savoir-faire", "item": DOMAINE + "/realisations.html"},
        {"@type": "ListItem", "position": 3, "name": svc['court'], "item": url}]},
    ]
    head = HEAD
    head = re.sub(r'<title>.*?</title>', f"<title>{esc(svc['titre'])} — Trouillet Décors</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{esc(svc["meta"])}">\n<link rel="canonical" href="{url}">\n'
                  f'<meta property="og:title" content="{esc(svc["titre"])}">\n<meta property="og:description" content="{esc(svc["meta"])}">\n'
                  f'<meta property="og:image" content="{DOMAINE}/images/{svc["id"]}/full/{cover}">\n'
                  f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>', head)

    jump = ''.join(f'<a href="#g{k}" data-jump="g{k}">{esc(g)} <sup>{len(ph)}</sup></a>' for k, (g, _, ph) in enumerate(groupes))
    n_res = sum(1 for p in allp if p[5] == 'resultat'); n_ch = sum(1 for p in allp if p[5] == 'chantier'); n_ill = sum(1 for p in allp if p[5] == 'illustration')
    toggle = ('<div class="stage-toggle" role="group" aria-label="Afficher"><button class="on" data-stage="">Tout</button>'
              '<button data-stage="resultat">Résultats</button><button data-stage="chantier">En chantier</button></div>') if n_res and n_ch else ''
    gal = []
    for k, (g, cid, ph) in enumerate(groupes):
        figs = ''.join(
            f'<figure class="pc" data-full="images/{cid}/full/{p[0]}" data-stage="{p[5]}" data-stage-label="{STAGE[p[5]]}" style="--d:{i % 8}">'
            f'<div class="pc-img"><img src="images/{cid}/thumb/{p[0]}" alt="{esc(p[3])}" width="{p[1]}" height="{p[2]}" loading="lazy">'
            f'<span class="stage stage-{p[5]}">{STAGE[p[5]]}</span></div></figure>'
            for i, p in enumerate(ph))
        gal.append(f'''      <section class="sub" id="g{k}">
        <div class="wrap">
          <div class="sub-head"><span class="sub-n">{k+1:02d}</span><h3>{esc(g)}</h3><span class="sub-count">{len(ph)} photo{"s" if len(ph) > 1 else ""}</span></div>
          <div class="pgrid">{figs}</div>
        </div>
      </section>''')

    projets = ''
    if svc.get('projets'):
        projets = '''
<section class="svc-projects">
  <div class="wrap">
    <div class="sec-head"><div><span class="eyebrow rv">Projets complets</span><h2 class="rv d1">Nos rénovations <em class="gold">de A à Z.</em></h2></div>
    <p class="lead rv d2" style="max-width:420px">Cliquez sur un projet pour suivre le chantier en images.</p></div>
    <div class="projects" style="margin-top:0">
      <a href="realisations.html#projets" class="proj big" data-project="correns"><img src="images/correns/full/correns-06.jpg" alt="Maison à Correns après rénovation" loading="lazy"><div class="proj-txt"><small>Provence Verte</small><b>Maison à Correns</b><span>Avant / après</span></div></a>
      <a href="realisations.html#projets" class="proj" data-project="villa-saint-maximin"><img src="images/villa-saint-maximin/thumb/villa-saint-maximin-03.jpg" alt="Villa à Aix-en-Provence" loading="lazy"><div class="proj-txt"><small>Pays d'Aix</small><b>Villa à Aix-en-Provence</b><span>20 photos</span></div></a>
      <a href="realisations.html#projets" class="proj" data-project="eygalieres"><img src="images/eygalieres/thumb/eygalieres-10.jpg" alt="Villa à Eygalières" loading="lazy"><div class="proj-txt"><small>Alpilles</small><b>Villa à Eygalières</b><span>11 photos</span></div></a>
    </div>
  </div>
</section>'''

    autres = ''.join(
        f'<a href="{s["fichier"]}" class="svc-other"><img src="images/{s["id"]}/thumb/{CATS[s["id"]]["cover"]}" alt="" loading="lazy"><span>{esc(s["court"])}</span></a>'
        for s in SERVICES if s is not svc)
    prest = ''.join(f'<li>{esc(x)}</li>' for x in svc['prestations'])
    paras = ''.join(f'<p class="lead rv d2">{esc(t)}</p>' for t in svc['texte'])

    body = f'''<section class="page-hero svc-hero" style="--img:url('images/{svc["id"]}/full/{cover}')">
  <div class="bg"></div>
  <div class="wrap">
    <nav class="crumb rv" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> &nbsp;/&nbsp; <a href="realisations.html">Savoir-faire</a> &nbsp;/&nbsp; {esc(svc["court"])}</nav>
    <span class="eyebrow rv d1">Savoir-faire {idx:02d} · Aix-en-Provence</span>
    <h1 class="rv d1">{esc(svc["h1"])} <em class="gold">à Aix-en-Provence.</em></h1>
    <p class="rv d2">{esc(svc["accroche"])}</p>
    <div class="hero-ctas rv d3"><a href="index.html#contact" class="btn btn-gold">Demander un devis gratuit</a><a href="#galerie" class="btn btn-ghost">Voir nos réalisations</a></div>
  </div>
</section>

<section class="svc-intro">
  <div class="wrap">
    <div class="svc-grid">
      <div>
        <span class="eyebrow rv">Notre savoir-faire</span>
        <h2 class="rv d1">{esc(svc["court"])}, <em class="gold">dans les règles de l'art.</em></h2>
        {paras}
      </div>
      <aside class="svc-box rv d2">
        <h3>Nos prestations</h3>
        <ul class="check">{prest}</ul>
        <p class="svc-zone"><b>Zone d'intervention</b>{VILLES} et alentours.</p>
        <a href="index.html#contact" class="btn btn-gold">Demander un devis</a>
      </aside>
    </div>
  </div>
</section>

<div class="svc-gallery" id="galerie">
  <section class="cat-intro">
    <div class="wrap">
      <div class="cat-intro-grid">
        <div><span class="eyebrow">Réalisations</span><h2>Nos chantiers en images</h2><p class="lead">Cliquez sur une photo pour l'agrandir.</p></div>
        <ul class="cat-stats"><li><b class="gold">{len(allp)}</b><span>Photos</span></li>{"<li><b class='gold'>%d</b><span>Résultats</span></li>" % n_res if n_res else ""}{"<li><b class='gold'>%d</b><span>En chantier</span></li>" % n_ch if n_ch else ""}{"<li><b class='gold'>%d</b><span>Illustrations</span></li>" % n_ill if n_ill else ""}</ul>
      </div>
      <div class="cat-tools"{"" if (len(groupes) > 1 or toggle) else " hidden"}>{"<div class='jump'><small>Rubriques</small>" + jump + "</div>" if len(groupes) > 1 else ""}{toggle}</div>
    </div>
  </section>
{chr(10).join(gal)}
</div>
{projets}
<section class="garanties" id="garanties" hidden></section>
<section class="svc-more">
  <div class="wrap">
    <span class="eyebrow rv">Un seul interlocuteur</span>
    <h2 class="rv d1">Tous nos <em class="gold">savoir-faire.</em></h2>
    <div class="svc-others rv d2">{autres}</div>
  </div>
</section>

<section class="empty-cta">
  <div class="wrap">
    <span class="eyebrow rv">Votre projet</span>
    <h2 class="rv d1">Un projet de {esc(svc["court"].lower())} ?<br><em class="gold">Parlons-en.</em></h2>
    <a href="index.html#contact" class="btn btn-gold rv d2">Demander un devis gratuit</a>
  </div>
</section>

'''
    foot = FOOT
    if svc.get('projets') and 'photos.js' not in foot:
        foot = foot.replace('<script src="site.js', '<script src="photos.js?v=1"></script>\n<script src="site.js', 1)
    return head + body + foot

for i, s in enumerate(SERVICES, 1):
    open(s['fichier'], 'w', encoding='utf-8').write(page(s, i))

# Correspondance catégorie -> page, utilisée par le site
open('pages.js', 'w', encoding='utf-8').write('// Généré par tools/generer-pages.py\nwindow.PAGES=' + json.dumps({s['id']: s['fichier'] for s in SERVICES}) + ';\n')

# sitemap.xml + robots.txt
urls = ['', 'entreprise.html', 'realisations.html'] + [s['fichier'] for s in SERVICES] + ['mentions-legales.html']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{DOMAINE}/{u}</loc></url>\n' for u in urls) + '</urlset>\n'
open('sitemap.xml', 'w').write(sm)
open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAINE}/sitemap.xml\n')
print(len(SERVICES), 'pages générées + sitemap.xml + robots.txt')
