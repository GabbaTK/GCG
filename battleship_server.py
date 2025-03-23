import os
import time
import random

import connman
import runtimedata
import data

import battleship_data

socket = None
connection = None
ships = []
hitShips = []

colors = data.Colors()
debug = print
print = data.betterPrint

def funcCall(func):
    return func()

def placeShips():
    global ships

    ships = battleship_data.placeShips()

    if not runtimedata.noCls: os.system("cls")

    data.printStatusBar()
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for other person...")

    socket.sync(connection)

def game(first):
    if first:
        while True:
            if not runtimedata.noCls: os.system("cls")

            data.printStatusBar()
            debug()

            battleship_data.drawBoard(hitShips)
            battleship_data.drawBoard(ships)
            coord = input("Enter coordinates to shoot >>>").upper()

            if not battleship_data.validCoord(coord, "single"): continue

            socket.send(f"SHOOT {coord}", connection)
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for response...")

            response = socket.receive(None, connection)

            if response == "RESP_SHOOT_HIT":
                ship = battleship_data.HitShip([1, ord(coord[0]) - 65, int(coord[1]) - 1])
                hitShips.append(ship)
            elif response == "RESP_SHOOT_MISS":
                ship = battleship_data.HitShip([0, ord(coord[0]) - 65, int(coord[1]) - 1])
                hitShips.append(ship)
            elif response == "RESP_SHOOT_SUNK":
                response = socket.receive(None, connection)
                startCoord, endCoord = response[0:2], response[2:4]
                startCoord = [ord(startCoord[0]) - 65, int(startCoord[1]) - 1]
                endCoord = [ord(endCoord[0]) - 65, int(endCoord[1]) - 1]

                for line in range(max(min(startCoord[1], endCoord[1]) - 1, 0), min(max(startCoord[1], endCoord[1]) + 1, 9) + 1):
                    for cell in range(max(min(startCoord[0], endCoord[0]) - 1, 0), min(max(startCoord[0], endCoord[0]) + 1, 9) + 1):
                        hitShips.append(battleship_data.HitShip([0, cell, line]))

                for line in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1]) + 1):
                    for cell in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0]) + 1):
                        hitShips.append(battleship_data.HitShip([1, cell, line]))
            else:
                print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from client: {response}")
                input()

            socket.receive(None, connection)

            break

    while True:
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for other person to shoot...")
        response = socket.receive(None, connection)
        if response.startswith("SHOOT"):
            coord = response[6:]
            coord = [ord(coord[0]) - 65, int(coord[1]) - 1]

            hit = False
            for ship in ships:
                if ship.hit(coord):
                    hit = True
                    if ship.sunk():
                        socket.send("RESP_SHOOT_SUNK", connection)
                        socket.send(f"{chr(ship.positions[0][1] + 65)}{ship.positions[0][2] + 1}{chr(ship.positions[-1][1] + 65)}{ship.positions[-1][2] + 1}", connection)
                    else:
                        socket.send("RESP_SHOOT_HIT", connection)

                    break

            if not hit:
                socket.send("RESP_SHOOT_MISS", connection)
                ship = battleship_data.HitShip([0, coord[0], coord[1]])
                ships.append(ship)

            for ship in ships:
                if not ship.sunk():
                    socket.send("CONTINUE", connection)
                    break

                socket.send("WIN", connection)
                print(colors.typeBold, colors.colorBlue, colors.backDefault, "You lost!")
                exit()
        
        else:
            print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from client: {response}")
            input()

        
        if not runtimedata.noCls: os.system("cls")

        data.printStatusBar()
        debug()


        battleship_data.drawBoard(hitShips)
        battleship_data.drawBoard(ships)
        coord = input("Enter coordinates to shoot >>>").upper()

        if not battleship_data.validCoord(coord, "single"): continue

        socket.send(f"SHOOT {coord}", connection)
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for response...")

        response = socket.receive(None, connection)

        if response == "RESP_SHOOT_HIT":
            ship = battleship_data.HitShip([1, ord(coord[0]) - 65, int(coord[1]) - 1])
            hitShips.append(ship)
        elif response == "RESP_SHOOT_MISS":
            ship = battleship_data.HitShip([0, ord(coord[0]) - 65, int(coord[1]) - 1])
            hitShips.append(ship)
        elif response == "RESP_SHOOT_SUNK":
            response = socket.receive(None, connection)
            startCoord, endCoord = response[0:2], response[2:4]
            startCoord = [ord(startCoord[0]) - 65, int(startCoord[1]) - 1]
            endCoord = [ord(endCoord[0]) - 65, int(endCoord[1]) - 1]

            for line in range(max(min(startCoord[1], endCoord[1]), 0), min(max(startCoord[1], endCoord[1]), 9)):
                for cell in range(max(min(startCoord[0], endCoord[0]), 0), min(max(startCoord[0], endCoord[0]), 9)):
                    hitShips.append(battleship_data.HitShip([0, cell, line]))

            for line in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1])):
                for cell in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0])):
                    hitShips.append(battleship_data.HitShip([1, cell, line]))
        else:
            print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from client: {response}")
            input()

        win = socket.receive(None, connection)
        if win == "WIN":
            print(colors.typeBold, colors.colorBlue, colors.backDefault, "You won!")
            exit()

def main():
    global socket, connection

    socket = connman.Socket(server=True)
    runtimedata.connectedServer = "server"

    if not runtimedata.noCls: os.system("cls")

    data.printStatusBar()
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for client connection...")

    socket.createServer(data.serverPort)
    connection, addr = socket.acceptConnection()

    print(colors.typeNormal, colors.colorWhite, colors.backDefault, f"Client connected from {addr[0]}:{addr[1]}")
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Starting game in 3 seconds...")
    time.sleep(3)

    socket.send("START_GAME", connection)
    placeShips()

    if random.random() > 0.5:
        socket.send("START_TURN_FIRST", connection) # Server goes second
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "You are going second")
        game(False)
    else:
        socket.send("START_TURN_SECOND", connection) # Server goes first
        game(True)
