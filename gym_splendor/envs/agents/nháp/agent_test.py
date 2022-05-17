from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def action(self, state):
        if state['Turn'] < 4:
            return [], state['Board']._Board__dict_Card_Stocks_Show['III'][0], []

        return [], self._Player__card_upside_down[0], []