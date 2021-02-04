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


def testFacils():
    print("========== testFacils ============")
    NTRC.ntrace(0,"test level 0")
    NTRC.ntrace(1,"test level 1")
    NTRC.ntracef(1,"AAA","facil AAA at test level 1")
    NTRC.ntracef(1,"BBB","facil AAA at test level 1")


def testOneLevel():
    print("============ testOneLevel =============")
    NTRC.ntracef(0,"A","facil A at test level 0")
    NTRC.ntracef(0,"B","facil B at test level 0")
    NTRC.ntracef(0,"C","facil C at test level 0")


def testVariousLevels():
    print("============ testVariousLevels =============")
    setNewDefaults(NTRC, mylevel=0, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    setNewDefaults(NTRC, mylevel=1, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()

    
def testAllFacils():
    print("\n============ testAllFacils =============")
    setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testFacils()

    lFacils = ("'' ALL ALL-A ALL-AAA "
                "NONE NONE+A NONE+AAA GIGO " 
                "all-aaa none+aaa").split()
    for sFacil in lFacils:
        setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
            myfacility=sFacil, mytime="", myhtml="", myproduction=0)
        testFacils()


def testAllTargets():
    print("\n============ testAllTargets =============")
    lTargets = [0,1,2,3,4,5,6,7]
    for iTarget in lTargets:
        setNewDefaults(NTRC, mylevel=5, mytarget=iTarget, 
            myfile="test_NewTrace.log", 
            myfacility="", mytime="", myhtml="", myproduction=0)
        testFacils()


def testAllHTMLs():
    print("\n============ testAllHTMLs =============")
    lHtmlStrings = "'' 0 | <BEG>|<END> <BEG> <beg>| |<end>".split()
    for sHtml in lHtmlStrings:
        setNewDefaults(NTRC, mylevel=5, mytarget=2, myfile="", 
            myfacility="", mytime="", myhtml=sHtml, myproduction=0)
        testFacils()
        

def testAllTimes():
    print("\n============ testAllTimes =============")
    lTimes = "'' 0 YES NO".split()
    for sTime in lTimes:
        setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
            myfacility="", mytime=sTime, myhtml="", myproduction=0)
        testFacils()




if 1:
    print ("============= Begin =============")
    setNewDefaults(NTRC, mylevel=6, mytarget=0, myfile="", 
        myfacility="all-aaa", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    
    setNewDefaults(NTRC, mylevel=0, mytarget=0, myfile="", 
        myfacility="all-aaa", mytime="", myhtml="", myproduction=0)
    testVariousLevels()
    setNewDefaults(NTRC, mylevel=3, mytarget=0, myfile="", 
        myfacility="all-aaa", mytime="", myhtml="", myproduction=0)
    testVariousLevels()
    setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
        myfacility="all-aaa", mytime="", myhtml="", myproduction=0)
    testVariousLevels()

    testAllFacils()

    testAllTargets()

    testAllHTMLs()
    
    testAllTimes()
    



if 0:
    pass




'''
What I actually should be testing:

- ntrace levels 0, 1, 5
- target 0,1,2,4,5,6
- file none, name.ext w target4, name.ext w target0
- facil "",all,all-a,all=aaa,none,none+a,none+aaa,gigo
- html "",|,<beg>|<end>,<beg>,<beg>|,|<end>
- production "",YES,NO

'''











#END
