#!/usr/bin/python
"""
NewTraceFac_test.py
specifically for v18py6.
"""

from NewTrace18py6 import NTRC, ntrace, ntracef
from os import environ


# Crack open the black box to replace the params
#  for testing.
def setNewDefaults(obj, mylevel=6, mytarget=0, myfile="", myfacility="", 
                mytime="", myhtml="", myproduction=0):
    obj.setDefaults(level=mylevel, target=mytarget, file=myfile, 
                facility=myfacility, time=mytime, html=myhtml, 
                production=myproduction)
    print("\nsetNewDef: level=|%d| target=|%d| file=|%s| facility=|%s| time=|%s| "
            "html=|%s| production|%s|" 
            % (mylevel, mytarget, myfile, myfacility, mytime, 
            myhtml, myproduction))


def testAllLevels():
    print("========== testAllLevels ============")
    NTRC.ntrace(0,"test level 0")
    NTRC.ntrace(1,"test level 1")
    NTRC.ntrace(2,"test level 2")
    NTRC.ntrace(3,"test level 3")
    NTRC.ntrace(4,"test level 4")
    NTRC.ntrace(5,"test level 5")

    NTRC.ntracef(0,"AAA","facil AAA at test level 0")
    NTRC.ntracef(1,"AAA","facil AAA at test level 1")
    NTRC.ntracef(2,"AAA","facil AAA at test level 2")
    NTRC.ntracef(3,"AAA","facil AAA at test level 3")
    NTRC.ntracef(4,"AAA","facil AAA at test level 4")
    NTRC.ntracef(5,"AAA","facil AAA at test level 5")

    NTRC.ntracef(0,"BBB","facil BBB at test level 0")
    NTRC.ntracef(1,"BBB","facil BBB at test level 1")
    NTRC.ntracef(2,"BBB","facil BBB at test level 2")
    NTRC.ntracef(3,"BBB","facil BBB at test level 3")
    NTRC.ntracef(4,"BBB","facil BBB at test level 4")
    NTRC.ntracef(5,"BBB","facil BBB at test level 5")

    NTRC.ntracef(0,"aaa","facil aaa at test level 0")
    NTRC.ntracef(1,"aaa","facil aaa at test level 1")
    NTRC.ntracef(2,"Aaa","facil Aaa at test level 2")
    NTRC.ntracef(3,"aAa","facil aAa at test level 3")
    NTRC.ntracef(4,"aaA","facil aaA at test level 4")
    NTRC.ntracef(5,"AaA","facil AaA at test level 5")


def testOneLevel():
    print("============ testOneLevel =============")
    NTRC.ntracef(0,"A","facil A at test level 0")
    NTRC.ntracef(0,"B","facil B at test level 0")
    NTRC.ntracef(0,"C","facil C at test level 0")


def testAllForTarget(target, filename):
    print("============ testAllForTarget =============")
    setNewDefaults(NTRC, 0, target, filename)
    testAllLevels()
    setNewDefaults(NTRC, 1, target, "")
    testAllLevels()
    setNewDefaults(NTRC, 2, target, "")
    testAllLevels()
    setNewDefaults(NTRC, 3, target, "")
    testAllLevels()
    setNewDefaults(NTRC, 4, target, "")
    testAllLevels()
    setNewDefaults(NTRC, 5, target, "")
    testAllLevels()
    setNewDefaults(NTRC, 5, target, "", "AAA")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "BBB")
    testAllLevels()
    setNewDefaults(NTRC, 5, target, "", "donttraceme")
    testAllLevels()
    setNewDefaults(NTRC, 5, target, "", "ALL")
    testAllLevels()

    setNewDefaults(NTRC, 5, target, "", "")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "all")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "none")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "-a")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "all-a")
    testOneLevel()
    setNewDefaults(NTRC, 5, target, "", "none+a")
    testOneLevel()


if 1:
    print ("============= Begin =============")
    setNewDefaults(NTRC, mylevel=5, mytarget=0, 
            myfile="", myfacility="none+a+aa+b", 
            mytime="", myhtml="", myproduction=0)
    testAllLevels()
    setNewDefaults(NTRC, mylevel=5, mytarget=0, 
            myfile="", myfacility="all-a-aa-b", 
            mytime="", myhtml="", myproduction=0)
    testAllLevels()
    setNewDefaults(NTRC, mylevel=5, mytarget=0, 
            myfile="", myfacility="all-aaa", 
            mytime="", myhtml="", myproduction=0)
    testAllLevels()


if 0:
    print("============== Test For Target ==============")
    testAllForTarget(0, "test_NewTrace.log")
    testAllForTarget(1, "test_NewTrace.log")
    testAllForTarget(2, "test_NewTrace.log")
    testAllForTarget(4, "test_NewTrace.log")

#END

'''
What I actually should be testing:

- ntrace levels 0, 1




'''
