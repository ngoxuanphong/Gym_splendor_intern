import json
import random
import gym

import numpy
from gym_splendor.envs.base.board import Board
from gym_splendor.envs.base.card import Card_Stock,Card_Noble
from gym_splendor.envs.agents import agents_inteface
from gym_splendor.envs.base import error
from gym_splendor.envs.convertAction import action_space as AS

def getType(dict_type):
        for j in dict_type.keys():
            if dict_type[j] == 1:
                return j
amount_player = 4
class SplendporEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.turn = 0
        self.amount_player = amount_player
        self.board = None
        self.player = None
        self.pVictory = None
        self.state = {}
        self.actioner = AS.Action_Space_State()

    def step(self, action):
        if self.close() and self.turn % self.amount_player == self.amount_player-1:
            self.state["Victory"] = self.pVictory
            self.turn = self.turn+1
            return self,None,True,None
        else:
            if isinstance(action, int)==True:
                # self.board.hien_the()
                action = self.player[self.turn % self.amount_player].transform(self.state,action)
            stocks = action[0]
            card = action[1]
            stock_return = action[2]
            try:
                prioritizes = action[3]
            except:
                prioritizes = 0
            self.state["Turn"] = self.turn+1
            self.player[self.turn % self.amount_player].action_real(self.state,stocks,card,stock_return,prioritize=prioritizes)
            self.turn = self.turn+1
            return self.state,None,None,None


    def reset(self):
        self.turn = 0
        self.amount_player = amount_player
        self.board = Board()
        self.player = random.sample(agents_inteface.ListPlayer, k=self.amount_player)
        for p in self.player:
            p.reset()
        self.pVictory = None
        self.state = {
            "Turn" : 0,
            "Board": self.board,
            "Player": self.player,
            "Victory": self.pVictory,
        }
        self.setup_board()

    def render(self, mode='human', close=False):
        print("Turn", self.turn, "Board Stocks",self.board.stocks)
        self.board.hien_the()
        t = 0
        for p in self.player:
            print(p.name,p.score,list(p.stocks.values()),list(p.stocks_const.values()),end="")
            print(" Card got: ",end="")
            for i in p.card_open:
                print(i.id, end=" ")
            t +=1
            if t % 2 == 0:
                print()
            else:
                print(end="    ")
        print("----------------------------------------------------------------------------------------------------------")

    def setup_board(self):
        self.board.Stocks(self.amount_player)
        with open('gym_splendor/envs/Cards_Splendor.json') as datafile:
            data = json.load(datafile)
        Ma = ""
        stt = 1
        dict_board_board_show = { 'I': [],
            'II': [],
            'III': [],
            'Noble': []}
        dict_board_upsite_down = { 'I': [],
            'II': [],
            'III': [],
            'Noble': []}
        for i in data:
            if stt <= 40:
                Ma = "I_" + str(stt)
            elif stt <= 70:
                Ma = "II_" + str(stt - 40)
            elif stt <= 90:
                Ma = "III_" + str(stt - 70)
            else : 
                Ma = "Noble_"+ str(stt - 90)
            stt+=1
            if i["type"] != "Noble":
                c = Card_Stock(Ma,
                    getType(i["type_stock"]), i["score"], i["stock"])
                dict_board_upsite_down[i["type"]].append(c)
            else:
                c = Card_Noble(Ma,i["score"], i["stock"])
                dict_board_upsite_down["Noble"].append(c)
        for i in dict_board_upsite_down.keys():
            random.shuffle(dict_board_upsite_down[i])

        for key in dict_board_board_show.keys():
            for i in range(4):
                dict_board_board_show[key].append(dict_board_upsite_down[key][0])
                dict_board_upsite_down[key].remove(dict_board_upsite_down[key][0])
        dict_board_board_show["Noble"].append(dict_board_upsite_down["Noble"][0])
        dict_board_upsite_down["Noble"].remove(dict_board_upsite_down["Noble"][0])
        self.state["Board"].setDict_Card_Stocks_Show(dict_board_board_show)
        self.state["Board"].setDict_Card_Stocks_UpsiteDown(dict_board_upsite_down)

    def close(self):
        arr_point = [i.score for i in self.player]
        max_point = max(arr_point)
        if max_point >= 15:
            arr_point = [1 if i == max_point else 0 for i in arr_point]
            arr_amount_card = [len(i.card_open) for i in self.player]
            min = 100
            for i in range(len(arr_point)):
                if arr_point[i] == 1 and arr_amount_card[i] < min:
                    min = arr_amount_card[i]
                    self.pVictory = self.player[i]
            return True
        return False
