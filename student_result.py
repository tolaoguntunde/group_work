# pandas library is used to read the excel file
import sqlite3
import argparse
import logging
import logging.config
from configs.configs import GMAIL_CONFIGS
from configs.configs import DB_CONFIGS
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path



#credentials for gmail 
config = GMAIL_CONFIGS
db_conn = DB_CONFIGS

logging.config.fileConfig('configs/logger.conf')
logger = logging.getLogger('student_app')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_conn['sqlite']['db'])

def get_student_grades():
        with sqlite3.connect(db_path) as db:
            cur =db.cursor()
            df_student = cur.execute('select * from student_result')
            logger.info('Open database successful')
            student_grades = {}
            for val in df_student:
                student_id,name,math,english, physics,chemistry = val
                student_grades[student_id]= [name,math,english, physics,chemistry]
            print(student_grades)
            return student_grades
   

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
    #setup argument parse
    parser = argparse.ArgumentParser(description='Student Result Application')
    parser.add_argument('student_id', help='Enter student id')
    parser.add_argument('email', help='Send result via email')
    args = parser.parse_args()

    # Extract student grades into dictionary
    student_grades_extracted = get_student_grades()
    
    #store student id from args parser
    student_input_received = get_student_id_input(student_grades_extracted,args.student_id)

    #store student result based on the id slected
    student_result = get_student_result(student_input_received,student_grades_extracted)

    #store student id from args parser
    student_email_received = student_email(args.email)

    #send student email
    send_email(student_email_received,student_result)

    print("Result has been processed successfully, please check email")

    logger.info("Email sent to student ")


if __name__ == "__main__":
    main()