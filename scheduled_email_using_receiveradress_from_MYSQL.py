import smtplib
import ssl
import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector

# Email configuration
sender_email = input("your_email:")
password = input("your_password:")

# Email content
subject = "Scheduled Update"
body = "This is a scheduled update message."

# Schedule time (24-hour format)
schedule_time = input("Time:")


def get_recipients_from_database():
    try:
        # Connect to your database
        connection = mysql.connector.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )

        cursor = connection.cursor()

        # Example query to retrieve email addresses from a table named 'recipients_table'
        cursor.execute("SELECT email FROM recipients_table")

        recipients = [row[0] for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return recipients

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []


def send_email():
    recipients = get_recipients_from_database()

    if not recipients:
        print("No recipients found or an error occurred while fetching the recipients.")
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipients, message.as_string())
            print(f"Email sent to {', '.join(recipients)}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def schedule_emails():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            send_email()
            # Avoid sending multiple emails within the same minute
            time.sleep(60)
        else:
            # Check every minute
            time.sleep(60)


if __name__ == "__main__":
    schedule_emails()
