import cffi
import wget
import os
import tarfile


def ensure_looptools():
    if not os.path.exists("LoopTools-2.16"):
        if not os.path.exists("LoopTools-2.16.tar.gz"):
            wget.download("https://feynarts.de/looptools/LoopTools-2.16.tar.gz", "LoopTools-2.16.tar.gz")
        f = tarfile.open("LoopTools-2.16.tar.gz")
        f.extractall()
    if not os.path.exists("LoopTools-2.16/build/libooptools.a"):
        os.system("cd LoopTools-2.16 && ./configure && make && cd ..")

ensure_looptools()

# file "example_build.py"

# Note: we instantiate the same 'cffi.FFI' class as in the previous
# example, but call the result 'ffibuilder' now instead of 'ffi';
# this is to avoid confusion with the other 'ffi' object you get below

from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_looptools_lib",
   r"""
        #include "clooptools.h"
    """,
    libraries=["ooptools", "gfortran"],
    include_dirs=["LoopTools-2.16/build/"],
    library_dirs=["LoopTools-2.16/build/"])   # or a list of libraries to link with
    # (more arguments like setup.py's Extension class:
    # include_dirs=[..], extra_objects=[..], and so on)

cdefs = """
typedef double _Complex complex;
"""

env_function_list =["clearcache", "markcache", "restorecache", "ltini", "ltexi"]
for i in env_function_list:
    cdefs += f"void {i}();\n"

set_get_list = ["mudim", "delta", "uvdiv", "lambda", "minmass", "maxdev", "diffeps", "zeroeps"]
for i in set_get_list:
    cdefs += f"void set{i}(double);\n"
    cdefs += f"double get{i}();\n"


head_id = ["A0i"]
no_head_id = ["A0", "A00"]
for i in head_id:
    cdefs += f"complex {i}(int, double);\n"
    cdefs += f"complex {i}C(int, complex);\n"
for i in no_head_id:
    cdefs += f"complex {i}(double);\n"
    cdefs += f"complex {i}C(complex);\n"
head_id = ["B0i"]
no_head_id = ["B0", "B1", "B00", "B11", "B001", "B111",
             "DB0", "DB1", "DB00", "DB11"]
for i in head_id:
    cdefs += f"complex {i}(int, double, double, double);\n"
    cdefs += f"complex {i}C(int, complex, complex, complex);\n"
for i in no_head_id:
    cdefs += f"complex {i}(double, double, double);\n"
    cdefs += f"complex {i}C(complex, complex, complex);\n"
head_id = ["C0i"]
no_head_id = ["C0"]
for i in head_id:
     cdefs += f"complex {i}(int, {','.join(['double'] * 6)});\n"
     cdefs += f"complex {i}C(int, {','.join(['complex'] * 6)});\n"
for i in no_head_id:
     cdefs += f"complex {i}({','.join(['double'] * 6)});\n"
     cdefs += f"complex {i}C({','.join(['complex'] * 6)});\n"
head_id = ["D0i"]
no_head_id = ["D0"]
for i in head_id:
     cdefs += f"complex {i}(int, {','.join(['double'] * 10)});\n"
     cdefs += f"complex {i}C(int, {','.join(['complex'] * 10)});\n"
for i in no_head_id:
     cdefs += f"complex {i}({','.join(['double'] * 10)});\n"
     cdefs += f"complex {i}C({','.join(['complex'] * 10)});\n"

cdefs += f"complex* Aget({','.join(['double'] * 1)});\n"
cdefs += f"complex* AgetC({','.join(['complex'] * 1)});\n"
cdefs += f"complex* Bget({','.join(['double'] * 3)});\n"
cdefs += f"complex* BgetC({','.join(['complex'] * 3)});\n"
cdefs += f"complex* Cget({','.join(['double'] * 6)});\n"
cdefs += f"complex* CgetC({','.join(['complex'] * 6)});\n"

def read_constant(file_name):
    ret = ""
    with open(file_name) as f:
        for i in f.readlines():
            if i.startswith("#define"):
                items = i.strip().split(" ")
                if len(items) == 3:
                    if all(j in "0123456789" for j in items[2]):
                        ret += i + "\n"
    return ret

cdefs += read_constant("LoopTools-2.16/build/clooptools.h")

ffibuilder.cdef(cdefs)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
