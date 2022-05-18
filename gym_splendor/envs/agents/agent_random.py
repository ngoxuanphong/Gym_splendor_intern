from re import T
from ..base.player import Player
import random
import math
import json
import numpy as np


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        # if len(a) == 0:
        #     return [], None, []
        number = random.randint(0,len(a)-1)
        # try:
        #     #read_json_file
        #     s_a = json.load(open('sample.json'))
        # except:
        #     s_a = {}

        # s_a = {}
        # list_a = []
        # for id_a in range(len(json.load(open('gym_splendor/envs/data_action/action_space.json')))):
        #     list_a.append({f'{id_a}': np.nan})
        # for id_s in range(len(t)):
        #     s_a[f'{id_s}_{t[id_s]}'] = list_a
        # with open("sample.json", "w") as outfile:
        #     json.dump(s_a, outfile)
        
        if self.check_victory(t) == 1:
            print(self.name, state['Turn'], self.score, 'thắng')
        elif self.check_victory(t) == 0:
            print(self.name, state['Turn'], self.score, 'Thua')
        # if state["Turn"] >40:
            # print(self.check_victory(t))
        print(number)
        return a[number]
