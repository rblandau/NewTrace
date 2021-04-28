# example2.py
# Simple example of function with decorator.

from NewTrace import ntrace

@ntrace
def absolute_value(num):
    """ This function returns the absolute
        value of the entered number."""
    if num >= 0:
        return num
    else:
        return -num


num = 2
print(f'The absolute value of {num} is {absolute_value(num)}')
num = -4
print(f'The absolute value of {num} is {absolute_value(num)}')

