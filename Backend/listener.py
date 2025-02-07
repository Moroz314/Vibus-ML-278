import websocket
<<<<<<< HEAD
from websocket import WebSocketApp
=======
>>>>>>> a6a076d2c779859ce9b613cfd473fd662a56b957
import keyboard


def KeyListener(ws):
    pressed = False
    text_rus = ""
    text_eng = ""
    web_soc = ws

    def translate(letter: str):
        x = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
        y = "йцукенгшщзхъфывапролджэячсмитьбю.ё"
        if len(letter) == 1:
            if letter.isalpha() or letter in ("[", "]", ",", ";", "'", ".", "/", "`"):
                tbl1 = letter.maketrans(x, y)
                tbl2 = letter.maketrans(y, x)
                return [letter.translate(tbl1), letter.translate(tbl2)]

    def handle_change_lang():
        nonlocal text_rus, text_eng
        text_eng += " смена языка "
        text_rus += " смена языка "

    def send_to_buffer():
        nonlocal text_rus, text_eng, web_soc
        try:
            web_soc.send(f"{text_rus}, {text_eng}")
            text_rus = ""
            text_eng = ""
        except:
            print("Error")

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


def on_open(ws):
    print("Connection opened")


handshake = False


def on_message(ws, message):
    global handshake
    if message == "OK":
        handshake = True
        print("Супер")
    KeyListener(ws)


<<<<<<< HEAD
ws = websocket.WebSocketApp("ws://192.168.0.108:8000/ws",
=======
ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws",
>>>>>>> a6a076d2c779859ce9b613cfd473fd662a56b957
                            on_open=on_open,
                            on_message=on_message,
                            )

ws.run_forever()

