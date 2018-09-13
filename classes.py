from collections import Counter
import numpy as np
import random
import tensorflow as tf

class Deck():
    def __init__(self):
        #self.cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4
        self.cards = []
        self.board = []
        self.bet_to_play = 0
        self.min_bet = 0.25
        self.pot = 0
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
        self.bet_to_play = 0
        self.min_bet = 0.25
        self.pot = 0



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
        self.check = False
        self.bet = 0
        self.cpu = cpu
        self.bigblind = False
        self.gain = 0


    def print_hand(self):
        card = self.hand
        rank_list = [ card['rank'] for card in card]
        suit_list = [ card['suit'] for card in card]
        print(self.name,'hands')
        print(rank_list)
        print(suit_list)

    def Get_action(self,bet_to_play,min_bet,check):

        if bet_to_play < min_bet: # if there is no bet yet
            call_bet = min_bet
        else:
            call_bet = bet_to_play #else its the bet in the game (if someone have bet before)

        if not self.cpu:
            while True:

                if check == True:
                    val = input('fold = f, call = c, bet = b ... , check = h...')
                    if val not in ['f','b','c','h']: # TODO mettre le check.
                        print ("Invalid input")
                    else:
                        break
                else:
                    val = input('fold = f, call = c, bet = b ... ')
                    if val not in ['f','b','c']: # TODO mettre le check.
                        print ("Invalid input")
                    else:
                        break

        #if its a computer that play
        else:
            rank_list = [ card['rank'] for card in self.hand]
            if check == True:
                list = ['f','c','b','h']
                if rank_list[0]+rank_list[1] > 15:
                    num = random.randint(1,20)
                    if num < 4:
                        val='b'
                    elif num>=4 and num<=13:
                        val='c'
                    elif num>13:
                        val='h'

                else:
                    val = 'f'
            else:
                list = ['f','c','b']
                if rank_list[0]+rank_list[1]>15:
                    num = random.randint(1,20)
                    if num < 5:
                        val='b'
                    else:
                        val='c'
                else:
                    val = 'f'

            # action from the input::
        if val == 'f':
            self.done = True
            self.fold = True
            self.hand = []
            money = 0
        elif val == 'c':
            bet_to_play = call_bet
            money = bet_to_play-self.bet
            self.money = self.money - money
            self.bet = bet_to_play
        elif val == 'b':
            bet_to_play = call_bet + min_bet # we add the min_bet when we bet.
            money = bet_to_play-self.bet
            self.money = self.money - money
            self.bet = bet_to_play
        elif val == 'h':
            print("check")
            money=0

        return bet_to_play, money





    def check_score(self):
        # the score is 0 if you fold.
        if self.fold == False:
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
        else:
            score = np.zeros(9)
            rank = np.zeros(9)





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





class Ai(Player):
    def __init__(self,money,cpu = False,name='jerry'):
        Player.__init__(self,money,cpu,name)
        self.num_input = 7 # there are 4 observation (like speed, angles, etc)
        self.num_hidden = 20 #dimension of the hidden_layer
        self.num_outputs = 1 # prob to go left
        self.learning_rate = 0.01
        self.gradients = []
        self.gradient_placeholders = []
        self.grads_and_vars_feed = []
        self.num_game_rounds = 500
        self.num_episodes = 50
        self.discount_rate = 0.95
        self.mean_score = []
        self.max_score = []
        self.all_rewards = []
        self.all_gradients = []
        self.current_score = []
        self.current_rewards = []
        self.current_gradients = []
        self.observations=np.zeros(7)
        self.done = False
        self.steps=0


    def Get_action(self,bet_to_play,min_bet,check):

        if bet_to_play < min_bet: # if there is no bet yet
            call_bet = min_bet
        else:
            call_bet = bet_to_play #else its the bet in the game (if someone have bet before)



            ##===========================================================================
            ##==============================The neural network============================
            ##===========================================================================


        initializer = tf.contrib.layers.variance_scaling_initializer()

        X = tf.placeholder(tf.float32, shape=[None,self.num_input])

        hidden_layer  = tf.layers.dense(X,self.num_hidden,activation = tf.nn.elu,kernel_initializer=initializer)
        #tf.layers.dropout(inputs=hidden_layer,rate=0.8)

        #hidden_layer  = tf.layers.dense(hidden_layer,num_hidden*2,activation = tf.nn.elu,kernel_initializer=initializer)
        #tf.layers.dropout(inputs=hidden_layer,rate=0.8)

        #hidden_layer  = tf.layers.dense(hidden_layer,num_hidden*4,activation = tf.nn.elu,kernel_initializer=initializer)
        #tf.layers.dropout(inputs=hidden_layer,rate=0.8)

        #hidden_layer  = tf.layers.dense(hidden_layer,num_hidden*2,activation = tf.nn.elu,kernel_initializer=initializer)
        #tf.layers.dropout(inputs=hidden_layer,rate=0.8)

        hidden_layer  = tf.layers.dense(hidden_layer,self.num_hidden,activation = tf.nn.elu,kernel_initializer=initializer)
        #tf.layers.dropout(inputs=hidden_layer,rate=0.8)

        logits = tf.layers.dense(hidden_layer,self.num_outputs)
        output = tf.nn.sigmoid(logits)

        prob = tf.concat(axis=1,values=[output,1-output])
        action = tf.multinomial(prob,num_samples=1) # this is the action done, left or right [L,R]

        y = 1.0 - tf.to_float(action)

        #optimizer
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=logits)
        optimizer = tf.train.AdamOptimizer(self.learning_rate)

        gradients_and_variables = optimizer.compute_gradients(cross_entropy)


        for gradient, variable in gradients_and_variables:
            self.gradients.append(gradient)
            gradient_placeholder = tf.placeholder(tf.float32, shape=gradient.get_shape())
            self.gradient_placeholders.append(gradient_placeholder)
            self.grads_and_vars_feed.append((gradient_placeholder, variable))

        #apply the calculated gradient with the discount
        training_op = optimizer.apply_gradients(self.grads_and_vars_feed)

        init = tf.global_variables_initializer()
        saver =tf.train.Saver()

        ## function to calculate the rewards discount

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
            return [(discounted_rewards - reward_mean)/reward_std for discounted_rewards in all_discounted_rewards]







        with tf.Session() as sess:
            sess.run(init)

            card = self.hand + self.board
            rank_list = [ card['rank'] for card in card]

            action_val, gradient_val = sess.run([action,self.gradients],feed_dict={X:self.observations.reshape(1,self.num_input)})
            self.observations=np.array(rank_list)
            self.done=False
            self.current_rewards.append(reward)
            self.current_gradients.append(gradient_val)

            if (action_val[0][0])==0:
                val='f'
            else:
                val='c'







            # action from the input::
        if val == 'f':
            self.done = True
            self.fold = True
            self.hand = []
            money = 0
        elif val == 'c':
            bet_to_play = call_bet
            money = bet_to_play-self.bet
            self.money = self.money - money
            self.bet = bet_to_play
        elif val == 'b':
            bet_to_play = call_bet + min_bet # we add the min_bet when we bet.
            money = bet_to_play-self.bet
            self.money = self.money - money
            self.bet = bet_to_play
        elif val == 'h':
            print("check")
            money=0

        return bet_to_play, money
