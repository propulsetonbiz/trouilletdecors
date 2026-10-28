#!/usr/bin/env python3
"""Régénère photos.js à partir du dossier images/ (à relancer après ajout de photos).
Chaque catégorie = un dossier images/<id>/ contenant thumb/ (≈700px) et full/ (≈1800px)."""
import os, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'images')

# (id, titre, description, photo de couverture)
CATEGORIES = [
  ("peinture",    "Peinture intérieure", "Peinture des murs et plafonds, mises en teinte, boiseries et plinthes, pour des intérieurs lumineux et impeccables.", "peinture-05.jpg"),
  ("placo",       "Placo & meubles en placo", "Cloisons, doublages, faux-plafonds, niches, bibliothèques et meubles maçonnés en plaques de plâtre.", "placo-14.jpg"),
  ("patines",     "Patines à la chaux & béton ciré", "Enduits à la chaux, patines et béton ciré : des murs et des sols minéraux, doux et sans joint.", "patines-04.jpg"),
  ("zelliges",    "Zelliges & carrelage décoratif", "Zelliges, carreaux ciment et panneaux de carrelage décoratif pour salles de bains, cuisines et crédences.", "zelliges-07.jpg"),
  ("sols",        "Sols : carrelage, parquet, LVT & moquette", "Carrelage grand format, parquet, lames LVT, moquette, habillage d'escaliers : tous vos revêtements de sol.", "sols-05.jpg"),
  ("finitions",   "Finitions décoratives", "Papiers peints panoramiques, claustras, panneaux acoustiques, bardages bois et feuille de pierre.", "finitions-40.jpg"),
  ("agencement",  "Agencement & montage de mobilier", "Rangements sur mesure, dressings, montage et ajustement de mobilier et de cuisines.", "agencement-01.jpg"),
  ("plomberie",   "Plomberie & électricité", "Réseaux d'eau et d'électricité encastrés, raccordements et appareillages, réalisés en même temps que vos travaux.", "plomberie-02.jpg"),
  ("preparation", "Préparation de chantier", "Démolition, curage et protection soignée des lieux avant le démarrage des travaux.", "preparation-01.jpg"),
]
PROJECTS = [
  ("eygalieres",          "Villa à Eygalières",            "Alpilles",               "Enduits à la chaux, escalier sculpté, ambiance minérale."),
  ("correns",             "Maison contemporaine à Correns", "Provence Verte",         "Rénovation de la pièce de vie : avant, pendant et après les travaux."),
  ("villa-saint-maximin", "Villa à Aix-en-Provence",        "Aix-en-Provence", "Rénovation complète, du gros œuvre de finition à la décoration."),
  ("airbnb-provence",     "Location saisonnière",          "Provence",               "Rénovation d'un logement destiné à la location courte durée."),
]

LEGENDES = json.load(open(os.path.join(ROOT, 'tools', 'legendes.json'), encoding='utf-8'))

ORDRE_CHANTIER = {'avant': 0, 'chantier': 1, 'resultat': 2, 'illustration': 3}

def scan(folder, chronologique=False):
    d = os.path.join(IMG, folder, 'thumb')
    files = sorted(f for f in os.listdir(d) if f.lower().endswith('.jpg'))
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight'] + [os.path.join(d, f) for f in files],
                         capture_output=True, text=True).stdout
    dims, cur = [], None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('pixelWidth'): cur = [int(line.split(': ')[1])]
        elif line.startswith('pixelHeight'): cur.append(int(line.split(': ')[1])); dims.append(cur)
    photos = []
    for f, (w, h) in zip(files, dims):
        groupe, legende, etape = LEGENDES.get(f, ["", "", "resultat"])
        if etape == 'masque':  # photo retirée du site
            continue
        photos.append([f, w, h, legende, groupe, etape])
    # Regroupe par sous-rubrique (ordre d'apparition), réalisations terminées en premier
    ordre = list(dict.fromkeys(p[4] for p in photos))
    if chronologique:  # projets : avant -> pendant -> après
        photos.sort(key=lambda p: ORDRE_CHANTIER.get(p[5], 2))
    else:              # catégories : par rubrique, réalisations terminées d'abord
        photos.sort(key=lambda p: (ordre.index(p[4]), {'resultat': 0, 'illustration': 1}.get(p[5], 2)))
    return photos

data = {
  "categories": [dict(id=i, title=t, desc=s, cover=c, photos=scan(i)) for i, t, s, c in CATEGORIES],
  "projects":   [dict(id=i, title=t, place=p, desc=s, photos=scan(i, chronologique=True)) for i, t, p, s in PROJECTS],
}
with open(os.path.join(ROOT, 'photos.js'), 'w') as fh:
    fh.write('// Fichier généré par tools/generer-photos.py — ne pas modifier à la main\n')
    fh.write('window.PHOTOS = ' + json.dumps(data, ensure_ascii=False) + ';\n')
sans = [p[0] for c in data['categories'] + data['projects'] for p in c['photos'] if not p[3]]
if sans: print('Photos sans légende :', ', '.join(sans))
print(sum(len(c['photos']) for c in data['categories']), 'photos en catégories,',
      sum(len(p['photos']) for p in data['projects']), 'photos de projets')
