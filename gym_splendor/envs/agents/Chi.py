from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        card = None
        stocks = []
        stock_return = []
        if self.target_cards(state['Board']):
            card = self.target_cards(state['Board'])
            stocks = []
        else:
            stocks, card = self.get_coins(state['Board'])
            if stocks is not None:
                card = None
        if (card is None) and (len(stocks) == 0):
            for key in state['Board'].stocks:
                if key != 'auto_color':
                    if state['Board'].stocks[key] > 0:
                        stocks.append(key)
            if len(stocks) > 3:
                stocks = stocks[:3]
        stock_return = self.return_coins(stocks)
        return stocks, card, stock_return

    def card_on_table(self, board):
        cards = []
        for key in board.dict_Card_Stocks_Show.keys():
            if key != 'Noble':
                cards.extend(board.dict_Card_Stocks_Show[key])
        cards.extend(self.card_upside_down)
        return cards

    def lack_of_coin(self, card):
        lack_of_coins = {}
        my_stock = {}
        for key in self.stocks_const.keys():
            my_stock[key] = self.stocks_const[key] + self.stocks[key]
        card_stock = card.stocks
        for key in card_stock.keys():
            if my_stock[key] < card_stock[key]:
                lack_of_coins[key] = card_stock[key] - my_stock[key]
        return lack_of_coins

    def review_cards_by_lack_coins(self, board):
        lack_of_coins = {}
        my_stock = {}
        for key in self.stocks_const.keys():
            my_stock[key] = self.stocks_const[key] + self.stocks[key]
        my_stock['auto_color'] = self.stocks['auto_color']
        cards = self.card_on_table(board)
        for card in cards:
            lack_coins = {}
            for key in card.stocks.keys():
                if my_stock[key] < card.stocks[key]:
                    lack_coins[key] = card.stocks[key] - my_stock[key]
            lack_of_coins[card] = sum(lack_coins.values()) - my_stock['auto_color']
        sorted_lack_of_coins = dict(sorted(lack_of_coins.items(), key=lambda item: item[1]))
        return sorted_lack_of_coins

    def get_coins(self, board):
        stocks = []
        bank_coins = board.stocks
        bank_coins['auto_color'] = 0
        dict_card_by_lack_coins = self.review_cards_by_lack_coins(board)
        for card in dict_card_by_lack_coins.keys():
            lack_of_coins = self.lack_of_coin(card)
            sorted_lack_of_coins = dict(sorted(lack_of_coins.items(), key=lambda item: item[1], reverse=True))
            for key in sorted_lack_of_coins.keys():
                if bank_coins[key] > 0:
                    stocks.append(key)
            if len(stocks) > 3:
                stocks = stocks[:3]
                return stocks, card
            elif len(stocks) == 1:
                if dict_card_by_lack_coins[card] == 1:
                    if (card.score > 0) and (board.stocks['auto_color'] > 0) and (len(self.card_upside_down) < 3):
                        if card not in self.card_upside_down:
                            stocks = []
                            return stocks, card
                elif dict_card_by_lack_coins[card] == 2:
                    if bank_coins[stocks[0]] > 3:
                        stocks.append(stocks[0])
                        return stocks, card
                    else:
                        for key in bank_coins.keys():
                            if (key not in stocks) and (bank_coins[key] > 0):
                                stocks.append(key)
                        if len(stocks) > 3:
                            stocks = stocks[:3]
                            return stocks, card
                        return stocks, card
            elif len(stocks) == 2:
                for key in bank_coins.keys():
                    if (key not in stocks) and (bank_coins[key] > 0):
                        stocks.append(key)
                        return stocks, card
            return stocks, card

    def return_coins(self, get_stock):
        my_stock = self.stocks
        return_coins = []
        for key in get_stock:
            my_stock[key] += 1
        sort_my_stock = dict(sorted(my_stock.items(), key=lambda item: item[1], reverse=True))
        if sum(my_stock.values()) > 10:
            for key in sort_my_stock.keys():
                return_coins.append(key)
            if 'auto_color' in return_coins:
                return_coins.remove('auto_color')
            return return_coins[:sum(my_stock.values()) - 10]
        return return_coins

    def target_cards(self, board):
        cards = self.card_on_table(board)
        dict_card_can_buy = {}
        list_card_can_buy = []
        for card in cards:
            if self.check_get_card(card):
                list_card_can_buy.append(card)
                dict_card_can_buy[card] = card.score
        if len(list_card_can_buy) > 0:
            for card in list_card_can_buy:
                if card.score == max(dict_card_can_buy.values()):
                    return card
        return None
