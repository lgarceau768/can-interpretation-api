import os, sys, readFile

# read the rules in from the file
canRulesFile = readFile.readRuleFile()

# translate them into something understandable by the api
codeRules = {}
for canRule in canRulesFile:
    translated = readFile.translate(canRule)
    canID = translated.canID
    codeRules[canID] = translated
    
# now need to loop through the csv file and apply the rules above
output = []
with open('vision_data.txt', 'r') as csvFile:
    lines = csvFile.readlines()
    # for vision
    for line in lines:
        line = line.strip().split(' ')
        newList = []
        for item in line:
            if len(item) > 0:
                newList.append(item)
        line = newList
        timestamp = line[0]
        canID = '0x%s' % line[2]
        canMessage = line[5:]
        try:
            rule = codeRules[canID]
            parsed = rule.parseCanMessage(canMessage)
            if parsed != None:
                output.append(parsed)
        except:
            pass
    # for e50
    # for line in lines:
    #     line = line.strip().replace(' ID: ','').replace(' Message: ',',').split(',')
    #     timestamp = line[0]
    #     canID = line[1]
    #     canMessage = line[2]
    #     # need to apply the rules to them
    #     # will check to see if we have a rule for the can id
    #     try:
    #         rule = codeRules[canID]
    #         parsed = rule.parseCanMessage(canMessage)
    #         if parsed != None:
    #             output.append(parsed)
    #     except:
    #         pass
    csvFile.close()
        
with open('outFile.txt','w') as file:
    for item in output:
        file.write('%s\n' % str(item))
