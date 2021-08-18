# NewTrace Debugging Facility for Python

(not to be confused with the Python "trace" facility)

   Copyright (c) 2004-2021, Richard Landau


## Abstract

NewTrace is an offline debugging facility that takes the place of all those print() statements that get sprinkled throughout code, and then later have to be commented out or removed.  This facility produces a list of compact, consistently formatted lines that can be used to follow the logic and the progress of data in a program.  

This facility provides 

- decorators `@ntrace` and `@ntracef` for displaying function entry and exit, including arguments and return value for all functions and classname for bound member functions.  

- functions `ntrace()` and `ntracef()` for displaying data and location whenever needed.  

This code works with Python versions 2 and 3.  


## Ten-cent Tutorial Tour

We have all sprinkled print() statments through our code to observe what the code is actually doing at runtime.  This facility is a greatly improved version of that type of printing.  

Using the NewTrace facility, if you simply change your debugging print() statement from

    print("some information that will help me understand this")

to 

    NTRC.ntrace(3, "some information that will help me understand this")

your debug printing will immediately receive the following advantages.

- You can turn the debug printing ON and OFF *without editing the source code*.

- You can print to a log file instead of stdout *without editing the source code*.

- You can choose the level of detail that you want to see printed *without editing the source code*.  

- Every line will include a date-and-time stamp.

The string to be printed may be any string that would work with print(); the string is evaluated before the ntrace() function is called.  

Even easier than that, you can place a decorator on the definition of any function that you wish to watch, and NewTrace will print debugging information about that function every time it is called.  On entry, it will print the function name and its incoming arguments; on exit it will print the function name and the returned value(s), if any.  

As a trivial example, adding just one line of decorator call to a function definition yields useful information at runtime.   

    @ntrace
    def absolute_value(num):
        """ This function returns the absolute
            value of the entered number."""
        if num >= 0:
            return num
        else:
            return -num
    num = -4
    print(f'The absolute value of {num} is {absolute_value(num)}')

results in the output:

    20210818_133839 1       entr absolute_value args=(-4,),kw={}
    20210818_133839 1       exit absolute_value result|4|
    The absolute value of -4 is 4

Additionally, if the function is a bound member function of a Python class, the printing will include the class name and, optionally, an identifier of the particular instance.  

The debug printing can be controlled by defining system environment variables *without the need to edit the source code*.  For example, simply set an environment variable that tells NewTrace how much detail to print.

    export TRACE_LEVEL=3
    # on Linux or Cygwin/Windows bash

or 

    set TRACE_LEVEL=3
    # on Windows cmd

will turn on debug printing and send the output to stdout (by default).  Optionally, you can send the output to a log file that you can examine later.  This is accomplished with another simple environment variable, as described below.  (And the use of the number 3 is also described below.)  

Un-defining the same environment variables will turn off debug printing, again *without the need to edit the source code*.  

Note: Yes, your program has to import some code from the NewTrace module, again, just one line.

    from NewTrace import NTRC, ntrace, ntracef

The NewTrace facility function decorators use the same debug printing functions and so are controlled by the same environment variables.  

It's as easy as all that.  


## Intended Use Caveat

This facility is **not** intended to do the same job as the Python logging facility.  It **is** intended to be a permanently-installed tracelog function for debugging running code.  This may be useful during initial development and during deployment and production use, should problems arise.  

Use it as you would print() statements that you use to debug code, **but leave it installed permanently in the production code and just turn it off with appropriate environment variables**.  The overhead is very, very small.  


## History

NewTrace tracelog facility for Python 2 and 3.

Copyright (C) 2008-2021, Richard Landau.  All rights reserved.

Evolved from old, really old PDP-11 assembler code, C, C++, VB, Perl, Java, and other 
similar trace facilities that I have done over the years.  

The basic functions of this facility originated in 1978-1979 as a tool for monitoring and debugging 
multiprocessing interactions in communication and transaction processing systems.  Many details have been improved (one-plussed) 
in minor ways over several decades.  The current version for Python may be thought of as `print()` on steroids, with a lot of optimizations.  

The idea is to print relatively fixed-format lines with a  standard timestamp, a priority level, a source facility,  and whatever information would be useful at that point.  

Tracing is enabled and controlled through environment variables, so that it may be turned on or off, subsetted, redirected, etc., **without any source code changes**.  

Output may be filtered by priority number and facility name.


## Control by Environment Variables

Set environment variables, if necessary, to specify the desired  level of detail, target (stdout or file), and filename, if necessary.   No source code change is needed to turn tracing on and off, or to redirect it to a file.  You need change only the running process environment.  

    Examples:
    
    export TRACE_LEVEL=3
    export TRACE_TARGET=4
    export TRACE_FILE="/var/trace file goes here for ease of finding.log"

(Use `export` for Linux, \*NIX, and Cygwin systems; use `SET` for vanilla Windows.)


## Supplied NTRC Object Instance

During import, the module instantiates an instance of the NewTrace class.  The `ntrace()` and `ntracef()` functions are accessible as member methods of this class using the instance.  

The singleton instance is named `NTRC`.  Call the `ntrace()` functions as members of this instance:

    NTRC.ntrace(priority, string)           or
    NTRC.ntracef(priority, facility, string)


### Examples

Call the `ntrace()` method of that instance, giving detail level number
 and string.  E.g., 

      NTRC.ntrace(1, "This is an item at level 1")
      NTRC.ntrace(2, "This is an item at level 2")
      NTRC.ntracef(3, "FOO", "The FOO facility says hi at level 3")
      NTRC.ntrace(5, "Way too much detail at level 5!"

If the `TRACE_LEVEL` specified in the program's environment is  greater than or equal to the detail level specified in the call, then the string will be printed to the trace log.  


## Using Facility Codes

If the `ntracef()` method is used, then a facility code string becomes part of the information to be printed.  The printing of NewTrace output can be filtered by the facility code string.  

If the facility string specified in the `ntracef()` call matches one of the facilities requested in the `TRACE_FACIL` environment variable, then the debug printing will be included in the output.  See the description below of the filtering method.  

The use of facility codes is purely optional.  If you do nothing, all `ntrace()` and `ntracef()` calls will print.   

- If `TRACE_FACIL` is "ALL" or 
the empty string ("") or null (not defined) or indecipherable, then all facility codes match, and all will be traced.  This is the default.  If you do nothing special, then all facility codes will print.  

- The `ntrace()` method alone prints an empty facility code, and therefore is always included in the printing.  


## Filtering by Facility Codes

The facility list may explicitly include and exclude some facilities.  The words `ALL` and `NONE` and the operators `+` and `-` may be used to specify the facilities desired.  

Examples of the values of `TRACE_FACIL`:

- If the `TRACE_FACIL` environment variable is not defined, then all facilities are traced.  
-  `""`                   traces all named facilities
-  `"ALL"`                traces all named facilities
-  `"NONE"`               traces no named facilities, only unnamed ones
-  `"ALL-A"` or `"all-a"`     traces all named facilities except facility A
-  `"NONE+A"` or `"none+a"`    traces only facility A
-  `"INDECIPHERABLECRUD"` traces all named facilities.

Please note that trace calls using `ntrace()` with no facility name are *always* printed.  

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

## Controlling Output With Environment Variables

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
    Reserved for messages that must always be printed, e.g., errors that the user must see.  If you call `ntrace()` or `ntracef()` with a level declaration of zero, the string will always be printed.  

- **1**     
    Reserved for entries to functions, with arguments listed, and exits from functions.  Any internal error conditions or error exits from functions, with status.  

- **2**     
    Formerly used for normal exits from functions, with status and maybe output arg values.  No longer reserved.  Currently function entries and exits are traced at level=1.

- **3**     
    Things that happen once per record, once per line, etc., that are repeated often, big-O the number of lines in the file or messages in the stream.  Most common debug printing occurs at level=3.  

- **4**     
    Really detailed info, such as syntax cracking of input lines, entries in data structures, and such, that happen once or more per line.  

- **5**     
    Really, really detailed info, such as routine accesses to  data structures.


## Contents of Environment Variables

Contents of environment variables:

`TRACE_LEVEL`   
    integer: levels 0 thru 5 (or more).  
If absent or null, defaults to zero.  

`TRACE_TARGET`   
    bitmask: target bits 1=print to stdout, 
2=print html to stdout, 4=print to file.
If null, defaults to 1 (that is, print on stdout).  \[Yes, this is crude; may come up with a better syntax RSN.\]

`TRACE_FILE`     
    file: name of log file to trace into.
If null, defaults to "./newtrace.log".

`TRACE_FACIL`    
    list of facility names to be traced.

- If "ALL", then all facilities will be
included.  
- If "NONE" then no named facilities will be included.  
- Facilities can be explicitly included after NONE, e.g., "NONE FOO" or "NONE +FOO".
- Facilities can be explicitly excluded after 
ALL, e.g., "ALL -FOO".
If null, then ALL is assumed.

Details above.  

`TRACE_PRODUCTION`  
    Turns on "production mode," which minimizes the resources used by tracing.  If "YES" then nothing will be traced, and the trace functions and decorators will attempt to use as little CPU resource as possible.  However, trace calls with priority zero will still be printed.

`TRACE_TIME`    
    Turns on high-resolution timestamps.  If nonempty, timestamps will include milliseconds.

`TRACE_HTML`      **NEW** **NEW** **NEW**    
    If nonempty, specifies HTML tags to precede and follow the string to be traced.  The variable should contain a string of the form "begintag|endtag", to separate the beginning and ending strings.  The vertical bar is required and cannot be escaped.  The default string is "\<br\>| ", which results in the default beginning and ending tags "\<br\>" and "".  Note that this HTML processing occurs *only if* the TRACE_TARGET=2.  


## Python decorators

There are two functions to use as Python decorators to report entry and exit of functions, including calling arguments in and return value out, painlessly.  

The decorator lists the tuple of input arguments and the keyword arguments.  

Input argument names (used in the function's source code) are not identified by the decorator version of `ntrace()` and `ntracef()`.  If you need individual identification of input arguments, you can call `NTRC.ntrace()` manually, as in the old days.  

    @ntrace                     for calls with no facility code attached
    @ntracef("ABCD")            for calls associated with a facility ABCD
    @ntracef("ABCD", level=5)   for calls with facility code and high-detail priority level

As usual, the facility code should be max four letters to preserve alignment and should be all caps for legibility in the output listing.  The `@ntrace` decorator prints function entry and exit at level=1.

The `@ntracef()` decorator also supports an optional level argument to change the trace level of the entry and exit lines.  This can be specified  positionally or keyword, e.g., 

    @ntracef("FOO",2)          or 
    @ntracef("FOO",level=2).

The `@ntrace` decorator does not directly support the level argument; but note that the facility on the `@ntracef()` decorator can be empty, e.g., `@ntracef("",5)`.  

The `@ntrace` and `@ntracef` decorators processes the first function argument specially **if** the argument is an instance pointer (usually `self` in class  methods).  In this case, it prints the classname, and the  instance's `self.ID` attribute, if it exists, on both entry and exit.  The class name and the ID attribute are much more informative than the hex address of the instance would be.  


## Examples

Summary examples in Python:

    from NewTrace import NTRC, ntrace, ntracef

    NTRC.ntrace(3, "just some plain string")
    
    NTRC.ntrace(3, "some string with %s %s" % ("two", "substitutions"))

    NTRC.ntracef(3, "ABCD", "some string with %s %s" % ("two", "substitutions"))

    NTRC.ntrace(3, "some string with {} {}".format("two", "substitutions")

Of course, any method of substituting values into the output string can be used.  

- Old, C-style `%s`, `%d`, etc. substitutions with the `%` binary operator
- `.format()` substitutions
- `f-string` substitutions

As mentioned previously, the string is evaluated and sustitutions performed before the trace functions are called.  


## Production Mode

To minimize CPU time consumed by ntrace calls in the code, there is a production mode that eliminates most of the trace code.  

The decorators `@ntrace` and `@ntracef`can be nulled out with the environment variable
    `TRACE_PRODUCTION=YES`  
This will also cause direct calls to the `ntrace()` and `ntracef()` functions
to return with as little work as possible.  

**Note well**: this environment variable is evaluated at **compile** **time** and results in different byte code being generated by CPython.  When you change into or out of production mode, delete all the .pyc files to force recompilation.  


## Time Resolution: Seconds or Milliseconds

If the environment variable `TRACE_TIME` is nonempty string or nonzero integer, timestamps will include milliseconds in the format `YYYYMMDD_HHMMSS.mmm`.


## How I Use NewTrace Myself

I've written a lot of Python using this facility for debugging, and I don't regret any of it.  Feel free to examine any of my code using this.  Examples can be found in 

- `github.com/rblandau/NewTrace`
- `github.com/rblandau/code-line-count`
- `github.com/rblandau/inetpub`
- `github.com/MIT-Informatics/PreservationSimulation/shelf`

My personal usage model, not perfect but based on long experience:

- Use an `@ntrace` or `@ntracef` decorator on *every* function.  Yes, every.  Just reflex now.  
- Most of the time, use `@ntracef()` with a facility name, four capital letters, so that I can examine or eliminate all calls to that facility using the filtering of `TRACE_FACIL`. 

- Trace almost all normal information at level=3.  Rarely, use level=4 for a higher level of detail, usually relating to regexes or other parsing operations.  
- Most significant decision points in functions have a level=3 trace telling which way the decision went, how the parsing succeeded or failed, etc.  Include the relevant data items: output that worked, and especially input and output that didn't work.
- Most of the time, when tracing is turned on, examine the output with `less` or similar good text browsing utility.  This makes it easy to search for function names, data values, and so forth.
- When something works, sort of, or more or less as expected, save a trace log to a file for future reference.  Easy to do this by redirecting output with `>`.  This also correctly interleaves the program's normal output and the trace output.  If I redirect the trace output to a file with `TRACE_OUTPUT`, then the normal output is separate and asynchronous.  
- If the program also uses `stderr`, then I have to remember to do 

        `python3 . . . 2>&1 | less`    
    to force the `stderr` stream to interdigitate with the `stdout` streams of the program and the trace.  If there are errors of any sort -- syntax, key errors, data not found, things like that -- these also come on `stderr`.

- It is often reassuring to go through a trace log in detail to see that it actually did what I thought it was supposed to do.  This is especially helpful if it is calculating something to which I do not know the answer beforehand.  

- Leave all the trace code in the source code, even for heavily CPU-intensive applications such as discrete event simulations.  
- When doing real production work, turn on `TRACE_PRODUCTION` and run that way.  Seems to save a few percent on CPU time.  

- A few small shell scripts to turn tracing on and off are helpful.  My typing is not perfect.  


## Future improvements desired

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




