
from classes import Player





class Class2(Player):
    def __init__(self,money,cpu=False,name='jerry'):
        Player.__init__(self,money,cpu,name)
        self.yolo='fo'


player1 = Class2(money=100,name='AI')
print(player1.yolo)
