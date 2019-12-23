import os, sys, canMessage

def readRuleFile():
    with open('rules.txt', 'r') as rulesFile:
        canRules = []
        canIDLine = []
        newRule = '+'
        index = -1

        lines =  rulesFile.readlines()
        for line in lines:
            line = line.strip()
            if index >= 0:
                canIDLine.append(line)
            if line == newRule:
                if len(canIDLine) > 0:
                    canRules.append(canIDLine)
                    index += 1
                    canIDLine = []
                else:
                    index += 1            
        if len(canIDLine) > 0:
            canRules.append(canIDLine)
        rulesFile.close()
    return canRules

# for one can rule
def translate(canRule):
    descriptionChar = '-d:'
    functionChar = '-f:'
    ifStatementChar = '-i='
    
    canID = canRule[0].strip().split(' ')[0]
    canDescription = canRule[0].strip().split(' ')[1].replace(descriptionChar, '')
    byteRules = {}
    canRules = {}
    complexRules = {}
    byte = -1
    # now need to loop through the rest of the list and intepret what it says into a rule
    for i in range(1, len(canRule)):
        description = None
        function = None
        # need to split the rule up based on bytes
        if '.' not in canRule[i] and '-c=' not in canRule[i] and '-o=' not in canRule[i]:
            line = canRule[i].strip().split(' ')
            byte = line[0]
            ifs = {}
            for k in range(1, len(line)):
                if descriptionChar in line[k]:
                    description = line[k].replace(descriptionChar, '')
                if functionChar in line[k]:
                    function = line[k].replace(functionChar, '')
                if ifStatementChar in line[k]:
                    ifState = line[k].replace(ifStatementChar, '')
                    ifWhat = ifState.split(':')[0]
                    ifThen = ifState.split(':')[1]
                    ifs[ifWhat] = ifThen

            byteRules[byte] = canMessage.ByteRule(description, function)
            for what in ifs:
                # need to add functionality for adding the if rule to a byte
                byteRules[byte].addIf(what, ifs[what])
            

        # need to also add something custom for checking if a can message is a straight thing
        elif '-c=' in canRule[i]:
            # -c='## ## ## ## ## ## ## ##':Description
            line = canRule[i].strip().replace('-c=','').replace("'",'').split(':')
            ifWhat = line[0]
            ifThen = line[1]
            canRules[ifWhat] = ifThen

        elif '-o=' in canRule[i]:
            line = canRule[i].strip().replace('-o=','').split(':')
            bytesList = line[0]
            ifWhat = line[1]
            complexRules[ifWhat] = bytesList



        # can find the byte by finding the first line w/out a ".""

        # will determine if the byte needs extra rules based on if convert to binary or not
        else:
            # this means that the line corresponds to a byte.binaryDigit
            line = canRule[i].strip().split(' ')
            ifs = {}
            # corresponds to the current byte 
            # need to pull out which binary digit the line corresponds to 
            binaryDigit = line[0][line[0].find('.')+1:]
            # need to also loop through the line and determine what to do because of it
            # if for binary values easy =1 or =0
            for k in range(1, len(line)):
                if ifStatementChar in line[k]:
                    ifState = line[k].replace(ifStatementChar, '')
                    ifWhat = ifState.split(':')[0]
                    ifThen = ifState.split(':')[1]
                    ifs[ifWhat] = ifThen
                if descriptionChar in line[k]:
                    description = line[k].replace(descriptionChar, '')
                    byteRules[byte].description = description
            # add the binary rules to the canRule
            for what in ifs:
                byteRules[byte].addIf(what, ifs[what], digit=binaryDigit)   

    # need to create the can rule from the above byte rules
    return canMessage.CanRule(canID, canDescription, byteRules=byteRules, canRules=canRules, complexRules=complexRules)
        

