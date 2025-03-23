# a1a4
# b1b3
# c1c3
# d1d2
# e1e2
# f1f2
# g1g1
# h1h1
# i1i1
# j1j1

import readkeys
import os

import data
import runtimedata

import battleship_client
import battleship_server
import battleship_data

colors = data.Colors()
debug = print
print = data.betterPrint

def printMain():
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "0", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "]", "")
    print(colors.typeNormal, colors.colorDefault, colors.backDefault, " Start a server")

    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "1", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "]", "")
    print(colors.typeNormal, colors.colorDefault, colors.backDefault, " Connect to a server")

    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "2", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "]", "")
    print(colors.typeNormal, colors.colorDefault, colors.backDefault, " Call a serverside function")

    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "3", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "]", "")
    print(colors.typeNormal, colors.colorDefault, colors.backDefault, " Call a clientside function")

    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "4", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "]", "")
    print(colors.typeNormal, colors.colorDefault, colors.backDefault, " Call a data function")

def main():
    if not runtimedata.noCls: os.system("cls")

    runtimedata.game = "Battle ship"

    if not runtimedata.localGame:
        socket = data.connectToMainServer()
        runtimedata.clientSocket = socket
        battleship_client.main()

    data.printStatusBar()
    debug()
    printMain()

    while True:
        key = readkeys.getch()

        if key == "0": battleship_server.main()
        elif key == "1": battleship_client.main()
        elif key == "2": 
            func = input("S_FUNC_CALL>")
            result = battleship_server.funcCall(getattr(battleship_server, func))
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Return: {result}")
        elif key == "3": 
            func = input("C_FUNC_CALL>")
            result = battleship_client.funcCall(getattr(battleship_client, func))
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Return: {result}")
        elif key == "3": 
            func = input("D_FUNC_CALL>")
            result = battleship_data.funcCall(getattr(battleship_data, func))
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Return: {result}")
