#!/usr/bin/python
# NewTraceFac.py
# 
# 
"""
NewTrace18py6 trace module
                                RBLandau 20080226
                                updated  20080830
                                updated  20081003
                                updated  20090207
                                updated  20090527
                                updated  20140114
                                updated  20140209
                                updated  20140315
                                updated  20140723
                                updated  20141020
                                updated  20150112
                                updated  20160921
                                updated  20170127
                                updated  20170129
                                updated  20180115
                                updated  20180515
                                updated  20181105
                                updated  20181121
                                updated  20201218
                                updated  20210202
                                
  Copyright (C) 2008,2009,2014,2015,2016,2017,2018,2020,2021 Richard Landau.  All rights reserved.
  
  Redistribution and use in source and binary forms, with or
  without modification, are permitted provided that the following
  conditions are met:
  
      * Redistributions of source code must retain the above
  copyright notice, this list of conditions and the following
  disclaimer.
  
      * Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.
  
      * Neither the name of Richard Landau nor the names of other
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.
  
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import print_function
import time
import os
import re
import datetime
from functools  import wraps

'''
    RBLandau 20080824
    NewTraceFac tracelog facility for Python.
    Copyright (C) 2008, Richard Landau.  All rights reserved.
    Evolved from old PDP-11 assembler, C, C++, VB, Perl, and other 
     similar trace facilities that I have done over the years.  
     Originated in approximately 1978, intended for debugging 
     multiprocessing problems on FIFE, and has been one-plussed 
     surprisingly only slightly over several decades.  
    The idea is to print relatively fixed-format lines with a 
     standard timestamp, a priority level, a source facility, 
     and whatever information would be useful at that point.  
    Tracing is enabled and controlled through environment variables,
     so that it may be turned on or off, subsetted, etc., without
     any source code change.  
    Output may be filtered by priority number and facility name.

    Usage: 
    Set environment variables, if necessary, to specify the desired 
     level of detail, target (stdout or file), and filename, if necessary.  
     Note that no source code change is needed to turn tracing on and off, 
     or to redirect it to a file, only changes to the running environment.  
      export TRACE_LEVEL=3
      export TRACE_TARGET=4
      export TRACE_FILE="c:\trace file goes here for ease of finding.log"
     (Use export for *NIX and Cygwin systems; use SET for vanilla Windows.)
    Instantiate the NewTrace object and store it global static so that any 
     module can use it.  E.g., 
          gt As NewTrace = New NewTrace    (VB)
          NTRC = NewTraceFac()             (Python)
    Call the ntrace() method of that instance, giving detail level number
     and string.  E.g., 
          gt.trace(1,"This is an item at level 1")
          NTRC.ntrace(2,"This is an item at level 2")
          NTRC.ntracef(3,"FOO","The FOO facility says hi at level 3")
    If the TRACE_LEVEL specified in the program's environment is 
     greater than or equal to the detail level specified in the call, 
     then the string will be printed to the trace log.  
    If the ntracef() method is used, then additionally, the facility string
     specified in the call must match one of the facilities requested
     in the TRACE_FACIL environment variable.  If TRACE_FACIL is "ALL" or 
     the empty string ("") or null (not defined) or indecipherable, then 
     all facilities match, and all will be traced.  This is the default.
    The ntrace() method alone prints a blank facility code.

    The facility list may explicitly include and exclude 
     some facilities.  
    Examples:
      ""                   traces all named facilities
      "ALL"                traces all named facilities
      "NONE"               traces no named facilities
      "ALL-A" "all-a"      traces all named facilities except facility A
      "NONE+A" "none+a"    traces only facility A
      "INDECIPHERABLECRUD" traces all named facilities.
    Trace calls using ntrace() with no facility name are always included.  
    Personally, I tend to restrict facility codes to exactly the same 
    length (in my case, four characters), again so that successive lines
    will have various fields aligned for easier recognition and searching.  
    Note that if you want only, say, facility A, then you must use
      export TRACE_FACIL=NONE+A
    to prevent other facilities from being listed.  

    A trace output line looks like 
          YYYYMMDD_HHMMSS L  user-specified string
     or 
          YYYYMMDD_HHMMSS L FACIL user-specified string
      HH is the 24-hour hour.
      L is the level of detail specified for this trace line.
    HTML output is slightly different, includes a "<BR>" at the start 
     of each line, or whatever prefix and suffix are specified in 
     the TRAC_HTML environment variable (q.v.).  

    Environment variables used by trace() are
      TRACE_LEVEL, TRACE_TARGET, TRACE_FILE, and TRACE_PRODUCTION.  
      TRACE_LEVEL is mandatory, the others optional.  Explanations below.  

    Typical use of trace levels is:
    0     Messages that always should be printed, e.g., errors that 
          the user must see.
    1     Entries to functions, with arguments listed.
          Any internal error conditions or error exits from 
          functions, with status.  
    2     Normal exits from functions, with status and maybe output arg values.  
    3     Things that happen once per record, once per line, etc., 
          that are repeated often, big-O the number of lines in the file
          or messages in the stream.  
    4     Really detailed info, such as syntax cracking of input lines, 
          entries in data structures, and such, that happen once or more
          per line.  
    5     Really, really detailed info, such as routine accesses to 
          data structures.

    Contents of environment veriables:
    TRACE_LEVEL;    # integer: levels 0 (or absent) thru 5.  
                    If null, defaults to zero.  
    TRACE_TARGET;   # bitmask: target bits 1=print to stdout, 
                    2=print html to stdout, 4=print to file.
                    If null, defaults to 1 (print on stdout).  
    TRACE_FILE;     # file: name of log file to trace into.
                    If null, defaults to "./newtrace.log".
                    Output to a file does not include HTML tags.  
    TRACE_FACIL;    # list of facility names to be traced.
                    Normally a plus-or-minus-separated list of 
                     facility names that will be included in
                     results of the tracef() call.
                    If "ALL", then all facilities will be
                     included.  If "NONE" then no facilities
                     will be included.  
                    Facilities can be explicitly included after
                     NONE, e.g., "NONE+FOO+BAR".
                    Facilities can be explicitly excluded after 
                     ALL, e.g., "ALL-FOO-BAR".
                    If null, then ALL is assumed.
                    If the syntax is not correct, results may be GIGO.
    TRACE_PRODUCTION;
                    If "YES" then nothing will be traced, and the 
                     trace functions and decorators will attempt 
                     to use as little CPU resource as possible.
                     NOTE: ntraces at priority zero always print.
    TRACE_TIME;     If nonempty or nonzero integer, timestamps will 
                     include milliseconds, in format "YYYYMMDD_HHMMSS.mmm".
    TRACE_HTML;     String specifying prefix and suffix for each
                     line emitted as HTML.
                     Syntax: "prefix|suffix", that is, the prefix
                     string and suffix strings separated by a 
                     vertical bar (sometimes called "pipe").  
                     Default is  "<br>| " if the environment
                     variable is absent or an empty string.
                     The value "|" will generate no prefix or
                     suffix.

Python decorators:
There are two new functions to use as Python decorators to
 report entry and exit of functions, including arguments in
 and return value out, painlessly.  
Input argument names cannot be identified by the decorator version
 of ntrace() and ntracef().  If you need individual identification 
 of input arguments, call the trace manually, as in the old days.  
    @ntrace             for calls with no facility code attached
    @ntracef("ABCD")    for calls associated with a facility ABCD
As usual, the facility code should be max four letters to preserve 
 alignment and should be all caps for legibility.  

The @ntrace decorator prints function entry and exit at level 1 by default.

The @ntracef() decorator also supports an optional level argument to change
 the trace level of the entry and exit lines.  This can be specified 
 positionally or keyword, e.g., @ntracef("FOO",2) or @ntracef("FOO",level=2).
The @ntrace decorator does not support the level argument; but note that
 the facility on @ntracef() can be left blank, e.g., @ntracef("",5).  
The @ntracef decorator processes the first argument specially if 
 the argument is an instance pointer (usually "self" in class 
 methods).  In this case, it prints the classname, and the 
 instance's self.ID if it exists, on both entry and exit.  
 Much more informative than the hex address.  

Summary examples in Python:
from NewTraceFac import NTRC, ntrace, ntracef
NTRC.ntrace(3, "some string with %s %s" % ("some", "substitutions"))
NTRC.ntracef(3, "ABCD", "some string with %s %s" % ("some", "substitutions"))

New 2017: The decorators can be nulled out with the environment variable
    TRACE_PRODUCTION=YES
 This will also cause direct calls to the ntrace() and ntracef() functions
 to return with as little work as possible.  
New 2018: 
    Run with Python versions 2 and 3.
    TRACE_TIME=nonempty gives timestamps in milliseconds.
    Speed up by using cheap isProduction() rather than interrogating 
     os.getenv() every time.
    NTRC really is a singleton, fixing long-standing double printing bug.  

'''


class CNewTrace(object):
    def __init__(self):
        self.getDefaults()


    def getDefaults(self, mylevel=0, mytarget=1, myfile="", myfacil=""):
        '''Collect defaults from the environment. '''
        btraceproduction = (os.getenv("TRACE_PRODUCTION", "NO") == "YES")
        btimehires = (not (os.getenv("TRACE_TIME", "") == ""))
        try:
            tracelevel = int(os.getenv("TRACE_LEVEL", mylevel))
        except ValueError:      # If not integer, take default.
            tracelevel = 0
        try:
            tracetarget = int(os.getenv("TRACE_TARGET", mytarget))
        except ValueError:      # If not integer, take default.
            pass
        tracefile = os.getenv("TRACE_FILE", myfile)
        tracefacil = os.getenv("TRACE_FACIL", myfacil).upper()
        tracehtml = os.getenv("TRACE_HTML", "<br>| ")
            
        self.setDefaults(tracelevel, tracetarget, tracefile, tracefacil, 
                btimehires, tracehtml, btraceproduction)
        if not btraceproduction:    # If normal mode
            if tracelevel > 0:
                self.ntrace(1, "DEBUGTRACE info level|%s| targets|%s| "
                            "facil|%s| file|%s| "
                            "time|%s| html|%s| production|%s|" 
                    % (tracelevel, tracetarget, 
                        tracefacil, tracefile, 
                        btimehires, tracehtml, btraceproduction))


# s e t D e f a u l t s 
    def setDefaults(self, level=0, target=1, file="newtrace.log",
            facility="", time="", html="", production=0):
        ''' Set all defaults so we can test from outside.'''

        self.tracelevel = level
        self.tracetarget = target
        self.tracefile = file

        self.tracefacil = facility.upper()
        self.bFacilDefault = True
        self.lFacilExceptions = []
        if self.tracefacil:
            if self.tracefacil.startswith("A"):
                self.lFacilExceptions = self.tracefacil.split("-")
                if self.lFacilExceptions[0] == "ALL":
                    self.bFacilDefault = True
            if self.tracefacil.startswith("N"):
                self.lFacilExceptions = self.tracefacil.split("+")
                if self.lFacilExceptions[0] == "NONE":
                    self.bFacilDefault = False

        self.btimehires = bool(time)

        self.tracehtml = html
        (self.tracehtmlL, self.tracehtmlR) = "<br>| ".split("|")
        if self.tracehtml:
            try:
                (self.tracehtmlL, self.tracehtmlR) = html.split("|")
            except ValueError:      # If not splittable, bad syntax
                (self.tracehtmlL, self.tracehtmlR) = ("|", "|")

        self.btraceproduction = production
        
        if 0:       # Did we get all the interpretations right?
                    #  Typical problems with strings vs integers.
            self.ntrace(0, "SETDEFAULTS  D E T A I L S")
            self.ntrace(0, "level=|%s|, target=|%s|, file=|%s|, "
                    "facility=|%s|, time=|%s|, html=|%s|, production=|%s|" 
                    % (self.tracelevel, self.tracetarget, self.tracefile, 
                        self.tracefacil, self.btimehires, 
                        self.tracehtml, self.btraceproduction))
            self.ntrace(0, "facildef|%s| except|%s| "
                            "htmlL|%s| htmlR|%s|" 
                        % (self.bFacilDefault, self.lFacilExceptions, 
                                self.tracehtmlL, self.tracehtmlR))
        return


# i s P r o d u c t i o n 
    def isProduction(self):
        return self.btraceproduction


# g e t L e v e l 
    def getLevel(self):
        return self.tracelevel


# n t r a c e     trace with no identified facility name.
    # Old style, calls new style.
    def trace(self, level, line):
        self.ntrace(level, line)


    def ntrace(self, level, line):
        # If not in production mode or yes in production mode with level==0.
        if (not self.isProduction() or level == 0):
            # If we are tracing at a high enough level to include this item, 
            #  then send it to the appropriate target(s).
            if level <= self.tracelevel:
                # Get a timestamp
                self.ascT = self.fnsGetTimestamp()
                self.linestart = "%s %1d %-4s " % (self.ascT,level,"    ")
                
                # If console only, or console and others, print to stdout.
                if (((self.tracetarget & 1) and not (self.tracetarget & 2)) 
                  or not (self.tracetarget & 6)):
                    print(self.linestart + " " + line)
                
                # If HTML format, add line break.
                if (self.tracetarget & 2):
                    print(self.tracehtmlL + self.linestart + " " 
                            + line + self.tracehtmlR)
                
                # Or append to trace file.
                if (self.tracetarget & 4):
                    self.fWriteCarefully(self.tracefile, 'a', 
                        self.linestart+" "+line, 5)
        else:       # If in production mode and level > 0
            pass    #  go away.


# n t r a c e f   trace associated with a named facility.
    # Old style, calls new style.
    def tracef(self, level, facility, line):
        self.ntracef(level, facility, line)


    def ntracef(self, level, facility, line):
        # If not in production mode or yes in production mode with level==0.
        if (not self.isProduction() or level == 0):
            # If we are tracing at a high enough level to include this item, 
            #  then send it to the appropriate target(s).
            if level <= self.tracelevel:
                # Now assess the facility: include line Y or N?
                if facility:
                    self.facilcaps = facility.upper()
                    # Take facility default unless this one is an exception.
                    self.traceme = ((not self.bFacilDefault) 
                                    if self.facilcaps in self.lFacilExceptions
                                    else self.bFacilDefault)
                if self.traceme:
                    # Get a timestamp
                    self.ascT = self.fnsGetTimestamp()
                    self.linestart = "%s %1d %-4s " % (self.ascT,level,facility)
                    # If console only, or console and others, print to stdout.
                    if (((self.tracetarget & 1) and not (self.tracetarget & 2)) 
                        or not (self.tracetarget & 6)):
                        print(self.linestart + " " + line)
                    
                    # If HTML format, add line break.
                    if (self.tracetarget & 2):
                        print(self.tracehtmlL + self.linestart + " " 
                                + line + self.tracehtmlR)
                    
                    # Or append to trace file.
                    if (self.tracetarget & 4):
                        self.fWriteCarefully(self.tracefile, 'a', 
                            self.linestart+" "+line, 10)
        else:       # If in production mode and level > 0
            pass    #  go away.


    # f W r i t e C a r e f u l l y     write to file avoiding file-busy errors.
    def fWriteCarefully(self, outfile, mode, outline, retries):
        # Careful: if the file is still busy with the last write, 
        #  wait a second and try it again.  A few times.
        #  Yes, this actually happens disturbingly frequently.
        for idxErrorCount in range(retries+1):
            try:
                with open(outfile, mode) as f:
                    if idxErrorCount == 0:
                        f.write(outline + "\n")
                    else:
                        outline += " filebusyretries|%s|"%(idxErrorCount)
                        f.write(outline + "\n")
                    #f.flush()
                    #f.close()
                break                   # Leaves the for loop.
            except IOError as e:
                time.sleep(0.050)
        # If we can't write after several retries, tough.  


    # f n s G e t T i m e s t a m p 
    def fnsGetTimestamp(self):
        '''Return timestamp with or without milliseconds.
        '''
        if self.btimehires:
            return datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        else:
            return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


# N T R C  i n s t a n c e 

''' Easy usage:

    Now, for the convenience of the lazy, populate a 
     globally accessible instance that can be used with
     no further action required.
    If the user really wants a particular facility name, 
     make another instance or use setFacility.
    
    Simplest way:
        from NewTraceFac import NTRC,ntrace,ntracef
    then
        @ntracef("NAME")         # or just "@ntrace" if no facility code
        def somefunction()
    and
        NTRC.ntracef(3, "NAME", "string with %s substitution%s" % ("two","s"))
                                # or just "NTRC.ntrace" if no facility code

    Since the function decorators use the strings "entr" and "exit" 
     between the facility name and the function name, it is recommended
     that one use some other four letter codes in the traced lines, 
     such as "proc" so that successive lines line up into clear columns.
'''

# Make a singleton of the NewTrace instance.  
class Singleton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args,**kwargs)
            cls._provenance = "singleton instance of class %s" % cls._instances[cls]
        return cls._instances[cls]

class CSingletonNewTrace(CNewTrace):
    __metaclass__ = Singleton
    _whatsit = "singleton instance of class NewTrace"

# NEW VERSION NTRC
NTRC = CSingletonNewTrace()
# OLD VERSION TRC
TRC = CSingletonNewTrace()


# D e c o r a t o r s 


# Plain decorator, no facility code.  Logs entry and exit.  

# NEW VERSION @ntrace
if NTRC.isProduction():
    def ntrace(func):
        return func
else:
    def ntrace(func):
        @wraps(func)
        def wrap2(*args,**kwargs):
            # E N T R Y 
            if len(args)>0 and (repr(args[0]).find(" object ") >= 0
                            or (repr(args[0]).find(" instance ") >= 0)):
                _id = getattr(args[0],"ID","")
                NTRC.ntrace(1,"entr %s <cls=%s id=|%s|> |%s| kw=%s" 
                    % (func.__name__,args[0].__class__.__name__,_id,
                    args[1:],kwargs))
            else:
                NTRC.ntrace(1,"entr %s args=%s,kw=%s" 
                    % (func.__name__,args,kwargs))
            result = func(*args,**kwargs)
            # E X I T 
            if len(args)>0 and (repr(args[0]).find(" object ") >= 0
                            or (repr(args[0]).find(" instance ") >= 0)):
                _id = getattr(args[0],"ID","")
                NTRC.ntrace(1,"exit %s <cls=%s id=|%s|> result|%s|" 
                    % (func.__name__,args[0].__class__.__name__,_id,result))
            else:
                NTRC.ntrace(1,"exit %s result|%s|" % (func.__name__,result))
            return result
        return wrap2


# OLD VERSION @trace
if NTRC.isProduction():
    def trace(func):
        return func
else:
    def trace(func):
        def wrap2(*args,**kwargs):
            TRC.trace(1,"entr %s args=%s,kw=%s" % (func.__name__,args,kwargs))
            result = func(*args,**kwargs)
            TRC.trace(1,"exit %s result|%s|" % (func.__name__,result))
            return result
        wrap2.__name__ = func.__name__
        return wrap2


# Decorator with facility code and priority level.  
# Facility code may be left blank to use priority or "self" printing.

# NEW VERSION @ntracef
if NTRC.isProduction():
    def ntracef(facil="",level=1):
        def tracefinner(func):
            return func
        return tracefinner
else:
    def ntracef(facil="",level=1):
        def tracefinner(func):
            @wraps(func)
            def wrap1(*args,**kwargs):
                if len(args)>0 and (repr(args[0]).find(" object ") >= 0
                                or (repr(args[0]).find(" instance ") >= 0)):
                    _id = getattr(args[0],"ID","")
                    NTRC.ntracef(level,facil,"entr %s <cls=%s id=|%s|> |%s| kw=%s" 
                        % (func.__name__,args[0].__class__.__name__,_id,
                        args[1:],kwargs))
                else:
                    NTRC.ntracef(level,facil,"entr %s args=%s,kw=%s" 
                        % (func.__name__,args,kwargs))
                result = func(*args,**kwargs)
                if len(args)>0 and (repr(args[0]).find(" object ") >= 0
                                or (repr(args[0]).find(" instance ") >= 0)):
                    _id = getattr(args[0],"ID","")
                    NTRC.ntracef(level,facil,"exit %s <cls=%s id=|%s|> result|%s|" 
                        % (func.__name__,args[0].__class__.__name__,_id,result))
                else:
                    NTRC.ntracef(level,facil,"exit %s result|%s|" % (func.__name__,result))
                return result
            return wrap1
        return tracefinner


# OLD VERSION @tracef
if NTRC.isProduction():
    def tracef(facil="",level=1):
        def tracefinner(func):
            return func
        return tracefinner
else:
    def tracef(facil="",level=1):
        def tracefinner(func):
            def wrap1(*args,**kwargs):
                if len(args)>0 and str(type(args[0])).find("class") >= 0:
                    _id = getattr(args[0],"ID","")
                    TRC.tracef(level,facil,"entr %s args=<%s id=|%s|> |%s| kw=%s" % (func.__name__,args[0].__class__.__name__,_id,args[1:],kwargs))
                else:
                    TRC.tracef(level,facil,"entr %s args=%s,kw=%s" 
                        % (func.__name__,args,kwargs))
                result = func(*args,**kwargs)
                if len(args)>0 and str(type(args[0])).find("class") >= 0:
                    _id = getattr(args[0],"ID","")
                    TRC.tracef(level,facil,"exit %s <%s id=|%s|> result|%s|" 
                        % (func.__name__,args[0].__class__.__name__,_id,result))
                else:
                    TRC.tracef(level,facil,"exit %s result|%s|" 
                        % (func.__name__,result))
                return result
            wrap1.__name__ = func.__name__
            return wrap1
        return tracefinner


# Edit history:
# 20141020  RBL Add fWriteCarefully routine to minimize problems with 
#                file-busy contention, which sometimes happens.
#                CHKNET suffers a lot of this type of error.
# 20150112  RBL Because of heat from various members of the Python
#                community about the use of the name "trace", I 
#                will change the name to "ntrace".  After some 
#                searching on Google, one finds that the name 
#                "rtrace" was already used for ray tracing, 
#                "dtrace" for some sort of debugging, and
#                "dbtrace" for some database debugging; but 
#                "ntrace" was relatively unused, appears only as
#                a variable name in a few places.  Voila!
#               Begin to add name changes: trace -> ntrace and 
#                all its relatives, ntrace(), ntracef(), and their
#                decorators, and TRC instance.  
# 20160921  RBL Begin to wean the code from the old "trace" to the 
#                new "ntrace" and from "TRC" to "NTRC".  Make those
#                new names the default call, so that they are the 
#                slightly faster versions.  
#               Clean up some of the longer-than-80 lines.
# 20170127  RBL V13: Add PRODUCTION versions of functions and decorators
#                that do as little as possible to reduce CPU burden
#                completely without editing any code; just set a 
#                new environment variable TRACE_PRODUCTION=YES and
#                poof, all the code goes away.  
#                Well, not all, exactly.  Have to honor traces at 
#                level zero, even in production mode, because they
#                are often important informational messages.  
#                (And optimize the tests for speed.)
# 20170129  RBL V14: Add method to tell if production mode is turned on
#                so that users can report it.  
# 20180115  RBL V14p3: Make minimal changes to permit use on Python3.
#               Future: make it work on both p2 and p3.  
# 20180515  RBL NewTrace15py6 test version that maybe runs on Python 2 and 3.  
#                Surprisingly hard to do and not efficient.  
#               Identify self (cls and id) for both ntrace and ntracef.
# 20181105  RBL NewTrace16py6: Add TRACE_TIME env var that prints 
#                milliseconds on all lines if it is non-empty.
#               Use cheap isProduction() instead of calling the os.getenv()
#                every time.
#               Turns out that both of these changes are less trivial than
#                first appears, given the need for these functions inside 
#                and outside the class.
# 20181121  RBL NewTrace17py6: Make NTRC a singleton.
# 20201218  RBL Clarify imports.
# 20210202  RBL NewTrace18py6: Import HTML prefix and suffix from TRACE_HTML 
#                envir var.
#               Separate getting and setting the environmental defaults
#                to make it easier to test using setDefaults().
#               Redo facility checking in ntracef() for runtime performance.  
# 20210219  RBL Correct defaults for level and target, oops.  
# 
# 

#END
