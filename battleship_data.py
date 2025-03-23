import data
import re
import os

import runtimedata

colors = data.Colors()
debug = print
print = data.betterPrint

class Ship:
    def __init__(self, positions):
        self.positions = positions # [ [ALIVE/DEAD X Y] ]

    def hit(self, position):
        if [1, position[0], position[1]] in self.positions:
            self.positions[self.positions.index([1, position[0], position[1]])][0] = 0
            return True
        
        return False
    
    def sunk(self):
        for position in self.positions:
            if position[0] == 1:
                return False
            
        return True
    
    def draw(self, board):
        for position in self.positions:
            if position[0] == 1:
                board[position[2]][position[1]] = colors.escapeSequence + colors.typeNormal + colors.colorBlue + colors.backDefault + colors.finish + "X" + colors.fullReset # Alive
            else:
                board[position[2]][position[1]] = colors.escapeSequence + colors.typeNormal + colors.colorRed + colors.backDefault + colors.finish + "X" + colors.fullReset # Dead

class HitShip:
    def __init__(self, position):
        self.position = position # [MISS/HIT X Y]
    
    def draw(self, board):
        if self.position[0] == 1:
            board[self.position[2]][self.position[1]] = colors.escapeSequence + colors.typeNormal + colors.colorRed + colors.backDefault + colors.finish + "X" + colors.fullReset # Alive
        else:
            board[self.position[2]][self.position[1]] = colors.escapeSequence + colors.typeNormal + colors.colorYellow + colors.backDefault + colors.finish + "X" + colors.fullReset # Dead

    def hit(self, _):
        return False

def funcCall(func):
    return func()

def drawBoard(ships):
    board = [[" " for _ in range(10)] for _ in range(10)]

    for ship in ships:
        ship.draw(board)

    print(colors.typeBold, colors.colorGreen, colors.backDefault, "    A B C D E F G H I J")

    for idx, line in enumerate(board):
        debug("   " + "-" * 21)
        debug(f"{colors.escapeSequence + colors.typeBold + colors.colorGreen + colors.backDefault + colors.finish}{idx + 1: <2}{colors.fullReset} |{"|".join(line)}|")

    debug("   " + "-" * 21)

def validCoord(coord, cType):
    if cType == "single":
        if re.match(r"[A-J]\d", coord):
            return True
    elif cType == "double":
        if re.match(r"[A-J]\d[A-J]\d", coord) and (coord[0] == coord[2] or coord[1] == coord[3]):
            return max(abs(ord(coord[0]) - ord(coord[2])), abs(int(coord[1]) - int(coord[3]))) + 1
    elif cType == "remove":
        if re.match(r"[A-J]\dX", coord):
            return True
        
    return False

def placeShips():
    remainingShips = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    ships = []

    while len(remainingShips) > 0:
        if not runtimedata.noCls: os.system("cls")

        data.printStatusBar()
        debug()

        drawBoard(ships)
        debug(f"You have ships of sizes ({colors.escapeSequence + colors.typeBold + colors.colorRed + colors.backDefault + colors.finish + " ".join(list(map(str, remainingShips))) + colors.fullReset}) remaining")
        debug("The ships have to be separated by at least one cell including diagonals")
        debug(f"To place a ship, type in the coordinates of the first and last cell of the ship (e.g. {colors.escapeSequence + colors.typeBold + colors.colorGreen + colors.backDefault + colors.finish}A1A4{colors.fullReset})")
        debug(f"To remove a ship, type in any coordinate of the ship followed by 'x' (e.g. {colors.escapeSequence + colors.typeBold + colors.colorGreen + colors.backDefault + colors.finish}A1x{colors.fullReset})")
        coord = input(">>>").upper()
        
        if distance := validCoord(coord, "double"):
            if distance not in remainingShips: continue

            startCoord, endCoord = coord[0:2], coord[2:4]
            startCoord = [ord(startCoord[0]) - 65, int(startCoord[1]) - 1]
            endCoord = [ord(endCoord[0]) - 65, int(endCoord[1]) - 1]

            invalid = False
            for line in range(max(min(startCoord[1], endCoord[1]) - 1, 0), min(max(startCoord[1], endCoord[1]) + 1, 9) + 1):
                for cell in range(max(min(startCoord[0], endCoord[0]) - 1, 0), min(max(startCoord[0], endCoord[0]) + 1, 9) + 1):
                    if [1, cell, line] in [position for ship in ships for position in ship.positions]:
                        invalid = True

            if invalid: continue

            if startCoord[0] == endCoord[0]:
                shipPos = []

                for y in range(min(startCoord[1], endCoord[1]), max(startCoord[1], endCoord[1]) + 1):
                    shipPos.append([1, startCoord[0], y])

                newShip = Ship(shipPos)
            elif startCoord[1] == endCoord[1]:
                shipPos = []

                for x in range(min(startCoord[0], endCoord[0]), max(startCoord[0], endCoord[0]) + 1):
                    shipPos.append([1, x, startCoord[1]])

                newShip = Ship(shipPos)
            else:
                print(colors.typeBold, colors.colorRed, colors.backDefault, "UNHANDELED ERROR OCCURED")

            ships.append(newShip)
            remainingShips.remove(distance)

        elif validCoord(coord, "remove"):
            coord = coord[:-1]
            coord = [ord(coord[0]) - 65, int(coord[1]) - 1]
            for ship in ships:
                if ship.hit(coord):
                    remainingShips.append(len(ship.positions))
                    ships.remove(ship)

                    break

    return ships
