"""Bounded complete two-sided strict-preference input. No solver or report construction."""
import json

def integer(x):
 if type(x)is not int:raise ValueError('expected non-boolean integer')
 return x

def keys(x,ks):
 if type(x)is not dict or set(x)!=set(ks):raise ValueError('unexpected fields')

def order(x,n):
 if type(x)is not list or len(x)!=n or any(type(v)is not int for v in x)or sorted(x)!=list(range(n)):raise ValueError('order must be a complete strict permutation')
 return x

def parse(p):
 keys(p,['version','n','a','b','cost'])
 if integer(p['version'])!=1:raise ValueError('version must be 1')
 n=integer(p['n'])
 if not 1<=n<=5:raise ValueError('side size must be 1..5')
 for side in ['a','b']:
  if type(p[side])is not list or len(p[side])!=n:raise ValueError('one preference row per participant')
  for row in p[side]:order(row,n)
 if type(p['cost'])is not list or len(p['cost'])!=n:raise ValueError('square cost matrix required')
 for row in p['cost']:
  if type(row)is not list or len(row)!=n:raise ValueError('square cost matrix required')
  for x in row:
   if not -1000<=integer(x)<=1000:raise ValueError('cost must be integer in -1000..1000')
 return n

def loads(text):
 def pairs(ps):
  out={}
  for k,v in ps:
   if k in out:raise ValueError('duplicate key')
   out[k]=v
  return out
 def no(_):raise ValueError('JSON decimals/constants forbidden')
 return json.loads(text,object_pairs_hook=pairs,parse_float=no,parse_constant=no)
