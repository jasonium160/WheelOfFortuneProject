import random

theWheel = [100,150,200,250,300,350,350,400,450,450,500,500,550,600,650,700,750,800,850,900,
            -10,-1,-1,-10]
aSpin = random.choice(theWheel)

print(len(theWheel))
if aSpin < 0:
    if aSpin == -1:
        print('you lose a turn')
        print(aSpin)
    else:
        print('you go bankrupt')
        print(aSpin)
else:
    print('you get a chance to win $', aSpin)

players = {'Player1': 0, 'Player2': 0, 'Player3': 10}
playerName = list(players.keys()) #since i'm storing the keys as a list, player 1 will be indexed at 0

r3player = max(players, key=players.get)
print(r3player)
print(players[r3player])