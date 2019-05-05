import numpy as np
import collections
import sys
import random
import copy

def announcement():
    '''Deals with the announcements which happen at the beginning and end of the journey. Also picks the stations that the journey will be between, and returns the destination station. Requires file Stations.txt, a list of stations.'''
    Stations = []
    f = open('Stations.txt', 'r')
    stations = f.readlines()
    numbs = random.sample(range(1,len(stations)),3)  # Origin, terminus and 'via' stations selected at random
    rand1 = np.random.randint(0,24)                  # Random hour
    rand2 = np.random.randint(0,59)                  # Random minute                        
    if np.random.randint(0,4) == 0:                  # Controls probability of going via another station
        print('Whooo! Whooo! All aboard the {0}:{1} from {2} to {3}, via {4}.'.format(str(rand1).zfill(2), str(rand2).zfill(2), stations[numbs[0]].split('  ')[0], stations[numbs[1]].split('  ')[0],stations[numbs[2]].split('  ')[0]))
    else:
        print('Whooo! Whooo! All aboard the {0}:{1} from {2} to {3}.'.format(str(rand1).zfill(2), str(rand2).zfill(2), stations[numbs[0]].split('  ')[0], stations[numbs[1]].split('  ')[0]))
        
    return(stations[numbs[1]].split('  ')[0])

def make_deck():
    '''Makes a deck of 52 cards. Resturns the deck, unshuffled.'''
    deck = []
    suits = ['Spades','Hearts','Clubs', 'Diamonds']
    numbers = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
    deck = []
    for i in range(4):
        for j in range(13):
            deck.append('{1} of {0}'.format(suits[i],numbers[j]))
    return(deck)

def shuffle_deck(ShuffledDecks, **options):
    '''Shuffles a new deck and appends it to the end of the deck list, keeping track of the current, previous and next deck. If newplayer='yes', the shuffle generates both a current and next deck, in this case it is then called again immediately with newplayer='no', so it always holds 3 decks during play. This also means that when first called, current and next decks can be the same without consequence.'''
    deck = make_deck()
    new_deck1 = []
    new_deck2 = []
    order1 = random.sample(range(52),52)      
    order2 = random.sample(range(52),52)
    if options.get('newplayer') == 'yes':
        for i in range(52):
            new_deck1.append(copy.deepcopy(deck[order1[i]]))            
        ShuffledDecks['current'] = new_deck1
        ShuffledDecks['next'] = new_deck1
        
    for i in range(52):
        new_deck2.append(copy.deepcopy(deck[order2[i]]))
    ShuffledDecks['previous'] = copy.deepcopy(ShuffledDecks['current'])
    ShuffledDecks['current'] = copy.deepcopy(ShuffledDecks['next'])
    ShuffledDecks['next'] = new_deck2
    return(ShuffledDecks)

def speech():
    '''Returns random comments when called. Expressions are delivered after a card is drawn. Advice is before the next card, this makes no difference unless stats mode is on, in which case advice comes after stats. '''
    Expressions = ['Shocker!', 'Oh dear!',"Well that's not what you want!","You've had a bad time, pal!", "Ooh, it's not easy."]
    Advice = ["If you see something that doesn't look right, text British Transport Police on 61016. See it, say it, sorted.",'Remember, ace is high!', "It's always clubs!", 'Ace is high!', 'There are no brakes on the train!']
    expression = Expressions[random.randint(0,len(Expressions)-1)]
    advice = Advice[random.randint(0,len(Advice)-1)]
    return(expression,advice)

def stats(decks):
    '''Calculates probabilities of the next card being red, black, higher, lower, in, out, suit. Takes the three shuffled decks as an argument and calculates this for every card when called. Returns a dictionary of probabilities.'''
    P = collections.OrderedDict()
    P['Hearts'] = np.zeros((156))
    P['Clubs'] = np.zeros((156))
    P['Spades'] = np.zeros((156))
    P['Diamonds'] = np.zeros((156))
    P['Red'] = np.zeros((156))
    P['Same1'] = np.zeros((156))
    P['Same2'] = np.zeros((156))
    P['Higher1'] = np.zeros((156))
    P['Higher2'] = np.zeros((156))
    P['In'] =np.zeros((156))
    suit = []
    number = []
    numbers =  ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    for tag in ['previous','current','next']:
        for i in range(52):
            suit.append(decks[tag][i].split(' ')[2])
            number.append(numbers.index(decks[tag][i].split(' ')[0]))
    for i in range(52,103):                      #52 cards in the current deck        
        for j in range(1,104-i):       #j runs from card 1 to 51, 1 to 50 etc until j=1 for i=102, the penultimate card in the current deck
            if suit[i+j] == 'Hearts' or suit[i+j] == 'Diamonds':             
                P['Red'][i] += 1/(103-i)            #Prob of card i+1 being red so display after card i
            if suit[i+j] == 'Hearts':
                P['Hearts'][i] += 1/(103-i)
            if suit[i+j] == 'Clubs':
                P['Clubs'][i] += 1/(103-i)
            if suit[i+j] == 'Spades':
                P['Spades'][i] += 1/(103-i)
            if suit[i+j] == 'Diamonds':
                P['Diamonds'][i] += 1/(103-i)
            if number[i+j] == number[i]:
                P['Same1'][i] += 1/(103-i)
            if number[i+j] == number[i-1]:
                P['Same2'][i] += 1/(103-i)
            if number[i+j] > number[i]:
                P['Higher1'][i] += 1/(103-i)
            if number[i+j] > number[i-1]:
                P['Higher2'][i] += 1/(103-i)
        if number[i] > number[i-1]:
            P['In'][i] = P['Higher2'][i]-P['Higher1'][i] - P['Same1'][i]
        elif number[i] < number[i-1]:
            P['In'][i] = P['Higher1'][i]-P['Higher2'][i] - P['Same2'][i]
        else:
            P['In'][i] = 0
    i = 103
    for j in range(1,53):
        if suit[i+j] == 'Hearts' or suit[i+j] == 'Diamonds':             
            P['Red'][i] += 1/(52)            #Prob of card i+1 being red so display after card i
        if suit[i+j] == 'Hearts':
            P['Hearts'][i] += 1/(52)
        if suit[i+j] == 'Clubs':
            P['Clubs'][i] += 1/(52)
        if suit[i+j] == 'Spades':
            P['Spades'][i] += 1/(52)
        if suit[i+j] == 'Diamonds':
            P['Diamonds'][i] += 1/(52)
        if number[i+j] == number[i]:
            P['Same1'][i] += 1/(52)
        if number[i+j] == number[i-1]:
            P['Same2'][i] += 1/(52)
        if number[i+j] > number[i]:
            P['Higher1'][i] += 1/(52)
        if number[i+j] > number[i-1]:
            P['Higher2'][i] += 1/(52)
    if number[i] > number[i-1]:
        P['In'][i] = P['Higher2'][i]-P['Higher1'][i] - P['Same1'][i]
    elif number[i] < number[i-1]:
        P['In'][i] = P['Higher1'][i]-P['Higher2'][i] - P['Same2'][i]
    else:
        P['In'][i] = 0
    return(P)


def main():
    '''Runs the game. Once started, the game keeps going through multiple shuffles of the deck until 'Brake' is given as an input. Toggling stats mode returns the stats on the next card. '''
    ShuffledDecks = collections.OrderedDict()    
    decks = shuffle_deck(ShuffledDecks, newplayer='yes')
    destination = announcement()
    continuous = True
    deckno = 0
    toggle = 0
    while continuous == True:
        deckno += 1
        decks = shuffle_deck(decks, newplayer='no')
        P = stats(decks)
        deck = decks['current']
        i = 0
        while i <52:
            expression, advice = speech()
            var = input("Hit enter or type 'Toggle stats' or 'Brake':")        
            cardsLeft = 51-i
            if var == 'Toggle stats':
                toggle += 1
                
                if i==0:
                    if toggle%2 == 1:
                        print("You should be able to do those stats yourself! You'll get them next turn.")
                else:
                    if toggle%2 == 1:
                        print("Probability:")
                        print(80*'-')
                        print("Red:     {0:05.2f}%    Black:   {1:05.2f}%".format(100*P['Red'][i+51],100*abs(1-P['Red'][i+51])))
                        print("Higher:  {0:05.2f}%    Lower:   {1:05.2f}%".format(100*P['Higher1'][i+51],100*abs(1-P['Higher1'][i+51]-P['Same1'][i+52])))
                        if deckno != 1 or i > 0:
                            print("In:      {0:05.2f}%    Out:     {1:05.2f}%".format(100*abs(P['In'][i+51]),100*abs(1-P['In'][i+51]-P['Same1'][i+51]-P['Same2'][i+51])))
                        print("Clubs:   100%, it's always clubs!")
                        print("Clubs:   {0:05.2f}%    Spades:  {1:05.2f}%   Diamonds:    {2:05.2f}%   Hearts:    {3:05.2f}%".format(100*P['Clubs'][i+51],100*P['Spades'][i+51],100*P['Diamonds'][i+51],100*P['Hearts'][i+51]))
                        print(80*'-')
            if var == '':
                print('\n')
                print( 17*'=')
                print(deck[i])
                print(17*'=')
                rand = np.random.randint(0,10)
                if rand == 0:
                    print('\n',expression)
                print('\n')
                print( 'Cards left: ', cardsLeft)
                if toggle%2 == 1:
                    print("Probability:")
                    print(80*'-')
                    print("Red:     {0:05.2f}%    Black:   {1:05.2f}%".format(100*P['Red'][i+52],100*abs(1-P['Red'][i+52])))
                    print("Higher:  {0:05.2f}%    Lower:   {1:05.2f}%".format(100*P['Higher1'][i+52],100*abs(1-P['Higher1'][i+52]-P['Same1'][i+52])))
                    if deckno != 1 or i > 0:
                        print("In:      {0:05.2f}%    Out:     {1:05.2f}%".format(100*abs(P['In'][i+52]),100*abs(1-P['In'][i+52]-P['Same1'][i+52]-P['Same2'][i+52])))
                    print("Clubs:   100%, it's always clubs!")
                    print("Clubs:   {0:05.2f}%    Spades:  {1:05.2f}%   Diamonds:    {2:05.2f}%   Hearts:    {3:05.2f}%".format(100*P['Clubs'][i+52],100*P['Spades'][i+52],100*P['Diamonds'][i+52],100*P['Hearts'][i+52]))
                    print(80*'-')
                if rand == 1:
                    print('\n',advice)
                print('\n')
                if cardsLeft == 0:
                    print('End of deck')
                i +=1
            elif var == 'Brake':
                rand = np.random.randint(0,4)
                if rand == 0:
                    print('We apologise once again for the delay in this service, please have another drink on us.')
                    print('We are now approaching {0}, please mind the gap between the train and the platform when alighting from the train. Please ensure you have all luggage and personal belongings with you when you leave the train.'.format(destination))
                    return
                else:
                    print('We are now approaching {0}, please mind the gap between the train and the platform when alighting from the train. Please ensure you have all luggage and personal belongings with you when you leave the train.'.format(destination))
                    return
            else:
                i=i        
            
    return()
                           
        
main()           

