from datetime import timedelta, datetime
import imaplib
import email
import time
import os
import configparser
import sys

config_name = 'config.ini'
last_mail = 0
new_mail = ''
pause_time = 15
server = 'imap.mail.com'
login = 'xxx@mail.com'
password = '12345678'
mail_cam = ['xxx@mail.ru']
infinity = 1

conf = configparser.ConfigParser()


def exit():
    imap.close()
    imap.logout()


def parseData(data):
    d = datetime(data[0], data[1], data[2], data[3], data[4], data[5])
    timeSecond = time.mktime(d.timetuple()) - data[9]
    return timeSecond


def NewConfig(conf):
    Def_text = f'[Email]\nServer = {server}\nLogin = {login}\nPassword = {password}\n[Cam]\nMail1 = {mail_cam}\n[Interval]\nPause_time = {pause_time}'
    conf.write(Def_text)
    conf.close()


def newMailer(f, n, l):
    global mail_cam
    status = False
    for line in mail_cam:
        print(f"Line: {line}")
        if line in f:
            print(f"n {n}")
            print(f"l {l}")
            if n > l:
                status = True
                break
        else:
            status = False
    return status


def Mail(mail_cam):
    global new_mail
    global last_mail

    imap.select("Inbox")
    _, msgnums = imap.search(None, "ALL")

    latest_email_uid = msgnums[0].split()[-1]
    _, data = imap.fetch(latest_email_uid, "(RFC822)")
    message = email.message_from_bytes(data[0][1])
    print(f"Time: {local_time}")
    print(f"From: {message.get('From')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('Subject')}")
    print('')

    fromMail = message.get('From')

    new_mail = parseData(email.utils.parsedate_tz(message["Date"]))

    statist = newMailer(fromMail, new_mail, last_mail)

    return statist


if not os.path.isfile(config_name):
    new_config = open(config_name, "w")
    NewConfig(new_config)
    infinity = 0
    print('New config')
    sys.exit()
else:
    print('Config ok!')
    body = ''
    config = open(config_name)
    for line in config:
        body += line

    config.close()

    if body and body.strip():
        print('ok')
        conf.read(config_name)
        server = conf["Email"]["Server"]
        login = conf["Email"]["Login"]
        password = conf["Email"]["Password"]
        pause_time = int(conf["Interval"]["Pause_time"])
        mail_cam.clear()
        for line in conf["Cam"]:
            mail_cam.append(conf["Cam"][f"{line}"])
    else:
        NewConfig(open(config_name, "w"))
        infinity = 0
        sys.exit()

print('Avtorization...')
imap = imaplib.IMAP4_SSL(server)
imap.login(login, password)

while infinity == 1:
    print('Mail cheack...')
    second = time.time()
    local_time = time.ctime(second)
    status = Mail(mail_cam)
    print(status)
    print(f'new_mail = {new_mail}\nlast_mail = {last_mail}')
    last_mail = new_mail
    print('')
    time.sleep(pause_time)