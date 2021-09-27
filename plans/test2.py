import random #imports random so i can choose a random word

#this function gets a random word from the words list and returns it as a lowercase and stripped of spaces
def getword():
    f = open('words.txt')
    sampleWords = f.readlines()
    randomWord = random.choice(sampleWords)
    theWord = randomWord.strip().lower()
    return theWord

#this function plays the game, does the looping and checking etc.
def playGame(theWord):
    guessesLeft = 7
    runningGuess = ""
    while guessesLeft > 0:
        guess = (str(input('\nGuess the word or a letter in the word: '))).lower()  
        if guess == theWord:
            guessesLeft = 0
            print('\nNice! You guessed the word!')
            return True

        elif guess in theWord and len(guess) == 1:  
            print("\n Yeah, that letter's in the word, keep guessing! ")
            runningGuess = runningGuess + guess 
            wrongL = 0 
            
            for letter in theWord:
                if letter in runningGuess:
                    print(letter, end="/")
                else:
                    print("_", end="|")
                    wrongL = wrongL + 1 
        
            if wrongL == 0:
                guessesLeft = 0
                print("\nNice! You guessed the word!")   
                return True
        else:
            guessesLeft = guessesLeft - 1
            print("Nope - that's not it, try again!")
            print("\n guesses left = " + str(guessesLeft))
            if guessesLeft == 0:
                print ("You couldn't guess it! :(")
                print ("\n the word was: " + theWord)
                return False

#body of my code - does one call then loops as long as the user selects y
gamesPlayed = 0
gamesWon = 0

theWord = getword()
firstGame = playGame(theWord)
gamesPlayed = gamesPlayed + 1

if firstGame == True:
    gamesWon = gamesWon + 1
else:
    gamesWon = 0

while input("Have another go? hit y to continue, otherwise hit any key to quit: ").lower() == "y":
    theWord = getword()
    playGame(theWord)

    gamesPlayed = gamesPlayed + 1
    if playGame(theWord) == True:
        gamesWon = gamesWon + 1
    else:
        gamesWon = gamesWon
    
    print("\nGames Played: " + str(gamesPlayed))
    print("\nGames Won: " + str(gamesWon))

print('Alright, bye!')
print('You won: ' + str(gamesWon) + ' and lost: ' + str(gamesPlayed - gamesWon) + ' games')





            for letter in puzzle:
                if letter == " ":
                    print("  ")
                elif letter in guesses:
                    print(letter.upper(), end="/")
                else:
                    print("_", end="|")



                    def miniMenu():

    print("""
        ---------------------------------

        What do you want to do?
        [1.] Spin the Wheel
        [2.] Buy a Vowel
        [3.] Rage Quit

        ----------------------------------
    """)

    try:
        selection = int(input('Choose an option from above: '))
        if selection == 1:
            spinWheel(theWheel)
        elif selection == 2:
            buyVowel()
        elif selection == 3:
            exitGame()
        else:
            print('wait, what? choose an option from the menu!')
            miniMenu()
    except ValueError:
        print('enter a number, and one that is from the menu!')
        miniMenu()