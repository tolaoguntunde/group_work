# pandas library is used to read the excel file
import argparse
import logging
import logging.config
from configs.configs import GMAIL_CONFIGS
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

logging.config.fileConfig('configs/logger.conf')
logger = logging.getLogger('student_app')

def read_student_records():
    try:
    # pass the excel location to dataframe
        df = pd.read_excel("student_record.xlsx") 
        print()
        print('***************************************')
        print('Student Result Application') 
        print('***************************************')  
        return df
    except FileNotFoundError:
        print("File not Found")


config = GMAIL_CONFIGS

def send_email(student_email_received,student_result):
    # Email configuration
    sender_email = config['login']['sender_email']
    receiver_email = student_email
    password = config['login']['password']

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = student_email_received
    msg['Subject'] = 'Student Result Now Available'

    # Attach student result to the email body
    body = student_result
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Send email
    server.sendmail(sender_email, student_email_received, msg.as_string())
    server.quit()
    logger.info(f'Email sent to - {student_email_received}')


#extract dataframe to dictionary
def get_student_grades(df_student):
    student_grades = {}
    # unpack the content of df
    for val in df_student.values:
        #convert val to tuple data type
        student_id,name,math,english, physics,chemistry = val
        #store record in dictionary data type
        student_grades[student_id]= [name,math,english, physics,chemistry]
    return student_grades


def student_email(student_email_args):
    #request student email to send the result
    student_email = student_email_args
    student_email = student_email.casefold() #this will convert email address to lowercase
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    while not re.match(email_regex,student_email):
        logger.error(f'Wrong email entered - {student_email}')
        student_email = input("Email incorrect, please check email and try again: ")
    return student_email


#colleect and store student id
def get_student_id_input(student_grades_extracted, student_id):
    #request student id to pull record
    check_studentid ="-"
    student_response = student_id
    # student_response = input("Enter your student id(e.g s****): ")
    check_studentid = student_response.casefold()
    while check_studentid not in student_grades_extracted.keys():
        logger.error(f'Student id - {student_response}, not found')
        student_response = input("Student record not found for studentid {}, please check studentid and try again: ".format(student_response))
        student_response = student_response.casefold()
        check_studentid = student_response
    return student_response
    student_email()



def get_student_result(student_input_received,student_grades_extracted):
#print student result to cmd
    if student_input_received in student_grades_extracted.keys():

        result = ' {0} grades are as follows:\n \
            \n Mathematics - {1} \
            \n English - {2} \
            \n Physics - {3} \
            \n Chemistry - {4}'.format(student_grades_extracted[student_input_received][0],\
            student_grades_extracted[student_input_received][1],student_grades_extracted[student_input_received][2],\
                student_grades_extracted[student_input_received][3],student_grades_extracted[student_input_received][4])
        
        return result


    
def main():

    parser = argparse.ArgumentParser(description='Student Result Application')
    parser.add_argument('student_id', help='Enter student id')
    parser.add_argument('email', help='Send result via email')
    args = parser.parse_args()

    df_student = read_student_records()
# Extract student grades into dictionary
    student_grades_extracted = get_student_grades(df_student)
    student_input_received = get_student_id_input(student_grades_extracted,args.student_id)
    student_result = get_student_result(student_input_received,student_grades_extracted)
    student_email_received = student_email(args.email)
    send_email(student_email_received,student_result)
    print("Result has been processed successfully, please check email")
    logger.info("Email sent to student ")

if __name__ == "__main__":
    main()



# parser = argparse.ArgumentParser(description='Student Result Application')
# parser.add_argument('email', help='Send result via email')
# args = parser.parse_args()
# print(args.email)


#TO DO
#Update code such that if wrong student id is entered, prompt user for another student id
#Refactor to use function where possible
#Import library that would allow connection to email: Connect to gmail or other email account to send the result
#Are we sending the result as an attachment or should it go in the body of the email
# use argument parse
# add security
# add logging
# transistion to database
# input checks and email validation; pattern matching
# admin portal
# use more functions

