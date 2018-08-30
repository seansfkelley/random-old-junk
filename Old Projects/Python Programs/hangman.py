#hangman!

def hangman(word):
    guess="-"*len(word)
    numwrong=0
    print "Hangman!"
    print guess
    while numwrong!=6:
        letter=raw_input("Guess: ")
        temp=guess
        guess=check(letter, guess, word)
        if guess==temp:
            numwrong+=1
            print "Wrong guess. " + str(6-numwrong) + " guesses left."
        else:
            print "Correct guess!"
        print
        print guess
        if guess==word:
            numwrong=6
            print "Congratulations!"
    print "Answer: " + word
    print "Game Over!"

def check(letter, guess, word):
    count=0
    while count<len(word):
        if letter==word[count]:
            guess=guess[0:count]+letter+guess[count+1:]
        count+=1
    return guess
