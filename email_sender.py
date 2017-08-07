# encoding=utf8
import smtplib
from decouple import config

def send(emailTo, emailMsg):

    recipients = [emailTo, 'iurimenin@gmail.com']
    emailSender = config('EMAILSENDER')
    passwordSender = config('PASSWORDSENDER')
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(emailSender, passwordSender)
    server.sendmail(emailSender, recipients, emailMsg)
    server.quit()

# if __name__ == '__main__':
#     send('iuri.menin@softfocus.com.br', 'Teste multiplos emails')