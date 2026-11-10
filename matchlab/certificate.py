"""Exhaustive independent matching replay. Imports only input validation, not solver."""
from itertools import permutations
from .model import parse,keys

def verify(r):
 try:
  keys(r,['version','kind','input','matchings','stable','a_proposing','b_proposing','attainable','lattice','unconstrained_cost','unconstrained_minima','stable_cost','stable_minima','stability_premium','frontier','blocking_caps'])
  n=parse(r['input']);p=r['input'];ids=list(range(n))
  def eq(a,b):
   if type(a)is not type(b):raise ValueError('wrong evidence type')
   if type(b)is dict:
    keys(a,b)
    for k in b:eq(a[k],b[k])
   elif type(b)is list:
    if len(a)!=len(b):raise ValueError('evidence length')
    for x,y in zip(a,b):eq(x,y)
   elif a!=b:raise ValueError('evidence mismatch')
  eq(r['version'],1);eq(r['kind'],'matchlab-stable');rows=[]
  for idx,m in enumerate(permutations(ids)):
   inverse=[m.index(b)for b in ids];pair=[];blocked=[]
   for a in ids:
    for b in ids:
     aa=p['a'][a].index(b);ac=p['a'][a].index(m[a]);bb=p['b'][b].index(a);bc=p['b'][b].index(inverse[b]);ap=aa<ac;bp=bb<bc;pair.append(dict(a=a,b=b,matched=m[a]==b,a_partner=m[a],b_partner=inverse[b],a_rank=aa,a_current=ac,b_rank=bb,b_current=bc,a_prefers=ap,b_prefers=bp,blocks=ap and bp))
     if ap and bp:blocked.append([a,b])
   ra=[p['a'][a].index(m[a])for a in ids];rb=[p['b'][b].index(inverse[b])for b in ids];rows.append(dict(id=idx,matching=list(m),inverse=inverse,a_ranks=ra,b_ranks=rb,a_rank_sum=sum(ra),b_rank_sum=sum(rb),rank_sum=sum(ra)+sum(rb),worst_rank=max(ra+rb),cost=sum(p['cost'][a][m[a]]for a in ids),blocking=blocked,stable=not blocked,pairs=pair))
  eq(r['matchings'],rows);stable=[z for z in rows if not z['blocking']];eq(r['stable'],[z['id']for z in stable]);assert stable
  # Validate supplied sequential proposal log, independently tracking each proposer.
  for side in ['a','b']:
   d=r[side+'_proposing'];eq(d['side'],side);keys(d,['side','matching','trace']);other='b'if side=='a'else'a';partners=[None]*n;held=[None]*n;cursor=[0]*n;expected=[]
   while None in partners:
    who=partners.index(None);to=p[side][who][cursor[who]];cursor[who]+=1;prev=held[to];accept=prev is None or p[other][to].index(who)<p[other][to].index(prev)
    if accept:
     if prev is not None:partners[prev]=None
     held[to]=who;partners[who]=to
    partial=partners[:]if side=='a'else held[:];expected.append(dict(step=len(expected),proposer=who,receiver=to,previous=prev,accepted=accept,rejected=prev if accept else who,held=held[:],next=cursor[:],free=[i for i in ids if partners[i]is None],partial=partial))
   eq(d['trace'],expected);m=partners if side=='a'else held;eq(d['matching'],m)
   # Extremum checked from full family, not accepted merely because the trace passes.
   for i in ids:
    partner=m[i]if side=='a'else m.index(i);best=min(p[side][i].index(z['matching'][i]if side=='a'else z['inverse'][i])for z in stable);eq(p[side][i].index(partner),best)
  attainable={side:[[v for v in p[side][i]if any((z['matching'][i]if side=='a'else z['inverse'][i])==v for z in stable)]for i in ids]for side in ['a','b']};eq(r['attainable'],attainable)
  # Compute lattice bounds by dominance across the whole stable family, not coordinate selection.
  def ge(x,y):return all(p['a'][a].index(x['matching'][a])<=p['a'][a].index(y['matching'][a])for a in ids)
  ops=[];covers=[]
  for x in stable:
   for y in stable:
    upper=[z for z in stable if ge(z,x)and ge(z,y)];lower=[z for z in stable if ge(x,z)and ge(y,z)];joins=[z for z in upper if all(ge(w,z)for w in upper)];meets=[z for z in lower if all(ge(z,w)for w in lower)];assert len(joins)==len(meets)==1;j,k=joins[0],meets[0];ops.append(dict(x=x['id'],y=y['id'],a_dominates=ge(x,y),join=j['id'],meet=k['id'],join_matching=j['matching'],meet_matching=k['matching']))
    if x['id']!=y['id']and ge(x,y)and not any(z['id']not in[x['id'],y['id']]and ge(x,z)and ge(z,y)for z in stable):covers.append([x['id'],y['id']])
  eq(r['lattice'],dict(orientation='A-prefers-greater',operations=ops,covers=covers))
  low=min(z['cost']for z in rows);sv=min(z['cost']for z in stable);eq(r['unconstrained_cost'],low);eq(r['unconstrained_minima'],[z['id']for z in rows if z['cost']==low]);eq(r['stable_cost'],sv);eq(r['stable_minima'],[z['id']for z in stable if z['cost']==sv]);eq(r['stability_premium'],sv-low)
  fronts=[]
  for z in rows:
   dominated=False
   for y in rows:
    a,b=len(y['blocking']),len(z['blocking'])
    if a<=b and y['cost']<=z['cost']and(a<b or y['cost']<z['cost']):dominated=True
   if not dominated:fronts.append(z['id'])
  eq(r['frontier'],fronts);caps=[]
  for k in range(n*(n-1)+1):
   costs=[(z['cost'],z['id'])for z in rows if len(z['blocking'])<=k];v=min(c for c,i in costs);caps.append(dict(cap=k,cost=v,matchings=[i for c,i in costs if c==v]))
  eq(r['blocking_caps'],caps);return True
 except(KeyError,TypeError,IndexError,OverflowError,AssertionError)as e:raise ValueError('malformed report')from e
