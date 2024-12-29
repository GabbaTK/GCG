import os
import socket as Isocket

import data
import runtimedata
import connman

import bytebreach_data
import bytebreach_commands

colors = data.Colors()
debug = print
print = data.betterPrint

knownIPs = [[f"{Isocket.gethostbyname(Isocket.gethostname()): <15}"]]
ramUsage = []
ramLimit = .2
ramLimitLineIdx = int((data.terminalY - 6) * ramLimit)
commandList = ["> Type 'help' to show all commands"]
connectionPath = [Isocket.gethostbyname(Isocket.gethostname())]
hasAdmin = [True]

def drawDisplay():
    if not runtimedata.noCls: os.system("cls")

    data.printStatusBar()
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "-" * (data.terminalX - 5))

    for lineIdx in range(data.terminalY - 6):
        if len(knownIPs) > lineIdx: currentIP = " ".join(knownIPs[lineIdx])
        else: currentIP = ""

        if len(ramUsage) > lineIdx: currentRam = ramUsage[lineIdx]
        else:
            if lineIdx == ramLimitLineIdx: currentRam = "-" * int(data.terminalX * bytebreach_data.ramSplit)
            else: currentRam = ""

        if len(commandList) > data.terminalY - 7 - lineIdx: currentCommand = commandList[::-1][data.terminalY - 7 - lineIdx]
        else: currentCommand = ""

        print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"| {currentIP: <{data.terminalX * bytebreach_data.ipSplit}} |{currentRam: <{data.terminalX * bytebreach_data.ramSplit}}|{currentCommand: <{data.terminalX * bytebreach_data.cmdSplit}}|")

    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "-" * (data.terminalX - 5))

def cheater():
    if not runtimedata.noCls: os.system("cls")

    print(colors.typeBold, colors.colorWhite, colors.backDefault, bytebreach_data.dontCheat)
    exit()

def shiftCommandLine(cmd):
    commandList.append(f"> {cmd}")

    if len(commandList) > data.terminalY - 6:
        del commandList[0]

def main():
    if not runtimedata.noCls: os.system("cls")

    data.printStatusBar()

    localServerSocket = connman.Socket(client=True)
    localServerSocket.connect("localhost", data.serverPort + 1, None)
    localServerSocket.send("local_init_server")
    localServerSocket.send(runtimedata.connectedServer)
    localServerSocket.disconnect()
    localServerSocket = connman.Socket(client=True)
    localServerSocket.connect("localhost", data.serverPort + 1, None) # Disconnect from the local function and into the global function (initFromLocal -> handleConnection)

    while True:
        if not runtimedata.noCls: os.system("cls")

        drawDisplay()

        localServerSocket.send("ping")
        response = localServerSocket.receive(3)

        if response != "pong": cheater()

        print(colors.typeNormal, colors.colorGreen, colors.backDefault, connectionPath[0], "")
        if len(connectionPath) > 1: print(colors.typeNormal, colors.colorBlue, colors.backDefault, " -> ", "")
        debug((colors.escapeSequence + colors.typeNormal + colors.colorBlue + colors.backDefault + colors.finish + " -> " + colors.fullReset).join(connectionPath[1:]), end="")

        userCmd = input(colors.escapeSequence + colors.typeNormal + colors.colorRed + colors.backDefault + colors.finish + " --> " + colors.fullReset)

        try:
            parsedCmd = userCmd.split(" ")
            cmd = parsedCmd[0]
            args = parsedCmd[1:]
            bytebreach_commands.commands[cmd]["handler"](args, shiftCommandLine, drawDisplay, connection_path=connectionPath, has_admin=hasAdmin)
        except KeyError:
            shiftCommandLine(f"Command not found: {cmd}")
