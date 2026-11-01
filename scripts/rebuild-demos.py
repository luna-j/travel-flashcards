"""Re-render all demo cards from checked-in JSON/media using a local skill checkout."""
import argparse,copy,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skill',type=Path,required=True);a=p.parse_args();skill=a.skill.resolve();root=Path(__file__).resolve().parents[1]/'demos'
assert (skill/'scripts/deck.py').is_file(),'Provide a scene-audio-flashcards checkout'
for entry in json.loads((root/'manifest.json').read_text()):
 data=root/'data'/entry['id'];deck=json.loads((data/'cards.json').read_text())
 with tempfile.TemporaryDirectory() as temp:
  out=Path(temp)/'render';out.mkdir()
  for c in deck['cards']:
   to=out/c['audio'];to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/c['audio'],to)
  def build(d):
   (out/'input.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
   subprocess.run([sys.executable,str(skill/'scripts/deck.py'),'build',str(out/'input.json'),'--out',str(out)],check=True)
  build(deck);shutil.copy2(out/'index.html',root/entry['href'])
  for name in ['cards.json','content.md','sources.md','report.md']:shutil.copy2(out/name,data/name)
  portable=copy.deepcopy(deck);portable['home_href']='library.html';build(portable)
  with zipfile.ZipFile(root/entry['download'],'w',zipfile.ZIP_DEFLATED) as z:
   for name in ['index.html','library.html','cards.json','content.md','sources.md','report.md']+[c['audio'] for c in deck['cards']]:z.write(out/name,name)
  anki=Path(temp)/'anki';subprocess.run([sys.executable,str(skill/'scripts/anki_export.py'),str(out),'--out',str(anki)],check=True)
  with zipfile.ZipFile(root/entry['anki'],'w',zipfile.ZIP_DEFLATED) as z:
   for f in sorted(anki.rglob('*')):
    if f.is_file():z.write(f,f.relative_to(anki))
print('Rebuilt demo pages, study/source documents and HTML/Anki downloads.')
