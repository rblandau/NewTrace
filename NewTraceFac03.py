"""
NewTraceFac03 trace module
                                RBLandau 20080226
                                updated  20080830
                                updated  20081003
                                
Copyright (C) 2008, Richard Landau.  All rights reserved.
"""

from time import localtime
from os import environ

# RBLandau 20080824
# NewTraceFac tracelog facility for Python.
# Copyright (C) 2008, Richard Landau.  All rights reserved.
# Evolved from old PDP-11, C, C++, VB, Perl, and other similar trace facilities 
#  that I have done over the years.  
# 
# Usage: 
# Set environment variables, if necessary, to specify the desired 
#  level of detail, target (stdout or file), and filename, if necessary.  
#   SET TRACE_LEVEL=3
#   SET TRACE_TARGET=4
#   SET TRACE_FILE="c:\trace file goes here for ease of finding.log"
# Instantiate the NewTrace object and store it global static so that any 
#  module can use it.  E.g., 
#       gt As NewTrace = New NewTrace   (VB)
#       TRC = NewTrace()                (Python)
# Call the trace() method of that instance, giving detail level number
#  and string.  E.g., 
#       gt.trace(1,"This is an item at level 1")
#       TRC.trace(2,"This is an item at level 2")
#       TRC.tracef(3,"FOO","The FOO facility says hi at level 3")
# If the TRACE_LEVEL specified in the program's environment is 
#  greater than or equal to the detail level specified in the call, 
#  then the string will be printed to the trace log.  
# If the tracef() method is used, then additionally, the facility string
#  specified in the call must match one of the facilities requested
#  in the TRACE_FACIL environment variable.  If TRACE_FACIL is "ALL" or 
#  the empty string ("") or null (not defined), then all facilities 
#  match, and will be traced.  
# Additionally, the facility list may explicitly include and exclude 
#  some facilities.  
# Examples:
#   ""                  traces all named facilities
#   "ALL"               traces all named facilities
#   "NONE"              traces no named facilities
#   "ALL -A"            traces all named facilities except facility A
#   "NONE A"            traces only facility A
## Trace calls using trace() with no facility name are always included.  
# 
# A trace output line looks like 
#       YYYYMMDD_HHMMSS L  user-specified string
#  or 
#       YYYYMMDD_HHMMSS L FACIL user-specified string
# HTML output is slightly different, includes a "<BR>" at the start 
#  of each line.  
#   HH is 24-hour hour.
#   L is the level of detail specified for this trace line.
# 
# Environment variables used by trace() are
#   TRACE_LEVEL, TRACE_TARGET, and TRACE_FILE.  
#   TRACE_LEVEL is mandatory, the others optional.  Explanations below.  
# 
# Typical use of trace levels is:
# 0     Messages that always should be printed, e.g., errors that 
#       the user must see.
# 1     Entries to functions, with arguments listed.
#       Any internal error conditions or error exits from 
#       functions, with status.  
# 2     Normal exits from functions, with status and maybe output arg values.  
# 3     Things that happen once per record, once per line, etc., 
#       that are repeated often, big-O the number of lines in the file
#       or messages in the stream.  
# 4     Really detailed info, such as syntax cracking of input lines, 
#       entries in data structures, and such, that happen once or more
#       per line.  
# 5     Really, really detailed info, such as routine accesses to 
#       data structures.
# 
# Contents of environment veriables:
# TRACE_LEVEL;   # integer: levels 0 (or absent) thru 5.  
#               If null, defaults to zero.  
# TRACE_TARGET;  # mask: target bits 1=print to stdout, 
#               2=print html to stdout, 4=print to file.
#               If null, defaults to 1 (print on stdout).  
# TRACE_FILE;    # file: name of log file to trace into.
#               If null, defaults to "./newtrace.log".
# TRACE_FACIL;   # list of facility names to be traced.
#               Normally a comma-separated list of 
#               facility names that will be included in
#               results of the tracef() call.
#               If "ALL", then all facilities will be
#               included.  If "NONE" then no facilities
#               will be included.  
#               Facilities can be explicitly included after
#               NONE, e.g., "NONE FOO".
#               Facilities can be explicitly excluded after 
#               ALL, e.g., "ALL -FOO".
#               If null, then ALL is assumed.
#


'''
Still need to add start line to init if TRACE_LEVEL>0.
All the others do that.  
'''


class CNewTrace:
    def __init__(self):
        self.setDefaults()

    def setDefaults(self,mylevel=0,mytarget=1,myfile="newtrace.log",myfacil=""):
        self.tracelevel = mylevel
        try:
          self.tracelevel = int(environ["TRACE_LEVEL"])
        except KeyError:
            pass
        self.tracetarget = mytarget
        try:
          self.tracetarget = int(environ["TRACE_TARGET"])
        except KeyError:
            pass
        self.tracefile = myfile
        try:
          self.tracefile = environ["TRACE_FILE"]
        except KeyError:
            pass
        self.tracefacil = myfacil
        try:
          self.tracefacil = environ["TRACE_FACIL"].upper()
        except KeyError:
            self.tracefacil = ""
            pass
        if self.tracelevel > 0:
            self.trace(1,"DEBUG info level %s targets %s facil %s" \
                % (self.tracelevel,self.tracetarget,self.tracefacil) )

    def trace(self, level, line):
        # If we are tracing at a high enough level to include this item, 
        #  then send it to the appropriate target(s).
        if level <= self.tracelevel:
            # Get a timestamp
            vecT = localtime()
            (yr,mo,da,hr,min,sec,x,y,z) = vecT
            ascT = "%4d%02d%02d_%02d%02d%02d" % (yr,mo,da,hr,min,sec)
            linestart = ascT + " " + "%1d"%level + " "
            
            # If console only, or console and others, print to stdout.
            if ((self.tracetarget & 1) and not (self.tracetarget & 2)) \
              or not (self.tracetarget & 6):
                print linestart + " " + line
            
            # If HTML format, add line break.
            if (self.tracetarget & 2):
                print "<br>" + linestart + " " + line
            
            # Or append to trace file.
            if (self.tracetarget & 4):
                # append to file
                f = file(self.tracefile, "a")
                f.write(linestart + " " + line + "\n")
                f.close()          

    def tracef(self, level, facility, line):
        # If we are tracing at a high enough level to include this item, 
        #  then send it to the appropriate target(s).
        if level <= self.tracelevel:
            # Now assess the facility: include Y or N?
            self.facilcaps = facility.upper()
            # If NONE, then the answer is probably No.  
            if self.tracefacil.find("NONE") >= 0:
                self.traceme = False
            # If ALL or mentioned explicitly, then the answer is probably Yes.  
            if self.tracefacil == "" \
            or self.tracefacil.find(self.facilcaps) >= 0 \
            or self.tracefacil.find("ALL") >= 0:
                self.traceme = True
            # If explicitly excluded, then the answer is definitely No.  
            if self.tracefacil.find(("-"+self.facilcaps)) >= 0:
                self.traceme = False
            if self.traceme:
                # Get a timestamp
                self.vecT = localtime()
                (self.yr,self.mo,self.da,self.hr,self.min,self.sec,\
                    self.x,self.y,self.z) \
                    = self.vecT
                self.ascT = "%4d%02d%02d_%02d%02d%02d" \
                    % (self.yr,self.mo,self.da,self.hr,self.min,self.sec)
                self.linestart = "%s %1d %-5s " % (self.ascT,level,facility)
                # If console only, or console and others, print to stdout.
                if ((self.tracetarget & 1) and not (self.tracetarget & 2)) \
                  or not (self.tracetarget & 6):
                    print self.linestart + " " + line
                
                # If HTML format, add line break.
                if (self.tracetarget & 2):
                    print "<br>" + self.linestart + " " + line
                
                # Or append to trace file.
                if (self.tracetarget & 4):
                    # append to file
                    f = file(self.tracefile, "a")
                    f.write(self.linestart + " " + line + "\n")
                    f.close()          

# Now, for the convenience of the lazy, populate a 
#  globally accessible instance that can be used with
#  no further action required.
#  If the user really wants a particular facility name, 
#  make another instance or use setFacility.
TRC = CNewTrace()
