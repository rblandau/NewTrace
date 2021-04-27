# NewTrace Debugging Facility for Python

(not to be confused with the Python "trace" facility)

## Abstract

NewTrace is an offline debugging facility that takes the place of all those icky print() statements that get sprinkled throughout code.  It produces a list of compact, consistently formatted lines that can be used to follow the logic and the progress of data in a program.  

This facility provides 

- decorators `@ntrace` and `@ntracef` for displaying function entry and exit, with arguments and return value for all functions and classname for bound member functions.  

- functions `ntrace()` and `ntracef()` for displaying data and location whenever needed.  

This code works with Python versions 2 and 3.  

## Ten-cent Tutorial Tour

We have all sprinkled print statments through our code to observe what the code is actually doing at runtime.  This facility is a greatly improved version of that type of printing.  

Using the NewTrace facility, if you simply change your debugging print statement from

    print("some information that will help me understand this")

to 

    NTRC.ntrace(3, "some information that will help me understand this")

your debug printing will immediately receive the following advantages.

- You can turn the debug printing ON and OFF *without editing the source code*.

- You can print to a log file instead of stdout *without editing the source code*.

- You can choose the level of detail that you want to see printed *without editing the source code*.  

These changes can be controlled by defining system environment variables without the need to edit the source code.  For example, 

    export TRACE_LEVEL=3
    export TRACE_LOG=./mydebuglogfile.log
    # on Linux or Cygwin/Windows bash

or 

    set TRACE_LEVEL=3
    set TRACE_LOG=.\mydebuglogfile.log
    # on Windows cmd

will turn on debug printing and send the output to a log file you can examine later.  The log file is, of course, optional; normally NewTrace debug printing goes to stdout.  

And un-defining the same environment variables will turn off debug printing.  

Note: Yes, your program has to import some code from the NewTrace module.

    from NewTrace import NTRC

And the NewTrace facility also has decorators for functions that will print entry and exit from a function, including input arguments and return value.  These are controlled by the same environment variables.  

Simply add a decorator to your function definition

    @ntrace
    def myfunction(someargs):
     . . . 

Note: Yes, the decorator definition must be imported.

    from NewTrace import ntrace

It's as easy as all that.  


## Intended Use Caveat

This facility is **not** intended to do the same job as the Python logging facility.  It **is** intended to be a permanently-installed tracelog function for debugging running code.  This may be useful during initial development and during deployment and production use, should problems arise.  

Use it as you would print() statements that you use to debug code, but leave it installed permanently in the production code and just turn it off with appropriate environment variables.  

## History

NewTrace tracelog facility for Python 2 and 3.

Copyright (C) 2008-2021, Richard Landau.  All rights reserved.

Evolved from old, really old PDP-11 assembler code, C, C++, VB, Perl, Java, and other 
similar trace facilities that I have done over the years.  

The basic functions of this facility originated in 1978-1979 as a tool for monitoring and debugging 
multiprocessing interactions in communication and transaction processing systems.  Many details have been improved (one-plussed) 
in minor ways over several decades.  The current version for Python may be thought of as `print()` on steroids, with a lot of optimizations.  

The idea is to print relatively fixed-format lines with a  standard timestamp, a priority level, a source facility,  and whatever information would be useful at that point.  

Tracing is enabled and controlled through environment variables, so that it may be turned on or off, subsetted, etc., **without any source code changes**.  

Output may be filtered by priority number and facility name.

## Control by Environment Variables

Set environment variables, if necessary, to specify the desired  level of detail, target (stdout or file), and filename, if necessary.   No source code change is needed to turn tracing on and off,  or to redirect it to a file; only changes to the running process environment.  

    Examples:
    
    export TRACE_LEVEL=3
    export TRACE_TARGET=4
    export TRACE_FILE="/var/trace file goes here for ease of finding.log"

(Use `export` for \*NIX and Cygwin systems; use `SET` for vanilla Windows.)

## Supplied Singleton Instance

During import, the module instantiates a singleton instance of the NewTrace class.  The `ntrace()` and `ntracef()` functions are accessible as member methods of this class using the instance.  

The singleton instance is named `NTRC`.  Call the `ntrace()` functions as members of this instance:

    `NTRC.ntrace(priority, string)`
    `NTRC.ntracef(priority, facility, string)`

### Examples

Call the `ntrace()` method of that instance, giving detail level number
 and string.  E.g., 

      NTRC.ntrace(1, "This is an item at level 1")
      NTRC.ntrace(2, "This is an item at level 2")
      NTRC.ntracef(3, "FOO", "The FOO facility says hi at level 3")
      NTRC.ntrace(5, "Way too much detail at level 5!"

If the `TRACE_LEVEL` specified in the program's environment is  greater than or equal to the detail level specified in the call, then the string will be printed to the trace log.  

## Using Facility Codes

If the `ntracef()` method is used, then the facility string specified in the call must match one of the facilities requested in the `TRACE_FACIL` environment variable (if there is such a variable).  

- If `TRACE_FACIL` is "ALL" or 
the empty string ("") or null (not defined) or indecipherable, then  all facilities match, and all will be traced.  This is the default.

- The `ntrace()` method alone prints a blank facility code.

## Filtering by Facility Codes

The facility list may explicitly include and exclude some facilities.  The words `ALL` and `NONE` and the operators `+` and `-` may be used to specify the facilities desired.  

Examples of the values of `TRACE_FACIL`:

-  `""`                   traces all named facilities
-  `"ALL"`                traces all named facilities
-  `"NONE"`               traces no named facilities, only unnamed ones
-  `"ALL-A"` or `"all-a"`     traces all named facilities except facility A
-  `"NONE+A"` or `"none+a"`    traces only facility A
-  `"INDECIPHERABLECRUD"` traces all named facilities.

Trace calls using `ntrace()` with no facility name are always printed.  

Personally, I tend to restrict facility codes to a maximum length (in my case, four characters), again so that successive lines will have various fields aligned for easier recognition and searching.  

Note that if you want only, say, facility FOO, then you must use

    export TRACE_FACIL=NONE+FOO

to prevent other facilities from being listed.  

## Output Lines

A trace output line looks like 

      YYYYMMDD_HHMMSS L      user-specified string
 or 

      YYYYMMDD_HHMMSS L FCIL user-specified string

where "L" is the detail level/priority, and "FCIL" is the facility code given in the `ntracef()` call.  The "user-specified string" is printed exactly as given in the call.  

HTML output is slightly different, includes a `<BR>` tag at the start 
of each line.  

The time is always given in 24-hour format.

## Controlling With Environment Variables

Environment variables used by `trace()` are

- `TRACE_LEVEL` 
- `TRACE_TARGET` 
- `TRACE_FILE`
- `TRACE_TIME` and 
- `TRACE_PRODUCTION`.  
  
  `TRACE_LEVEL` is mandatory; the others optional.  Explanations below.  

## Trace Detail Levels

Typical use of trace levels is:

- **0**     
    Messages that must always be printed, e.g., errors that the user must see.

- **1**     
    Entries to functions, with arguments listed. Any internal error conditions or error exits from  functions, with status.  
- **2**     
    Formerly used for normal exits from functions, with status and maybe output arg values.  Currently function exits are traced at level=1.

- **3**     
    Things that happen once per record, once per line, etc.,  that are repeated often, big-O the number of lines in the file or messages in the stream.  

- **4**     
    Really detailed info, such as syntax cracking of input lines,  entries in data structures, and such, that happen once or more per line.  

- **5**     
    Really, really detailed info, such as routine accesses to  data structures.

## Contents of Environment Variables

Contents of environment variables:

`TRACE_LEVEL`    
    integer: levels 0 (or absent) thru 5 (or more).  
If null, defaults to zero.  

`TRACE_TARGET`   
    bitmask: target bits 1=print to stdout, 
2=print html to stdout, 4=print to file.
If null, defaults to 1 (print on stdout).  \[Yes, this is crude; will come up with a better syntax RSN.\]

`TRACE_FILE`     
    file: name of log file to trace into.
If null, defaults to "./newtrace.log".

`TRACE_FACIL`    
    list of facility names to be traced.
Normally a blank-separated list of 
facility names that will be included in
results of the tracef() call.

- If "ALL", then all facilities will be
included.  If "NONE" then no facilities
will be included.  
- Facilities can be explicitly included after
NONE, e.g., "NONE FOO" or "NONE +FOO".
- Facilities can be explicitly excluded after 
ALL, e.g., "ALL -FOO".
If null, then ALL is assumed.

Details above.  

`TRACE_PRODUCTION`  
    If "YES" then nothing will be traced, and the  trace functions and decorators will attempt  to use as little CPU resource as possible.  However, trace calls with priority zero will still be printed.

`TRACE_TIME`    
    If nonempty, timestamps will include milliseconds.

## Python decorators

There are two functions to use as Python decorators to report entry and exit of functions, including calling arguments in and return value out, painlessly.  

Input argument names cannot be identified by the decorator version of `ntrace()` and `ntracef()`.  If you need individual identification  of input arguments, call the trace manually, as in the old days.  

    @ntrace                     for calls with no facility code attached
    @ntracef("ABCD")            for calls associated with a facility ABCD
    @ntracef("ABCD", level=5)   for calls with facility code and detail priority level

As usual, the facility code should be max four letters to preserve alignment and should be all caps for legibility.  The `@ntrace` decorator prints entry at level 1 and exit at level 2.

The `@ntracef()` decorator also supports an optional level argument to change the trace level of the entry and exit lines.  This can be specified  positionally or keyword, e.g., `@ntracef("FOO",2)` or `@ntracef("FOO",level=2)`.

The `@ntrace` decorator does not support the level argument; but note that
 the facility on `@ntracef()` can be left blank, e.g., `@ntracef("",5)`.  

The `@ntracef` decorator processes the first function argument specially if  the argument is an instance pointer (usually `self` in class  methods).  In this case, it prints the classname, and the  instance's `self.ID` attribute if it exists, on both entry and exit.  The class name and the ID attribute are much more informative than the hex address.  

## Examples

Summary examples in Python:

    from NewTrace import NTRC, ntrace, ntracef

    NTRC.ntrace(3, "some string with %s %s" % ("some", "substitutions"))

    NTRC.ntracef(3, "ABCD", "some string with %s %s" % ("some", "substitutions"))

Of course, any method of substituting values into the output string can be used.  

## Production Mode

To minimize CPU time consumed by ntrace calls in the code, there is a production mode that eliminates most of the trace code.  

The decorators `@ntrace` and `@ntracef`can be nulled out with the environment variable
    `TRACE_PRODUCTION=YES`  
This will also cause direct calls to the `ntrace()` and `ntracef()` functions
to return with as little work as possible.  

## Time Resolution: Seconds or Milliseconds

If the environment variable `TRACE_TIME` is nonempty string or nonzero integer, timestamps will include milliseconds in the format `YYYYMMDD_HHMMSS.mmm`.


## Future improvements desired

* FIXME: HTML output to specify prefix and suffix strings.  Currently only <br/> prefix, but some user might want more.

    Probably leave \<br/\> as the default if HTML but not otherwise specified.

* FIXME: production mode should permit Y as well as YES.

    do getenv(...).upper().startswith("Y") instead of =="YES" currently.

* FIXME: optimize yes/no checking of facility name.

    Probably lists or dictionaries of names with 0/1 answers, 
added as they are encountered during run.  Not very common but might be good anyway. 

* FIXME: thread-safe.

    Thread lock anytime state is changed, e.g., printing.

* FIXME: multiprocessor-safe.

    Don't know how to guarantee this across operating systems:
Windows, several Linices.  

* FIXME: find better syntax than TRACE_TARGET bitmask.

    And make sure that TRACE_FILE is used if it is nonempty 
regardless of the bitmask.  




