from classes import Deck, Player
import random





def player_turn(player,bet,min_bet):
    #player play only if they have not fold.
    if (not player.fold)  and (player.bet < bet):
        player.board = deck.board
        action, bet = player.Get_action(bet,min_bet)
    else:
        #player dont play
        player.done = True
    return bet


def initialize_round(num_hit):
    player1.bet=0
    player1.done=False
    cpu1.bet=0
    cpu1.done=False
    deck.board.extend(deck.hit(num_hit))

def round_turn(bet,min_bet):
    player1.print_hand() # SHOW CARDS
    deck.print_board()
    print("Bet %0.2f: " % bet)
    bet = player_turn(player1,bet,min_bet)
    bet = player_turn(cpu1,bet,min_bet)
    return bet

def isFinish():
    num_player = [player1,cpu1]
    count = len(num_player)
    for player in num_player:
        if player.fold == True:
            count -= 1
    if count == 0 or count ==1:
        return True
    else:
        return False



def game():

    i=1
    num_player = 5
    while not isFinish():
        #hit card to each player.
        player1.hand = deck.hit(2)
        cpu1.hand = deck.hit(2)
        #cpu2.hand = deck.hit(2)
        #cpu3.hand = deck.hit(2)
        #cpu4.hand = deck.hit(2)
        min_bet = 0.25 # 1$ min de bet

        print("your money : %0.1f " %player1.money)
        bet = min_bet
        #Bet on their hands, prior to
        while not isFinish():
            bet = round_turn(bet,min_bet)
            #flop
            if (player1.done == True) and ( cpu1.done == True):
                initialize_round(num_hit=3)
                while not isFinish():
                    bet = round_turn(bet,min_bet)
                    #the turn
                    if (player1.done == True) and ( cpu1.done == True):
                        initialize_round(num_hit=1)
                        min_bet=2*min_bet
                        while not isFinish():
                            bet = round_turn(bet,min_bet)
                            #the River
                            if (player1.done == True) and ( cpu1.done == True):
                                initialize_round(num_hit=1)
                                #min_bet=2*min_bet
                                while not isFinish():
                                    bet = round_turn(bet,min_bet)
                                    if (player1.done == True) and ( cpu1.done == True):
                                        return

    check_winner()


def check_winner():
    score1 = player1.check_score()
    score2 = cpu1.check_score()
    for i in range(len(score1)):
        if score1[i]>score2[i]:
            print('player1 win')
        else: print('player 2 win')

deck = Deck()
player1 = Player(money=1000)
cpu1 = Player(money = 1000, cpu = True)
cpu2 = Player(money = 1000, cpu = True)
cpu3 = Player(money = 1000, cpu = True)
cpu4 = Player(money = 1000, cpu = True)

game()




#print(player.doublet)
