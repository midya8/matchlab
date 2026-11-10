"""Optional input-built HiGHS assignment/stable-assignment integer reference."""
import json,sys
from pathlib import Path
import scipy,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from matchlab import analyze
from cases import cases
solves=0;constraints=0;worst=0.
for p in cases():
 n=p['n'];r=analyze(p);c=np.array([p['cost'][a][b]for a in range(n)for b in range(n)],dtype=float);rows=[];lo=[];hi=[]
 for side in [0,1]:
  for i in range(n):rows.append([float((a if side==0 else b)==i)for a in range(n)for b in range(n)]);lo.append(1.);hi.append(1.)
 for stable in [False,True]:
  aa=rows[:];ll=lo[:];hh=hi[:]
  if stable:
   for a in range(n):
    for b in range(n):
     # Pair is matched, or at least one member receives a strictly preferred partner.
     row=[0.]*(n*n);row[a*n+b]=1.
     for j in p['a'][a][:p['a'][a].index(b)]:row[a*n+j]=1.
     for i in p['b'][b][:p['b'][b].index(a)]:row[i*n+b]=1.
     aa.append(row);ll.append(1.);hh.append(np.inf)
  z=milp(c,integrality=np.ones(n*n),bounds=Bounds(np.zeros(n*n),np.ones(n*n)),constraints=LinearConstraint(np.array(aa),ll,hh),options={'mip_rel_gap':0.});assert z.success,z.message;target=r['stable_cost']if stable else r['unconstrained_cost'];err=abs(z.fun-target);worst=max(worst,err);assert err<=1e-8;xx=np.rint(z.x).astype(int).reshape(n,n);assert np.max(np.abs(z.x-xx.ravel()))<=1e-8;assert all(xx.sum(axis=0)==1)and all(xx.sum(axis=1)==1);m=xx.argmax(axis=1).tolist();score=sum(p['cost'][i][m[i]]for i in range(n));assert score==target
  if stable:
   inv=[m.index(j)for j in range(n)]
   for a in range(n):
    for b in range(n):assert not(p['a'][a].index(b)<p['a'][a].index(m[a])and p['b'][b].index(a)<p['b'][b].index(inv[b]))
  solves+=1;constraints+=len(aa)
print(json.dumps(dict(scipy=scipy.__version__,profiles=len(cases()),integer_solves=solves,constraint_rows=constraints,worst_abs_error=worst,tolerance=1e-8)))
