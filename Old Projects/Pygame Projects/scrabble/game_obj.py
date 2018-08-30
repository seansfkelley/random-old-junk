from aux import *

class Player:
    def __init__(self):
        self.letters=[]
        for i in xrange(NUM_LETTERS):
            self.letters.append(all_letters.pop(randint(0,len(all_letters)-1)))
    def add_letters(self):
        while len(self.letters)<NUM_LETTERS and all_letters:
            self.letters.append(all_letters.pop(randint(0,len(all_letters)-1)))
    
