import data
import os
import readkeys
import time
import threading
import socket as Isocket

import runtimedata
import connman

import bytebreach_data

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
            runtimedata.connectedServer = "Main Server" + colors.escapeSequence + colors.typeBold + colors.colorRed + colors.backDefault + colors.finish + "NOT IMPLEMENTED" + colors.fullReset
            break

    if status == False:
        print(colors.typeNormal, colors.colorRed, colors.backDefault, "Failed to connect to server")
        exit()

def connection():
    global socket

    if not runtimedata.noCls: os.system("cls")

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
            runtimedata.runningServer = True
            runtimedata.serverSocket = socket

            socket = connman.Socket(client=True)
            while True:
                status = socket.connect("localhost", data.serverPort, 5)
                
                if not status:
                    print(colors.typeNormal, colors.colorRed, colors.backDefault, "Failed to connect to server")
                else:
                    runtimedata.clientSocket = socket
                    break

        else:
            socket = connman.Socket(client=True)

            while True:
                ip = input(">>>")
                status = socket.connect(ip, data.serverPort, 5)
                
                if not status:
                    print(colors.typeNormal, colors.colorRed, colors.backDefault, "Failed to connect to server", "")
                else:
                    runtimedata.connectedServer = ip
                    runtimedata.clientSocket = socket
                    break

def main():
    if not runtimedata.noCls: os.system("cls")

    runtimedata.game = "ByteBreach"

    data.printStatusBar()
    bytebreach_data.init()

    # First init the import these as they use PyTimedInput
    import bytebreach_client
    import bytebreach_server

    debug(bytebreach_data.logoMain) # Have to use debug as the logo is already encoded with colors
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"{"Press any key to start": ^{bytebreach_data.terminalX}}")

    readkeys.getch()

    for idx in range(8):
        if not runtimedata.noCls: os.system("cls")
        data.printStatusBar()
        bytebreach_data.graduallyRemoveText(bytebreach_data.logoMain, idx)
        time.sleep(0.25)

    # Begin game
    connection()

    threadClient = threading.Thread(target=bytebreach_client.main)
    threadServer = threading.Thread(target=bytebreach_server.main)

    threadClient.start()
    threadServer.start()
    os.startfile("bytebreach_localserver.py")
