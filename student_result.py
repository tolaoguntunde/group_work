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

#request student id to pull record
student_response = input("Please type your student id(e.g s****): ")
#request student email to send the result
student_email = input("Please type student email address: ")
student_email = student_email.casefold() #this will convert email address to lowercase
student_response = student_response.casefold()
print("\n --------- Student Record -----------\n")

#print student result to cmd
if student_response in student_grades.keys():
    print(' {0} grades are as follows:\n \
        \n Mathematics - {1} \
        \n English - {2} \
        \n Physics - {3} \
        \n Chemistry - {4}'.format(student_grades[student_response][0],\
        student_grades[student_response][1],student_grades[student_response][2],\
            student_grades[student_response][3],student_grades[student_response][4]))
  
    print("\n------------------------------------")

else:
    print('Student record not found, please check the student id and try again')


#TO DO
#Update code such that if wrong student id is entered, prompt user for another student id
#Refactor to use function where possible
#Import library that would alloe connection to email: Connect to gmail or other email account to send the result
#Are we sending the result as an attachment or should it go in the body of the email

