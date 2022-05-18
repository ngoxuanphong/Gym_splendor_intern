from ..base.player import Player
from copy import deepcopy
import random

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        card = self.check_lat_the(state['Board'])

        if card != None:
            return [], card, []

        list_nl_target = self.board_nl_target(state['Board'])
        n = list_nl_target.__len__()
        if n >= 2:
            snl_lay = min(3,n)
            stocks = list_nl_target[0:snl_lay]
            stocks_return = self.Tim_nl_tra(stocks)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            
            if stocks.__len__() != 0:
                return stocks, None, stocks_return

        if (state['Board'].stocks['auto_color'] > 0 and self.card_upside_down.__len__() < 3) or (self.card_upside_down.__len__() < 3 and sum(state['Board'].stocks.values()) == state['Board'].stocks['auto_color']):
            card = self.Tim_the_up(state['Board'])
            if card != None:
                stocks_return = self.Tim_nl_tra(['auto_color'])

                return [], card, stocks_return

        if n == 1:
            stock = list_nl_target[0]
            stocks = [stock]
            if state['Board'].stocks[stock] >= 4:
                stocks.append(stock)

                stocks_return = self.Tim_nl_tra(stocks)
                
                nl_trung_nhau = list(set(stocks) & set(stocks_return))
                for i in nl_trung_nhau:
                    stocks.remove(i)
                    stocks_return.remove(i)
                
                if stocks.__len__() >= 2:
                    return stocks, None, stocks_return
        
        stocks = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        
        if stocks.__len__() > 0:
            return stocks, None, []

        for i in range(3):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))

        stocks_return = []
        nl_thua = max(sum(self.stocks.values()) + stocks.__len__() - 10, 0)
        pl_st = deepcopy(self.stocks)
        for i in range(nl_thua):
            temp_list = [mau for mau in pl_st.keys() if mau != 'auto_color' and pl_st[mau] > 0]
            mau_choice = random.choice(temp_list)
            stocks_return.append(mau_choice)
            pl_st[mau_choice] -= 1
        
        return stocks, None, stocks_return

    def Tim_the_up(self, board):
        list_card = []
        hand_vc = deepcopy(self.stocks_const)
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board.dict_Card_Stocks_Show[type_card]:
                    nl_thieu = {}
                    for mau in card.stocks.keys():
                        nl_thieu[mau] = max(0, card.stocks[mau] - hand_vc[mau])
                        if sum(nl_thieu.values()) <= 10:
                            list_card.append(card)

        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_card]
        if value_cards.__len__() == 0:
            return None

        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]

    def Tim_nl_tra(self, stocks):
        nl_hien_tai = deepcopy(self.stocks)
        for i in stocks:
            nl_hien_tai[i] += 1

        snl = sum(list(nl_hien_tai.values()))
        if snl <= 10:
            return []

        list_stock_return = []
        for i in range(snl-10):
            x = self.lua_chon_nl_tra(nl_hien_tai)
            list_stock_return.append(x)
            nl_hien_tai[x] -= 1
        
        return list_stock_return

    def lua_chon_nl_tra(self, nl_hien_tai):
        x = deepcopy(self.stocks_const)
        dict_nl = {}
        for key in x.keys():
            if nl_hien_tai[key] > 0:
                dict_nl[key] = x[key] + nl_hien_tai[key]

        dict_nl_bo = {k:v for k,v in sorted(dict_nl.items(), key = lambda item: item[1], reverse=False)}

        return list(dict_nl_bo.keys())[0]

    def board_nl_target(self, board):
        list_nl_can = []
        dict_board_nl = self.board_nl(board)
        for key in dict_board_nl.keys():
            if dict_board_nl[key] > 0:
                list_nl_can.append(key)

        return list_nl_can

    def board_nl(self, board):
        x = deepcopy(board.stocks)
        x.pop('auto_color')
        y = deepcopy(self.stocks_const)

        dict_nl = {}
        for key in x.keys():
            dict_nl[key] = x[key] - y[key]

        dict_nl_can = {k:v for k,v in sorted(dict_nl.items(), key = lambda item: item[1], reverse=True)}
        for key in x.keys():
            dict_nl_can[key] = x[key]

        return dict_nl_can

    def check_lat_the(self, board):
        list_card = []

        for card in self.card_upside_down:
            if self.check_get_card(card):
                list_card.append(card)

        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board.dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card.append(card)

        if list_card.__len__() == 0:
            return None

        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_card]
        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]