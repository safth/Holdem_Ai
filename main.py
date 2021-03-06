from classes import Deck, Player, Ai
import random
import numpy as np
import tensorflow as tf

def check_winner(pot):
    #player1.print_hand() # SHOW CARDS
    #cpu1.print_hand()
    #deck.print_board()
    score1, rank1 = player1.check_score()
    score2, rank2 = cpu1.check_score()
    score3, rank3 = cpu2.check_score()
    #print(score1)
    #print(score2)
    #print(score3)
    for i in range(len(score1)):

        if (score1[i] > score2[i]) and (score1[i] > score3[i]):
            #print('player1 win')
            player1.money = player1.money+pot
            break

        elif (score2[i] > score1[i]) and (score2[i] > score3[i]):
            #print('player2 win')
            cpu1.money = cpu1.money+pot
            break

        elif (score3[i] > score1[i]) and (score3[i] > score2[i]):
            #print('player3 win')
            cpu2.money = cpu2.money+pot
            break

            #si c'est égal entre 1 et 2
        if score1[i]==score2[i] and score1[i]>0 and score1[i] > score3[i]:
            if rank1[i] > rank2[i]:
                #print('player1 win')
                player1.money = player1.money+pot
                break
            elif rank1[i] < rank2[i]:
                #print('player2 win')
                cpu1.money = cpu1.money+pot
                break
            elif rank1[i] == rank2[i]:
                if rank1[8] > rank2[8]:
                    #print('player1 win')
                    player1.money = player1.money+pot
                    break
                elif rank1[8] < rank2[8]:
                    #print('player2 win')
                    cpu1.money = cpu1.money+pot
                    break
                else:
                    #print('egal')
                    cpu1.money = cpu1.money+pot/2
                    player1.money = player1.money+pot/2
                    break
                    #si c'est égal entre 1 et 3
            if score1[i]==score3[i] and score1[i]>0 and score1[i] > score2[i]:
                if rank1[i] > rank3[i]:
                    #print('player1 win')
                    player1.money = player1.money+pot
                    break
                elif rank1[i] < rank3[i]:
                    #print('player3 win')
                    cpu2.money = cpu2.money+pot
                    break
                elif rank1[i] == rank3[i]:
                    if rank1[8] > rank3[8]:
                        #print('player1 win')
                        player1.money = player1.money+pot
                        break
                    elif rank1[8] < rank3[8]:
                        #print('player3 win')
                        cpu2.money = cpu2.money+pot
                        break
                    else:
                        #print('egal')
                        cpu2.money = cpu2.money+pot/2
                        player1.money = player1.money+pot/2
                        break

                #si c'est égal entre 2 et 3
        if score2[i]==score3[i] and score2[i]>0 and score2[i] > score1[i]:
            if rank2[i] > rank3[i]:
                #print('player2 win')
                cpu1.money = cpu1.money+pot
                break
            elif rank2[i] < rank3[i]:
                #print('player3 win')
                cpu2.money = cpu2.money+pot
                break
            elif rank2[i] == rank3[i]:
                if rank2[8] > rank3[8]:
                    #print('player2 win')
                    cpu1.money = cpu1.money+pot
                    break
                elif rank2[8] < rank3[8]:
                    #print('player3 win')
                    cpu2.money = cpu2.money+pot
                    break
                else:
                    #print('egal')
                    cpu2.money = cpu2.money+pot/2
                    cpu1.money = cpu1.money+pot/2
                    break
                #TODO faire une triple égalité
    #print(pot,'$')

def fold_winner(pot):
    if cpu1.fold and cpu2.fold and player1.fold:
        if cpu1.bigblind:
            cpu1.money = cpu1.money+pot
        elif cpu2.bigblind:
            cpu2.money = cpu2.money+pot
        elif player1.bigblind:
            player1.money = player1.money+pot

    elif cpu1.fold == True and cpu2.fold == True:
        #print('player1 win')
        player1.money = player1.money+pot
    elif cpu2.fold == True and player1.fold == True:
        #print('player2 win')
        cpu1.money = cpu1.money+pot
    elif cpu1.fold == True and player1.fold == True:
        #print('player3 win')
        cpu2.money = cpu2.money+pot


def round_finish():
    if (player1.done == True) and ( cpu1.done == True) and ( cpu2.done == True):
        return True
    else:
        return False

def isFinish():
    num_player = [player1, cpu1, cpu2]
    count = len(num_player)
    for player in num_player:
        if player.fold == True:
            count -= 1
    if count == 0 or count ==1:
        return True
    else:
        return False


def player_turn(player,action_val):
    #If player have fold, no more play
    if player.fold  :
        player.done = True
        return
        # if the bet on the table is 0, you can check.
    elif deck.bet_to_play == 0:
        deck.bet_to_play, money = player.Get_action(deck.bet_to_play,deck.min_bet,check=True,action_val=action_val)
        deck.pot += money

    elif player.bigblind == True and deck.bet_to_play == player.bet and player.done == False:
        #if you're the bigblind, you can check before the flop if nobody have bet
        deck.bet_to_play, money = player.Get_action(deck.bet_to_play,deck.min_bet,check=True,action_val=action_val)
        deck.pot += money
        #he is the last to play, he is done automaticly
        player.done = True

        #if there is a bet and you have not bet as much, you can call, fold or bet
    elif (player.bet < deck.bet_to_play):
        deck.bet_to_play, money = player.Get_action(deck.bet_to_play,deck.min_bet,check=False,action_val=action_val)
        deck.pot += money
    else:
        #player dont play
        player.done = True


def print_bet_pot():
    deck.bet_to_play
    deck.min_bet
    if deck.bet_to_play == 0 : print("Bet %0.2f: " % deck.min_bet)
    else : print("Bet %0.2f: " % deck.bet_to_play)
    print('pot :',deck.pot,'$')

def round_turn(iturn):
    #player1.print_hand() # SHOW CARDS
    #deck.print_board()
    global action
    global gradients
    if iturn == 1:
        #print_bet_pot()

        player1.Get_observation(deck.bet_to_play,deck.pot)

        action_val, gradient_val = sess.run([Taction,Tgradients],feed_dict={X:player1.observations})
        action_val = action_val[0]
        player1.current_rewards.append(1.)
        player1.current_gradients.append(gradient_val)
        player_turn(player1, action_val)

        player_turn(cpu1, action_val=0)
        player_turn(cpu2, action_val=0)
    elif iturn == 2:
        player_turn(cpu2, action_val=0)
        #print_bet_pot()

        player1.Get_observation(deck.bet_to_play,deck.pot)
        action_val, gradient_val = sess.run([Taction,Tgradients],feed_dict={X:player1.observations})
        action = action_val[0]
        player1.current_rewards.append(1.)
        player1.current_gradients.append(gradient_val)
        player_turn(player1, action_val)
        player_turn(cpu1, action_val=0)

    elif iturn == 3:
        player_turn(cpu1, action_val=0)
        player_turn(cpu2, action_val=0)
        #print_bet_pot()

        player1.Get_observation(deck.bet_to_play,deck.pot)
        action_val, gradient_val = sess.run([Taction,Tgradients],feed_dict={X:player1.observations})
        action_val = action_val[0]
        player1.current_rewards.append(1.)
        player1.current_gradients.append(gradient_val)
        player_turn(player1, action_val)



def initialize_round(num_hit):
    deck.bet_to_play = 0
    deck.board.extend(deck.hit(num_hit))
    player1.bet = 0
    player1.done = False
    cpu1.bet = 0
    cpu1.done = False
    cpu2.bet = 0
    cpu2.done = False
    player1.board = deck.board
    cpu1.board = deck.board
    cpu2.board = deck.board

def big_blind_bet(player,yes):
        if yes:
            player.bigblind = True
            deck.bet_to_play = deck.min_bet
            player.bet = deck.bet_to_play
            player.money = player.money-player.bet
            deck.pot = deck.bet_to_play
        else:
            player.bigblind = False



def game(iturn):
    player_list = [cpu2,cpu1,player1]
    while not isFinish():
        #hit card to each player.
        player1.hand = deck.hit(2)
        cpu1.hand = deck.hit(2)
        cpu2.hand = deck.hit(2)
        #cpu3.hand = deck.hit(2)
        #cpu4.hand = deck.hit(2)
        big_blind_bet(player_list[iturn-1],True)
        #print("your money : %0.1f " %player1.money)
        #Bet on their hands, prior to
        while not isFinish():
            round_turn(iturn)
            #flop
            if round_finish() :
                big_blind_bet(player_list[iturn-1],False)
                initialize_round(num_hit=3)
                while not isFinish():
                    round_turn(iturn)
                    #the turn
                    if round_finish() :
                        initialize_round(num_hit=1)
                        deck.min_bet = 2*deck.min_bet
                        while not isFinish():
                            round_turn(iturn)
                            #the River
                            if round_finish() :
                                initialize_round(num_hit=1)
                                #min_bet=2*min_bet
                                while not isFinish():
                                    round_turn(iturn)
                                    if round_finish() :
                                        check_winner(deck.pot)
                                        return
    fold_winner(deck.pot) # celui qui a pas fold







deck = Deck()
player1 = Ai(money=100,name='AI')
cpu1 = Player(money = 100, cpu = True, name='cpu')
cpu2 = Player(money = 100, cpu = True, name='cpu')
#cpu3 = Player(money = 10, cpu = True, name='cpu')
#cpu4 = Player(money = 10, cpu = True, name='cpu')
def jeux(num_game_rounds):

    i=1 #order of play
    for i_round in range(num_game_rounds):
        # AI stuffs
        player1.current_rewards = []
        player1.current_gradients = []

        # Game
        pre_money  = player1.money
        game(i)


        gain = player1.money-pre_money # this is the reward
        #we put the reward (money) on each step in the game (=1)
        for index in range(len(player1.current_rewards)):
            player1.current_rewards[index] = gain

        player1.all_rewards.append(player1.current_rewards)
        player1.all_gradients.append(player1.current_gradients)
        player1.current_score.append(gain)



        #print('GAINS: ',player1.gain,'$')
        player1.reset()
        cpu1.reset()
        cpu2.reset()
        deck.reset()
        i += 1
        if i==4 : i=1




num_input = 15 # there are 4 observation (like speed, angles, etc)
num_hidden = 20 #dimension of the hidden_layer
num_outputs = 4 # prob to go left
learning_rate = 0.01
initializer = tf.contrib.layers.variance_scaling_initializer()

X = tf.placeholder(tf.float32, shape=[None,num_input])

hidden_layer  = tf.layers.dense(X,num_hidden,activation = tf.nn.elu,kernel_initializer=initializer)
#tf.layers.dropout(inputs=hidden_layer,rate=0.8)

#hidden_layer  = tf.layers.dense(hidden_layer,num_hidden*2,activation = tf.nn.elu,kernel_initializer=initializer)
#tf.layers.dropout(inputs=hidden_layer,rate=0.8)

hidden_layer  = tf.layers.dense(hidden_layer,num_hidden,activation = tf.nn.elu,kernel_initializer=initializer)
#tf.layers.dropout(inputs=hidden_layer,rate=0.8)
logits = tf.layers.dense(hidden_layer,num_outputs)
output = tf.sigmoid(logits)

#prob = tf.concat(axis=1,values=[output[],output])

Taction = output
prob= tf.multinomial(output,num_samples=1) # this is the action done, left or right [L,R]

y = 1.0 - tf.to_float(prob)

#optimizer
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=output,logits=logits)
optimizer = tf.train.AdamOptimizer(learning_rate)

gradients_and_variables = optimizer.compute_gradients(cross_entropy)


Tgradients = []
gradient_placeholders = []
grads_and_vars_feed = []

for gradient, variable in gradients_and_variables:
    Tgradients.append(gradient)
    gradient_placeholder = tf.placeholder(tf.float32, shape=gradient.get_shape())
    gradient_placeholders.append(gradient_placeholder)
    grads_and_vars_feed.append((gradient_placeholder, variable))

#apply the calculated gradient with the discount
training_op = optimizer.apply_gradients(grads_and_vars_feed)

init = tf.global_variables_initializer()
saver =tf.train.Saver()

def helper_discount_rewards(rewards, discount_rate):
    '''
    Takes in rewards and applies discount rate
    '''
    discounted_rewards = np.zeros(len(rewards))
    cumulative_rewards = 0
    for step in reversed(range(len(rewards))):
        cumulative_rewards = rewards[step] + cumulative_rewards * discount_rate
        discounted_rewards[step] = cumulative_rewards
    return discounted_rewards

def discount_and_normalize_rewards(all_rewards, discount_rate):
    '''
    Takes in all rewards, applies helper_discount function and then normalizes
    using mean and std.
    '''
    all_discounted_rewards = []

    for rewards in all_rewards:
        all_discounted_rewards.append(helper_discount_rewards(rewards,discount_rate))

    flat_rewards = np.concatenate(all_discounted_rewards)
    reward_mean = flat_rewards.mean()
    reward_std = flat_rewards.std()
    if reward_std == 0:
        reward_std=1
    return [(discounted_rewards - reward_mean)/reward_std for discounted_rewards in all_discounted_rewards]




num_episodes = 1
num_game_rounds = 4 #number of complete round per episodes
discount_rate = 0.95

with tf.Session() as sess:
    sess.run(init)

    mean_score = []
    max_score = []
    for episode in range(num_episodes):
        player1.all_rewards = []
        player1.all_gradients = []
        player1.current_score = []

        jeux(num_game_rounds)

        mean_score.append(np.mean(player1.current_score))
        max_score.append(np.max(player1.current_score))

        print("on episode: {}, max score = {} mean_score = {} ".format(episode, max_score[episode],mean_score[episode] ))


        all_rewards = discount_and_normalize_rewards(player1.all_rewards,discount_rate)
        feed_dict = {}

        for var_index, gradient_placeholder in enumerate(gradient_placeholders):
            mean_gradients = np.mean([reward * player1.all_gradients[game_index][step][var_index]
                                      for game_index, rewards in enumerate(player1.all_rewards)
                                          for step, reward in enumerate(rewards)], axis=0)
            feed_dict[gradient_placeholder] = mean_gradients


        sess.run(training_op,feed_dict=feed_dict)


#print(player.doublet)
