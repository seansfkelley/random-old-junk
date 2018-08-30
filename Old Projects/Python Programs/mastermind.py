from random import randint
def makeeasycode():
    count=0
    code=""
    digit=0
    while count<4:
        digit=randint(1, 6)
        while str(digit) in code:
            digit=randint(1, 6)
        code+=str(digit)
        count+=1
    return code

def makehardcode():
    count=0
    code=""
    while count<4:
        code+=str(randint(1, 6))
        count+=1
    return code

def checkguess(guess, answer):
    count=0
    ret=[0, 0]
    for i in answer:
        if i in guess:
            ret[0]+=1
    while count<4:
        if guess[count]==answer[count]:
            ret[1]+=1
        count+=1
    ret[0]-=ret[1]
    return ret

def mastermind():
    congrats=[0,"Wow. Just wow.", "That was incredible!", "Awesome job!", "Nicely done!", "Very good!", "Better than most people.","Congratulations, you're average!","Not bad.","Cutting it close!", "Lucky guess!"]
    mode=0
    print "Beginner: non-repeating code. Advanced: possible repeating code."
    print "In advanced, a one right guess may correspond to two or more different"
    print "but of equal value answers, in which case you are given a hint for"
    print "both. Answer [1233] and guess [5634] will get 1 correct, correct"
    print "position, 1 correct, wrong postion."
    print
    print "Good luck."
    while mode<1 or mode>2:
        mode=input("Enter 1 for beginner and 2 for advanced: ")
    if mode==1:
        answer=makeeasycode()
    else:
        answer=makehardcode()
    guesses=0
    guess=""
    while guess!=answer and guesses<10:
        guess=raw_input("Enter a 4 digit number, using only numbers from 1-6: ")
        g=list(guess)
        x=checkguess(g, answer)
        if guess==answer:
            guesses+=1
            break
        print
        print x[0],"correct, wrong position.",x[1],"correct, correct position."
        guesses+=1
        if guesses!=11:
            print guesses,"guess(es), of 10."
        print
    if guess==answer:
        print congrats[guesses],guesses,"guess(es)."
    else:
        print "Sorry, you lose. The answer was",answer
    a=raw_input("Press enter to restart.")
    if a=="":
        print
        mastermind()

mastermind()

