import random
from matchlab.controls import controls

def cases():
 ps=[c['input']for c in controls()];r=random.Random(873091)
 for n in range(1,6):
  for _ in range(12):ps.append(dict(version=1,n=n,a=[r.sample(range(n),n)for i in range(n)],b=[r.sample(range(n),n)for i in range(n)],cost=[[r.randrange(-20,21)for j in range(n)]for i in range(n)]))
 return ps
