from __future__ import print_function
from NewTrace15py6 import ntrace,ntracef,NTRC
import sys
class CFoo:
    @ntracef("FOO")
    def __init__(self, id):
        self.ID = id
    @ntracef("FOO")
    def method1(self,a,b):
        return a+b
    @ntrace
    def method2(self,a,b):
        return a+b
print(sys.version_info)
f=CFoo(999)
f.method1(2,3)
g=CFoo(3456)
#g.add1(22,33)
g.method2(55,66)

@ntracef("none")
def function1(c,d):
    return c-d
@ntrace
def function2(c,d):
    return c-d

function1(78.0, 67)
function2(98,76)
