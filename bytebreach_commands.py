import time
import socket as Isocket

import data
import runtimedata

# Shift Command Line
# Draw Display

commandsPerPage = (data.terminalY - 6) // 4
def help(cmd, scl, dd, **kwargs):
    if cmd == []: cmd = ["1"]

    page = int(cmd[0]) - 1

    for key in list(commands.keys())[page * commandsPerPage:page + commandsPerPage]:
        data = commands[key]

        scl("")
        scl(f"Command '{(key + " " + data["args"]).strip()}'")
        scl(f"Full name '{data["name"]}'")
        scl(data["description"])

    dd()

def test(cmd, scl, dd, **kwargs):
    if runtimedata.runningServer:
        scl("Cannot test the connection as you are running the server")
        dd()
        return
    
    scl("Testing connection...")
    scl("Please wait...")
    dd()
    runtimedata.clientSocket.send("ping")
    response = runtimedata.clientSocket.receive(10)

    if response == "pong":
        scl("Connection status: good")
    else:
        scl("Connection status: no response")

    dd()

def connect(cmd, scl, dd, **kwargs):
    if cmd == []:
        scl("No IP address specified")
        dd()
        return
    
    if not kwargs["has_admin"][0]:
        scl("Cannot use this target as a proxy if you don't have admin on it")
        dd()
        return

    scl(f"Attempting to connect to {cmd[0]}")
    dd()
    
    if cmd[0] == Isocket.gethostbyname(Isocket.gethostname()) and runtimedata.runningServer: cmd[0] = "127.0.0.1"
    
    runtimedata.clientSocket.send("action_connect")
    runtimedata.clientSocket.send("-".join(kwargs["connection_path"]))
    runtimedata.clientSocket.send(cmd[0])

    response = runtimedata.clientSocket.receive(5)

    if response == None: raise Exception("Server failed to respond in time")

    time.sleep(2)

    if response == "response_action_success":
        kwargs["connection_path"].append(cmd[0])

        scl("Successfully connected to target")
        dd()

        runtimedata.clientSocket.send("action_check_admin")
        runtimedata.clientSocket.send(cmd[0])

        response = runtimedata.clientSocket.receive(5)
        
        if response == "1": kwargs["has_admin"][0] = True
        else: kwargs["has_admin"][0] = False
    elif response == "response_action_fail":
        scl("Failed to connect to target")
        dd()

    else:
        scl(f"Unknown response: {response}")
        dd()

commands = {
    "help": {
        "args": "<page>",
        "name": "Help",
        "description": "Display all the commands",
        "handler": help
    },
    "test": {
        "args": "",
        "name": "Test",
        "description": "Test the connection to the main server",
        "handler": test
    },
    "connect": {
        "args": "<ip>",
        "name": "Connect",
        "description": "Connect to a target machine",
        "handler": connect
    }
}
