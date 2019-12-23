import os, sys, cv

class ByteRule:
    def __init__(self, description, function):
        self.ifs = {}
        self.binary = False
        self.description = description
        if function != None:
            self.function = function.strip()
            if self.function == '->B':
                self.binary = True  
        super().__init__()

    # when given an input byte it will return the corresponding output based on the rules
    def processRule(self, byteValue):
        if self.binary:
            # need to intepret rule from format {'digit':'if:then'}
            for digit in self.ifs:
                ifWhat = self.ifs[digit].split(':')[0]
                ifThen = self.ifs[digit].split(':')[1]
                byteValue = cv.binLong(byteValue)
                if byteValue[int(digit)] == ifWhat:
                    return cv.json(self.description, ifThen)
        else:
            for what in self.ifs:
                if byteValue == what:
                    return cv.json(self.description, self.ifs[what])

    # add if to the rules for this byte 
    # can only process ==
    def addIf(self, what, then, digit=None):
        if digit == None:
            self.ifs[what] = then
        else:
            # format {'digit':'if:then'}
            self.ifs[digit] = '%s:%s' % (what, then)

class CanRule:
    def __init__(self, canID, description, byteRules=None):
        self.byteRules = {}
        if byteRules != None:
            self.byteRules = byteRules
        self.canID = canID
        self.description = description
        super().__init__()
    
    def addByteRule(self, byteNum, description, function):
        self.byteRules[byteNum] = ByteRule(description, function)

    def parseCanMessage(self, dataBytes):
        messages = []
        dataBytes = dataBytes.strip().split(' ')
        for i in range(0, len(dataBytes)):
            # 0-7 = total of 8 iterations
            try:
                rule = self.byteRules[str(i)]
                # if this passes then there is a rule associated with that byte
                processed = rule.processRule(dataBytes[i])
                if processed != None:
                    messages.append(processed)
            except:
                # no rule on that byte
                pass
        if len(messages) > 0:
            return messages
        return None


