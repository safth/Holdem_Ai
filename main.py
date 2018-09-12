from classes import Deck, Player
import random

def check_winner(pot):
    player1.print_hand() # SHOW CARDS
    cpu1.print_hand()
    deck.print_board()
    score1, rank1 = player1.check_score()
    score2, rank2 = cpu1.check_score()
    score3, rank3 = cpu2.check_score()
    print(score1)
    print(score2)
    print(score3)
    for i in range(len(score1)):

        if (score1[i] > score2[i]) and (score1[i] > score3[i]):
            print('player1 win')
            player1.money = player1.money+pot
            break

        elif (score2[i] > score1[i]) and (score2[i] > score3[i]):
            print('player2 win')
            cpu1.money = cpu1.money+pot
            break

        elif (score3[i] > score1[i]) and (score3[i] > score2[i]):
            print('player3 win')
            cpu2.money = cpu2.money+pot
            break

            #si c'est égal entre 1 et 2
        if score1[i]==score2[i] and score1[i]>0 and score1[i] > score3[i]:
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
                    #si c'est égal entre 1 et 3
            if score1[i]==score3[i] and score1[i]>0 and score1[i] > score2[i]:
                if rank1[i] > rank3[i]:
                    print('player1 win')
                    player1.money = player1.money+pot
                    break
                elif rank1[i] < rank3[i]:
                    print('player3 win')
                    cpu2.money = cpu2.money+pot
                    break
                elif rank1[i] == rank3[i]:
                    if rank1[8] > rank3[8]:
                        print('player1 win')
                        player1.money = player1.money+pot
                        break
                    elif rank1[8] < rank3[8]:
                        print('player3 win')
                        cpu2.money = cpu2.money+pot
                        break
                    else:
                        print('egal')
                        cpu2.money = cpu2.money+pot/2
                        player1.money = player1.money+pot/2
                        break

                #si c'est égal entre 2 et 3
        if score2[i]==score3[i] and score2[i]>0 and score2[i] > score1[i]:
            if rank2[i] > rank3[i]:
                print('player2 win')
                cpu1.money = cpu1.money+pot
                break
            elif rank2[i] < rank3[i]:
                print('player3 win')
                cpu2.money = cpu2.money+pot
                break
            elif rank2[i] == rank3[i]:
                if rank2[8] > rank3[8]:
                    print('player2 win')
                    cpu1.money = cpu1.money+pot
                    break
                elif rank2[8] < rank3[8]:
                    print('player3 win')
                    cpu2.money = cpu2.money+pot
                    break
                else:
                    print('egal')
                    cpu2.money = cpu2.money+pot/2
                    cpu1.money = cpu1.money+pot/2
                    break
                #TODO faire une triple égalité
    print(pot,'$')




def player_turn(player,bet,min_bet,flop=False):
    #player play only if they have not fold.
    if bet == 0:
        player.check = True
    else:
        player.check = False

    if (not player.fold)  and ((player.bet < bet) or (player.check==True)):
        player.board = deck.board
        bet, actual_bet = player.Get_action(bet,min_bet)
        player.done = False
    else:
        #player dont play
        player.done = True
        actual_bet = 0
    return bet, actual_bet


def initialize_round(num_hit):
    player1.bet=0
    player1.done=False
    cpu1.bet=0
    cpu1.done=False
    cpu2.bet=0
    cpu2.done=False
    deck.board.extend(deck.hit(num_hit))

def round_turn(bet,min_bet,iturn,pot):
    player1.print_hand() # SHOW CARDS
    deck.print_board()
    if iturn == 1:
        print("Bet %0.2f: " % bet)
        print('pot :',pot,'$')
        bet, actual_bet = player_turn(player1,bet,min_bet)
        pot += actual_bet
        bet, actual_bet = player_turn(cpu1,bet,min_bet)
        pot += actual_bet
        bet, actual_bet = player_turn(cpu2,bet,min_bet)
        pot += actual_bet
    if iturn == 2:
        bet, actual_bet = player_turn(cpu2,bet,min_bet)
        pot += actual_bet
        print("Bet %0.2f: " % bet)
        print('pot :',pot,'$')
        bet, actual_bet = player_turn(player1,bet,min_bet)
        pot += actual_bet
        bet, actual_bet = player_turn(cpu1,bet,min_bet)
        pot += actual_bet
    if iturn == 3:
        bet, actual_bet = player_turn(cpu1,bet,min_bet)
        pot += actual_bet
        bet, actual_bet = player_turn(cpu2,bet,min_bet)
        pot += actual_bet
        print("Bet %0.2f: " % bet)
        print('pot :',pot,'$')
        bet, actual_bet =  player_turn(player1,bet,min_bet)
        pot += actual_bet

    return bet, pot

def isFinish():
    num_player = [player1,cpu1,cpu2]
    count = len(num_player)
    for player in num_player:
        if player.fold == True:
            count -= 1
    if count == 0 or count ==1:
        return True
    else:
        return False

def game(iturn):
    while not isFinish():
        #hit card to each player.
        player1.hand = deck.hit(2)
        cpu1.hand = deck.hit(2)
        #cpu2.hand = deck.hit(2)
        #cpu3.hand = deck.hit(2)
        #cpu4.hand = deck.hit(2)
        min_bet = 0.25 # 1$ min de bet
        pot = 0
        bet = 0
        print("your money : %0.1f " %player1.money)
        print(pot,'$')
        #Bet on their hands, prior to
        while not isFinish():
            bet, pot = round_turn(bet,min_bet,iturn,pot)
            #flop
            if (player1.done == True) and ( cpu1.done == True) and ( cpu2.done == True) :
                initialize_round(num_hit=3)
                while not isFinish():
                    bet = 0
                    bet, pot = round_turn(bet,min_bet,iturn,pot)
                    #the turn
                    if (player1.done == True) and ( cpu1.done == True) and ( cpu2.done == True):
                        initialize_round(num_hit=1)
                        min_bet=2*min_bet
                        bet = min_bet
                        while not isFinish():
                            bet, pot = round_turn(bet,min_bet,iturn,pot)
                            #the River
                            if (player1.done == True) and ( cpu1.done == True) and ( cpu2.done == True):
                                initialize_round(num_hit=1)
                                #min_bet=2*min_bet
                                while not isFinish():
                                    bet, pot = round_turn(bet,min_bet,iturn,pot)
                                    if (player1.done == True) and ( cpu1.done == True) and ( cpu2.done == True):
                                        check_winner(pot)
                                        return
    print("lui qui a pas fold gagne") # celui qui a pas fold
    # TODO faire que tu perd quanfd tu fold.




deck = Deck()
player1 = Player(money=10,name='simon')
cpu1 = Player(money = 10, cpu = True, name='cpu')
cpu2 = Player(money = 10, cpu = True, name='cpu')
#cpu3 = Player(money = 10, cpu = True, name='cpu')
#cpu4 = Player(money = 10, cpu = True, name='cpu')

i=1 #order of play
while player1.money > 0 and cpu1.money > 0:
    game(i)
    player1.reset()
    cpu1.reset()
    cpu2.reset()
    deck.reset()
    #TODO put it back
    #i += 1
    #if i==4 : i=1





#print(player.doublet)
