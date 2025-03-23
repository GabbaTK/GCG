import data
import os
import readkeys
import uuid

import runtimedata

colors = data.Colors()
debug = print
print = data.betterPrint

def main():
    while True:
        if not runtimedata.noCls: os.system("cls")

        print(colors.typeBold, colors.colorWhite, colors.backDefault, data.logo)

        print(colors.typeItalic, colors.colorWhite, colors.backDefault, "Whether to directly connect to the server on the local network, or to connect to a main server running outside the network, which hosts the game.")
        print("", "", "", "")

        print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
        print(colors.typeBold, colors.colorBlue, colors.backDefault, "0", "")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Back")
        print("", "", "", "")

        print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
        print(colors.typeBold, colors.colorBlue, colors.backDefault, "1", "")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Change")

        key = readkeys.getch()

        if key == "0": break
        elif key == "1":
            runtimedata.localGame = not runtimedata.localGame
            runtimedata.serverPassword = input("Enter a secret password that only the players know >>>")
            runtimedata.serverPassword += "_" + str(uuid.uuid4())[0:4]
            break
