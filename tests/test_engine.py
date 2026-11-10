import copy,itertools,json,random,subprocess,sys,unittest,tempfile
from pathlib import Path
from matchlab import analyze,verify
from matchlab.controls import controls
from matchlab.model import parse,loads
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from cases import cases
class Tests(unittest.TestCase):
 def test_complete_profiles(self):
  rs=[analyze(p)for p in cases()]
  for r in rs:self.assertTrue(verify(r))
  print('REPORTS',len(rs),'MATCHINGS',sum(len(r['matchings'])for r in rs),'PAIR_WITNESSES',sum(len(z['pairs'])for r in rs for z in r['matchings']),'STABLE',sum(len(r['stable'])for r in rs),'OPERATIONS',sum(len(r['lattice']['operations'])for r in rs),'PROPOSALS',sum(len(r[s+'_proposing']['trace'])for r in rs for s in ['a','b']))
 def test_default_separation(self):
  r=analyze(controls()[0]['input']);self.assertEqual(r['stable'],[1,2,4]);self.assertEqual(r['stable_minima'],[4]);self.assertEqual(r['stable_cost'],13);self.assertEqual(r['unconstrained_cost'],3);self.assertEqual(r['stability_premium'],10);self.assertEqual(r['matchings'][3]['blocking'],[[2,1]]);self.assertEqual(r['a_proposing']['matching'],[1,0,2]);self.assertEqual(r['b_proposing']['matching'],[0,2,1]);self.assertEqual(r['lattice']['covers'],[[2,4],[4,1]])
 def test_diamond_not_total_order(self):
  r=analyze(controls()[1]['input']);self.assertEqual(len(r['stable']),4);self.assertEqual(len(r['lattice']['covers']),4);ops=r['lattice']['operations'];self.assertTrue(any(not z['a_dominates']and not next(t for t in ops if(t['x'],t['y'])==(z['y'],z['x']))['a_dominates']for z in ops))
 def test_singleton(self):
  r=analyze(controls()[3]['input']);self.assertEqual(r['stable'],[0]);self.assertEqual(r['stability_premium'],0);self.assertEqual(r['blocking_caps'],[dict(cap=0,cost=-7,matchings=[0])]);self.assertTrue(verify(r))
 def test_all_two_by_two_preferences(self):
  orders=list(itertools.permutations(range(2)));count=0
  for rows in itertools.product(orders,repeat=4):
   p=dict(version=1,n=2,a=[list(x)for x in rows[:2]],b=[list(x)for x in rows[2:]],cost=[[3,-2],[1,0]]);self.assertTrue(verify(analyze(p)));count+=1
  self.assertEqual(count,16)
 def test_no_repeat_proposals(self):
  for c in controls():
   r=analyze(c['input']);n=c['input']['n']
   for s in ['a','b']:
    pairs=[(z['proposer'],z['receiver'])for z in r[s+'_proposing']['trace']];self.assertEqual(len(set(pairs)),len(pairs));self.assertLessEqual(len(pairs),n*n)
 def test_receivers_only_improve(self):
  for c in controls():
   r=analyze(c['input'])
   for side,other in [('a','b'),('b','a')]:
    for z in r[side+'_proposing']['trace']:
     if z['accepted']and z['previous']is not None:self.assertLess(c['input'][other][z['receiver']].index(z['proposer']),c['input'][other][z['receiver']].index(z['previous']))
 def test_alternative_proposal_schedules(self):
  rng=random.Random(41)
  for c in controls():
   p=c['input'];n=p['n'];r=analyze(p)
   for side,other in [('a','b'),('b','a')]:
    for _ in range(6):
     held=[None]*n;cursor=[0]*n
     while None in held:
      i=rng.choice([x for x in range(n)if x not in held]);j=p[side][i][cursor[i]];cursor[i]+=1
      if held[j]is None or p[other][j].index(i)<p[other][j].index(held[j]):held[j]=i
     m=[held.index(i)for i in range(n)]if side=='a'else held
     self.assertEqual(m,r[side+'_proposing']['matching'])
 def test_lattice_laws(self):
  for c in controls():
   r=analyze(c['input']);op={(z['x'],z['y']):z for z in r['lattice']['operations']}
   for x,y,z in itertools.product(r['stable'],repeat=3):
    for key in ['join','meet']:
     self.assertEqual(op[x,y][key],op[y,x][key]);self.assertEqual(op[op[x,y][key],z][key],op[x,op[y,z][key]][key])
    self.assertEqual(op[x,op[x,y]['meet']]['join'],x);self.assertEqual(op[x,op[x,y]['join']]['meet'],x)
 def test_opposite_side_order(self):
  for c in controls():
   r=analyze(c['input'])
   for z in r['lattice']['operations']:
    x,y=r['matchings'][z['x']],r['matchings'][z['y']];self.assertEqual(z['a_dominates'],all(a>=b for a,b in zip(x['b_ranks'],y['b_ranks'])))
 def test_side_reversal(self):
  for c in controls():
   p=copy.deepcopy(c['input']);r=analyze(p);p['a'],p['b']=p['b'],p['a'];p['cost']=[list(z)for z in zip(*p['cost'])];s=analyze(p);self.assertTrue(verify(s));self.assertEqual(r['stable_cost'],s['stable_cost']);self.assertEqual(sorted([r['matchings'][i]['inverse']for i in r['stable']]),[s['matchings'][i]['matching']for i in s['stable']]);self.assertEqual(r['stability_premium'],s['stability_premium'])
 def test_agent_relabeling(self):
  for c in controls():
   p=copy.deepcopy(c['input']);n=p['n'];r=analyze(p);f=lambda i:n-1-i;p['a']=[[f(j)for j in c['input']['a'][f(i)]]for i in range(n)];p['b']=[[f(j)for j in c['input']['b'][f(i)]]for i in range(n)];p['cost']=[[c['input']['cost'][f(i)][f(j)]for j in range(n)]for i in range(n)];z=analyze(p);self.assertTrue(verify(z));self.assertEqual(z['stable_cost'],r['stable_cost']);self.assertEqual(z['stability_premium'],r['stability_premium'])
 def test_cost_shift_and_scale(self):
  p=copy.deepcopy(controls()[0]['input']);r=analyze(p);p['cost']=[[2*v+7 for v in row]for row in p['cost']];z=analyze(p);self.assertEqual(z['stable'],r['stable']);self.assertEqual(z['stable_minima'],r['stable_minima']);self.assertEqual(z['frontier'],r['frontier']);self.assertEqual(z['stability_premium'],2*r['stability_premium']);self.assertEqual(z['stable_cost'],2*r['stable_cost']+7*p['n'])
 def test_cost_caps_and_frontier(self):
  for c in controls():
   r=analyze(c['input']);self.assertEqual(r['blocking_caps'][0]['cost'],r['stable_cost']);self.assertEqual(r['blocking_caps'][-1]['cost'],r['unconstrained_cost']);self.assertTrue(all(a['cost']>=b['cost']for a,b in zip(r['blocking_caps'],r['blocking_caps'][1:])))
 def test_cost_ties(self):
  r=analyze(controls()[6]['input']);self.assertEqual(r['stable_minima'],r['stable']);self.assertEqual(r['unconstrained_minima'],list(range(6)));self.assertEqual(r['frontier'],r['stable'])
 def test_import_independence(self):subprocess.run([sys.executable,'-c','from matchlab import verify;import sys;assert "matchlab.engine"not in sys.modules'],check=True)
 def test_primitive_forgery_rejection(self):
  count=0
  for c in [controls()[0],controls()[2],controls()[3]]:
   r=analyze(c['input']);paths=[]
   def walk(v,path):
    if type(v)is dict:
     for k,x in v.items():
      if path or k!='input':walk(x,path+[k])
    elif type(v)is list:
     for i,x in enumerate(v):walk(x,path+[i])
    else:paths.append(path)
   walk(r,[])
   for path in paths:
    z=copy.deepcopy(r);q=z
    for k in path[:-1]:q=q[k]
    v=q[path[-1]];q[path[-1]]=v+1 if type(v)is int else not v if type(v)is bool else'forged'
    with self.assertRaises(ValueError,msg=str(path)):verify(z)
   count+=len(paths)
  print('PRIMITIVE_FORGERIES',count)
 def test_structural_forgeries(self):
  r=analyze(controls()[0]['input'])
  for k in r:
   z=copy.deepcopy(r);del z[k]
   with self.assertRaises(ValueError):verify(z)
  for z in [dict(r,extra=0),dict(r,stable=[]),dict(r,matchings=[]),dict(r,stable_cost=True),dict(r,lattice={})]:
   with self.assertRaises(ValueError):verify(z)
 def test_schema(self):
  p=controls()[0]['input']
  for k,v in [('n',True),('n',0),('n',6),('n',3.0),('version',True),('a',[]),('b',[[0,1,1]]*3),('cost',[[0]*3]*2),('cost',[[True]*3]*3),('cost',[[1001]*3]*3),('cost',[[-1001]*3]*3)]:
   q=copy.deepcopy(p);q[k]=v
   with self.assertRaises(ValueError):parse(q)
  for t in ['{"x":1,"x":2}','{"x":1.0}','{"x":1e0}','{"x":NaN}']:
   with self.assertRaises(ValueError):loads(t)
 def test_cli_and_resource_limits(self):
  z=subprocess.run([sys.executable,'-m','matchlab','demo'],capture_output=True,text=True,check=True);self.assertTrue(verify(json.loads(z.stdout)))
  with tempfile.TemporaryDirectory()as d:
   f=Path(d)/'bad.json'
   for s in ['x'*65537,'['*2000+']'*2000,'{}']:
    f.write_text(s);z=subprocess.run([sys.executable,'-m','matchlab','run',str(f)],capture_output=True,text=True);self.assertEqual(z.returncode,2);self.assertFalse(z.stdout);self.assertNotIn('Traceback',z.stderr)
if __name__=='__main__':unittest.main()
