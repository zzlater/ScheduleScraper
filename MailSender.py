import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# input your email including @ and extension
receiver_email = "example@gmail.com" # email you would like to receive mail at
login = "" # login from Mailtrap
password = ""  # password from Mailtrap
filename = "file.txt" # same file name from main.py
def Send():
    port = 2525
    smtp_server = "smtp.mailtrap.io:2525" # Utilizes smpt server w/ port 2525
    
    subject = "Class availability has changed.."
    sender_email = "mailtrap@example.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # We assume that the file is in the directory where you run your Python script from
    with open(filename, "rb") as attachment:
        # The content type "application/octet-stream" means that a MIME attachment is a binary file
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to your message and convert it to string
    message.attach(part)
    text = message.as_string()

    # send your email
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(login, password)
        server.sendmail(
            sender_email, receiver_email, text
        )
    print('Sent')
