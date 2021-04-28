# example1.py
# program to display student's marks from record

from NewTrace import NTRC
import random

marks = {'James': 90, 'Jules': 55, 'Arthur': 77}
student_list = list(marks.keys())
# Include a ringer, a name that is not in the dictionary, to test for failure.
student_list.append('Soyuj')

# Pick a student at random from the list.
student_name = student_list[random.randrange(len(student_list))]
print("Looking for grades of student " + student_name)

# Look through the list one by one, the hard way.
# (The easy way would be getattr() or try-except.)
for student in marks.keys():
    NTRC.ntrace(3, f'found {student}, looking for {student_name}')
    if student == student_name:
        print(f"Marks for student {student_name} = {marks[student]}")
        break
else:
    print(f'No entry found for the name: {student_name}.')

