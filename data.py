import requests

import runtimedata
import os
import connman

class Colors:
    def __init__(self):
        self.escapeSequence = "\033["

        self.typeNormal = "0;"
        self.typeBold = "1;"
        self.typeItalic = "3;"
        self.typeUnderline = "4;"
        self.typeShiftHue = "5;"

        self.colorBlack = "30;"
        self.colorRed = "31;"
        self.colorGreen = "32;"
        self.colorYellow = "33;"
        self.colorBlue = "34;"
        self.colorPink = "35;"
        self.colorWhite = "37;"
        self.colorDefault = "49;"

        self.backBlack = "40"
        self.backRed = "41"
        self.backGreen = "42"
        self.backYellow = "43"
        self.backBlue = "44"
        self.backPurple = "45"
        self.backWhite = "47"
        self.backDefault = "49"

        self.finish = "m"

        self.fullReset = "\033[0;0;0m"

colors = Colors()
terminalX, terminalY = os.get_terminal_size()
serverPort = 13900
logo = f"""
█████▀██████████████████████████████████████████████████████████▀███████████████████████████
█─▄▄▄▄██▀▄─██▄─▄─▀█▄─▄─▀██▀▄─██─▄▄▄─█─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄██▀▄─██▄─▀█▀─▄█▄─▄▄─█─▄▄▄▄█
█─██▄─██─▀─███─▄─▀██─▄─▀██─▀─██─███▀█─██─██─██─██─▄█▀█▄▄▄▄─█─██▄─██─▀─███─█▄█─███─▄█▀█▄▄▄▄─█
▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
                             Made by {colors.escapeSequence + colors.typeBold + colors.colorRed + colors.backDefault + colors.finish}Gabba{colors.escapeSequence + colors.typeBold + colors.colorWhite + colors.backDefault + colors.finish} (github.com/GabbaTK)                             
"""

def betterPrint(textType, textColor, textBackground, text, end="\n"):
    print(colors.escapeSequence + textType + textColor + textBackground + colors.finish + text + colors.fullReset, end=end)

def printStatusBar():
    betterPrint(colors.typeBold, colors.colorBlack, colors.backWhite, f" {runtimedata.game} / {runtimedata.connectedServer}" + " " * (terminalX - len(f"{runtimedata.game} / {runtimedata.connectedServer}") - 1))

def keyboard_soft_cancel(cancel_text=""):
    def __make_wrapper(func):
        def wrapper(*args, **kwargs):
            try:
                funcReturn = func(*args, **kwargs)

                return funcReturn
            except KeyboardInterrupt:
                print()
                print(cancel_text)

        return wrapper
    return __make_wrapper

def connectToMainServer():
    socket = connman.Socket(client=True)

    for retry in range(3):
        betterPrint(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Connecting, attempt {retry}...")

        response = requests.get("http://gabba.ivma.hr/gcg/ip")
        response.raise_for_status()
        data = response.json()
        ipAddr = data.get("ip")
        #status = socket.connect("gabba.ivma.hr", serverPort, 5)
        status = socket.connect(ipAddr, serverPort, 5)

        if status:
            runtimedata.connectedServer = f"Main Server ({runtimedata.serverPassword})"# + colors.escapeSequence + colors.typeBold + colors.colorRed + colors.backDefault + colors.finish + "NOT IMPLEMENTED" + colors.fullReset
            break

    if status == False:
        betterPrint(colors.typeNormal, colors.colorRed, colors.backDefault, "Failed to connect to server")
        exit()

    socket.send(f"CONNECT BATTLESHIP {runtimedata.serverPassword}")
    response = socket.receive(5)
    if response != "SUCCESS":
        betterPrint(colors.typeNormal, colors.colorRed, colors.backDefault, "Server denied connection")
        exit()

    return socket
