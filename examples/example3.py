# example3.py
# Small program with decorated function, inline trace, and *args.

from NewTrace import ntrace, NTRC

@ntrace
def greet2(*names):
    NTRC.ntrace(3, f"proc namelist={names!r}")
    print('Hello', end='')
    for name in names:
        print(', ' + name, end='')
    print(':')
        

greet2('Steve', 'Bill', 'Yash') 
greet2('Steve', 'Bill', 'Yash', 'Kapil', 'John', 'Amir') 

