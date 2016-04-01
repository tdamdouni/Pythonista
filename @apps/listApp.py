# Current version at https://gist.github.com/cclauss/6656495
import console

addPrompt = """Item to be added to the list?
or [M] to return to the main menu:"""

removePrompt = """Item to be removed from the list?
or [M] to return to the main menu:"""

def writeListToFile(inFileName, inList):
    with open(inFileName, 'w') as theFile:
        for theItem in inList:
            theFile.write(theItem + '\n')

def readListFromFile(inFileName, inList = []):
    try:
        with open(inFileName) as theFile:
            for theLine in theFile.readlines():
                inList.append(theLine.rstrip())
    except IOError:
        print('File not found: ' + inFileName)
    return inList

def askUser(inList, inPrompt = ''):
    printList(inList, inPrompt)
    return raw_input().title()

def printList(inList, inPrompt = ''):
    print('{} items: {}'.format(len(inList), inList))
    print('-' * 11)
    if inPrompt:
        print(inPrompt)

def addToList(inList):
    theItem = askUser(inList, addPrompt)
    if theItem == 'M':
        return inList
    elif theItem in inList:  # prevent duplicates
        print(theItem + ' is already in the list.')
    else:
        inList.append(theItem)
    return addToList(inList)

def removeFromList(inList):
    theItem = askUser(inList, removePrompt)
    if theItem == 'M':
        return inList
    elif theItem in inList:
        inList.remove(theItem)
        if not inList:
            return inList
    else:
        print(theItem + ' is not in the list.')
    return removeFromList(inList)

def viewList(inList):
    print("Viewing Data")
    printList(inList)
    return inList

menuChoice = ( '[A]dd to list',
               '[R]emove from list',
               '[V]iew the list',
               '[Q]uit listApp' )

menuDict = { 'A' : addToList,
             'R' : removeFromList,
             'V' : viewList}

def mainLoop(inList):
    print("List App")
    userChoice = askUser(inList, '\n'.join(menuChoice))
    if userChoice == 'Q':
        return inList  # we are done
    elif userChoice in menuDict:
        inList = menuDict[userChoice](inList)
    else:
        print(userChoice + ' is not a recognized command.')
    return mainLoop(inList)  # not yet done; keep looping...

def main():
    console.clear()
    fileName = 'listApp.txt'
    theList = readListFromFile(fileName)
    theList = mainLoop(theList)
    writeListToFile(fileName, theList)
    print('Thank you for using listApp.')

if __name__ == '__main__':
    main()
