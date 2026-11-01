"""Validate the isolated public demo library, referenced media and downloads."""
from pathlib import Path
import json,re,zipfile
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]/'demos'
entries=json.loads((root/'manifest.json').read_text());assert len(entries)==4
assert len({x['id'] for x in entries})==4
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key=='href' and value and not value.startswith(('https:','http:','#','mailto:')):assert (root/value).is_file(),value
p=Links();p.feed((root/'index.html').read_text())
for e in entries:
 page=(root/e['href']).read_text();d=json.loads((root/'data'/e['id']/'cards.json').read_text())
 assert len(d['cards'])==3 and d['header']['languages']==e['languages']
 assert d['home_href']=='index.html' and 'id="languagePair"' in page
 assert page.count('id="scriptNotice"')==1
 assert len({c['id'] for c in d['cards']})==3
 for c in d['cards']:assert (root/c['audio']).stat().st_size>1000,c['audio']
 for key in ['content','sources','download','anki']:assert (root/e[key]).is_file()
 with zipfile.ZipFile(root/e['download']) as z:
  assert {'index.html','library.html','cards.json','content.md','sources.md','report.md'}<=set(z.namelist())
  assert json.loads(z.read('cards.json'))['home_href']=='library.html'
  assert len([n for n in z.namelist() if n.endswith('.mp3')])==3
 with zipfile.ZipFile(root/e['anki']) as z:
  assert 'notes.tsv' in z.namelist() and len([n for n in z.namelist() if n.startswith('media/')])==3
 for file in (root/'data'/e['id']).glob('*'):
  assert not re.search(r'/Users/|/private/var/|/var/folders/',file.read_text()),file
print('PASS: four separate demos, 12 audio cards, three-line headers, home links, HTML/Anki bundles and no personal filesystem paths')
