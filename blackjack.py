import random
import os, sys, subprocess
from os import system, name

#@leochao
def main():
    clear()
    users=[]
    
    #Checks if save.txt exists
    if os.path.isfile("save.txt"):
        with open("save.txt", "r") as f:
            temp = f.read()
            userList = temp.split(":")
            for u in userList:
                if u.strip():
                    userParts = u.split(",")
                    users.append([userParts[0],userParts[1],userParts[2]])
    loop = True
    card = 0
    account = 0
    while(loop):
        new = int(input("Welcome to Leo's Casino!\nAre you a returning user or a new user?\n 1 - Returning User\n 2 - New User\n"))
        if new == 1: #Returning user
            username = input("\nUsername: \n") #Enter username
            password = ""
            userExists=False
            index=0
            for i in range(len(users)): #Tests if username is in users directory
                if users[i][0]==username: #If user is in directory, userExists is True, index = i
                    userExists=True
                    index=i
                    break
            if userExists: #If userExists, prompt password entry
                password = input("\nPassword: \n")
                if password == users[index][1]: #If password is correct, make account = index
                    #Asks user if they want to add more money to their card
                    wantsToAdd = input("\nYour current balance is ${}. Would you like to add money to your account?\n 1 - Yes\n 2- No\n".format(users[index][2]))
                    if int(wantsToAdd) == 1:
                        amount = input("\nEnter an amount to add:\n")
                        users[index][2] = str(int(users[index][2])+int(amount))
                    account = index
                    loop = False
                else: #If incorrect password, loop back again
                    print("\nIncorrect password\n")
            else: #If user does not exist, loop back again
                print("\nUser does not exist\n")
        elif new ==2: #New User
            username = input("\nUsername: \n")
            password = input("\nPassword: \n")
            deposit = input("\nHow much money would you like to deposit in your card?\n")
            users.append([username, password, deposit])
            account = len(users)-1
            loop = False
    card = int(users[account][2])
    users[account][2]=str(casino(card))
    print("\nThis is your current card: {}".format(users[account][2]))
    
    #Tracks users
    with open('save.txt','w') as f:
        for user in users:
            f.write(user[0]+","+user[1]+","+user[2]+":")

#@param: a card (int)
#Allows user to select game, runs game program
#return: the card (int)
def casino(card):
    while card > 0:
        game= int(input("\nWhat would you like to  play? \n 1 - Blackjack\n 0 - Return to main page\n"))
        if game==1: #blackjack
            while True:
                wager=int(input("\nHow much are you going to wager?\n"))
                if wager>card:
                    print("\nNot enough money")
                else:
                    card-=wager
                    win=blackjack()
                    if win>0:
                        card += wager*2
                    elif win == 0:
                        card += wager
                
                if int(input("\nCard: ${}\nDo you want to keep playing?\n 1 - Yes\n 0 - No\n".format(card)))==0: 
                    return card
        if game==0: #return to main page
            break
        else:
            print("\nGame does not exist")
    return card

#@param void
#Runs blackjack program, creates deck, deals cards, etc.
#@return 1 if player wins, 0 if draw, -1 if computer wins    
def blackjack():
    deck=createDeck()
    hand=[]
    deal(deck,hand)
    deal(deck,hand)
    cpuHand=[]
    deal(deck,cpuHand)
    deal(deck,cpuHand)
    # print("\nComputer cards: {}".format(display(cpuHand,True)))
    playerScore=play(deck,hand,cpuHand)
    if(playerScore==0):
        print("\nYou lose!")
        return -1
    cpuScore=cpu(deck,cpuHand)
    if playerScore > cpuScore:
        print("\nYou  win!")
        return 1
    elif playerScore==cpuScore:
        print("\nDraw")
        return 0
    else:
        print("\nYou lose!")
        return -1

#@param void
#@return random dictionary of 52 elements, of four suits, and 13 numbers each
def createDeck():
    deck=[]
    for num in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
        for suit in ['♠', '♦', '♥', '♣']:
            deck.append([num,suit])
    return deck

#@param void
#return a random card within a given deck, removes card from that deck
def deal(deck,hand):
    randNum=random.randint(0,len(deck)-1)
    hand += [deck[randNum]]
    del deck[randNum]

#@param an array of cards
#returns sum of cards
def checkScore(hand):
    total=0
    exception=0
    if hand==[["Busted"]]:
        return 0
    for i in hand:
        if i[0]=='A':
            total += 11
            exception+=1
        elif i[0] =='J' or i[0]=='Q' or i[0]=='K':
            total += 10
        else:
            total += int(i[0])
    while(total > 21 and exception>0):
        total-=10
        exception -=1
    return total

#@param a dictionary of cards, an array of two cards
#returns a score
def play(deck,hand, cpuHand):
    while True:
        if checkScore(hand) > 21:
            print("\nYour cards: {}".format(display(hand)))
            print("Busted!")
            return 0
        print("\nComputer cards: {}".format(display(cpuHand,True)))
        print("\nYour cards: {}".format(display(hand)))
        print("Your total: {}".format(checkScore(hand)))
        if(hand[0][0]==hand[1][0]):
            move=int(input("\nWhat would you like to do?\n 1 - Hit\n 2 - Stand\n 3 - Split\n"))
        else:
            move=int(input("\nWhat would you like to do?\n 1 - Hit\n 2 - Stand\n"))
        if move==1:
            deal(deck,hand)
        elif move==2:
            return checkScore(hand)
        elif move==3 and hand[0][0]==hand[1][0]:
            hand1=[hand[0]]
            deal(deck,hand1)
            hand2=[hand[1]]
            deal(deck,hand2)
            return max(play(deck,hand1),play(deck,hand2))
        else:
            print("\nInvalid move")
        
#@param a dictionary of cards, an array of two cards
#computer will run blackjack, always hits before 17
#returns a score
def cpu(deck,hand):
    while True:
        print("\nComputer cards: {}".format(display(hand)))
        print("Computer total: {}".format(checkScore(hand)))
        if checkScore(hand) < 17:
            deal(deck,hand)
        elif checkScore(hand) >= 17:
            return checkScore(hand)
        if checkScore(hand) > 21:
            print("\nComputer cards: {}".format(display(hand)))
            print("Computer Busted!")
            return 0
    return checkScore(hand)

#@param a dictionary of cards, an array of two cards
#smarter computer algorithm, hits when less than playerHand
def smarterCPU(deck,hand,playerHand):
    while True:
        print("\nComputer cards: {}".format(display(hand)))
        print("Computer total: {}".format(checkScore(hand)))
        if checkScore(hand) < playerHand:
            deal(deck,hand)
        elif checkScore(hand) >= playerHand:
            return checkScore(hand)
        if checkScore(hand) > 21:
            print("\nComputer cards: {}".format(display(hand)))
            print("Computer Busted!")
            return 0
    return checkScore(hand)

#@param an array of two cards
#returns a string of the card dispalyed beautifully
def display(hand, hidden=False):
    
    cards = []

    for i in hand:
        
        if(hidden):
            lines = [""]*9
            lines[0]='┌─────────┐'
            lines[1]='│░░░░░░░░░│'
            lines[2]='│░░░░░░░░░│'
            lines[3]='│░░░░░░░░░│'
            lines[4]='│░░░░░░░░░│'
            lines[5]='│░░░░░░░░░│'
            lines[6]='│░░░░░░░░░│'
            lines[7]='│░░░░░░░░░│'
            lines[8]='└─────────┘'
            hidden=False
        else:
            if(i[0]=="10"):
                print("10")
                spaces=""
            else:
                spaces=" "
            lines = [""]*9
            lines[0]='┌─────────┐'
            lines[1]='│{}{}       │'.format(i[0], spaces)
            lines[2]='│         │'
            lines[3]='│         │'
            lines[4]='│    {}    │'.format(i[1])
            lines[5]='│         │'
            lines[6]='│         │'
            lines[7]='│       {}{}│'.format(spaces, i[0])
            lines[8]='└─────────┘'
        cards.append(lines)

    ret="\n"
    for i in range(9):
        for j in range(len(cards)):
            ret = ret + cards[j][i]
        ret = ret + "\n"
    return ret[:-1]


#clear function to clear terminal
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
if __name__=='__main__':
    main()
