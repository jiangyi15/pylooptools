LoopTools Interface for Python
==============================

This project is based on [LoopTools](https://feynarts.de/looptools/) and [cffi](https://github.com/python-cffi/cffi), in order to provide python module for LoopTools.

Installation
------------

You can download it and build from source.
```
git clone https://github.com/jiangyi15/pylooptools.git
cd pylooptools
pip install .
```

The script `looptools_build.py` will download LoopTools automatically and build it.
It require C/C++ and Fortran compilers.


Or you can directly for github
```
pip install git+https://github.com/jiangyi15/pylooptools.git
```


Examples
--------

```
# import module, F is function and C is constant
from looptools import F, C
# use BO
F.B0(1000, 50, 80)
# or use BOi
F.B0i(C.bb0, 1000, 50, 80)
```
The result is `array(-4.40593283+2.7041431j)`, the same as `-4.40593 + 2.70414 I` in LoopTools User’s Guide.

The function also support [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) in numpy. So we can input array directly as

```
F.B0(1000, 50, [80, 80])
```

The results will also be arrays.
