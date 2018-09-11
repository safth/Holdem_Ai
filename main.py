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

def check_winner(pot):
    player1.print_hand() # SHOW CARDS
    cpu1.print_hand()
    deck.print_board()
    score1, rank1 = player1.check_score()
    score2, rank2 = cpu1.check_score()
    print(score1)
    print(score2)
    for i in range(len(score1)):
        if score1[i]>score2[i]:
            print('player1 win')
            player1.money = player1.money+pot
            break
        elif score2[i]>score1[i]:
            print('player2 win')
            cpu1.money = cpu1.money+pot
            break
        if score1[i]==score2[i] and score1[i]>0:
            if rank1[i] > rank2[i]:
                print('player1 win')
                player1.money = player1.money+pot
                break
            elif rank1[i] < rank2[i]:
                print('player2 win')
                cpu1.money = cpu1.money+pot
                break
            elif rank1[i] == rank2[i]:
                if rank1[8] > rank2[8]:
                    print('player1 win')
                    player1.money = player1.money+pot
                    break
                elif rank1[8] < rank2[8]:
                    print('player2 win')
                    cpu1.money = cpu1.money+pot
                    break
                else:
                    print('egal')
                    cpu1.money = cpu1.money+pot/2
                    player1.money = player1.money+pot/2
                    break
    print(pot,'$')

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
        pot=0
        print("your money : %0.1f " %player1.money)
        bet = min_bet
        print(pot,'$')
        #Bet on their hands, prior to
        while not isFinish():
            bet = round_turn(bet,min_bet)
            pot += bet
            print(pot,'$')
            #flop
            if (player1.done == True) and ( cpu1.done == True) :
                initialize_round(num_hit=3)
                while not isFinish():
                    bet=min_bet
                    bet = round_turn(bet,min_bet)
                    pot += bet
                    print(pot,'$')
                    #the turn
                    if (player1.done == True) and ( cpu1.done == True):
                        initialize_round(num_hit=1)
                        min_bet=2*min_bet
                        bet = min_bet
                        while not isFinish():
                            bet = round_turn(bet,min_bet)
                            pot += bet
                            print(pot,'$')
                            #the River
                            if (player1.done == True) and ( cpu1.done == True):
                                initialize_round(num_hit=1)
                                #min_bet=2*min_bet
                                while not isFinish():
                                    bet = round_turn(bet,min_bet)
                                    pot += bet
                                    print(pot,'$')
                                    if (player1.done == True) and ( cpu1.done == True):
                                        check_winner(pot)
                                        return
    print("lui qui a pas fold gagne") # celui qui a pas fold







deck = Deck()
player1 = Player(money=10,name='simon')
cpu1 = Player(money = 10, cpu = True, name='cpu')
#cpu2 = Player(money = 10, cpu = True, name='cpu')
#cpu3 = Player(money = 10, cpu = True, name='cpu')
#cpu4 = Player(money = 10, cpu = True, name='cpu')
while player1.money > 0 and cpu1.money > 0:
    game()
    player1.reset()
    cpu1.reset()
    deck.reset()




#print(player.doublet)
