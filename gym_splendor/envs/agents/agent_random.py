from re import T
from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        number = random.randint(0,len(a)-1)
        # print(a[number])
        # print(self.check_victory(t))
        # if state["Turn"] >40:
            # print(self.check_victory(t))
        return a[number]