#lab28.py

import random
import time
import copy

class char:
    def __init__(self, name, hp, mana, gold=0, xp=0, items=[None], equip=False,\
                 spells=[None], inroom=None, loc=[0,0]):
        self.__maxhp=hp
        self.__name=name
        self.__hp=hp
        self.__mana=mana
        self.__gold=gold
        self.__xp=xp
        self.__items=items
        self.__spells=spells
        if inroom!=None:
            self.__inroom=inroom.name()
        self.stringitemlist()
        self.__weapon=Unarmed
        self.__loc=loc
        if equip:
            for i in self.__items:
                for j in allweapons:
                    if i==j.name() and self.__weapon.name()=="Unarmed":
                        self.equipweap(i)
                        break
    def __str__(self):
        return self.__name+":\nWeapon - "+self.__weapon.name()\
               +"\nHP - "+str(self.__hp)+"\nGold - "+str(self.__gold)\
               +"\nXP - "+str(self.__xp)
    def name(self):
        return self.__name
    def items(self):
        return self.__items
    def removeitem(self, name):##str arg
        self.__items.remove(name)
    def additem(self, name):##str arg
        self.__items+=[name]
    def equipweap(self, weapon):##str arg
        weapon=lowercase(weapon)
        weapon=capitalize(weapon)
        indexnum=self.__items.index(weapon)
        for i in allweapons:
            if i.name()==weapon:
                self.__weapon=i
                break
        if self.__weapon.name()!=weapon:
            print "Invalid weapon."
    def weapon(self):
        return self.__weapon
    def hp(self):
        return self.__hp
    def hurt(self, dmg):
        self.__hp-=dmg
    def heal(self, amt):
        self.__hp+=amt
    def mana(self):
        return self.__mana
    def usemana(self, cost):
        self.__mana-=cost
    def regenmana(self, amt):
        self.__mana+=amt
    def spells(self):##str agr
        return self.__spells
    def addspells(self, name):##str arg
        #does it automatically overwrite the None when the first spell is added?
        self.__spells+=[name]
    def gold(self):
        return self.__gold
    def chnggold(self, gold):
        self.__gold=gold
    def xp(self):
        return self.__xp
    def chngxp(self, xp):
        self.__xp=xp
    def inroom(self):
        return self.__inroom
    def enter(self, rm, start=[-1,-1]):
        print "Entering "+rm.name()+":"
        print rm.desc()
        if start==[-1,-1]:
            self.__loc=rm.start()
        else:
            self.__loc=start
        self.__inroom=rm
        rm.addchar(self)
        rm.update()
        print rm
    def leave(self, rm):
        for i in rm.doors():
            if i[:2]==self.__loc[:2]:
                temp=[i[3], i[4]]
                print temp
                self.enter(i[2], temp)
                break
        rm.removechar(self)
        rm.update()
        walk(self)
    def inroom(self):
        return self.__inroom
    def loc(self):
        return self.__loc
    def chngloc(self, x, y): #this function changes rm.__start
        self.__loc[0]=x
        self.__loc[1]=y
    def stringitemlist(self):
        #replaces all 'instances' with their respective names
        #a list with strings already in it will crash this func
        count=0
        while count<len(self.__items):
            if self.__items[count]!=None: #check if its already a string
                self.__items[count]=self.__items[count].name()
            count+=1

class weap:
    def __init__(self, name, dmg, acc):
        self.__name=name
        self.__dmg=dmg
        self.__acc=acc
    def __str__(self):
        return self.__name+":\nDamage - "+str(self.__dmg)\
               +"\nAccuracy - "+str(self.__acc)+"%"
    def name(self):
        return self.__name
    def dmg(self):
        return self.__dmg
    def chngdmg(self, dmg):
        self.__dmg=dmg
    def acc(self):
        return self.__acc
    def chngacc(self, acc):
        self.__acc=acc

class room:
    def __init__(self, name, desc, x, y, start=[0,0], clist=[]):
        self.__name=name
        self.__desc=desc
        self.__x=x
        self.__y=y
        self.__clist=clist
        self.__start=start
        self.__doors=[]
        count=0
        out=[]
        line=""
        while count<self.__x:
            line+="  "#tile type
            count+=1
        count=0
        while count<self.__y:
            out+=[line]
            count+=1
        self.__layout=out
        self.adddoor(self.__start)
    def __str__(self):
        out=""
        for i in self.__layout:
            out+="\n|"+i[1:]+"|"
        out="_"*(len(self.__layout[0])-1)+out
        out=" "+out
        out+="\n "
        out=out+"¯"*(len(self.__layout[0])-1)
        return out
    def layout(self):
        return self.__layout
    def addobstacle(self, x, y):
        change=self.__layout[y]
        change=change[:(x*2)]+" O"+change[((x+1)*2):]#obstacle type
        self.__layout[y]=change
    def removeobstacle(self, x, y):
        change=self.__layout[y]
        change=change[:(x*2)]+"  "+change[((x+1)*2):]#tile type
        self.__layout[y]=change
    def update(self):
        count=0
        while count<len(self.__layout):
            scount=0
            while scount<len(self.__layout[count]):
                if self.__layout[count][scount] not in "| ":#obstacle type
                    self.__layout[count]=self.__layout[count][:scount]+" "+self.__layout[count][scount+1:]#tile type
                scount+=1
            scount=0
            while scount<len(self.__layout[count]):
                for i in self.__doors:
                    if count==i[1] and scount==i[0]:
                        self.__layout[count]=self.__layout[count][:(scount*2)+1]+""+self.__layout[count][(scount*2)+2:]
                scount+=1
            count+=1
        for i in self.__clist:
            change=self.__layout[i.loc()[1]]
            change=change[:((i.loc()[0])*2)]+" X"+change[((i.loc()[0]+1)*2):]#hero type
            self.__layout[i.loc()[1]]=change
    def name(self):
        return self.__name
    def desc(self):
        return self.__desc
    def chngdesc(self):
        self.__desc=desc
    def clist(self):
        return self.__clist
    def addchar(self, c):#instance arg
        self.__clist+=[c]
    def removechar(self, c):#instance arg
        self.__clist.remove(c)
    def start(self):
        return self.__start
    def doors(self):
        return self.__doors
    def resetdoors(self, all):
        self.__doors=[]
        self.__doors=copy.deepcopy(all)
    def adddoor(self, loc):#doors: ?
        #should have a 3rd arg: which room it goes into, 4th arg: starting loc of that other room
        self.__doors+=[loc]
        self.update()
    def removedoor (self, loc):
        self.__doors.remove(loc)
        self.update()

def lowercase(string):
    out=""
    for i in string:
        if ord(i)>64 and ord(i)<91:
            out+=chr(ord(i)+32)
        else:
            out+=i
    return out

def capitalize(string):
    return chr(ord(string[0])-32)+string[1:]

def walk(c): #when changing obstacle tile, change here too!
    rm=c.inroom()
    directions=[]
    layout=rm.layout()
    loc=c.loc()
    if loc[1]>0 and (layout[loc[1]-1][(loc[0]*2)+1] not in "|"):
        directions+=["N"]
    if loc[0]<(len(layout[0])/2)-1 and (layout[loc[1]][(loc[0]*2)+3] not in "|"):
        directions+=["E"]
    if loc[1]<len(layout)-1 and (layout[loc[1]+1][(loc[0]*2)+1] not in "|"):
        directions+=["S"]
    if loc[0]>0 and (layout[loc[1]][(loc[0]*2)-1] not in "|"):
        directions+=["W"]
    print "You may move",directions
    direct="a"
    directions=lowercase(directions)
    while lowercase(direct) not in directions:
        direct=raw_input("")
    temp=copy.deepcopy(rm.doors())##TEMPORARY SOLUTION - if char.loc is changed manually, the room gets confused
    if direct=="n":
        c.chngloc(c.loc()[0], c.loc()[1]-1)
    if direct=="e":
        c.chngloc(c.loc()[0]+1, c.loc()[1])
    if direct=="s":
        c.chngloc(c.loc()[0], c.loc()[1]+1)
    if direct=="w":
        c.chngloc(c.loc()[0]-1, c.loc()[1])
    rm.resetdoors(temp)
    rm.update()
    for i in rm.doors():
        if c.loc()[:2]==i[:2]:
            c.leave(rm)
        else:
            print rm
            walk(c)

def battle(c1, c2, c2AI=False):
    while c1.hp()>0 and c2.hp()>0:
        action=battleaction(c1)
        if action=="attack":
            attack(c1, c2)
        elif action=="run":
            tobreak=run(c1, c2)
            if tobreak:
                break
        if not c2AI:
            action=battleaction(c2)
        else:
            action="attack"
        if c2.hp()>0:
            if action=="attack":
                attack(c2, c1)
            elif action=="run":
                tobreak=run(c2, c1)
                if tobreak:
                    break

def battleaction(player):
    print
    print player.name()+" ("+str(player.hp())+" HP, "\
          +str(player.mana())+" MP):"
    print "What will you do?"
    actions=["attack", "run"]
    action=" "
    while action not in actions:
        action=raw_input(str(actions)+"\n")
        action=lowercase(action)

def attack(atkr, dfndr):
    if random.randint(1, 100)<=atkr.weapon().acc():
        print atkr.name(),"hits for",atkr.weapon().dmg(),"damage."
        dfndr.hurt(atkr.weapon().dmg())
    else:
        print atkr.name(),"misses!"
    time.sleep(.5)
    if dfndr.hp()<=0:
        print atkr.name(),"is victorious!"

def run(runner, other):
    if random.randint(1, 3)!=1:
        print
        print runner.name(),"runs!"
        print other.name(),"is victorious!"
        return True
    else:
        print "Could not escape!"
        return False

Unarmed=weap("Unarmed", 2, 50)
Hammer=weap("Hammer", 20, 75)
Axe=weap("Axe", 15, 90)
allweapons=[Unarmed,Hammer,Axe]
Thor=char("Thor", 100, 0, 100, 0, [Hammer], True)
Skeletor=char("Skeletor", 100, 0, 100, 0, [Axe], True)
rm3=room("Room 3", "", 3, 3)
rm1=room("Room 1", "A room.", 5, 5, [0,0,rm3,0,0])
rm2=room("Room 2", "A second room", 2, 2, [1,1,rm1,0,0])
Thor.enter(rm2)
walk(Thor)
