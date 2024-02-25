# pandas library is used to read the excel file

import pandas as pd
try:
    # pass the excel location to dataframe
    df = pd.read_excel("student_record.xlsx") 
    print()
    print('***************************************')
    print('Student Result Application') 
    print('***************************************')  
except FileNotFoundError:
    print("File not Found")

#extract dataframe to dictionary
student_grades = {}
# unpack the content of df
for val in df.values:
    #convert val to tuple data type
    student_id,name,math,english, physics,chemistry = val
    #store record in dictionary data type
    student_grades[student_id]= [name,math,english, physics,chemistry]
print()

student_response = input("Please type your student id(e.g s****): ")
student_response = student_response.casefold()
print("\n --------- Student Record -----------\n")

if student_response in student_grades.keys():
    print(' {0} grades are as follows:\n \
        \n Mathematics - {1} \
        \n English - {2} \
        \n Physics - {3} \
        \n Chemistry - {4}'.format(student_grades[student_response][0],\
        student_grades[student_response][1],student_grades[student_response][2],\
            student_grades[student_response][3],student_grades[student_response][4]))
  
    print("\n------------------------------------")