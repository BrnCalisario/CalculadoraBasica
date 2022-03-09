buttonNameList = [
    "C", "CC", ":)", "÷",
    "7", "8", "9", "x",
    "4", "5", "6", "-",
    "1", "2", "3", "+",
    "0", ".", ":D", "="
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
        
