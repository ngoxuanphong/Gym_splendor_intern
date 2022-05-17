from ..base.player import Player
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state=None,action_space = None):

        card = self.check_lat_the(state['Board'])

        if card != None:
            return [], card, [], 2

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

            return stocks, None, stocks_return, 1

        if state['Board']._Board__stocks['auto_color'] > 0 and self._Player__card_upside_down.__len__() < 3:
            card = self.Tim_the_up(state['Board'])
            stocks_return = self.Tim_nl_tra([], 9)

            return [], card, stocks_return, 3

        if n == 1:
            stock = list_nl_target[0]
            stocks = [stock]
            if state['Board']._Board__stocks[stock] >= 4:
                stocks.append(stock)

            stocks_return = self.Tim_nl_tra(stocks)

            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)

            return stocks, None, stocks_return, 1

        # return [], None, [], 0

    def Tim_the_up(self, board):
        list_card = []
        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board._Board__dict_Card_Stocks_Show[type_card]:
                    list_card.append(card)

        value_cards = [car._Card__score / sum(list(car._Card__stocks.values())) for car in list_card]
        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]
        

    def Tim_nl_tra(self, stocks, n=10):
        dict_hien_tai = deepcopy(self._Player__stocks)
        for i in stocks:
            dict_hien_tai[i] += 1

        snl = sum(list(dict_hien_tai.values()))
        if snl <= n:
            return []

        list_stock_return = []
        nl_thua = snl - n
        for i in range(nl_thua):
            x = self.lua_chon_nl_tra(dict_hien_tai)
            list_stock_return.append(x)
            dict_hien_tai[x] -= 1

        return list_stock_return

    def lua_chon_nl_tra(self, dict_input):
        x = deepcopy(self._Player__stocks_const)
        dict_nl = {}
        for key in x.keys():
            if dict_input[key] > 0:
                dict_nl[key] = x[key] - dict_input[key]
        
        dict_nl_can_bo = {k:v for k,v in sorted(dict_nl.items(), key = lambda item: item[1], reverse=True)}

        return list(dict_nl_can_bo.keys())[0]

    def board_nl_target(self, board):
        list_nl_can = []
        dict_board_nl = self.board_nl(board)
        for key in dict_board_nl.keys():
            if dict_board_nl[key] > 0:
                list_nl_can.append(key)

        return list_nl_can

    def board_nl(self, board):
        x = deepcopy(board._Board__stocks)
        x.pop('auto_color')
        y = deepcopy(self._Player__stocks_const)

        dict_nl = {}
        for key in x.keys():
            dict_nl[key] = x[key] - y[key]

        dict_nl_can = {k:v for k,v in sorted(dict_nl.items(), key = lambda item: item[1], reverse=True)}
        for key in x.keys():
            dict_nl_can[key] = x[key]

        return dict_nl_can

    def check_lat_the(self, board):
        list_card = []
        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board._Board__dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card.append(card)

        for card in self._Player__card_upside_down:
            if self.check_get_card(card):
                list_card.append(card)

        if list_card.__len__() == 0:
            return None
            
        value_cards = [car._Card__score / sum(list(car._Card__stocks.values())) for car in list_card]
        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]