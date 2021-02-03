"""
NewTrace_test.py
"""

from NewTrace import TRC
from os import environ

# Crack open the black box to replace the params
#  for testing.
def setNewDefaults(obj,level,target,tracefile):
    obj.tracelevel = level
    obj.tracetarget = target
    if tracefile != "":
        obj.tracefile = tracefile
    print "level %d target %d file %s" % (level, target, obj.tracefile)

def testAllLevels():
    TRC.trace(0,"test level 0")
    TRC.trace(1,"test level 1")
    TRC.trace(2,"test level 2")
    TRC.trace(3,"test level 3")
    TRC.trace(4,"test level 4")
    TRC.trace(5,"test level 5")

def testAllForTarget(target, filename):
    setNewDefaults(TRC, 0, target, filename)
    testAllLevels()
    setNewDefaults(TRC, 1, target, "")
    testAllLevels()
    setNewDefaults(TRC, 2, target, "")
    testAllLevels()
    setNewDefaults(TRC, 3, target, "")
    testAllLevels()
    setNewDefaults(TRC, 4, target, "")
    testAllLevels()
    setNewDefaults(TRC, 5, target, "")
    testAllLevels()

testAllLevels()

testAllForTarget(0, "test_NewTrace.log")
testAllForTarget(1, "test_NewTrace.log")
testAllForTarget(2, "test_NewTrace.log")
testAllForTarget(4, "test_NewTrace.log")

