import cv2 
import os
import smtplib
import imaplib
import email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, freeze_support

cam = cv2.VideoCapture(0)  

def create_message(from_ad, to_ad, text):
    msg = MIMEMultipart()
    msg['From'] = from_ad
    msg['To'] = to_ad
    image_path = "e:/code_moroz/Vibeus-ML-278/Vibus-ML-278/py/screenshot.jpg"
    with open(image_path, "rb") as img:
        msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))
    return msg.as_string()


def connect_smtp(messages: list, from_ad, to_ad, mypass):
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(from_ad, mypass)
    server.sendmail(from_ad, to_ad, messages[0])
    server.sendmail(from_ad, to_ad, messages[1])
    server.sendmail(from_ad, from_ad, messages[0])
    server.sendmail(from_ad, from_ad, messages[1])
    server.quit()


def MailSender(ready):
    fromaddr = "9662061@mail.ru"
    toaddr = "vladmorozov2020@mail.ru"
    mypass = "qKKA8pUQm3FJCY0ViEv2"
    while True:
        if ready.value:
            print('оу ес')
        
          
            ret, frame = cam.read() 
            cv2.imwrite("screenshot.jpg", frame)  
            cam.release()
            print('окей')
            text = create_message(fromaddr, toaddr)
            connect_smtp(text, fromaddr, toaddr, mypass)
            ready.value = False



def ImapListener(ready):
    fromaddr = "9662061@mail.ru"
    mypass = "qKKA8pUQm3FJCY0ViEv2"
    connected = False
    imap = None

    while not connected:
        try:
            imap = imaplib.IMAP4_SSL("imap.mail.ru")
            imap.login(fromaddr, mypass)
            imap.select("INBOX/ToMyself")
            connected = True
        except:
            continue

    while True:
        if imap:
            try:
                messages = imap.search(None, "UNSEEN")
                if messages[1][0]:
                    mes = messages[1][0].decode().split()
                    res, msg = imap.fetch(f'{mes[-1]}', '(RFC822)')
                    msg = email.message_from_bytes(msg[0][1])
                    for part in msg.walk():
                        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                            text = base64.b64decode(part.get_payload()).decode().strip()
                            if text == "1":
                                ready.value = True
                                print(ready.value)

            except imaplib.IMAP4.abort:
                imap = imaplib.IMAP4_SSL("imap.mail.ru")
                imap.login(fromaddr, mypass)
                imap.select("INBOX/ToMyself")


if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    ready = manager.Value('i', False)
    with ProcessPoolExecutor(max_workers=3) as pool:
        pool.submit(ImapListener, ready)
        pool.submit(MailSender, ready)








 

