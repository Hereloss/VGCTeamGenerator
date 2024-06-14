import requests
import html2text
import re
import random

baseUrl = "https://munchstats.com/gen9vgc2024regg/1760/"

listOfPokemonDetails = []

restrictedAdded = False

listOfRestricted = ["Calyrex-Shadow", "Calyrex-Ice", "Terapagos", "Miraidon", "Koraidon", "Groudon", "Zamazenta",
                    "Zacian", "Lunala", "Kyurem-White", "Kyurem-Black", "Kyogre", "Eternatus", "Zamazenta-Crowned",
                    "Zacian-Crowned", "Mewtwo", "Dialga", "Palkia", "Lugia", "Ho-Oh", "Rayquaza", "Giratina", "Zekrom",
                    "Reshiram", "Solgaleo", "Necrozma-Dawn-Wings", "Necrozma-Dusk-Mane", "Necrozma", "Calyrex",
                    "Dialga-Origin", "Palkia-Origin", "Giratina-Origin", "Kyurem"]

usedItems = []

potentialPartners = {}

fullyNamedTeam = False

teamNames = []

choiceBannedMoves = ["Protect", "Helping Hand", "Follow Me", "Nasty Plot", "Trick Room", "Tailwind", "Decorate",
                     "Encore", "Wide Guard", "Spore", "Rage Powder", "Calm Mind"]


def generateTeam(name):
    print("Getting details for your captain")
    restrictedAdded = False
    name = name
    currentNumberOnForNamedTeam = 0
    while len(listOfPokemonDetails) < 6:
        print("Generating " + name)
        data = getPokemonDetails(name)
        createPokemon(name, data)
        if any(name in s for s in listOfRestricted):
            restrictedAdded = True
        addToPartners(data)
        if (fullyNamedTeam):
            name = teamNames[currentNumberOnForNamedTeam]
            if name == "":
                name = findNextPokemon()
            currentNumberOnForNamedTeam += 1
        else:
            name = findNextPokemon()
            if restrictedAdded:
                # print("Error - double restricted!")
                while any(name in s for s in listOfRestricted):
                    name = findNextPokemon()
            else:
                if (len(listOfPokemonDetails) == 5):
                    print("No restricted pokemon - last one will be forced as one")
                    name = getARestricted()

    print("Complete! Your team is: \n")
    print("\n\n".join(listOfPokemonDetails))


def addToPartners(data):
    for (pokemon, percentage) in data[1].items():
        if pokemon in potentialPartners:
            currentPercentage = potentialPartners[pokemon] * (len(listOfPokemonDetails) - 1)
            percentageNum = float(percentage)
            potentialPartners[pokemon] = (percentageNum + currentPercentage) / len(listOfPokemonDetails)
        else:
            percentageNum = float(percentage)
            potentialPartners[pokemon] = percentageNum / len(listOfPokemonDetails)


def findNextPokemon():
    complete = False
    newTeammate = ""
    while not complete:
        allowed = True
        newTeammate = getTeamFromPercentage(potentialPartners)
        for pokemon in listOfPokemonDetails:
            if re.search(newTeammate, pokemon):
                # print("New teammate: " + newTeammate + " not allowed")
                allowed = False
            elif re.search(newTeammate.split("-")[0], pokemon):
                # print("New teammate: " + newTeammate + " not allowed")
                allowed = False
        complete = allowed
    return newTeammate


def getARestricted():
    for (name, value) in potentialPartners.items():
        for (restrictedName) in listOfRestricted:
            if name == restrictedName:
                return name
    print("No potential restricted partners - will default to first in list")
    return restrictedName[0]


def getPokemonDetails(name):
    url = baseUrl + name
    r = requests.get(url)
    text = r.text
    formattedData = formatText(name, text)
    return formattedData


def createPokemon(name, data):
    moves = generateMovesFromPercentages(data[0])
    item = getItemFromPercentage(data[2], moves)
    while any(item in s for s in usedItems):
        item = getItemFromPercentage(data[2], moves)
    usedItems.append(item)
    ability = getFromPercentage(data[3])
    nature = getFromPercentage(data[5])
    stats = chooseStatDist(data[4], nature)
    tera = getFromPercentage(data[6])
    print("Pokemon created!")
    paste = formatPokemon(name, moves, item, ability, stats, tera)
    listOfPokemonDetails.append(paste)


def formatPokemon(name, moves, item, ability, stats, tera):
    formatMoves = ""
    for move in moves:
        formatMoves += "- " + move + "\n"
    nature = stats.split(":")[0]
    actualStats = stats.split(":")[1]
    formatStats = ""
    index = 0
    for stat in actualStats.split("/"):
        if index == 0:
            formatStats += stat + " HP /"
        elif index == 1:
            formatStats += stat + " Atk /"
        elif index == 2:
            formatStats += stat + " Def /"
        elif index == 3:
            formatStats += stat + " SpA /"
        elif index == 4:
            formatStats += stat + " SpD /"
        elif index == 5:
            formatStats += stat + " Spe"
        index += 1
    return name + " @ " + item + " \n Ability: " + ability + "\n Level: 50 \n Tera Type: " + tera + "\n EVs: " + formatStats + " \n " + nature + " Nature \n" + formatMoves


def generateMovesFromPercentages(data):
    moves = []
    total = sumValues(data)
    while len(moves) < 4:
        randomNum = random.random() * (total / 4)
        currentNum = 0
        for (key, value) in data.items():
            valueNum = float(value)
            currentNum += valueNum
            if (randomNum < currentNum):
                moves.append(key)
                break
        data.pop(key)
    return moves


def getFromPercentage(data):
    total = sumValues(data)
    randomNum = random.random() * total
    currentNum = 0
    for (key, value) in data.items():
        valueNum = float(value)
        currentNum += valueNum
        if (randomNum < currentNum):
            return key


def sumValues(data):
    total = 0
    for (key, value) in data.items():
        total = total + float(value)
    return total


def getItemFromPercentage(data, moves):
    total = sumValues(data)
    randomNum = random.random() * total
    choiceBannedCount = 0
    currentNum = 0
    choiceBanned = False
    for (move) in moves:
        if any(move in s for s in choiceBannedMoves):
            choiceBanned = True
    item = ""
    while item == "":
        for (key, value) in data.items():
            valueNum = float(value)
            currentNum += valueNum
            if (randomNum < currentNum):
                item = key
                break
        if choiceBanned & has_choice(item):
            if (choiceBannedCount > 20):
                item = getNonChoiceItem(data)
                print("Choice banned - but no other items found within 20 attempts, using: " + item)
                break
            item = ""
            choiceBannedCount += 1
    return item

def getNonChoiceItem(data):
    for (key, value) in data.items():
        if not re.search('Choice', key):
            if not re.search('Assault', key):
                return key
    return random.choice(list(data.items()))



def has_choice(inputString):
    if re.search('Choice', inputString):
        return True
    elif re.search('Assault', inputString):
        return True
    else:
        return False


def getTeamFromPercentage(data):
    total = 0
    for (key, value) in data.items():
        valueNum = float(value)
        total += valueNum
    randomNum = random.random() * total
    currentNum = 0
    while True:
        for (key, value) in data.items():
            valueNum = float(value)
            currentNum += valueNum
            if (randomNum < currentNum):
                return key
        randomNum = random.random() * total


def chooseStatDist(data, nature):
    total = 0
    newData = {}
    for (key, value) in data.items():
        if re.search(nature, key):
            valueNum = float(value)
            total += valueNum
            newData[key] = value

    if newData == {}:
        newData = data
    randomNum = random.random() * total
    currentNum = 0

    for (key, value) in newData.items():
        valueNum = float(value)
        currentNum += valueNum
        if (randomNum < currentNum):
            return key


def formatText(name, text):
    response = html2text.html2text(text)
    if not re.search(name, text):
        print(
            "Chosen Captain is not usable in the meta - most used pokemon picked instead (or you misspelt its name). Name will be unchanged on paste")
        subCaptain = text.split("Current Pokemon:")[1].split("</span>")[0].split("<span>")[1]
        print("Substitute Captain: " + subCaptain)
    moves = response.split("Moves")[1].split("## Teammates")[0].split("*")
    moveMap = ConvertToMap(moves, " ")
    teammates = response.split("Teammates")[1].split("## Items")[0].split("*")
    teammateMap = ConvertToMap(teammates, "\n\n")
    items = response.split("Items")[1].split("## Abilities")[0].split("*")
    itemsMap = ConvertToMap(items, "\n\n")
    abilities = response.split("Abilities")[1].split("## EV Spreads")[0].split("*")
    abilitiesMap = ConvertToMap(abilities, " ")
    evSpreads = response.split("EV Spreads")[1].split("## Natures")[0].split("*")
    evSpreadsMap = ConvertToMap(evSpreads, " ")
    natures = response.split("Natures")[1].split("## Top EVs By Category")[0].split("*")
    naturesMap = ConvertToMap(natures, " ")
    teraType = response.split("Tera Type")[1].split("## Export Pokemon")[0].split("*")
    teraTypeMap = ConvertToMap(teraType, " ")
    return [moveMap, teammateMap, itemsMap, abilitiesMap, evSpreadsMap, naturesMap, teraTypeMap]


def ConvertToMap(list, splitter):
    res_dct = {}
    for (item) in enumerate(list):
        splitList = item[1].split(splitter)
        split = mysplit(splitList).split(";")
        key = split[0]
        value = split[1].replace("%", "")
        if key.strip() == "":
            continue
        elif value.strip() == "":
            continue
        res_dct[key] = value
    return res_dct


def mysplit(s):
    name = ""
    value = ""
    for (attribute) in s:
        if not has_numbers(attribute):
            name += attribute + " "
        else:
            if has_slash(attribute):
                name += attribute + " "
            else:
                value = attribute.strip()
    nameList = name.split(" ")
    name = " ".join(filter(None, nameList))
    return name + ";" + value


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def has_slash(inputString):
    if re.search('/', inputString):
        return True
    else:
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    name = input("Name your captain:")
    if (name == ""):
        print("No name given, will pick a random restricted captain")
        name = random.choice(listOfRestricted)
        print("Your captain is: " + name)
    bo3 = input("Best of 3?")
    if bo3 == "y":
        baseUrl = "https://munchstats.com/gen9vgc2024reggbo3/1760/"
        print("Best of 3 is being used")
    fullyNamed = input("Do you want to name all your pokemon?")
    if fullyNamed == "y":
        fullyNamedTeam = True
        while len(teamNames) < 5:
            nextName = input("Please input the next name:")
            teamNames.append(nextName)
        teamNames.append("End")
    generateTeam(name)
