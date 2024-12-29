import threading

import runtimedata
import connman
import data

connectedClients = {}
socket = None
globalKillSwitch = threading.Event()

def handleConnection(connection):
    while True:
        if globalKillSwitch.is_set(): return

        received = socket.receive(5, connection)

        if received == "ping":
            socket.send("pong", connection)
        elif received == "disconnect":
            del connectedClients[connectedClients.index(connection.getpeername()[0])]
            return
        
        elif received == "action_connect":
            connectionPath = socket.receive(5, connection)
            connectingIp = socket.receive(5, connection)

            if connectingIp in connectedClients:
                socket.send("response_action_success", connection)
            else:
                socket.send("response_action_fail", connection)
            
            if len(connectionPath.split("-")) > 1:
                connectionPathFull = connectionPath.split("-")
                connectionPathFull.append(connectingIp)
                for clientIdx, client in enumerate(connectionPathFull[1:-1]):
                    tmpSocket = connman.Socket(client=True)
                    tmpSocket.connect(client, data.serverPort + 1, 2)

                    tmpSocket.send("action_log")
                    tmpSocket.send(f"Forwarding data from {connectionPathFull[clientIdx - 1]} to {connectionPathFull[clientIdx + 1]}")

                    tmpSocket.send("disconnect")
                    tmpSocket.socket.close()

        elif received == "action_check_admin":
            ip = socket.receive(5, connection)

            tmpSocket = connman.Socket(client=True)
            tmpSocket.connect(ip, data.serverPort + 1, 2)

            tmpSocket.send("action_check_admin")
            tmpSocket.send(connection.getpeername()[0])

            hasAdmin = tmpSocket.receive(5)
            
            socket.send(hasAdmin, connection)

def acceptConnections():
    while True:
        connection, addr = socket.acceptConnection()

        connectedClients[addr[0]] = connection

        thread = threading.Thread(target=handleConnection, args=(connection,))
        thread.start()

def main():
    global socket

    if not runtimedata.runningServer: return
    
    socket = runtimedata.serverSocket

    thread = threading.Thread(target=acceptConnections)
    thread.start()

    globalKillSwitch.wait()
    socket.socket.close()
    exit()
