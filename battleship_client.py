import os
import time

import connman
import runtimedata
import data as gcgData

import battleship_data

colors = gcgData.Colors()
debug = print
print = gcgData.betterPrint

socket = connman.Socket(client=True)
ships = []
hitShips = []

def funcCall(func):
    return func()

def placeShips():
    global ships

    ships = battleship_data.placeShips()

    if not runtimedata.noCls: os.system("cls")

    gcgData.printStatusBar()
    debug()
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for other person...")

    socket.sync()

def game(first):
    if first:
        while True:
            if not runtimedata.noCls: os.system("cls")

            gcgData.printStatusBar()
            debug()

            battleship_data.drawFull(ships, hitShips)
            
            while True:
                coord = input("Enter coordinates to shoot >>>").upper()

                if not battleship_data.validCoord(coord, "single"): continue
                else: break

            socket.send(f"SHOOT {coord}")
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for response...")

            response = socket.receive(None)

            if response == "RESP_SHOOT_HIT":
                ship = battleship_data.HitShip([1, ord(coord[0]) - 65, int(coord[1:]) - 1])
                hitShips.append(ship)
            elif response == "RESP_SHOOT_MISS":
                ship = battleship_data.HitShip([0, ord(coord[0]) - 65, int(coord[1:]) - 1])
                hitShips.append(ship)
                socket.receive(None)
                break
            elif response == "RESP_SHOOT_SUNK":
                response = socket.receive(None)
                data = battleship_data.validCoord(response, "double")
                startCoord, endCoord = data[0][0], data[0][1]
                startCoord = [ord(startCoord[0]) - 65, int(startCoord[1]) - 1]
                endCoord = [ord(endCoord[0]) - 65, int(endCoord[1]) - 1]

                for line in range(max(min(startCoord[1], endCoord[1]) - 1, 0), min(max(startCoord[1], endCoord[1]) + 1, 9) + 1):
                    for cell in range(max(min(startCoord[0], endCoord[0]) - 1, 0), min(max(startCoord[0], endCoord[0]) + 1, 9) + 1):
                        hitShips.append(battleship_data.HitShip([0, cell, line]))

                for line in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1]) + 1):
                    for cell in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0]) + 1):
                        hitShips.append(battleship_data.HitShip([1, cell, line]))
            else:
                print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from server: {response}")
                input()

            socket.receive(None)

    while True:
        if not runtimedata.noCls: os.system("cls")

        gcgData.printStatusBar()
        debug()

        battleship_data.drawFull(ships, hitShips)

        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for other person to shoot...")
        response = socket.receive(None)
        if response.startswith("SHOOT"):
            coord = response[6:]
            coord = [ord(coord[0]) - 65, int(coord[1:]) - 1]

            hit = False
            for ship in ships:
                if ship.hit(coord):
                    hit = True
                    if ship.sunk():
                        battleship_data.laterPrint(colors.typeBold, colors.colorRed, colors.backDefault, "Your ship sank!")

                        socket.send("RESP_SHOOT_SUNK")
                        socket.send(f"{chr(ship.positions[0][1] + 65)}{ship.positions[0][2] + 1}{chr(ship.positions[-1][1] + 65)}{ship.positions[-1][2] + 1}")

                        startCoord = [ship.positions[0][1], ship.positions[0][2]]
                        endCoord = [ship.positions[-1][1], ship.positions[-1][2]]
                        for line in range(max(min(startCoord[1], endCoord[1]) - 1, 0), min(max(startCoord[1], endCoord[1]) + 1, 9) + 1):
                            for cell in range(max(min(startCoord[0], endCoord[0]) - 1, 0), min(max(startCoord[0], endCoord[0]) + 1, 9) + 1):
                                ships.append(battleship_data.HitShip([0, cell, line]))

                        for line in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1]) + 1):
                            for cell in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0]) + 1):
                                ships.append(battleship_data.HitShip([1, cell, line]))
                    else:
                        battleship_data.laterPrint(colors.typeBold, colors.colorRed, colors.backDefault, "Your ship got hit!")
                        socket.send("RESP_SHOOT_HIT")

                    gameContinue = False
                    for ship in ships:
                        if not ship.sunk():
                            socket.send("CONTINUE")
                            gameContinue = True
                            break

                    if not gameContinue:
                        socket.send("WIN")
                        print(colors.typeBold, colors.colorBlue, colors.backDefault, "You lost!")
                        time.sleep(10)
                        exit()

            if hit: continue

            #if not hit:
            socket.send("RESP_SHOOT_MISS")
            socket.send("CONTINUE")
            ship = battleship_data.HitShip([0, coord[0], coord[1]])
            ships.append(ship)
        
        else:
            print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from server: {response}")
            input()



        while True:
            if not runtimedata.noCls: os.system("cls")

            gcgData.printStatusBar()
            debug()

            battleship_data.drawFull(ships, hitShips)

            while True:
                coord = input("Enter coordinates to shoot >>>").upper()

                if not battleship_data.validCoord(coord, "single"): continue
                else: break

            socket.send(f"SHOOT {coord}")
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for response...")

            response = socket.receive(None)

            if response == "RESP_SHOOT_HIT":
                ship = battleship_data.HitShip([1, ord(coord[0]) - 65, int(coord[1:]) - 1])
                hitShips.append(ship)
            elif response == "RESP_SHOOT_MISS":
                ship = battleship_data.HitShip([0, ord(coord[0]) - 65, int(coord[1:]) - 1])
                hitShips.append(ship)
                win = socket.receive(None)
                break
            elif response == "RESP_SHOOT_SUNK":
                response = socket.receive(None)
                data = battleship_data.validCoord(response, "double")
                startCoord, endCoord = data[0][0], data[0][1]
                startCoord = [ord(startCoord[0]) - 65, int(startCoord[1]) - 1]
                endCoord = [ord(endCoord[0]) - 65, int(endCoord[1]) - 1]

                for line in range(max(min(startCoord[1], endCoord[1]) - 1, 0), min(max(startCoord[1], endCoord[1]) + 1, 9) + 1):
                    for cell in range(max(min(startCoord[0], endCoord[0]) - 1, 0), min(max(startCoord[0], endCoord[0]) + 1, 9) + 1):
                        hitShips.append(battleship_data.HitShip([0, cell, line]))

                for line in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1]) + 1):
                    for cell in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0]) + 1):
                        hitShips.append(battleship_data.HitShip([1, cell, line]))
            else:
                print(colors.typeNormal, colors.colorRed, colors.backDefault, f"Invalid response from server: {response}")
                input()

            win = socket.receive(None)
            if win == "WIN":
                print(colors.typeBold, colors.colorBlue, colors.backDefault, "You won!")
                time.sleep(10)
                exit()

def main():
    global socket

    if not runtimedata.noCls: os.system("cls")

    gcgData.printStatusBar()
    debug()

    if not runtimedata.localGame:
        socket = runtimedata.clientSocket

        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Waiting for server to start the game...")

        socket.receive(10)
        placeShips()

        turn = socket.receive(5)

        if turn == "START_TURN_FIRST":
            game(True)
        else:
            print(colors.typeNormal, colors.colorWhite, colors.backDefault, "You are going second")
            game(False)

        exit()
    
    ip = input("Enter ip address of the server >>>")
    runtimedata.connectedServer = ip
    socket.connect(ip, gcgData.serverPort, 5)

    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "Connected to server")
    print(colors.typeNormal, colors.colorWhite, colors.backDefault, "The game will start soon...")

    socket.receive(10)
    placeShips()

    turn = socket.receive(5)

    if turn == "START_TURN_FIRST":
        game(True)
    else:
        print(colors.typeNormal, colors.colorWhite, colors.backDefault, "You are going second")
        game(False)
