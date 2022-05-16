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

        #tìm thẻ có điểm trên bàn theo thứ tự I, II, III
        # card = state['Board'].dict_Card_Stocks_Show['II'][0]
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for C_tg in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             print(C_tg.id, C_tg.stocks.values(), C_tg.score, sum(C_tg.stocks.values()))
        #             if (C_tg.score > card.score) and (sum(C_tg.stocks.values()) <= sum(card.stocks.values())):
        #                 card = C_tg

        # for type_card in reversed(state['Board'].dict_Card_Stocks_Show):
        #     print(type_card)
        # print(card.stocks, card.score)
        stocks = ['red', 'red']
        return stocks, card, stock_return
    
