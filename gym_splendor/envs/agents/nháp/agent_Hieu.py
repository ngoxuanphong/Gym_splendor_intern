from ..base.player import Player
import random
import math
import json
import pandas as pd
import os
'''
format state:
0 Scores
1 board.stock
2 player.stock
3 player.stock_const
4 list_card:
    -chưa xuất hiện: 0
    -trên bàn chơi: 1
    -mình đã lấy: 2
    -mình đang úp: 3
'''
file_train = pd.read_csv('./TRAIN_HIEU/file_train.csv')


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)




    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        print(self.NL_board(state))
        # self.check_winner(state)
        
        card = self.Checklatthe(state["Board"])
        nlnhamtoi = list(self.check_board_nl(state["Board"]).keys())
        if card != None:
            return stocks,card,stock_return
        if len(nlnhamtoi) >= 3:
            stocks = nlnhamtoi[:3]
        stock_return = list(self.TimNguyenLieuTra(stocks))

        return stocks, card, stock_return
    
    def board_nl(self,board):
        x = board.stocks
        y = self.stocks_const
        x.pop("auto_color")
        dic_nl = {}
        for i in x.keys():
            nl = x[i] - y[i]
            dic_nl[i] = nl
        dict_nl = {k: v for k, v in sorted(
            dic_nl.items(), key=lambda item: item[1], reverse=True)}
        return dict_nl
    
    def check_board_nl(self,board):
        dict_check_nl = {}
        for i in self.board_nl(board):
            if self.board_nl(board)[i] > 0:
                dict_check_nl[i] = self.board_nl(board)[i]
        return dict_check_nl

    def Checklatthe(self,board):
        list_card = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != "Noble":
                for card in board.dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card.append(card)
        ti_so = []
        for i in list_card:
            x = i.score
            y = sum(list(i.stocks.values()))
            dinh_gia = x/y
            ti_so.append(dinh_gia)
        dinh_gia_max = 0
        for i in ti_so:
            if dinh_gia_max < i:
                dinh_gia_max = i
        for i in range(len(ti_so)):
            if ti_so[i] == dinh_gia_max:
                return list_card[i]
    
    def TimNguyenLieuTra(self,arr):
        dict_hien_tai = self.stocks.copy()
        for i in arr:
            dict_hien_tai[i] += 1
        snl = sum(list(dict_hien_tai.values()))
        dict_tra = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
            "auto_color": 0,
        }
        if snl <= 10:
            return dict_tra
        else:
            for i in range(snl - 10):
                x = self.NLTTvaNLC(self.stocks_const, dict_hien_tai)
                dict_hien_tai[x] -= 1
                dict_tra[x] += 1
        for key,value in dict_tra.items():
            for i in range(value):
                yield key

    def NLTTvaNLC(self,const_stock, stock):
        x = const_stock
        y = stock
        dict_nl_can_bo = {}
        for i in x.keys():
            if y[i] > 0:
                nl_can_bo = x[i] - y[i]
            else:
                nl_can_bo = -10
            dict_nl_can_bo[i] = nl_can_bo
        dict_nl_can_bo = {k: v for k, v in sorted(
            dict_nl_can_bo.items(), key=lambda item: item[1], reverse=True)}
        return list(dict_nl_can_bo.keys())[0]   

    def NL_board(self, state):
        board = state['Board']
        list_card_open = []
        list_score = [player.score for player in state['Player']]
        
        for i in board.dict_Card_Stocks_Show.keys():
            for j in board.dict_Card_Stocks_Show[i]:
                list_card_open.append((convert_card_to_id(j.id)))
        list_all_card = []
        list_player_card = [convert_card_to_id(card.id) for card in self.card_open]
        list_player_noble = [convert_card_to_id(card.id) for card in self.card_noble]
        list_player_upside_down = [convert_card_to_id(card.id) for card in self.card_upside_down]
        list_player_card_test = [card.id for card in self.card_open]

        list_card_check = []
        for player in state['Player']:
            for card in player.card_open:
                if convert_card_to_id(card.id) <= 40:
                    list_card_check.append(card.id)

        print('CHECK', len(list_card_check),list_player_card, list_player_noble, list_player_card_test)
        for i in range(1, 101):
            if i in list_card_open:
                list_all_card.append(1)
            elif i in list_player_card or i in list_player_noble:
                list_all_card.append(2)
            elif i in list_player_upside_down:
                list_all_card.append(3)
            else:
                list_all_card.append(0)

        list_ = ['-'.join(str(i) for i in list_score) +'/'+
                '-'.join(str(i) for i in list(board.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks.values())) +'/'+
                '-'.join(str(i) for i in list(self.stocks_const.values())) +'/'+
                '-'.join(str(i) for i in list_all_card)]

        return list_


def convert_card_to_id(id):
    if 'Noble_' in id:
        return int(id.replace('Noble_', '')) + 90
    elif 'III_' in id:
        return int(id.replace('III_', '')) + 70
    elif 'II_' in id:
        return int(id.replace('II_', '')) + 40
    elif 'I_' in id:
        return int(id.replace('I_', ''))
'''
['13-14-14-2/7-6-5-5-6-5/0-0-0-1-0-0/4-15-1-2-3
/0-2-0-0-0-0-0-0-1-0-0-2-0-0-2-1-0-0-1-0-2-2-0-0-0-0-0-1-2-0-0-2-0-2-2-2-0-0-0-0-0-0-0-0-0-0-0-0-0-1-0-0-0-0-0-0-0-0-0-0-1-0-0-0-0-0-0-1-0-1-0-0-0-0-0-0-0-0-0-1-0-0-0-0-1-0-0-1-1-0-0-1-0-0-0-1-0-1-1-1']
'''