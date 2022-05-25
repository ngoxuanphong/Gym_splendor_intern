from ..base.player import Player
import random
import math
import copy


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        affordable_cards_list = self.get_affordable_cards(state['Board'])
        if len(affordable_cards_list) == 0:
            wanted_card, _ = self.get_most_viable_unaffordable_card(state)
            stocks = self.check_get_stocks(wanted_card, state['Board'].stocks)
            stock_return = self.get_stock_return(stocks, wanted_card)
            if stocks == []:
                return stocks, wanted_card, stock_return, 3

            card = None
        else:
            card_afford = self.get_most_viable_affordable_card(affordable_cards_list)
            card_unafford, _ = self.get_most_viable_unaffordable_card(state)
            chip_buy_afford = self.evaluate_affordable_card(card_afford)
            stocks_need_unafford = self.get_stocks_need(card_unafford)
            ratio_afford = card_afford.score / (chip_buy_afford + 2)
            ratio_unafford = card_unafford.score / (sum(stocks_need_unafford.values()) + 0.01)
            # if chip_buy_afford > sum(stocks_need_unafford.values()):
            if ratio_afford > ratio_unafford:
                stocks = self.check_get_stocks(card_unafford, state['Board'].stocks)
                stock_return = self.get_stock_return(stocks, card_unafford)
                if stocks == []:
                    return stocks, card_unafford, stock_return, 3
                card = None
            else:
                card = card_afford
                stocks = []
                stock_return = []
        return stocks, card, stock_return
    

    def get_stocks_need(self, wanted_card):
        '''
        Return a dictionary containing the stocks needed to buy the wanted_card
            param: 
                wanted_card(class Card)
            return: 
                a dictionary containing the stocks needed to buy the wanted_card
        '''
        if wanted_card is None:
            return {'no wanted card' : 999}
        price = wanted_card.stocks # dict
        ret = {}
        needed_stocks = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0
        }
        stock_dict = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0,
            "auto_color": 0
        }
        for key in stock_dict.keys():
            if key != 'auto_color':
                stock_dict[key] += self.stocks[key]
                stock_dict[key] += self.stocks_const[key]
            else:
                stock_dict[key] += self.stocks[key]
        for key in price.keys():
            needed_stocks[key] = max(0, price[key] - stock_dict[key])
        auto_color = stock_dict['auto_color']
        for _ in range(auto_color):
            if sum(needed_stocks.values()) == 0:
                break
            for key in needed_stocks.keys():
                if needed_stocks[key] != 0:
                    needed_stocks[key] -= 1
                    break
        for key, val in needed_stocks.items():
            if val != 0:
                ret.update({key : val})
        return ret
    

    def check_get_stocks(self, wanted_card, stocks_onboard):
        '''
        check whether the player can get the stocks needed
            param:
                stocks_need: dict
                stocks_onboard: dict
            return:
                stocks that the player wants to get
        '''
        stocks_onboard_can_get = {}
        wanted_stocks = []
        stocks_need = self.get_stocks_need(wanted_card)
        # get intersect keys betweenn stock_onboard and stock_need
        for key, val in stocks_onboard.items():
            if key != 'auto_color' and val != 0:
                stocks_onboard_can_get.update({key: val})
        intersect_keys = Agent.find_intersection(list(stocks_need.keys()), list(stocks_onboard_can_get.keys()))
        
        # get list_stocks_onboard
        list_stocks_onboard = list(stocks_onboard_can_get.items())
        list_stocks_onboard.sort(key=lambda x:x[1], reverse=True)

        # get list_stocks_need
        list_stocks_need = list(stocks_need.items())
        list_stocks_need.sort(key=lambda x:x[1], reverse=True)
        
        # get wanted_stocks
        if len(intersect_keys) == 0:
            if stocks_onboard['auto_color'] != 0 and len(self.card_upside_down) < 2 and wanted_card not in self.card_upside_down:
                return []
            tmp_length = len(list_stocks_onboard)
            if tmp_length == 1:
                if list_stocks_onboard[0][1] >= 4:
                    wanted_stocks.append(list_stocks_onboard[0][0])
                    wanted_stocks.append(list_stocks_onboard[0][0])
                elif list_stocks_onboard[0][1] < 4:
                    wanted_stocks.append(list_stocks_onboard[0][0])
            elif tmp_length == 2:
                wanted_stocks.append(list_stocks_onboard[0][0])
                wanted_stocks.append(list_stocks_onboard[1][0])
            elif tmp_length == 3:
                wanted_stocks.append(list_stocks_onboard[0][0])
                wanted_stocks.append(list_stocks_onboard[1][0])
                wanted_stocks.append(list_stocks_onboard[2][0])
            elif tmp_length == 4:
                wanted_stocks.append(list_stocks_onboard[-1][0])
                wanted_stocks.append(list_stocks_onboard[-2][0])
                wanted_stocks.append(list_stocks_onboard[-3][0])
        elif len(intersect_keys) == 1:
            if stocks_onboard_can_get[intersect_keys[0]] >= 4:
                wanted_stocks.append(intersect_keys[0])
                wanted_stocks.append(intersect_keys[0])
            elif stocks_onboard_can_get[intersect_keys[0]] < 4:
                wanted_stocks.append(intersect_keys[0])
        elif len(intersect_keys) == 2:
            wanted_stocks.append(intersect_keys[0])
            wanted_stocks.append(intersect_keys[1])
        elif len(intersect_keys) == 3:
            wanted_stocks.append(intersect_keys[0])
            wanted_stocks.append(intersect_keys[1])
            wanted_stocks.append(intersect_keys[2])
        elif len(intersect_keys) == 4:
            wanted_stocks.append(list_stocks_need[0][0])
            wanted_stocks.append(list_stocks_need[1][0])
            wanted_stocks.append(list_stocks_need[2][0])
        return wanted_stocks
        

    def get_affordable_cards(self, my_board):
        '''
        param:
            my_board(class Board) - get the board from the state
        return:
            a list of cards that the player can get (include upside down cards)
        '''
        card_onboard = my_board.dict_Card_Stocks_Show  # dict
        card_deposit = self.card_upside_down # list
        ret = []
        for item in card_deposit:
            if self.check_get_card(item):
                ret.append(item)
        for key in card_onboard.keys():
            if key != 'Noble':
                for item in card_onboard[key]:
                    if self.check_get_card(item):
                        ret.append(item)
        return ret


    def get_stock_return(self, wanted_stocks, wanted_card):
        '''
        return list of excess stocks
            param:
                wanted_stocks: list of string - stocks that the player wants to take
                wanted_cards: card obj 
            return:
                stocks_return: list of string
        '''
        # get num of excess chips
        my_stocks_dict = copy.deepcopy(self.stocks)
        for item in wanted_stocks:
            # if item in my_stocks_dict.keys():
            my_stocks_dict[item] += 1
        excess = max(0, sum(my_stocks_dict.values()) - 10)
        if excess == 0:
            return []

        # get wanted_card_stocks
        wanted_card_stocks = wanted_card.stocks

        # get list of returnable stocks
        returnable_stocks = {}
        for item in my_stocks_dict:
            if item in wanted_card_stocks and item != 'auto_color':
                returnable_stocks.update({item : max(0, my_stocks_dict[item] - wanted_card_stocks[item])})
        list_returnable_stocks = []
        for key, val in returnable_stocks.items():
            list_returnable_stocks.append([key, val])
        list_returnable_stocks.sort(key=lambda x:x[1], reverse=True)

        # get stocks_return
        ret = []
        if sum(returnable_stocks.values()) >= excess:
            for _ in range(excess):
                ret.append(list_returnable_stocks[0][0])
                list_returnable_stocks[0][1] -= 1
                list_returnable_stocks.sort(key=lambda x:x[1], reverse=True)
        else:
            # get new_returnable_list
            card_stocks_dict = {}
            for key, val in wanted_card_stocks.items():
                if val != 0:
                    card_stocks_dict.update({key : val})
            new_returnable_list = []
            for key in card_stocks_dict:
                if my_stocks_dict[key] != 0:
                    new_returnable_list.append([key, my_stocks_dict[key], card_stocks_dict[key]])
            new_returnable_list.sort(key=lambda x : x[2], reverse=False)

            # get unnecessary type stocks
            unnecessary_stocks = []
            for key in my_stocks_dict:
                if key not in card_stocks_dict and key != 'auto_color' and my_stocks_dict[key] != 0:
                    unnecessary_stocks.append(key)

            #
            if len(unnecessary_stocks) == 0:
                if excess == 1:
                    ret.append(new_returnable_list[0][0])
                elif excess == 2:
                    ret.append(new_returnable_list[0][0])
                    ret.append(new_returnable_list[1][0])
                elif excess == 3:
                    ret.append(new_returnable_list[0][0])
                    ret.append(new_returnable_list[1][0])
                    ret.append(new_returnable_list[2][0])
            elif len(unnecessary_stocks) > 0:
                for type_stock in unnecessary_stocks:
                    if len(ret) < excess:
                        for _ in range(returnable_stocks[type_stock]):
                            ret.append(type_stock)
                new_excess = excess - len(ret)
                if new_excess == 1:
                    ret.append(new_returnable_list[0][0])
                elif new_excess == 2:
                    ret.append(new_returnable_list[0][0])
                    ret.append(new_returnable_list[1][0])
                elif new_excess == 3:
                    ret.append(new_returnable_list[0][0])
                    ret.append(new_returnable_list[1][0])
                    ret.append(new_returnable_list[2][0])
        return ret


    def get_most_viable_unaffordable_card(self, state):
        '''
        return the most viable card
            param: 
                state: dictionary
            return:
                the most viable card (card object), diff value from evaluate_unaffordable_card()
        '''
        board = state['Board']  # board obj
        # affordable_cards = self.get_affordable_cards(board)
        cards_onboard = board.dict_Card_Stocks_Show  # dictionary
        cards_deposit = self.card_upside_down  # list
        list_card = cards_deposit + cards_onboard['I'] + cards_onboard['II'] + cards_onboard['III']
        # list_card = cards_onboard['I'] + cards_onboard['II'] + cards_onboard['III']

        # get unaffordable cards
        unaffordable = []
        for card in list_card:
            # if card not in affordable_cards:
            if not self.check_get_card(card):
                unaffordable.append(card)
        
        if len(unaffordable) != 0:
            unaffordable.sort(key=self.evaluate_unaffordable_card, reverse=True)
            diff = self.evaluate_unaffordable_card(unaffordable[0])
            card_ret = unaffordable[0]
        else:
            card_ret = None
            diff = -1

        return card_ret, diff
        
    
    def get_most_viable_affordable_card(self, affordable_card_list):
        '''
        return the most viable affordable card
            param:
                affordable_card_list: list of card object
            return:
                card obj - the most viable affordable card
        '''
        affordable_card_list.sort(key=self.evaluate_affordable_card, reverse=True)
        return affordable_card_list[0]


    def evaluate_unaffordable_card(self, unaffordable_card):
        '''
        calculate the difference between score of the card and the ultilities
            param:
                unaffordable_card: card obj
            return:
                difference between score of the card and the ultilities
        '''
        needed_stocks = self.get_stocks_need(unaffordable_card)
        # return sum(needed_stocks.values()) - unaffordable_card.score
        return unaffordable_card.score / (sum(needed_stocks.values()) + 0.01)


    def evaluate_affordable_card(self, affordable_card):
        '''
        return the total number of chips needed to buy the affordable_card
            param:
                affordable_card: card obj - the player can afford to buy
            return:
                the total number of chips needed to buy the affordable_card
        '''
        dict_buy = affordable_card.stocks
        chips_buy = {}
        for key in self.stocks_const:
            chips_buy.update({key: max(0, dict_buy[key] - self.stocks_const[key])})
            
        return affordable_card.score / (sum(chips_buy.values()) + 3)


    @staticmethod
    def find_intersection(lst1, lst2):
        # Use of hybrid method
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3
    