import os

import data
import runtimedata
import connman

socket = connman.Socket(client=True)

def main():
    os.system("cls")

    data.printStatusBar()

    socket.connect("localhost", data.serverPort + 1, None)
    socket.send("local_init_server")
    socket.send(runtimedata.connectedServer)
    socket.disconnect()
    socket.connect("localhost", data.serverPort + 1, None) # Disconnect from the local function and into the global function (initFromLocal -> handleConnection)
