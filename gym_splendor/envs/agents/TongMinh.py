from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name, turn=1000, stocks_const_limit=7):
        super().__init__(name)
        self.turn = turn
        self.stocks_const_limit = stocks_const_limit

    def action(self, state):
        stocks = []
        card = None
        stock_return = []

        if self.check_cards_buy(state):
            card = self.get_card_by_strategy(state)
        else:
            if self.check_get_n_stocks(state, n_stocks=3):
                stocks = self.get_stocks_by_strategy(state, n_stocks=3)
                if self.check_return_stocks(stocks):
                    stock_return = self.return_stocks(stocks)
            else:
                if self.check_get_n_stocks(state, n_stocks=2, DIFF=True):
                    stocks = self.get_stocks_by_strategy(state, n_stocks=2, DIFF=True)
                    if self.check_return_stocks(stocks):
                        stock_return = self.return_stocks(stocks)
                else:
                    if self.check_reserve_card():
                        card = self.reserve_card(state)
                        if self.check_return_stocks(stocks):
                            stock_return = self.return_stocks(stocks)
                    else:
                        if self.check_get_n_stocks(state, n_stocks=2, DIFF=False):
                            stocks = self.get_stocks_by_strategy(state, n_stocks=2, DIFF=False)
                            if self.check_return_stocks(stocks):
                                stock_return = self.return_stocks(stocks)
                        else:
                            if self.check_get_n_stocks(state, n_stocks=1):
                                stocks = self.get_stocks_by_strategy(state, n_stocks=1)
                                if self.check_return_stocks(stocks):
                                    stock_return = self.return_stocks(stocks)
        
        return stocks, card, stock_return

    def consider_cards_on_board(self, state):
        cards_on_board = state["Board"].dict_Card_Stocks_Show # dict
        if state["Turn"] > self.turn:
            del cards_on_board["I"]
        return cards_on_board

    # cards

    def check_cards_buy(self, state):
        for type_card in self.show_cards_buy(state):
            if self.show_cards_buy(state)[type_card]:
                return True
        return False

    def get_card_by_strategy(self, state):
        cards_available_buy = self.show_cards_buy(state)
        lst_cards_available_buy = []
        for type_card in cards_available_buy:
            lst_cards_available_buy += cards_available_buy[type_card]
        lst_cards_available_buy_order = sorted(lst_cards_available_buy, key=lambda x: x.score, reverse=True)
        if lst_cards_available_buy[0].score != 0:
            return lst_cards_available_buy[0]
        else:
            for card in lst_cards_available_buy_order:
                if self.stocks_const[card.type_stock] <= self.stocks_const_limit:
                    return card
            else:
                return random.choice(lst_cards_available_buy_order)

    def show_cards_buy(self, state):
        cards_on_board = self.consider_cards_on_board(state) # dict
        cards_down_hand = self.card_upside_down # list
        cards_available_buy = {
            "I": [],
            "II": [],
            "III": [],
            "Noble": []
        } # dict
        for type_card in cards_on_board:
            if type_card != "Noble":
                for card in cards_on_board[type_card]:
                    if self.check_get_card(card):
                        cards_available_buy[type_card].append(card)
        for card in cards_down_hand:
            if self.check_get_card(card):
                type_card = card.id.split("_")[0]
                cards_available_buy[type_card].append(card)
        return cards_available_buy # dict

    def show_stocks_shortage(self, _card):
        price = _card.stocks # dict, 5 keys
        my_stocks = {}
        for key in self.stocks_const.keys():
            my_stocks[key] = self.stocks[key] + self.stocks_const[key]
        my_stocks['auto_color'] = self.stocks['auto_color']
        lack_of_stocks = {}
        for key in price.keys():
            lack_of_stocks[key] = max(0, price[key] - my_stocks[key])
        n = my_stocks['auto_color']
        for i in range(n):
            if sum(lack_of_stocks.values()) == 0:
                break

            for key in lack_of_stocks.keys():
                if lack_of_stocks[key] != 0:
                    lack_of_stocks[key] -= 1
                    break
        return lack_of_stocks # no auto-color
        
    # stocks

    def get_stocks_by_strategy(self, state, n_stocks, DIFF=True):
        stocks_popular = self.show_stocks_popular(self.consider_cards_on_board(state))
        return_stocks_get = None

        if n_stocks == 3 and DIFF:
            def prioritize_triplet(combos):
                if self.check_stocks_on_board_get(state, combos[0]):
                    return combos[0]
                elif self.check_stocks_on_board_get(state, combos[1]):
                    return combos[1]
                else:
                    return self.get_stocks_uncommon_on_hand(state, n_stocks=3)

            # combo 1: black/r/w
            BRW = ["red", "black", "white"]
            BRW_popular = stocks_popular["red"] + stocks_popular["black"] + stocks_popular["white"]
            # combo 2: g/blue/w
            BGW = ["blue", "green", "white"]
            BGW_popular = stocks_popular["blue"] + stocks_popular["green"] + stocks_popular["white"]
            
            if BRW_popular > BGW_popular:
                return_stocks_get = prioritize_triplet([BRW, BGW])
            elif BRW_popular < BGW_popular:
                return_stocks_get = prioritize_triplet([BGW, BRW])
            else:
                BRW_common_hand = self.stocks["red"] + self.stocks["black"] + self.stocks["white"]
                BGW_common_hand = self.stocks["blue"] + self.stocks["green"] + self.stocks["white"]
                if BRW_common_hand < BGW_common_hand:
                    return_stocks_get = prioritize_triplet([BRW, BGW])
                elif BRW_common_hand > BGW_common_hand:
                    return_stocks_get = prioritize_triplet([BGW, BRW])
                else:
                    return_stocks_get = prioritize_triplet([BRW, BGW]) # prior to BRW
        
        elif n_stocks == 2 and not DIFF:
            stocks_available_get = self.show_stocks_on_board_get(state, threshold=3)
            common_stocks_available_get = sorted(stocks_available_get, key = lambda stock: stocks_popular[stock], reverse=True)
            return_stocks_get = [common_stocks_available_get[0]] * 2
        
        elif n_stocks == 2 and DIFF:
            def prioritize_couple(combos):
                if self.check_stocks_on_board_get(state, combos[0]):
                    return combos[0]
                elif self.check_stocks_on_board_get(state, combos[1]):
                    return combos[1]
                else:
                    return self.get_stocks_uncommon_on_hand(state, n_stocks=2)

            # combo 1: black/r/w
            BR = ["red", "black"]
            BR_popular = stocks_popular["red"] + stocks_popular["black"]
            # combo 2: g/blue/w
            BG = ["blue", "green"]
            BG_popular = stocks_popular["blue"] + stocks_popular["green"]
            
            if BR_popular > BG_popular:
                return_stocks_get = prioritize_couple([BR, BG])
            elif BR_popular < BG_popular:
                return_stocks_get = prioritize_couple([BG, BR])
            else:
                BR_common_hand = self.stocks["red"] + self.stocks["black"]
                BG_common_hand = self.stocks["blue"] + self.stocks["green"]
                if BR_common_hand < BG_common_hand:
                    return_stocks_get = prioritize_couple([BR, BG])
                elif BR_common_hand > BG_common_hand:
                    return_stocks_get = prioritize_couple([BG, BR])
                else:
                    return_stocks_get = prioritize_couple([BR, BG]) # prior to BRW
        
        elif n_stocks == 1:
            stocks_available_get = self.show_stocks_on_board_get(state, threshold=0)
            common_stocks_available_get = sorted(stocks_available_get, key = lambda stock: stocks_popular[stock], reverse=True)
            return_stocks_get = [common_stocks_available_get[0]]

        return return_stocks_get

    
    def get_stocks_uncommon_on_hand(self, state, n_stocks):
        # get stocks on board that are most uncommon on hands
        return sorted(self.show_stocks_on_board_get(state), key=lambda stock: self.total_stocks()[stock])[:n_stocks] # list

    def check_get_n_stocks(self, state, n_stocks, DIFF=True):
        stocks_on_board = state["Board"].stocks

        def check_type_stock_diff(threshold, stocks_on_board=stocks_on_board):
            count_type_stock = 0
            for type_stock in stocks_on_board:
                if type_stock != "auto_color":
                    if stocks_on_board[type_stock] > 0:
                        count_type_stock += 1
                    if count_type_stock >= threshold:
                        return True
            return False

        if n_stocks == 2 and not DIFF:
            for type_stock in stocks_on_board:
                if type_stock != "auto_color":
                    if stocks_on_board[type_stock] >= 4:
                        return True
            return False
        return check_type_stock_diff(n_stocks)

    def check_stocks_on_board_get(self, state, stocks, threshold=0):
        stocks_on_board = state["Board"].stocks
        for stock in stocks:
            if stock != "auto_color":
                if stocks_on_board[stock] <= threshold:
                    return False
        return True
   
    def total_stocks(self):
        total_stocks = self.stocks_const
        for type_stock in self.stocks_const:
            total_stocks[type_stock] = self.stocks_const[type_stock] + self.stocks[type_stock]
        return total_stocks # dict

    def show_stocks_popular(self, cards):
        stocks_popular = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0
        }
        for type_card in cards:
            for card in cards[type_card]:
                for stock in card.stocks:
                    if card.stocks[stock] > 0:
                        stocks_popular[stock] += 1
        return stocks_popular # dict
    
    def show_stocks_on_board_get(self, state, threshold=0):
        stocks_on_board = state["Board"].stocks
        stocks_get = []
        for stock in stocks_on_board:
            if stock != "auto_color":
                if stocks_on_board[stock] > threshold:
                    stocks_get.append(stock)
        return stocks_get

    # reserve

    def show_n_stocks(self):
        n_stocks = 0
        for stock in self.stocks:
            n_stocks += self.stocks[stock]
        return n_stocks

    def check_reserve_card(self):
        if len(self.card_upside_down) >= 3:
            return False
        return True


    def reserve_card(self, state):
        cards_on_board = self.consider_cards_on_board(state)
        players = state["Player"]
        stocks_common_players = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0
        }
        for player in players:
            for stock in stocks_common_players:
                stocks_common_players[stock] += player.stocks[stock] + player.stocks_const[stock]
        opponent_wish_card = self.consider_cards_on_board(state)["II"][0]
        max_heu = self.wish_heuristic(opponent_wish_card, stocks_common_players, score_lever=5)
        for type_card in cards_on_board:
            if type_card != "Noble":
                for card in cards_on_board[type_card]:
                    heu = self.wish_heuristic(card, stocks_common_players, score_lever=5)
                    if heu > max_heu:
                        max_heu = heu
                        opponent_wish_card = card
        
        return opponent_wish_card


    def wish_heuristic(self, card, stocks_common_players, score_lever=2):
        heu = 0
        for stock in stocks_common_players:
            heu += stocks_common_players[stock] - card.stocks[stock] + card.score * score_lever
        return heu

    # return

    def check_return_stocks(self, get_stocks):
        n_stocks = 0
        for type_stock in self.stocks:
            n_stocks += self.stocks[type_stock]
        n_stocks += len(get_stocks)
        if n_stocks > 10:
            return True
        return False
    

    def return_stocks(self, get_stocks):
        stocks_on_hand = self.stocks
        stocks_return = []
        n_stocks = 0
        for stock in self.stocks:
            n_stocks += stocks_on_hand[stock] + get_stocks.count(stock)
        for _ in range(n_stocks - 10):
            stock_common_on_hand = sorted(stocks_on_hand.items(), key=lambda x: x[1], reverse=True)[0][0]
            stocks_on_hand[stock_common_on_hand] -= 1
            stocks_return.append(stock_common_on_hand)
        
        return stocks_return 

