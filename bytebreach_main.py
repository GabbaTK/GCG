import data
import os
import readkeys
import time
import threading
import socket as Isocket

import runtimedata
import connman

import bytebreach_data
import bytebreach_client
import bytebreach_server

colors = data.Colors()
debug = print
print = data.betterPrint

socket = None

def connectionMainServer():
    global socket

    socket = connman.Socket(client=True)

    for retry in range(3):
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Connecting, attempt {retry}...")
        status = socket.connect("gcg.ivma.hr", data.serverPort, 5)

        if status:
            runtimedata.connectedServer = "Main Server"
            break

def connection():
    global socket

    os.system("cls")

    data.printStatusBar()

    debug()

    if not runtimedata.localGame: connectionMainServer()
    else:
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
        print(colors.typeBold, colors.colorBlue, colors.backDefault, "1", "")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Create server")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
        print(colors.typeBold, colors.colorBlue, colors.backDefault, "2", "")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Join server")

        while True:
            key = readkeys.getch()

            if key == "1" or key == "2": break

        if key == "1":
            socket = connman.Socket(server=True)
            socket.createServer(data.serverPort)

            runtimedata.connectedServer = Isocket.gethostbyname(Isocket.gethostname())

        else:
            socket = connman.Socket(client=True)

            while True:
                ip = input(">>>")
                status = socket.connect(ip, data.serverPort, 5)
                
                if not status:
                    print(colors.typeNormal, colors.colorRed, colors.backDefault, "Failed to connect to server ", "")
                else:
                    runtimedata.connectedServer = ip
                    runtimedata.runningServer = True
                    break

def main():
    os.system("cls")

    runtimedata.game = "ByteBreach"

    data.printStatusBar()
    bytebreach_data.init()

    debug(bytebreach_data.logoMain) # Have to use debug as the logo is already encoded with colors
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"{"Press any key to start": ^{bytebreach_data.terminalX}}")

    readkeys.getch()

    for idx in range(8):
        os.system("cls")
        data.printStatusBar()
        bytebreach_data.graduallyRemoveText(bytebreach_data.logoMain, idx)
        time.sleep(0.25)

    # Begin game
    connection()

    runtimedata.socket = socket

    threadClient = threading.Thread(target=bytebreach_client.main)
    threadServer = threading.Thread(target=bytebreach_server.main)

    threadClient.start()
    threadServer.start()
    os.startfile("bytebreach_localserver.py")
