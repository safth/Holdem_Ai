from collections import Counter
import numpy as np
import random

class Deck():
    def __init__(self):
        #self.cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4
        self.cards = []
        self.board = []
        for suit in ['Spade','Heart','Club','Diamond']:
            for rank in range(2,15):
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
    def __init__(self,money,cpu = False,name='jerry'):
        self.name = name
        self.hand = []
        self.money = money
        self.board = []
        self.Best_rank = 0
        self.doublet_rank = 0
        self.triplet_rank = 0
        self.quadruplet_rank = 0
        self.straight_rank = 0 # TODO
        self.flush_rank = 0
        self.doublet = 0
        self.triplet = 0
        self.quadruplet = 0
        self.straight = 0
        self.flush = 0
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
        print(self.name,'hands')
        print(rank_list)
        print(suit_list)

    def Get_action(self,bet,min_bet):
        if not self.cpu:
            while True:

                val = input('fold = f, call = c, bet = b ... , check = h...')
                if val not in ['f','b','c','h']: # TODO mettre le check.
                    print ("Invalid input")
                else:
                    break
        #if its a computer that play
        else:
            list = ['f','c','b','h']
            val = list[random.randint(1,1)]

        if val == 'f':
            self.done = True
            self.fold = True
        elif val == 'b':
            bet = bet+min_bet
        elif val == 'c':
            bet=bet
        self.money = self.money - (bet - self.bet)
        self.bet = bet
        return val, bet





    def check_score(self):
        card = self.hand + self.board
        rank_list = [ card['rank'] for card in card]
        suit_list = [ card['suit'] for card in card]
        #check for duplicated cards
        counter_rank = Counter(rank_list)
        for key in counter_rank:
            #TODO mettre le highest rank de la carte apres
            #la pair. (si j'ai une pair d'As, la highest c'Est pas un As)
            if counter_rank[key] == 2:
                self.doublet += 1
                if self.doublet_rank < key:
                    self.doublet_rank = key
                    new_list = rank_list
                    for i in range(2):rank_list.remove(key)
                    self.best_rank = max(new_list)
                    # TODO avoir la deuxime meilleurs pair en compte
            elif counter_rank[key] == 3:
                self.triplet += 1
                if self.triplet_rank < key:
                    self.triplet_rank = key
                    new_list = rank_list
                    for i in range(3):rank_list.remove(key)
                    self.best_rank = max(new_list)
            elif counter_rank[key] == 4:
                self.quadruplet += 1
                self.quadruplet_rank = key
                new_list = rank_list
                for i in range(4):rank_list.remove(key)
                self.best_rank = max(new_list)

        #check for flush (5 card of same suit)
        counter_suit = Counter(suit_list)
        for key in counter_suit:
            if counter_suit[key] == 5:
                self.flush = 1
                # TODO faire le flush_rank, si c'est égal.

        #check for higest cards
        self.best_rank = max(rank_list)
        #check for straight (5 card in order)
        for icard in card:
            if (icard['rank']+1 in rank_list and icard['rank']+2 in rank_list and icard['rank']+3 in rank_list and icard['rank']+4 in rank_list):
                val = icard['rank']
                self.straight = 1
                self.straight_rank = icard['rank']+4
                #check for straigth flush
                suit_in_straight = [suit_list[rank_list.index(val+i)] for i in range(5) ]
                if(len(set(suit_in_straight))==1):
                    self.straightflush = 1
                #TODO check la flush de As à 5
                #(14 in rank_list and 2 in rank_list and 3 in rank_list and 4 in rank_list and 5 in rank_list)
            # straigth royale
            if 10 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list and 14 in rank_list :
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

        score = [self.Rflush,
                self.straightflush,
                self.quadruplet,
                self.fullHouse,
                self.flush,
                self.straight,
                self.triplet,
                self.doublet,
                self.best_rank]
        rank =  [0,
                self.flush_rank,
                self.quadruplet_rank,
                0,
                self.flush_rank,
                self.straight_rank,
                self.triplet_rank,
                self.doublet_rank,
                self.best_rank]





        return score, rank

    def reset(self):
        self.hand = []
        self.board = []
        self.Best_rank = 0
        self.doublet_rank = 0
        self.triplet_rank = 0
        self.quadruplet_rank = 0
        self.straight_rank = 0 # TODO
        self.flush_rank = 0
        self.doublet = 0
        self.triplet = 0
        self.quadruplet = 0
        self.straight = 0
        self.flush = 0
        self.Rflush = 0
        self.straightflush = 0
        self.fullHouse = 0
        self.action = 'f'
        self.done = False
        self.fold = False
        self.bet = 0
