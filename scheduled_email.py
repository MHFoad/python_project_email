import smtplib
import ssl
import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = input("your_email:")
password = input("your_password:")

# Recipients list
recipients = ["re_emails","re_emails2", "re_emails3"]

# Email content
subject = "Scheduled Update"
body = "This is a scheduled update message."

# Schedule time (24-hour format)
schedule_time = input("Time: ")
def send_email():
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
