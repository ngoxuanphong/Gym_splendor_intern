from ..base.player import Player
import random
from copy import deepcopy
from colorama import Fore, Style

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        action_space = self.get_action_space(state)
        selected_action = random.choice(action_space)
        card_id = selected_action.split('_')[1]
        card_code = self.get_card_code(int(card_id))

        list_card_can_be_got_immediately = self.list_card_can_be_got_immediately(state)
        list_card_can_be_got_in_future = self.list_card_can_be_got_in_future(state)

        card = None
        for car in (list_card_can_be_got_immediately + list_card_can_be_got_in_future):
            if car.id == card_code:
                card = car
                break
        
        # print(Fore.LIGHTYELLOW_EX, selected_action, card.id, card.stocks, end='')
        # print(Style.RESET_ALL)
        
        if selected_action.startswith('Get'):
            return [], card, [], 2
        
        if selected_action.startswith('Upside'):
            stocks_return = []
            if state['Board'].stocks['auto_color'] > 0:
                stocks_return = self.Tim_nl_tra(card, ['auto_color'], state)
            
            # print(Fore.LIGHTYELLOW_EX, stocks_return, end='')
            # print(Style.RESET_ALL)
            return [], card, stocks_return, 3
        
        if selected_action.startswith('Target'):
            stocks_get = self.Tim_nl_lay(card, state)
            stocks_return = self.Tim_nl_tra(card, stocks_get, state)

            # print(Fore.LIGHTYELLOW_EX, stocks_get, stocks_return, end='')
            # print(Style.RESET_ALL)
            return stocks_get, None, stocks_return, 1

        return [], None, []

    def Tim_nl_lay(self, card, state):
        nl_hien_tai = deepcopy(self.stocks)
        dict_nl_thieu_temp = {}
        for mau in card.stocks.keys():
            if nl_hien_tai[mau] + self.stocks_const[mau] < card.stocks[mau]:
                dict_nl_thieu_temp[mau] = card.stocks[mau] - nl_hien_tai[mau] - self.stocks_const[mau]
        
        dict_nl_thieu_temp = dict(sorted(dict_nl_thieu_temp.items(), key=lambda x: x[1], reverse=True))

        temp = [mau for mau in dict_nl_thieu_temp.keys() if state['Board'].stocks[mau] > 0]
        list_nl_lay = []
        if temp.__len__() >= 3:
            if temp.__len__() > 3:
                for i in range(3):
                    temp_ = [state['Board'].stocks[mau] for mau in temp if mau not in list_nl_lay]
                    if temp_.__len__() > 0:
                        list_nl_lay.append(temp[temp_.index(min(temp_))])
                        temp.remove(temp[temp_.index(min(temp_))])
            
                return list_nl_lay
            
            return temp

        if temp.__len__() == 2:
            temp_ = [mau for mau in card.stocks.keys() if state['Board'].stocks[mau] > 0 and mau not in temp]
            temp__ = [state['Board'].stocks[mau] for mau in temp_]
            if temp__.__len__() > 0:
                temp.append(temp_[temp__.index(min(temp__))])

            return temp
        
        if temp.__len__() == 1:
            if dict_nl_thieu_temp[temp[0]] >=2 and state['Board'].stocks[temp[0]] > 3:
                return [temp[0], temp[0]]
        
            for i in range(2):
                board_stocks = deepcopy(state['Board'].stocks)
                temp_ = [mau for mau in card.stocks.keys() if state['Board'].stocks[mau] > 0 and mau not in temp]
                temp__ = [board_stocks[mau] for mau in temp_]
                if temp__.__len__() > 0:
                    temp.append(temp_[temp__.index(min(temp__))])
            
            return temp
        
        return []

    def Tim_nl_tra(self, card, stocks_get, state):
        nl_hien_tai = deepcopy(self.stocks)
        for i in stocks_get:
            nl_hien_tai[i] += 1

        snl = sum(list(nl_hien_tai.values()))
        if snl <= 10:
            return []

        list_stock_return = []
        nl_thua = snl - 10
        dict_nl_thua_temp = {}
        if card != None:
            for mau in card.stocks.keys():
                if nl_hien_tai[mau] + self.stocks_const[mau] > card.stocks[mau] and nl_hien_tai[mau] > 0:
                    dict_nl_thua_temp[mau] = min(nl_hien_tai[mau], nl_hien_tai[mau] + self.stocks_const[mau] - card.stocks[mau])

            for i in range(nl_thua):
                temp = [mau for mau in dict_nl_thua_temp.keys() if dict_nl_thua_temp[mau] > 0]
                temp_ = [state['Board'].stocks[mau] for mau in temp]
                if temp_.__len__() > 0:
                    mau_ = temp[temp_.index(max(temp_))]
                    dict_nl_thua_temp[mau_] -= 1
                    nl_hien_tai[mau_] -= 1
                    list_stock_return.append(mau_)
            
            if list_stock_return.__len__() != nl_thua:
                nl_tra = nl_thua - list_stock_return.__len__()
                nl_hien_tai.pop('auto_color')
                for i in range(nl_tra):
                    temp = [mau for mau in nl_hien_tai.keys() if nl_hien_tai[mau] > 0]
                    temp_ = [state['Board'].stocks[mau] for mau in temp]
                    mau_ = temp[temp_.index(max(temp_))]
                    nl_hien_tai[mau_] -= 1
                    list_stock_return.append(mau_)
                    break

        else:
            nl_hien_tai.pop('auto_color')
            for i in range(nl_thua):
                temp = [mau for mau in nl_hien_tai.keys() if nl_hien_tai[mau] > 0]
                temp_ = [state['Board'].stocks[mau] for mau in temp]
                mau_ = temp[temp_.index(max(temp_))]
                nl_hien_tai[mau_] -= 1
                list_stock_return.append(mau_)
                break

        return list_stock_return

    def get_action_space(self, state):
        list_card_can_be_got_immediately = self.list_card_can_be_got_immediately(state)
        immediately_card_id = [self.get_card_id(card.id) for card in list_card_can_be_got_immediately]
        immediately_card_id.sort()
        list_action_get_card = ['Get_' + str(_id) for _id in immediately_card_id]

        list_card_can_be_got_in_future = self.list_card_can_be_got_in_future(state)
        future_card_id = [self.get_card_id(card.id) for card in list_card_can_be_got_in_future]
        future_card_id.sort()
        list_action_target_card = ['Target_' + str(_id) for _id in future_card_id]

        list_action_upside_card = []
        if self.card_upside_down.__len__() < 3:
            upside_card_id = [self.get_card_id(card.id) for card in list_card_can_be_got_in_future if card not in self.card_upside_down]
            upside_card_id.sort()
            list_action_upside_card = ['Upside_' + str(_id) for _id in upside_card_id]

        return list_action_get_card + list_action_target_card + list_action_upside_card

    def list_card_can_be_got_in_future(self, state):
        list_card_check = []
        for card in self.card_upside_down:
            if not self.check_get_card(card):
                list_card_check.append(card)
        
        for type_card in state['Board'].dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(card):
                        list_card_check.append(card)
        
        temp = ["red", "blue", "green", "white", "black"]
        list_return = []
        for card in list_card_check:
            stock_const_thieu = {}
            for color in temp:
                stock_const_thieu[color] = max(0, card.stocks[color] - self.stocks_const[color])
            
            if sum(stock_const_thieu.values()) <= 10:
                list_return.append(card)

        return list_return

    def list_card_can_be_got_immediately(self, state):
        list_return = []
        for card in self.card_upside_down:
            if self.check_get_card(card):
                list_return.append(card)
        
        for type_card in state['Board'].dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_return.append(card)

        return list_return

    def get_card_code(self, _int):
        if _int <= 39:
            return 'I_' + str(_int+1)
        elif _int <= 69:
            return 'II_' + str(_int-39)
        elif _int <= 89:
            return 'III_' + str(_int-69)
        else:
            return 'Noble_' + str(_int-89)

    def get_card_id(self, _str):
        temp = _str.split('_')
        temp_ = [-1,39,69,89]
        temp__ = ['I', 'II', 'III', 'Noble']
        return int(temp[1]) + temp_[temp__.index(temp[0])]