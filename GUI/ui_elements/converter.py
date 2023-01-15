import os.path
from os import listdir
from os.path import isfile, join
import sys
mypath = os.path.dirname(os.path.abspath(__file__))
files = [f[:-3] for f in listdir(mypath) if isfile(join(mypath, f)) and f[-2:] == "ui"]
print(files)
for f in files:
    f = os.path.join(mypath, f)
    os.system(f"pyuic5 {f}.ui -o {f}.py")