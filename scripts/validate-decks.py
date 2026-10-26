"""Validate local deck links and all first-lesson audio references before deployment."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
decks=json.loads((root/'data/decks.json').read_text())
assert len({d['id'] for d in decks})==len(decks)
for d in decks:assert (root/d['href']).is_file(),d['href']
cards=json.loads((root/'data/sejong-lesson1.json').read_text())
assert len(cards)==48 and len({c['id'] for c in cards})==48
for c in cards:
 assert c['audio_kind'] in ['human','synth']
 assert (root/c['audio']).stat().st_size>1000,c['audio']
 assert c['front'] and c['meaning'] and c['explanation']
print(f'PASS: {len(decks)} deck links; {len(cards)} complete cards and audio files')
