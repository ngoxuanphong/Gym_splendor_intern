from ..base.player import Player
from copy import deepcopy
import random

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):

        # print(self.check_winner(state))

        card = self.check_lat_the(state['Board'])

        if card != None:
            # Lấy thẻ
            return [], card, []

        list_nl_target = self.board_nl_target(state['Board'])
        n = list_nl_target.__len__()
        if n >= 2:
            snl_lay = min(3,n)
            stocks = list_nl_target[0:snl_lay]
            stocks_return = self.Tim_nl_tra(stocks)
            # print(stocks, stocks_return)
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            # print(stocks, stocks_return)
            return stocks, None, stocks_return

        if state['Board']._Board__stocks['auto_color'] > 0 and self._Player__card_upside_down.__len__() < 3:
            card = self.Tim_the_up(state['Board'])
            stocks_return = self.Tim_nl_tra(['auto_color'])

            return [], card, stocks_return

        if n == 1:
            stock = list_nl_target[0]
            stocks = [stock]
            if state['Board']._Board__stocks[stock] >= 4:
                stocks.append(stock)

            stocks_return = self.Tim_nl_tra(stocks)
            # print(stocks, stocks_return)
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            # print(stocks, stocks_return)
            return stocks, None, stocks_return
        
        stocks = []
        for i in range(3):
            temp_list = [mau for mau in state['Board']._Board__stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board']._Board__stocks[mau] > 0]
            if temp_list.__len__() != 0:
                stocks.append(random.choice(temp_list))

        stocks_return = self.Tim_nl_tra(stocks)
        # print(stocks, stocks_return)
        nl_trung_nhau = list(set(stocks) & set(stocks_return))
        for i in nl_trung_nhau:
            stocks.remove(i)
            stocks_return.remove(i)
        # print(stocks, stocks_return)
        return stocks, None, stocks_return

    def Tim_the_up(self, board):
        list_card = []
        hand_vc = deepcopy(self._Player__stocks_const)
        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board._Board__dict_Card_Stocks_Show[type_card]:
                    nl_thieu = {}
                    for mau in card._Card__stocks.keys():
                        nl_thieu[mau] = max(0, card._Card__stocks[mau] - hand_vc[mau])
                        if sum(nl_thieu.values()) <= 10:
                            list_card.append(card)

        value_cards = [car._Card__score / sum(list(car._Card__stocks.values())) for car in list_card]
        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]

    def Tim_nl_tra(self, stocks):
        nl_hien_tai = deepcopy(self._Player__stocks)
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
        x = deepcopy(self._Player__stocks_const)
        dict_nl = {}
        for key in x.keys():
            if nl_hien_tai[key] > 0:
                dict_nl[key] = x[key] + nl_hien_tai[key]

        dict_nl_bo = {k:v for k,v in sorted(dict_nl.items(), key = lambda item: item[1], reverse=True)}

        return list(dict_nl_bo.keys())[0]

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

        for card in self._Player__card_upside_down:
            if self.check_get_card(card):
                list_card.append(card)

        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board._Board__dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card.append(card)

        if list_card.__len__() == 0:
            return None

        value_cards = [car._Card__score / sum(list(car._Card__stocks.values())) for car in list_card]
        max_value = max(value_cards)

        return list_card[value_cards.index(max_value)]

    #####################################################################################################

    # def check_winner(self, state):
    #     name = ''
    #     score_max = 14
    #     player_win = None
    #     if state['Turn']%4 == 0:
    #         for player in list(state['Player']):
    #             if player.score > score_max:
    #                 score_max = player.score 
    #         if score_max > 14:

    #             for player in list(state['Player']):
    #                 if player.score >= score_max:
    #                     score_max = player.score 
    #                     player_win = player
    #                 elif player.score == score_max:
    #                     if len(player.card_open) < len(player_win.card_open):
    #                         player_win = player
    #             if score_max > 14:
    #                 print('Tap trung vao day nao')
    #                 print(player_win.name, 'win với ', score_max, 'ở turn ',  state['Turn']/4)