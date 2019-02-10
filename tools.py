import random

letters = "abcdefghijklmnopqrstuvwxyz"


# Generates a random code of length codeClass.codeLen
def genCode():
    code = ""
    for _ in range(codeClass.codeLen):
        code += random.choice(letters)
    return code


# Ensures the code has not already been created.
def genUniqueCode():
    code = genCode()
    while code in codeClass.codes:
        code = genCode()
    return code


# Find a monster type from monsterClass.monsterTypes, through the String name of the type
def searchMonsterTypesByName(name):
    for monsterType in monsterClass.monsterTypes:
        if monsterType.name == name:
            return monsterType
    return None


# Generate a random, vaguely-pronounceable word.
def generateRandomName(length=3):
    vowels = "aeiou"
    name = ""
    for _ in range(random.randint(1, length)):
        name += random.choice(letters)
        name += random.choice(vowels)
    if bool(random.randint(0, 1)):
        name += random.choice(letters)
    if len(name) == 2 and bool(random.randint(0, 10)):
        name += random.choice(letters)
    return name


# Generates random unicode symbol to use as display symbol in the room.
def unicodeChar():
    exoticChars = 800

    # Banlist blocks stupid unicode chars (like spaces and inconsistent length ones, etc.)
    banList = ["\n", " ", "\t", "\r"]
    for i in range(len(banList)):
        banList[i] = ord(banList[i])
    banList += [4, 21, 127, 128, 149, 17, 26, 2, 144]

    randomChar = random.randint(0, exoticChars)
    while randomChar in banList or chr(randomChar).isspace():
        randomChar = random.randint(0, exoticChars)
    return chr(randomChar).ljust(len(roomClass.emptyChar))


def searchRoomsByCode(code):
    for room in roomClass.rooms:
        if room.code.code == code:
            return room
    return None


def createPlayer():
    validName = False
    playerName = None
    while not validName:
        playerName = input("Enter your name")
        if len(playerName) < 1:
            print("Whoops, that's not a real name! :/")
        else:
            validName = True
    assert playerName is not None, "Oops, something went wrong :/"
    return playerClass(playerName)


# Class representing a unique String used to identify each room
class codeClass:
    codes = []
    codeLen = 3

    def __init__(self):
        self.code = genUniqueCode()
        codeClass.codes.append(self.code)


# Class which holds monsters and other objects, which the player can move around in
class roomClass:
    minRoomSize = 3
    maxRoomSize = 20
    rooms = []
    spaceChar = " "
    emptyChar = " "

    def __init__(self):
        self.size = random.randint(roomClass.minRoomSize, roomClass.maxRoomSize)
        self.contents = [[] for _ in range(self.size)]
        self.code = codeClass()
        self.populateRoom()
        self.playerHere = []
        roomClass.rooms.append(self)

    def printRoom(self):
        print("\n ".ljust(
            int(len(self.contents)) * int(
                len(roomClass.spaceChar) / 2)) + self.code.code.upper())  # Centering room code
        for x in self.contents:
            row = ""
            for y in x:
                if y is not None:
                    row += y.symbol + roomClass.spaceChar
                else:
                    row += roomClass.emptyChar + roomClass.spaceChar
            print(row.ljust(len(self.contents * len(roomClass.spaceChar))))

    def populateRoom(self):
        for x in self.contents:
            for y in range(self.size):
                if not bool(random.randint(0, 5)):
                    x.append(monsterClass())
                else:
                    x.append(None)


# Monsters which can inhabit rooms and attack players, etc.
class monsterClass:
    healthMin = 1
    healthMax = 10
    monsterTypes = []  # Stores types of monsters previously generated
    monsterVariety = 5

    def __init__(self, name=None):
        if name is None:
            if not bool(random.randint(0, monsterClass.monsterVariety)) or len(monsterClass.monsterTypes) == 0:
                self.name = generateRandomName()
                self.health = random.randint(monsterClass.healthMin, monsterClass.healthMax)
                self.symbol = unicodeChar()

                monsterClass.monsterTypes.append(self)
            else:
                monsterType = random.choice(monsterClass.monsterTypes)
                self.copyAttributes(monsterType)
        else:
            monsterType = searchMonsterTypesByName(name)
            self.copyAttributes(monsterType)

    def copyAttributes(self, monsterType):
        self.name = monsterType.name
        self.health = monsterType.health
        self.symbol = monsterType.symbol


# Class for player, stores health, items, etc.
class playerClass:
    def __init__(self, name):
        self.name = name
        self.symbol = name[0].upper()
        self.health = 10
        self.room = None
        self.coords = []
        self.speed = 1
        self.contents = [itemClass("weapon")]

    # Low abstraction method to move player in their room
    def move(self, direction):
        y = self.coords[0]
        x = self.coords[1]
        speed = self.speed
        roomContents = self.room.contents

        # DirectionalKey abstracts movement and attack methods, containing the change in coordinates and edge detection
        directionalKey = {"n": [-speed, 0, y > speed - 1],
                          "e": [0, speed, x < len(roomContents) - speed],
                          "s": [speed, 0, y < len(roomContents) - speed],
                          "w": [0, -speed, x > speed - 1]}
        targetSquare = directionalKey[direction]
        target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
        print(targetSquare)
        if targetSquare[2] and target is None:
            roomContents[y + targetSquare[0]][x + targetSquare[1]] = self
            roomContents[y][x] = None
            self.coords[0] += targetSquare[0]
            self.coords[1] += targetSquare[1]

    # Method for attacking monster in room
    def attack(self, direction, display=False):
        y = self.coords[0]
        x = self.coords[1]
        weapon = self.getWeapon()
        weaponRange = weapon.range
        roomContents = self.room.contents

        # DirectionalKey abstracts movement and attack methods, containing the change in coordinates and edge detection
        directionalKey = {"n": [-weaponRange, 0],
                          "e": [0, weaponRange],
                          "s": [weaponRange, 0],
                          "w": [0, -weaponRange]}
        targetSquare = directionalKey[direction]
        if weapon.range > 0:
            target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
            if target is not None:
                target.health -= weapon.damage
                if target.health < 1:
                    roomContents[y + targetSquare[0]][x + targetSquare[1]] = None
        else:
            weaponRange = 1
            directionalKey = {"n": [-weaponRange, 0],
                              "e": [0, weaponRange],
                              "s": [weaponRange, 0],
                              "w": [0, -weaponRange]}
            targetSquare = directionalKey[direction]
            target = roomContents[y + targetSquare[0]][x + targetSquare[1]]
            if target is not None:
                target.health -= weapon.damage
                self.health -= target.health
                roomContents[y][x] = None
                roomContents[y + targetSquare[0]][x + targetSquare[1]] = self
        if display and target is not None and type(target) is not playerClass:
            player.room.printRoom()
            print(f"HEALTH: {player.health}")
            print(f"{target.name.capitalize()}: {target.health}")

    # Returns the first weapon found in self.contents
    def getWeapon(self):
        for item in self.contents:
            if item.itemType == "weapon":
                return item
        return None


# Items which can be picked up and used by the player
class itemClass:
    itemTypes = ["weapon"] + ["item" for _ in range(30)]

    def __init__(self, itemType=None, power=None):
        if power is None:
            power = random.randint(2, 10)
        self.name = generateRandomName(int(power / 3) + 2)
        self.range = random.randint(0, int(power / 3))
        self.symbol = unicodeChar()
        self.damage = random.randint(1, int(power / 2) + 1)
        self.itemType = itemType
        if itemType is None:
            self.itemType = random.choice(itemClass.itemTypes)  # Determines type of this item


player = createPlayer()  # Includes free code
