"""Validate local deck links and all Sejong lesson audio references before deployment."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
decks=json.loads((root/'data/decks.json').read_text())
assert len({d['id'] for d in decks})==len(decks)
for d in decks:
 assert (root/d['href']).is_file(),d['href']
 page=(root/d['href']).read_text()
 assert 'class="icon-btn home-button" href="index.html" aria-label="返回首页"' in page, 'Missing standard home link: '+d['href']
total_cards=0
for deck in decks:
 if not deck['id'].startswith('sejong1-lesson'):
  continue
 data_path=root/'data'/Path(deck['href']).with_suffix('.json').name
 cards=json.loads(data_path.read_text())
 assert cards and len({c['id'] for c in cards})==len(cards),data_path
 for c in cards:
  assert c['audio_kind'] in ['human','synth']
  assert (root/c['audio']).stat().st_size>1000,c['audio']
  assert c['front'] and c['meaning'] and c['explanation']
 total_cards+=len(cards)
print(f'PASS: {len(decks)} deck links; {total_cards} complete Sejong cards and audio files')
