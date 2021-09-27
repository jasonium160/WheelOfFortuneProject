import csv
import random

#loading a csv containing puzzles, categories and hints I made up, and saving it to a dictionary
f = open('WOFDictionary.csv','r')
reader = csv.reader(f)
wofStuff = {}
for row in reader:
    puzzle = row[0]
    wofStuff[puzzle] = {'category':row[1], 'hint':row[2]}
f.close()

#24 choices, repeated some numbers to make it up to 24, -1 is lose a chance, -10 is bankrupt
#tried a shorthand way to keep the datatype consistent for my logic checks later on
theWheel = [100,150,200,250,300,350,350,400,450,450,500,500,550,600,650,700,750,800,850,900,
            -10,-1,-1,-10]
vowels = ('a e i o u').split()
consonants = ('b c d f g h j k l m n p q r s t v w x y z').split()

usedPuzzles = [] #made a list to keep track of puzzles already used in case of playing the same puzzle twice

# 3 players stored in a dictionary as player-name: bank pairs
players = {'Player1': 0, 'Player2': 0, 'Player3': 0}
playerName = list(players.keys()) #since i'm storing the keys as a list, player 1 will be indexed at 0

#------------------------------------------------------------------------------------------------------------------------------
# gets the puzzle from the dictionary wofStuff, I can then use the puzzle as a key to get its hint and category
def getPuzzle():
    thePuzzle = random.choice(list(wofStuff.keys()))
    if thePuzzle not in usedPuzzles:  #checks if it's been used in a previous round
        usedPuzzles.append(thePuzzle)
        return thePuzzle
    else:
        thePuzzle = getPuzzle()

#-------------------------------------------------------------------------------
# 'spins' the wheel - randomly chooses an item in the list and returns it
def spinWheel(theWheel):
    aSpin = random.choice(theWheel)
    return aSpin

#-------------------------------------------------------------------------------
# buy a vowel, if a vowel isn't selected it calls itself again until one is
# otherwise, it returns the vowel
def buyVowel(vowels):
    print('Choose a vowel: A E I O U')
    selection = str(input('Which one do you want?: ')).lower()
    if selection in vowels:
        return selection
    else:
        print('Choose something from the list!')
        buyVowel(vowels)

#-------------------------------------------------------------------------------
# mini menu so player can spin wheel, buy vowel or guess the puzzle
# returns the choice which will be evaluted in the main code block, i couldn't figure
# out an easy way of doing the evaluations in the individual functions without losing 
# track of player's bank and guesses
def miniMenu():
    print("""\n Select an option from below: 
                [1]. Spin the Wheel
                [2]. Buy a Vowel
                [3]. Guess the whole puzzle
    """)
    try:
        selection = int(input("What'll it be? "))
        if selection == 1: 
           return 1 #returns 1 to main code, so i know they chose 1 from there
        elif selection == 2: 
            return 2 #same reasoning for 2 and 3
        elif selection == 3:
            print('You chose to guess the puzzle, good luck!')
            return 3
        else: #they didn't choose a menu option
            print('wait, what? choose something from the menu!')
            miniMenu()
    except ValueError: #they probably entered a string etc.
        print('Huh?! what happened? choose something from the menu, either 1, 2 or 3!!')
        miniMenu()

#-------------------------------------------------------------------------------
#shows the puzzle board and updates it as it gets filled in
def showBoard(puzzle,guesses):
    print('\nThe Board: ')
    print('-'*40)
    for letter in puzzle:
        if letter == " ":
            print("  ")
        elif letter in guesses:
            print(letter.upper(), end=" ")
        else:
            print("_", end="|")
    print('')
    print('-'*40)

#-------------------------------------------------------------------------------
#takes the puzzle phrase or word, and the boolean wordguessed as arguments
#iterates through a while loop until worguessed returns true when the puzzle is
#filled in completely
def playGame(puzzle, wordGuessed, playerTurn):
    while wordGuessed == False:
        #playerturn is the index of the list of keys from players, i use this to indirectly identify 
        #the key i.e. index 0 represents player 1, index 1 represents player 2 etc.
        currPlayer = playerName[playerTurn] #the current player is set using playerturn as the key
        currentbank = players[currPlayer] #i also get the player's bank info from the key and set it
        guess = "" #initialized guess to get round some testing errors here, still trying to figure it out
        spin = 0 #also initized spin for the same reason, didn't find any testing errors, but still keeping it
        
        print('='*30)
        print('Category: ', category)
        print('Hint: ', hint)
        print('\nCurrent player: ',currPlayer)
        print('Player bank: [$',currentbank ,']')
        print('='*30)

        showBoard(puzzle,guesses)
        
        #after the user interface is setup, the player is given an option to spin,buy vowel or guess
        userchoice = miniMenu()
        #they chose to spin
        if userchoice == 1:
            spin = spinWheel(theWheel)
            # i define bankrupt and lose a turn as -10 and -1 respectively, to make my logic checks easier
            if spin < 0: 
                if spin == -1:
                    print('You lose a turn!')
                    #possible players are 0,1,2 for this setup, so if it increments from player 3, it loops
                    #back to player 1; switches to next player
                    print('------Switching Player--------')
                    playerTurn = playerTurn + 1 
                    if playerTurn > 2:
                        playerTurn = 0
                else:
                    print('You go BANKRUPT!...and lose a turn! :(')
                    print('----------Switching Player----------')
                    players[currPlayer] = 0
                    playerTurn = playerTurn + 1
                    if playerTurn > 2:
                        playerTurn = 0
            # they get an option to win some money from the wheel
            else: 
                print('You get a chance to win: $', spin)
                consonant = (str(input('Enter a consonant you would like to guess: '))).lower()
                while consonant not in consonants: #checking to make sure they enter a consonant, loops until they do
                    consonant = (str(input('Enter something that is not a vowel!: '))).lower()
                guess = consonant

        #they chose to buy a vowel
        elif userchoice == 2:
            if currentbank < 250: #checking to see if they can afford it first
                print("You can't afford it! Vowels cost $250, and your current balance is: $",currentbank)
                userchoice = miniMenu() #if they can't afford it, takes them back to the menu
            else:
                #vowels cost 250, gets subtracted from their bank
                vowel = buyVowel(vowels)
                guess = vowel
                players[currPlayer] = players[currPlayer] - 250
        else:
        # they chose to guess the puzzle
            guess = (str(input("Alright, have a go and guess the whole puzzle: "))).lower()

        #if they guess right either the whole puzzle or a correct letter, this bit gets executed
        if guess == puzzle:
            players[currPlayer] = players[currPlayer] + spin
            wordGuessed = True
            print('\nNice! You guessed the entire puzzle!')
            print('\n-----', currPlayer, ' wins this round!-----')
            print('\nIt was indeed: ', puzzle.upper())
            guesses.clear() #clears list for next round
            return playerTurn #returns the winner for display

        elif guess in puzzle and len(guess) == 1:
            if guess in guesses:
                print('You guessed ', guess, ' already!, letters and words guesssed: ', *guesses, sep=" ")
            else:
                players[currPlayer] = players[currPlayer] + spin
                guesses.append(guess)
                puzzleLetters.remove(guess)
                if len(puzzleLetters) == 0:
                    wordGuessed = True
                    print("\nNice! You guessed the puzzle!")
                    print("\n-----", currPlayer, " wins this round!-----")
                    showBoard(puzzle,guesses)
                    guesses.clear() #clears list for next round
                    return playerTurn
                else:
                    print("\n", guess, " is in there! Letters used so far: ", *guesses, sep=" ")
        else:
            #they guessed wrong, switiching player
            guesses.append(guess)
            print("\nNope ", guess, " is not in it!, letters guesssed: ", *guesses, sep=" ")
            print("-----SWITCHING TO NEXT PLAYER-----")
            playerTurn = playerTurn + 1
            if playerTurn > 2:
                playerTurn = 0

#-------------------------------------------------------------------------------
# round 3 game
def playFinalRnd(puzzle, wordGuessed, r3player):
    while wordGuessed == False:
        currPlayer = r3player 
        currentbank = players[currPlayer] 
        guesses = ['r','s','t','l','n','e']
        
        print('='*30)
        print('Category: ', category)
        print('Hint: ', hint)
        print('\nCurrent player: ',currPlayer)
        print('Player bank: [$',currentbank ,']')
        print('='*30)

        showBoard(puzzle,guesses)
        consonantGuesses = 3
        while consonantGuesses > 0:
            guess = (str(input('Guess three consonants, one at a time: '))).lower()
            if guess in consonants:
                guesses.append(guess)
                consonantGuesses = consonantGuesses - 1
            else:
                print("You didn't guess a consonant!")

        print("Let's have another look at the board\n")   
        showBoard(puzzle,guesses)
        vowelGuess = 1
        while vowelGuess > 0:
            guess = (str(input('Guess a vowel: '))).lower()
            if guess in vowels:
                guesses.append(guess)
                vowelGuess = vowelGuess - 1
            else:
                print("You didn't guess a vowel!")
        print("Let's have another look at the board\n")
        showBoard(puzzle,guesses)

        print('Alright, now you have only one guess to figure out the word!')
        guess = (str(input("Good luck!, enter your guess: "))).lower()

        if guess == puzzle:
            wordGuessed = True
            print('\nWell done! You guessed it!')
            print('\nIt was indeed: ', puzzle.upper())
            print('\n----- ', currPlayer, ' wins the final round and is our champion! -----')
            print('\nYou get the grand prize of $100,000!')
            players[currPlayer] = players[currPlayer] + 100000
            print('======|Your Winnings: $', players[currPlayer], '|=======')
        else:
            print("Too bad, you didn't win :(")
            print('You go home with $', players[currPlayer], ' on the plus side, though!')
            break

playerTurn = 0 #starting off with player 1

puzzle = getPuzzle()
pzlett = puzzle.split() #intermediate step - I'm splitting the prhase to words if it's a prhase
pzlt = ''.join(pzlett)  #i'm joining them to a single string
#i saved the letters from the string to a set, i'll use the set to check whether the word has been 
#guessed by subtracting a guess from the set everytime the player guesses a correct letter
puzzleLetters = set(pzlt) 
hint = wofStuff[puzzle]['hint']
category = wofStuff[puzzle]['category']

wordGuessed = False
guesses = []
print("""
    =======================|| Wheel of Fortune, Ghetto Edition ||=======================
""")
print('vvvvvvvvvv| Round 1 |vvvvvvvvvvvvvv')
winner1 = playGame(puzzle,wordGuessed,playerTurn)
print('^^^^^| The First Round Goes To: ', playerName[winner1], ' |^^^^^')
print('vvvvvvvvvv| End of First Round |vvvvvvvvvvvv')
#setting up for second round, if this happened indefinitely, i'd put this in a function 

puzzle2 = getPuzzle()
pzlett = puzzle2.split() #intermediate step - I'm splitting the prhase to words if it's a prhase
pzlt = ''.join(pzlett)  #i'm joining them to a single string
#i saved the letters from the string to a set, i'll use the set to check whether the word has been 
#guessed by subtracting a guess from the set everytime the player guesses a correct letter
puzzleLetters = set(pzlt) 
hint = wofStuff[puzzle2]['hint']
category = wofStuff[puzzle2]['category']

print('vvvvvvvvvv| Round 2 |vvvvvvvvvvvvvv')
winner2 = playGame(puzzle2,wordGuessed,playerTurn)
print('^^^^^| The Second Round Goes To: ', playerName[winner2], ' |^^^^^')
print('vvvvvvvvvv| End of Round 2 |vvvvvvvvvvvv')

#find player with highest bank
r3player = max(players, key=players.get)
print("=========== FINAL ROUND ===========")
print('\n', r3player, 'will be the one doing the final round!')

#setting up for round 3
puzzle3 = getPuzzle()
pzlett = puzzle3.split() 
pzlt = ''.join(pzlett)
puzzleLetters = set(pzlt) 
hint = wofStuff[puzzle3]['hint']
category = wofStuff[puzzle3]['category']
playFinalRnd(puzzle3,wordGuessed,r3player)
print("==========================| Game Over |================================")