from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        
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


# def action(board, arr_player):
#     # print(board_nl(board))
#     Check_laythe = Checklatthe(board)
#     nlnhamtoi = list(check_board_nl(board).keys())

#     if Check_laythe != None:
#         return player_02.getCard(Check_laythe, board)
#     if len(nlnhamtoi) >= 3:
#         if player_02.checkThreeStocks(board, nlnhamtoi[0], nlnhamtoi[1], nlnhamtoi[2]):
#             return player_02.getThreeStocks(nlnhamtoi[0], nlnhamtoi[1], nlnhamtoi[2], board, TimNguyenLieuTra(nlnhamtoi[0], nlnhamtoi[1], nlnhamtoi[2]))

#     elif len(nlnhamtoi) == 2:
#         if player_02.checkOneTwoStock(board, nlnhamtoi[0], nlnhamtoi[1]):
#             return player_02.getOneTwoStock(nlnhamtoi[0], nlnhamtoi[1], board, TimNguyenLieuTra(nlnhamtoi[0], nlnhamtoi[1]))

#     elif len(nlnhamtoi) == 1:
#         if player_02.checkOneTwoStock(board, nlnhamtoi[0], "Null"):
#             return player_02.getOneTwoStock(nlnhamtoi[0], "Null", board, TimNguyenLieuTra(nlnhamtoi[0]))
#     else:
#         return board
