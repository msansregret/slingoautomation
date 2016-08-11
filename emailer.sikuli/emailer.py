import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.MIMEBase import MIMEBase
from email import Encoders

mailer = None

def sendMail(send_from, send_to, subject, text):
    server='mail.bstage.ca'
   
    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    #msg.preamble = subject
    body = ''.join(text)
    
    msg.attach(MIMEText('Plain Text version not supported', 'plain'))
    msg.attach(MIMEText(body, 'html'))

    ##### File Attachement code commented out until needing to send an attachment
    #part = MIMEBase('application', "octet-stream")
    #part.set_payload(open(file, "rb").read())
    #Encoders.encode_base64(part)

    #part.add_header('Content-Disposition', 'attachment; filename="report.csv')

    #msg.attach(part)
    
    mailer = smtplib.SMTP(server)
    mailer.sendmail(send_from, send_to, msg.as_string())
    mailer.quit()

def sendMailAttach(send_from, send_to, subject, text, filename, filepath):
    server='mail.bstage.ca'
   
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    #msg.preamble = subject
    
    body = ''.join(text)
    msg.attach(MIMEText(body, 'plain'))

    ##### File Attachement code commented out until needing to send an attachment
    attachment = open(filepath, 'rb')
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload((attachment).read())
    Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

    msg.attach(part)
    
    mailer = smtplib.SMTP(server)
    mailer.sendmail(send_from, send_to, msg.as_string())
    mailer.quit()
                
def main():
    #dir = "C:/Sikuli/HTMLTestRunner" #Windows path
    dir = "/Users/tporter/Development/Sikuli/HTMLTestRunner" #MAC path
    f = open(r'/Users/tporter/Development/Sikuli/HTMLTestRunner/test.html', 'r') #Mac path
    sendMail('noreply@gamehouse.com', 'msansregret@gamehouse.com', 'Testbot Report', f)
    f.close()

    
if __name__ == '__main__':
    main()