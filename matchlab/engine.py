"""Classical deferred acceptance, complete finite census and stable lattice evidence."""
from itertools import permutations
from .model import parse

def analyze(p):
 n=parse(p);ids=list(range(n));ranks={k:[{x:j for j,x in enumerate(row)}for row in p[k]]for k in ['a','b']};ar,br=ranks['a'],ranks['b']
 def inv(m):return[m.index(j)for j in ids]
 def da(side):
  other='b'if side=='a'else'a';pref=p[side];rr=ranks[other];held=[None]*n;nexts=[0]*n;trace=[]
  while len([x for x in held if x is not None])<n:
   free=[x for x in ids if x not in held];i=free[0];j=pref[i][nexts[i]];nexts[i]+=1;old=held[j];accept=old is None or rr[j][i]<rr[j][old];rejected=old if accept else i
   if accept:held[j]=i
   partial=[None]*n
   for receiver,proposer in enumerate(held):
    if proposer is not None:partial[proposer if side=='a'else receiver]=receiver if side=='a'else proposer
   trace.append(dict(step=len(trace),proposer=i,receiver=j,previous=old,accepted=accept,rejected=rejected,held=held[:],next=nexts[:],free=[x for x in ids if x not in held],partial=partial))
  m=inv(held)if side=='a'else held[:]
  return dict(side=side,matching=m,trace=trace)
 rows=[]
 for idx,perm in enumerate(permutations(ids)):
  m=list(perm);back=inv(m);pairs=[]
  for a in ids:
   for b in ids:
    ap=ar[a][b]<ar[a][m[a]];bp=br[b][a]<br[b][back[b]];pairs.append(dict(a=a,b=b,matched=m[a]==b,a_partner=m[a],b_partner=back[b],a_rank=ar[a][b],a_current=ar[a][m[a]],b_rank=br[b][a],b_current=br[b][back[b]],a_prefers=ap,b_prefers=bp,blocks=ap and bp))
  blockers=[[x['a'],x['b']]for x in pairs if x['blocks']];ra=[ar[a][m[a]]for a in ids];rb=[br[b][back[b]]for b in ids];rows.append(dict(id=idx,matching=m,inverse=back,a_ranks=ra,b_ranks=rb,a_rank_sum=sum(ra),b_rank_sum=sum(rb),rank_sum=sum(ra)+sum(rb),worst_rank=max(ra+rb),cost=sum(p['cost'][a][m[a]]for a in ids),blocking=blockers,stable=not blockers,pairs=pairs))
 lookup={tuple(x['matching']):x['id']for x in rows};stable=[x for x in rows if x['stable']];sids=[x['id']for x in stable]
 # A-oriented order: x >= y iff every A participant weakly prefers x.
 def above(x,y):return all(a<=b for a,b in zip(x['a_ranks'],y['a_ranks']))
 operations=[];covers=[]
 for x in stable:
  for y in stable:
   join=[min([x['matching'][a],y['matching'][a]],key=lambda b:ar[a][b])for a in ids];meet=[max([x['matching'][a],y['matching'][a]],key=lambda b:ar[a][b])for a in ids];j=lookup[tuple(join)];k=lookup[tuple(meet)];assert j in sids and k in sids
   operations.append(dict(x=x['id'],y=y['id'],a_dominates=above(x,y),join=j,meet=k,join_matching=join,meet_matching=meet))
   if x['id']!=y['id']and above(x,y)and not any(z['id']not in[x['id'],y['id']]and above(x,z)and above(z,y)for z in stable):covers.append([x['id'],y['id']])
 attainable={side:[[j for j in p[side][i]if any((z['matching'][i]if side=='a'else z['inverse'][i])==j for z in stable)]for i in ids]for side in ['a','b']}
 minimum=min(z['cost']for z in rows);stable_min=min(z['cost']for z in stable);frontier=[z['id']for z in rows if not any(len(y['blocking'])<=len(z['blocking'])and y['cost']<=z['cost']and(len(y['blocking'])<len(z['blocking'])or y['cost']<z['cost'])for y in rows)]
 caps=[]
 for cap in range(n*(n-1)+1):
  eligible=[z for z in rows if len(z['blocking'])<=cap];v=min(z['cost']for z in eligible);caps.append(dict(cap=cap,cost=v,matchings=[z['id']for z in eligible if z['cost']==v]))
 return dict(version=1,kind='matchlab-stable',input=p,matchings=rows,stable=sids,a_proposing=da('a'),b_proposing=da('b'),attainable=attainable,lattice=dict(orientation='A-prefers-greater',operations=operations,covers=covers),unconstrained_cost=minimum,unconstrained_minima=[z['id']for z in rows if z['cost']==minimum],stable_cost=stable_min,stable_minima=[z['id']for z in stable if z['cost']==stable_min],stability_premium=stable_min-minimum,frontier=frontier,blocking_caps=caps)
