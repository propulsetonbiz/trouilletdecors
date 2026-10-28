#!/usr/bin/env python3
"""Ajoute des photos à une catégorie du site, puis met tout à jour.

Exemples :
  python3 tools/ajouter-photos.py peinture ~/Downloads/salon-beige.jpg --ia --rubrique "Murs & plafonds" --legende "Séjour vide repeint en beige"
  python3 tools/ajouter-photos.py plomberie ~/Downloads/a.jpg ~/Downloads/b.jpg --etape resultat --rubrique "Plomberie"

--ia : image générée par intelligence artificielle -> affichée avec l'étiquette « Illustration »
       (pour ne pas la présenter comme un chantier réel).
Catégories : peinture, placo, patines, zelliges, sols, finitions, agencement, plomberie, preparation
"""
import argparse, json, os, re, subprocess, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ap = argparse.ArgumentParser()
ap.add_argument('categorie')
ap.add_argument('fichiers', nargs='+')
ap.add_argument('--ia', action='store_true', help="image générée par IA (étiquette « Illustration »)")
ap.add_argument('--etape', default='resultat', choices=['resultat', 'chantier', 'avant'])
ap.add_argument('--rubrique', default='')
ap.add_argument('--legende', default='', help="description de la photo (texte alternatif, lu par Google)")
a = ap.parse_args()

dossier = f'images/{a.categorie}'
if not os.path.isdir(dossier):
    raise SystemExit(f"Catégorie inconnue : {a.categorie}")
leg = json.load(open('tools/legendes.json', encoding='utf-8'))
existants = [int(m.group(1)) for f in os.listdir(f'{dossier}/full') if (m := re.match(rf'{a.categorie}-(\d+)\.jpg$', f))]
n = max(existants, default=0)

def taille(f):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', f], capture_output=True, text=True).stdout
    return max(int(x) for x in re.findall(r': (\d+)', out))

for src in a.fichiers:
    src = os.path.expanduser(src)
    n += 1
    nom = f'{a.categorie}-{n:02d}.jpg'
    m = taille(src)
    for sous, maxi, q in (('full', 1600, 78), ('thumb', 700, 70)):
        cmd = ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(q)]
        if m > maxi:
            cmd += ['-Z', str(maxi)]  # réduit seulement, n'agrandit jamais
        subprocess.run(cmd + [src, '--out', f'{dossier}/{sous}/{nom}'], capture_output=True, check=True)
    leg[nom] = [a.rubrique, a.legende, 'illustration' if a.ia else a.etape]
    print('ajoutée :', nom)

json.dump(leg, open('tools/legendes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
subprocess.run(['python3', 'tools/generer-photos.py'], check=True)
subprocess.run(['python3', 'tools/generer-pages.py'], check=True)

# Nouveau numéro de version pour que les navigateurs rechargent les fichiers
v = time.strftime('%Y%m%d%H%M')
for f in os.listdir('.'):
    if f.endswith('.html'):
        s = open(f, encoding='utf-8').read()
        open(f, 'w', encoding='utf-8').write(re.sub(r'\?v=\w+"', f'?v={v}"', s))
print('Site mis à jour.')
