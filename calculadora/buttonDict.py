buttonNameList = [
    "C", "CC", " ", " ",
    "7", "8", "9", "÷",
    "4", "5", "6", "x",
    "1", "2", "3", "-",
    "0", ".", "+", "="
    ]

maxPerRow = 3
actualRow = 0
actualColumn = 0
buttonDict = {}

for i in range(len(buttonNameList)):
    if actualColumn > maxPerRow:
        actualColumn = 0
        actualRow += 1

    buttonDict[i+1] = {}
    buttonDict[i+1]['char'] = buttonNameList[i]
    buttonDict[i+1]['row'] = actualRow
    buttonDict[i+1]['column'] = actualColumn
    actualColumn += 1
        
