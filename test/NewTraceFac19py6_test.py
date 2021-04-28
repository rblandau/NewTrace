#!/usr/bin/python
"""
NewTraceFac_test.py
specifically for v19py6.
"""

from NewTrace19py6 import NTRC, ntrace, ntracef
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


#  A L L   L E V E L S 
def testAllLevels():
    print("\n========== testAllLevels ============\n")
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


#     M  A  J  O  R     T  E  S  T  S  

#  V A R I O U S   L E V E L S 
def testVariousLevels():
    print("\n============ testVariousLevels =============\n")
    setNewDefaults(NTRC, mylevel=0, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    
    setNewDefaults(NTRC, mylevel=1, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    
    setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testAllLevels()


#  A L L   F A C I L I T I E S 
def testAllFacils():
    print("\n============ testAllFacils =============\n")
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


#  A L L   T A R G E T S 
def testAllTargets():
    print("\n============ testAllTargets =============\n")
    lTargets = [0,1,2,3,4,5,6,7]
    for iTarget in lTargets:
        setNewDefaults(NTRC, mylevel=5, mytarget=iTarget, 
            myfile="test_NewTrace.log", 
            myfacility="", mytime="", myhtml="", myproduction=0)
        testFacils()

    setNewDefaults(NTRC, mylevel=5, mytarget=0, 
        myfile="test_NewTrace_shouldnotbehere.log", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testOneLevel()


#  A L L   H T M L S 
def testAllHTMLs():
    print("\n============ testAllHTMLs =============\n")
    lHtmlStrings = ["", 0, "00", "|", "<BEG>|<END>", "<BEG>", "<beg>|", "|<end>"]
    for sHtml in lHtmlStrings:
        setNewDefaults(NTRC, mylevel=5, mytarget=2, myfile="", 
            myfacility="", mytime="", myhtml=sHtml, myproduction=0)
        testFacils()
        

#  A L L   T I M E S 
def testAllTimes():
    print("\n============ testAllTimes =============\n")
    lTimes = [0, "", "00", "YES", "NO"]
    for sTime in lTimes:
        setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
            myfacility="", mytime=sTime, myhtml="", myproduction=0)
        testFacils()


#  D E C O R A T O R   L E V E L S 
def testAllDecoratorLevels():
    print("\n========== testAllDecoratorLevels ============\n")
    @ntrace
    def testDecoPlain():
        return "MePlain"
    @ntracef("FANC", level=4)
    def testDecoFancy1():
        return "MeFancy1 elevated level"
    @ntracef("", level=4)
    def testDecoFancy2():
        return "MeFancy2 elevated level no facility"

    setNewDefaults(NTRC, mylevel=5, mytarget=0, myfile="", 
        myfacility="", mytime="", myhtml="", myproduction=0)
    testDecoPlain()
    testDecoFancy1()
    testDecoFancy2()


#  E N T R Y   P O I N T 
if 1:
    print ("============= Begin =============")
    setNewDefaults(NTRC, mylevel=0, mytarget=0, myfile="", 
        myfacility="", mytime="YES", myhtml="", myproduction=0)
    NTRC.ntrace(0, "BEGIN")

    setNewDefaults(NTRC, mylevel=6, mytarget=0, myfile="", 
        myfacility="all-aaa", mytime="", myhtml="", myproduction=0)
    testAllLevels()
    
    testVariousLevels()

    testAllFacils()

    testAllDecoratorLevels()

    testAllTargets()

    testAllHTMLs()
    
    testAllTimes()

    setNewDefaults(NTRC, mylevel=0, mytarget=0, myfile="", 
        myfacility="", mytime="YES", myhtml="", myproduction=0)
    NTRC.ntrace(0, "DONE!")


'''
What I actually should be testing:

- ntrace levels 0, 1, 5
- target 0,1,2,4,5,6,7
- file none, name.ext w target=4, name.ext w target=0
- facil "",all,all-a,all-aaa,none,none+a,none+aaa,gigo
- html "",|,<beg>|<end>,<beg>,<beg>|,|<end>
- time 0,"","0","YES","NO"
- production "",YES,NO

'''

#END
