__version__='0.1.0'
def analyze(p):
 from .engine import analyze as run
 return run(p)
def verify(r):
 from .certificate import verify as check
 return check(r)
