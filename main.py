try:
    import readkeys
    import requests
except ImportError:
    import os

    os.system("pip install requests")
    os.system("pip install readkeys")

import data
import os
import readkeys
import sys

import runtimedata
import localgameconfig

import battleship_main
import bytebreach_main

colors = data.Colors()
debug = print
print = data.betterPrint

args = sys.argv

games = ["Battle ship", "ByteBreach"]

def printMain():
    print(colors.typeBold, colors.colorWhite, colors.backDefault, data.logo)

    print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
    print(colors.typeBold, colors.colorBlue, colors.backDefault, "0", "")
    print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Local game: {runtimedata.localGame}")
    print("", "", "", "")

    for idx, game in enumerate(games):
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "[", "")
        print(colors.typeBold, colors.colorBlue, colors.backDefault, str(idx + 1), "")
        print(colors.typeBold, colors.colorWhite, colors.backDefault, "] ", "")
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, game)

def main():
    if "-ncls" in args: runtimedata.noCls = True

    printMain()

    while runtimedata.game == "":
        key = readkeys.getch()

        if key == "0":
            localgameconfig.main()

            if not runtimedata.noCls: os.system("cls")
            printMain()

        elif key == "1": battleship_main.main()
        elif key == "2": bytebreach_main.main()

if __name__ == "__main__":
    if not runtimedata.noCls: os.system("cls")

    main()
else:
    if not runtimedata.noCls: os.system("cls")

    print(colors.typeItalic, colors.colorDefault, colors.backDefault, "Why are you running this as an import?")
    print(colors.typeItalic, colors.colorDefault, colors.backDefault, "Anyways, here is the game manager.\n")

    main()
