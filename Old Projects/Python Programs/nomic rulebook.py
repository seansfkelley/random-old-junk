from copy import deepcopy

class rule:
    def __init__(self, text, number, mutable=True):
        self.__text=text
        self.__number=number
        self.__mutable=mutable
        self.__amendments=[]
        self.__errata=[]
    def setText(self, text):
        self.__text=text
    def getText(self):
        return self.__text
    def setNumber(self, number):
        self.__number=number
    def getNumber(self):
        return self.__number
    def getMutable(self):
        return self.__mutable
    def transmute(self):
        self.__mutable=not self.__mutable
    def amend(self, text):
        self.__amendments+=[text]
    def repealAmend(self, number):
        self.__amendments=self.__amendments[:number-1]+self.__amendments[number:]
    def getAmendment(self, number):
        return self.__amendments[number-1]
    def errata(self, text):
        self.__errata+=[text]
    def repealErrata(self, number):
        self.__errata=self.__errata[:number-1]+self.__errata[number:]
    def getErrata(self, number):
        return self.__errata[number-1]
    def __str__(self):
        ret='Rule '+str(self.__number)+':\nMutable: '+str(self.__mutable)+'\n'+self.__text
        if len(self.__amendments)>0:
            ret+='\nAmendments:'
            for i in range(0, len(self.__amendments)):
                ret=ret+'\n '+str(i+1)+'. '+self.__amendments[i]
        if len(self.__errata)>0:
            ret+='\nErrata:'
            for i in range(0, len(self.__errata)):
                ret=ret+'\n '+str(i+1)+'. '+self.__errata[i]
        return ret
    def dataString(self):
        a='0'
        if self.__mutable:
            a='1'
        ret=str(self.__number)+'\n'+a+'\n'+self.__text
        if len(self.__amendments)>0:
            ret+='\nA'
            for i in range(0, len(self.__amendments)):
                ret=ret+'\n'+self.__amendments[i]
        if len(self.__errata)>0:
            ret+='\nE'
            for i in range(0, len(self.__errata)):
                ret=ret+'\n'+self.__errata[i]
        return ret

def setRules(name):
    ruleFile=open(name+'.txt', 'r')
    rules=ruleFile.readlines()
    for i in range(0, len(rules)):
        rules[i]=rules[i][:-1]
    i=0
    newRules=[]
    while len(rules)>2:
        if rules[i]=='':
            newRule=rule(rules[2], int(rules[0]), bool(int(rules[1])))
            ##start adding amends/errata
            tempRules=rules[3:i]
            if len(tempRules)>0:
                if tempRules[0]=='A':
                    tempRules=tempRules[1:]
                    while len(tempRules)>0 and tempRules[0]!='E':
                        newRule.amend(tempRules[0])
                        tempRules=tempRules[1:]
                if tempRules[0]=='E':
                    tempRules=tempRules[1:]
                    while len(tempRules)>0:
                        newRule.errata(tempRules[0])
                        tempRules=tempRules[1:]
            newRules+=[deepcopy(newRule)]
            rules=rules[i+1:]
            i=-1
        i+=1
    return newRules

def saveRules(name, rules):
    ruleFile=open(name+'.txt', 'w')
    for i in range(0, len(rules)):
        ruleFile.writelines(rules[i].dataString()+'\n\n')

def getRuleByNum(number, rules):
    temp=[]
    for i in range(0, len(rules)):
        if rules[i].getNumber==number:
            temp+=rules[i]
    return temp

def play():
    x='a'
    while x not in 'ynYN':
        x=raw_input('Load old game? Y/N: ')
    name='defaultRules'
    if x in 'yY':
        name=raw_input('Filename? ')
    rules=setRules(name)
    legalCommands=['amend', 'errata', 'repeal', 'get', 'save', 'quit']
    while True:
        x=raw_input('')
        x=x.lower()
        x=x.split(' ')
        if x[0] not in legalCommands:
            print 'Unrecognized command: '+x[0]
            continue
        if x[0]=='save':
            name='defaultRules'
            while name=='defaultRules':
                name=raw_input('Filename? ')
            saveRules(name, rules)
            continue
        if x[0]=='quit':
            a='a'
            while a not in 'ynYN':
                a=raw_input('Save before quitting? Y/N: ')
            if a in 'yY':
                name='defaultRules'
                while name=='defaultRules':
                    name=raw_input('Filename? ')
                saveRules(name, rules)
            break
        if x[0]=='get':
            if x[1]=='all':
                for i in rules:
                    print i
                continue
            if x[1][4]=='-':
                pass
                ##print in range with format 'get 100-101'
            
