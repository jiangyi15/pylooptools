from _looptools_lib import lib
import atexit

try :
    from numpy import vectorize
except:
    vectorize = lambda x: x

lib.ltini()
atexit.register(lib.ltexi)

class F:
    pass

class C:
    pass

for k, v in lib.__dict__.items():
    if callable(v):
        if not any(i in k for i in ["get", "set", "cache", "eval"]):
            setattr(F, k, staticmethod(vectorize(v)))
        else:
            setattr(F, k, staticmethod(v))
    elif isinstance(v, int):
        setattr(C, k, v)
    else:
        print("not used for ", k)
