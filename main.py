import imaplib
import email
import time

pause_time = 10
server = 'imap.mail.com'
login = 'xxx@mail.com'
password = '12345678'
mail_cap = 'xxx@mail.com'
infinity = 1



def Mail(mail_cap):
    imap.select("Inbox")
    _, msgnums = imap.search(None, "ALL")

    latest_email_uid = msgnums[0].split()[-1]
    _, data = imap.fetch(latest_email_uid, "(RFC822)")
    message = email.message_from_bytes(data[0][1])
    print(f"From: {message.get('From')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('Subject')}")
    print(f'')

    return mail_cap in message.get('From')

while infinity == 1:
    print('Avtorization...')
    imap = imaplib.IMAP4_SSL(server)
    imap.login(login, password)
    status = Mail(mail_cap)
    imap.close()
    print(status)
    if status:
        break
    time.sleep(pause_time)



#for msgnum in msgnums[0].split():
#    _, data = imap.fetch(msgnum, "(RFC822)")
#    message = email.message_from_bytes(data[0][1])
#    if mail_cap in message.get('From'):
#        print(f"Num: {msgnum}")
#        print(f"From: {message.get('From')}")
#        print(f"Date: {message.get('Date')}")
#        print(f"Subject: {message.get('Subject')}")
#        print(f'')


