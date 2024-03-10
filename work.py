import argparse
import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Tuple
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constants
STUDENT_RECORD_FILE = "student_record.xlsx"
ADMIN_EMAIL = "admin@example.com"
DATABASE = "student_database.db"


def read_student_records(filename: str) -> pd.DataFrame:
    """Read student records from Excel file."""
    try:
        df = pd.read_excel(filename)
        return df
    except FileNotFoundError:
        logger.error("Student record file not found.")
        raise


def send_email(sender_email: str, receiver_email: str, password: str, result: str) -> None:
    """Send email to student with result attached."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Student Result Now Available'

    body = result
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def extract_student_grades(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Extract student grades from DataFrame to dictionary."""
    student_grades = {}
    for val in df.values:
        student_id, name, math, english, physics, chemistry = val
        student_grades[student_id] = [name, math, english, physics, chemistry]
    return student_grades


def validate_email(email: str) -> bool:
    """Validate email format."""
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_regex, email))


def get_student_id_input(student_grades: Dict[str, List[str]]) -> str:
    """Prompt user for student ID and validate."""
    while True:
        student_response = input("Enter your student id (e.g s****): ").strip().lower()
        if student_response in student_grades:
            return student_response
        else:
            logger.error("Student record not found for student ID: %s", student_response)
            print("Student record not found. Please check and try again.")


def get_student_email_input() -> str:
    """Prompt user for email address and validate."""
    while True:
        student_email = input("Enter your email address: ").strip().lower()
        if validate_email(student_email):
            return student_email
        else:
            logger.error("Invalid email address: %s", student_email)
            print("Invalid email address. Please enter a valid email.")


def generate_result(student_grades: Dict[str, List[str]], student_id: str) -> str:
    """Generate result string for the given student ID."""
    name, math, english, physics, chemistry = student_grades[student_id]
    result = f"{name}'s grades are as follows:\n \
        \n Mathematics - {math} \
        \n English - {english} \
        \n Physics - {physics} \
        \n Chemistry - {chemistry}"
    return result


def save_result_to_file(result: str) -> None:
    """Save result to a text file."""
    with open('result.txt', 'w') as res:
        res.write(result)


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Student Result Application')
    parser.add_argument('--email', action='store_true', help='Send result via email')
    args = parser.parse_args()

    # Read student records
    try:
        df = read_student_records(STUDENT_RECORD_FILE)
    except FileNotFoundError:
        logger.error("Student record file not found. Exiting.")
        return

    # Extract student grades
    student_grades = extract_student_grades(df)

    # Get student ID input
    student_id = get_student_id_input(student_grades)

    # Get student email input
    student_email = get_student_email_input()

    # Generate result
    result = generate_result(student_grades, student_id)

    # Save result to file
    save_result_to_file(result)

    # Send email if requested
    if args.email:
        sender_email = input("Enter your email address: ").strip().lower()
        sender_password = input("Enter your email password: ")
        if validate_email(sender_email):
            send_email(sender_email, student_email, sender_password, result)
        else:
            logger.error("Invalid sender email address: %s", sender_email)
            print("Invalid sender email address. Email not sent.")
    else:
        print("\n--------- Student Record -----------\n")
        print(result)
        print("\n------------------------------------")


if __name__ == "__main__":
    main()


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