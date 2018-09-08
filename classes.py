from collections import Counter
import numpy as np
import random

class Deck():
    def __init__(self):
        #self.cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4
        self.cards = []
        self.board = []
        for suit in ['Spade','Heart','Club','Diamond']:
            for rank in range(1,14):
                self.cards.append({'rank':rank, 'suit':suit})
        random.shuffle(self.cards)

    #give x random cards
    def hit(self,num_card):
        card = []
        for i in range(num_card):
            card.append(self.cards.pop())
        return card


    def print_board(self):
        cards = self.board
        rank_list = [ card['rank'] for card in cards]
        suit_list = [ card['suit'] for card in cards]
        print('Board')
        print(rank_list)
        print(suit_list)

    #reset le deck
    def reset(self):

        self.cards = []
        for suit in ['Spade','Heart','Club','Diamond']:
            for rank in range(1,14):
                self.cards.append({'rank':rank, 'suit':suit})
        random.shuffle(self.cards)
        self.board = []



class Player():
    def __init__(self,money,cpu = False):
        self.hand = []
        self.money = money
        self.board = []
        self.Best_rank = 0
        self.doublet = 0
        self.doublet_rank = 0
        self.triplet = 0
        self.triplet_rank = 0
        self.quadruplet = 0
        self.straight = 0
        self.straight_rank = 0
        self.flush = 0
        self.flush_rank = 0
        self.Rflush = 0
        self.straightflush = 0
        self.fullHouse = 0
        self.action = 'f'
        self.done = False
        self.fold = False
        self.bet = 0
        self.cpu = cpu


    def print_hand(self):
        card = self.hand
        rank_list = [ card['rank'] for card in card]
        suit_list = [ card['suit'] for card in card]
        print('your hands')
        print(rank_list)
        print(suit_list)

    def Get_action(self,bet,min_bet):
        if not self.cpu:
            while True:
                val = input('fold = f, call = c, bet = b ... ')
                if val not in ['f','b','c']:
                    print ("Invalid input")
                else:
                    break
        #if its a computer that play
        else:
            list = ['f','c','b']
            val = list[random.randint(1,2)]

        if val == 'f':
            self.done = True
            self.fold = True
        elif val == 'b':
            bet = bet+min_bet
        elif val == 'c':
            bet=bet
        self.bet = bet
        self.money = self.money - bet
        return val, bet





    def check_score(self):
        card = self.hand + self.board
        rank_list = [ card['rank'] for card in card]
        suit_list = [ card['suit'] for card in card]
        #check for duplicated cards
        counter_rank = Counter(rank_list)
        for key in counter_rank:
            if counter_rank[key] == 2:
                self.doublet += 1
                if self.doublet_rank > key:
                    self.doublet_rank = key
            elif counter_rank[key] == 3:
                self.triplet += 1
                if self.triplet_rank > key:
                    self.triplet_rank = key
            elif counter_rank[key] == 4:
                self.quadruplet += 1

        #check for flush (5 card of same suit)
        counter_suit = Counter(suit_list)
        for key in counter_suit:
            if counter_suit[key] == 4:
                self.flush = 1
                # TODO faire le flush_rank, si c'est égal.

        #check for higest cards
        self.best_rank = max(rank_list)
        #check for straight (5 card in order)
        for icard in card:
            if icard['rank']+1 in rank_list and icard['rank']+2 in rank_list and icard['rank']+3 in rank_list and icard['rank']+4 in rank_list :
                val = icard['rank']
                self.straight = 1
                self.straight_rank = icard['rank']+4
                #check for straigth flush
                suit_in_straight = [suit_list[rank_list.index(val+i)] for i in range(5) ]
                if(len(set(suit_in_straight))==1):
                    self.straightflush = 1
            # straigth royale
            if 10 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list and 1 in rank_list :
                val = icard['rank']
                self.straight = 1
                #check for straigth flush
                suit_in_straight = [suit_list[rank_list.index(val+i)] for i in range(5) ]
                if(len(set(suit_in_straight))==1):
                    self.Rflush = 1
        #print(rank_list)
        #print(suit_list)
        if self.triplet != 0 and self.doublet !=0:
            self.fullHouse = 1

        score = [self.Rflush, self.straightflush, self.quadruplet, self.fullHouse, self.flush,
                    self.straight, self.triplet, self.doublet, self.best_rank]

        print(self.doublet)
        print(self.triplet)
        print(self.quadruplet)
        print(self.straight)
        print(self.flush)
        print(self.Rflush)
        print(self.straightflush)
        
        return score

        def reset(self):
            self.hand = []
            self.board = []
            self.Best_rank = 0
            self.doublet = 0
            self.doublet_rank = 0
            self.triplet = 0
            self.triplet_rank = 0
            self.quadruplet = 0
            self.straight = 0
            self.flush = 0
            self.Rflush = 0
            self.straightflush = 0








"""
class Deck():
    def __init__(self):
        self.deck = ['A','2','3','4','5','6',
        '7','8','9','10','J','Q','K']*4
        self.player_card = ['','']
        self.board = []
        self.deck_color =[0,1]*2*13
        self.symbol = ['square','diamond','heart','clove']*13
        self.play = []

        #initialisation of the plasyer 2 card
    def set_player_card(self,a,b):
        self.player_card = [a,b]
        self.deck.remove(a)
        self.deck.remove(b)
        # initialisation of the board
    def set_board(self,a,b,c):
        self.board = [a,b,c]
        self.deck.remove(a)
        self.deck.remove(b)
        self.deck.remove(c)

        #append a card to the board
    def append_board(self,a):
        self.board.append(a)
        self.deck.remove(a)

    def check_play(self):
        # check what is the statue of my hand and the game (doublet, flush, etc)

        play = self.player_card+self.deck
        #if self.player_card[0]==self.player_card[1]: #our card are the same
        #    print('oui')
        #else:
        #    print('non')


        # calcul prob qu'une carte pareille aux mienne sorte à la prochaine carte
        #for player_card in self.player_card:
        #    prob = 0
        #    for deck_card in self.deck:
        #        if player_card == deck_card:
        #            prob += 1
        #    print(100*(prob/(len(self.deck))))
"""
