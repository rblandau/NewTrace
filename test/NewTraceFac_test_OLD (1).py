"""
NewTraceFac_test.py
"""

from NewTraceFac02 import TRC
from os import environ

# Crack open the black box to replace the params
#  for testing.
def setNewDefaults(obj,level,target,tracefile="",facility=""):
    obj.tracelevel = level
    obj.tracetarget = target
    if tracefile != "":
        obj.tracefile = tracefile
    obj.tracefacil = facility.upper()
    print "level=%d target=%d file=%s facility=%s" % (level, target, obj.tracefile, obj.tracefacil)

def testAllLevels():
    TRC.trace(0,"test level 0")
    TRC.trace(1,"test level 1")
    TRC.trace(2,"test level 2")
    TRC.trace(3,"test level 3")
    TRC.trace(4,"test level 4")
    TRC.trace(5,"test level 5")

    TRC.tracef(0,"AAA","facil AAA at test level 0")
    TRC.tracef(1,"AAA","facil AAA at test level 1")
    TRC.tracef(2,"AAA","facil AAA at test level 2")
    TRC.tracef(3,"AAA","facil AAA at test level 3")
    TRC.tracef(4,"AAA","facil AAA at test level 4")
    TRC.tracef(5,"AAA","facil AAA at test level 5")

    TRC.tracef(0,"BBB","facil BBB at test level 0")
    TRC.tracef(1,"BBB","facil BBB at test level 1")
    TRC.tracef(2,"BBB","facil BBB at test level 2")
    TRC.tracef(3,"BBB","facil BBB at test level 3")
    TRC.tracef(4,"BBB","facil BBB at test level 4")
    TRC.tracef(5,"BBB","facil BBB at test level 5")

    TRC.tracef(0,"aaa","facil aaa at test level 0")
    TRC.tracef(1,"aaa","facil aaa at test level 1")
    TRC.tracef(2,"Aaa","facil Aaa at test level 2")
    TRC.tracef(3,"aAa","facil aAa at test level 3")
    TRC.tracef(4,"aaA","facil aaA at test level 4")
    TRC.tracef(5,"AaA","facil AaA at test level 5")

def testOneLevel():
    TRC.tracef(0,"A","facil A at test level 0")
    TRC.tracef(0,"B","facil A at test level 0")
    TRC.tracef(0,"C","facil A at test level 0")

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
    setNewDefaults(TRC, 5, target, "", "AAA")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "BBB")
    testAllLevels()
    setNewDefaults(TRC, 5, target, "", "donttraceme")
    testAllLevels()
    setNewDefaults(TRC, 5, target, "", "ALL")
    testAllLevels()

    setNewDefaults(TRC, 5, target, "", "")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "all")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "none")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "-a")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "all -a")
    testOneLevel()
    setNewDefaults(TRC, 5, target, "", "none a")
    testOneLevel()

testAllLevels()

testAllForTarget(0, "test_NewTrace.log")
testAllForTarget(1, "test_NewTrace.log")
testAllForTarget(2, "test_NewTrace.log")
testAllForTarget(4, "test_NewTrace.log")

