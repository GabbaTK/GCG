import connman
import data
import runtimedata

colors = data.Colors()
debug = print
print = data.betterPrint

socket = None

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
        pass

def main():
    createServer()
    initFromLocal()

    data.printStatusBar()

    while True:
        connection, addr = socket.acceptConnection()

        handleConnection(connection)

main()
