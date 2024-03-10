# # pandas library is used to read the excel file

# import pandas as pd
# from email.message import EmailMessage
# import ssl
# import smtplib



# try:
#     # pass the excel location to dataframe
#     df = pd.read_excel("student_record.xlsx") 
#     print()
#     print('*************')
#     print('Student Result Application') 
#     print('*************')  
# except FileNotFoundError:
#     print("File not Found")

# #extract dataframe to dictionary
# student_grades = {}
# # unpack the content of df
# for val in df.values:
#     #convert val to tuple data type
#     student_id,name,math,english, physics,chemistry = val
#     #store record in dictionary data type
#     student_grades[student_id]= [name,math,english, physics,chemistry]
# print()

# #request student id to pull record
# student_response = input("Please type your student id(e.g s**): ")
# #request student email to send the result
# student_email = input("Please type student email address: ")
# student_email = student_email.casefold() #this will convert email address to lowercase
# student_response = student_response.casefold()
# #print("\n --------- Student Record -----------\n")

# #print student result to cmd
# if student_response in student_grades.keys():
#   result = ' {0} grades are as follows:\n \
#         \n Mathematics - {1} \
#         \n English - {2} \
#         \n Physics - {3} \
#         \n Chemistry - {4}'.format(student_grades[student_response][0],\
#         student_grades[student_response][1],student_grades[student_response][2],\
#             student_grades[student_response][3],student_grades[student_response][4])


# else:
#   result ='Student record not found, please check the student id and try again'


# #creating email sender login and password
# email_sender = "projectcomputer83@gmail.com"
# email_password = "pdup sfin zntl rbto"

# email_receiver = student_email
# subject = "Final year result"
# body = result

# em = EmailMessage()
# em["From"] = email_sender
# em["To"] = email_receiver
# em["Subject"] = subject
# em.set_content(body)

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#   smtp.login(email_sender, email_password)
#   smtp.sendmail(email_sender, email_receiver, em.as_string())

import requests
r = requests.get('https://')