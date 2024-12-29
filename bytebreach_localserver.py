import os
import threading

import connman
import data
import runtimedata

colors = data.Colors()
debug = print
print = data.betterPrint

terminalX, terminalY = os.get_terminal_size()
socket = None
logs = []
globalKillSwitch = threading.Event()
adminIps = ["127.0.0.1"] # Which IPs have admin on this computer

def log(textType, textColor, backColor, text):
    logs.append(text)

    if len(logs) > terminalY - 2:
        if not runtimedata.noCls: os.system("cls")
        data.printStatusBar()

        for logEntry in logs[len(logs) - terminalY + 2:]:
            print(textType, textColor, backColor, logEntry)
    else:
        print(textType, textColor, backColor, text)

def createServer():
    global socket

    socket = connman.Socket(server=True)
    socket.createServer(data.serverPort + 1)

def initFromLocal():
    connection, _ = socket.acceptConnection()
    data = socket.receive(None, connection)

    if data == "local_init_server":
        runtimedata.game = "ByteBreach (LOCAL SERVER)"
        runtimedata.connectedServer = socket.receive(None, connection)
    else:
        print(colors.typeBold, colors.colorRed, colors.backDefault, "FIRST MESSAGE WAS NOT A LOCAL_INIT MESSAGE")

def handleConnection(connection):
    while True:
        if globalKillSwitch.is_set(): return

        received = socket.receive(5, connection)

        if received == "ping":
            socket.send("pong", connection)
        elif received == "disconnect":
            if connection.getpeername()[0] != "127.0.0.1" and connection.getpeername()[0] != runtimedata.connectedServer:  log(colors.typeNormal, colors.colorWhite, colors.backDefault, f"{connection.getpeername()[0]} disconnected")
            return
        
        elif received == "action_log":
            received = socket.receive(5, connection)
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, received)

        elif received == "action_check_admin":
            ip = socket.receive(5, connection)

            if ip in adminIps: socket.send("1", connection)
            else: socket.send("0", connection)

def acceptConnections():
    while True:
        connection, addr = socket.acceptConnection()

        if addr[0] != "127.0.0.1" and addr[0] != runtimedata.connectedServer: log(colors.typeNormal, colors.colorWhite, colors.backDefault, f"New connection from {addr[0]}")

        thread = threading.Thread(target=handleConnection, args=(connection,))
        thread.start()

def main():
    global logs

    createServer()
    initFromLocal()

    data.printStatusBar()
    log(colors.typeBold, colors.colorWhite, colors.backRed, f"{"DO NOT CLOSE THIS": ^{terminalX}}")
    logs = []

    thread = threading.Thread(target=acceptConnections)
    thread.start()

    globalKillSwitch.wait()
    socket.socket.close()
    exit()

main()
