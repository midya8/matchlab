"""Guard source controls, examples, static references and publication inputs."""
import json,sys
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from matchlab.controls import controls
root=Path(__file__).resolve().parents[1];cs=controls();assert json.loads((root/'docs/controls.json').read_text())==cs
for c in cs:assert json.loads((root/'examples'/f"{c['id']}.json").read_text())==c['input']
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.refs=[]
 def handle_starttag(self,t,attrs):
  attrs=dict(attrs)
  if 'id'in attrs:assert attrs['id']not in self.ids;self.ids.add(attrs['id'])
  for k in ['src','href']:
   v=attrs.get(k,'')
   if v and not v.startswith(('https:','#')):self.refs.append(v)
p=Parse();p.feed((root/'docs/index.html').read_text())
for v in p.refs:assert(root/'docs'/v).is_file()
assert p.ids=={'control','input','input-help','run','export','status','output'}
for name in ['README.md','METHOD.md','SOURCES.md','LICENSE','pyproject.toml']:assert(root/name).stat().st_size>0
print(json.dumps(dict(controls=len(cs),examples=len(cs),static_references=len(p.refs),html_ids=len(p.ids))))
