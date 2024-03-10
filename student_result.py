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

# Rest-api
import requests
import random

def get_random_quote():
    # Send a GET request to the API endpoint
    response = requests.get("https://type.fit/api/quotes")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Select a random quote from the list
        random_quote = random.choice(data)
        # Extract text and author from the selected quote
        quote_text = random_quote["text"]
        quote_author = random_quote["author"].split(",", 1)[0] if random_quote["author"] else "Unknown"
        # Return the random quote
        # return f"<i>\"{quote_text}\"</i> - {quote_author}"
        return f"\"{quote_text}\" - {quote_author}"
    else:
        # Print an error message if the request was unsuccessful
        print("Failed to fetch data from the API.")


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
            record_count = 0 
            for val in df_student:
                student_id,name,math,english, physics,chemistry = val
                student_grades[student_id]= [name,math,english, physics,chemistry]
                record_count = record_count+1
            # print("This database only have {} student(s)".format(record_count)) 
            return student_grades
   

def send_email(student_email_received,student_result):
    # Email configuration
    sender_email = config['login']['sender_email']
    receiver_email = student_email_received
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
        student_email = input("Email incorrect, please check email and try again or press 'q' to exit: ")
        if student_email == 'q':
            print("Application exiting ...")
            logger.info('User quitt application')
            break
    return student_email


#collect and store student id
def get_student_id_input(student_grades_extracted, student_id):
    #request student id to pull record
    check_studentid ="-"
    student_response = student_id
    check_studentid = student_response.casefold()
    while check_studentid not in student_grades_extracted.keys():
        logger.error(f'Student id - {student_response}, not found')
        student_response = input("Student record not found for studentid {}, please check the student id and try again or press 'q' to exit: ".format(student_response))
        student_response = student_response.casefold()
        if student_response == 'q':
            print("Application exiting ...")
            logger.info('User quit application')
            break
        check_studentid = student_response
        
    return student_response


def get_student_result(student_input_received,student_grades_extracted):
#print student result to cmd
    if student_input_received in student_grades_extracted.keys():

        result = ' {0} grades are as follows:\n \
            \n Mathematics - {1} \
            \n English - {2} \
            \n Physics - {3} \
            \n Chemistry - {4} \
             \n\nQuote: {5}'.format(student_grades_extracted[student_input_received][0],\
            student_grades_extracted[student_input_received][1],student_grades_extracted[student_input_received][2],\
                student_grades_extracted[student_input_received][3],student_grades_extracted[student_input_received][4],get_random_quote()
                )
        # print(result)
        return result


    
def main():
    #setup argument parse
    parser = argparse.ArgumentParser(description='Student Result Application')
    parser.add_argument('student_id', help='Enter student id to generate result')
    parser.add_argument('email', help='Enter email address to get result via email')
    args = parser.parse_args()

    # Extract student grades into dictionary
    student_grades_extracted = get_student_grades()
    
    #store student id from args parser
    student_input_received = get_student_id_input(student_grades_extracted,args.student_id)
    if student_input_received != 'q':
        student_result = get_student_result(student_input_received,student_grades_extracted)
        student_email_received = student_email(args.email)
    #store student result based on the id slected

    #store student id from args parser
    #send student email
        if student_email_received != 'q':
            send_email(student_email_received,student_result)
            print("***********************************************************************")
            print("----- Result has been processed successfully, please check email -----")
            print("***********************************************************************")

            logger.info("Email sent to student ")
        


if __name__ == "__main__":
    main()