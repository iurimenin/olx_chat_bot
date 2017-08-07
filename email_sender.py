# encoding=utf8
import smtplib

def send(emailTo, emailMsg):
    print emailMsg

    recipients = [emailTo, 'iurimenin@gmail.com']
    emailSender = 'olx.chat.bot@gmail.com'
    passwordSender = 'chatbot@020293'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(emailSender, passwordSender)
    server.sendmail(emailSender, recipients, emailMsg)
    server.quit()

# if __name__ == '__main__':
#     send('iuri.menin@softfocus.com.br', 'Teste multiplos emails')