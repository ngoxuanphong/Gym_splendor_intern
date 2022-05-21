from ..base.player import Player
import random
from copy import deepcopy
import math

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        board = state['Board']
        thecothelay = self.list_card_can_buy(board)
        nguyenlieucothelay2 = self.listnguyenlieulay2(board)
        nguyenlieucon = self.listnguyenlieucon(board)

        if len(thecothelay) > 0:
            list_card_value = []
            for card in thecothelay:
                if card.score > 1:
                    card_value = card.score/self.price_card(card)
                    list_card_value.append([card, card_value])
            
            if len(list_card_value) > 0:
                card_get = list_card_value[0][0]
                card_value = list_card_value[0][1]
                for item in list_card_value:
                    if item[1] > card_value:
                        card_get = item[0]
                        card_value = item[1]

                return [], card_get, []
            
            if 1:
                
                thecothelay = self.get_card_to_get_noble(board)
                if thecothelay != None:
                    for card in thecothelay:
                        if card.score == 0:
                            card_value = math.sqrt(sum(list(card.stocks.values())) + 1.78)
                            list_card_value.append([card, card_value])
                        elif card.score > 0:
                            card_value = sum(list(card.stocks.values()))/card.score
                            list_card_value.append([card, card_value])
                    
                    card_get = list_card_value[0][0]
                    card_value = list_card_value[0][1]
                    for item in list_card_value:
                        if item[1] < card_value:
                            card_get = item[0]
                            card_value = item[1]

                    return [], card_get, []

                if 1:
                    thecothelay = self.list_card_can_buy(board)
                    for card in thecothelay:
                        if card.score == 0:
                            card_value = math.sqrt(sum(list(card.stocks.values())) + 1.78)
                            list_card_value.append([card, card_value])
                        else:
                            card_value = sum(list(card.stocks.values()))/card.score
                            list_card_value.append([card, card_value])
                    
                    card_get = list_card_value[0][0]
                    card_value = list_card_value[0][1]
                    for item in list_card_value:
                        if item[1] < card_value:
                            card_get = item[0]
                            card_value = item[1]
                    
                    return [], card_get, []

        if sum(list(self.stocks.values())) <= 7:   
            dict_token_important = self.get_important_token(board)
            if len(dict_token_important) >= 3:
                stocks_get = [list(dict_token_important.keys())[0], list(dict_token_important.keys())[1], list(dict_token_important.keys())[2]]
                # print(stocks_get, '1111')
                return stocks_get, None, []
            
            if len(dict_token_important) > 0 and len(nguyenlieucothelay2) > 0:
                for token in list(dict_token_important.keys()):
                    if token not in nguyenlieucothelay2:
                        del dict_token_important[token]
                type_card = list(dict_token_important.keys())[0]
                value = list(dict_token_important.values())[0]
                for typecard in list(dict_token_important.keys()):
                    if board.stocks[typecard] > 3:
                        stocks_get = [typecard, typecard]
                        # print(stocks_get, '2222')
                        return stocks_get, None, []
            
            if 1:
                dict_token_choose = self.get_Three_Most_Token(board)
                for token in list(dict_token_choose.keys()):
                    if token not in nguyenlieucon:
                        del dict_token_choose[token]
                
                if len(dict_token_choose) >= 3:
                    stocks_get = [list(dict_token_choose.keys())[0], list(dict_token_choose.keys())[1], list(dict_token_choose.keys())[2]]
                    # print(stocks_get, '3333')
                    return stocks_get, None, []

                if 1:
                    if len(nguyenlieucothelay2) > 0:
                        dict_token_choose_keys = list(dict_token_choose.keys()).copy()
                        for token in list(dict_token_choose_keys):
                            if token not in nguyenlieucothelay2:
                                del dict_token_choose[token]

                    if len(dict_token_choose) > 0 and board.stocks[list(dict_token_choose.keys())[0]] > 3:
                        stocks_get = [list(dict_token_choose.keys())[0], list(dict_token_choose.keys())[0]]
                        # print(stocks_get, '4444')
                        return stocks_get, None, []
                    
                    if 1:
                        card = self.get_card_value(board)
                        if self.check_get_card(card):
                            return [], card, [], 3

        if sum(list(self.stocks.values())) <= 7:
            if sum(self.stocks.values()) < 9:
                dict_token_important = self.get_important_token(board)
                if len(dict_token_important) > 0:
                    for token in list(dict_token_important.keys()):
                        if token not in nguyenlieucothelay2:
                            del dict_token_important[token]
                if len(dict_token_important) > 0:
                    type_card = list(dict_token_important.keys())[0]
                    value = list(dict_token_important.values())[0]
                    for typecard in list(dict_token_important.keys()):
                        if board.stocks[typecard] > 3:
                            stocks_get = [typecard, typecard]
                            # print(stocks_get, '5555')
                            return stocks_get, None, []

                card = self.get_card_value(board)
                if self.check_get_card(card):
                    return [], card, [], 3

            if sum(self.stocks.values()) == 9:
                card = self.get_card_value(board)
                if self.check_get_card(card):
                    return [], card, [], 3

                dict_token_important = self.get_important_token(board)
                if len(dict_token_important) > 0 and len(nguyenlieucothelay2) > 0 :
                    for token in list(dict_token_important.keys()):
                        if token not in nguyenlieucothelay2:
                            del dict_token_important[token]
                    
                    if len(dict_token_important) > 0:
                        list_token = list(dict_token_important.keys())
                        stocks_get = [list_token[0], list_token[0]]
                        stocks_return = self.Luachonbothe(board, stocks_get)
                        # print(stocks_get, stocks_return, '6666')
                        return stocks_get, None, stocks_return
                    if 1:
                        dict_token_important = self.get_important_token(board)
                        for token in list(dict_token_important.keys()):
                            if token not in nguyenlieucon:
                                del dict_token_important[token]
                        if len(dict_token_important) > 2:
                            stocks_get = [list(dict_token_important.keys())[0], list(dict_token_important.keys())[1], list(dict_token_important.keys())[2]]
                            stocks_return = self.Luachonbothe(board, stocks_get)
                            # print(stocks_get, stocks_return, '6666')
                            return stocks_get, None, stocks_return
        
            else:
                stocks_return = []
                if board.stocks['auto_color'] > 0:
                    stocks_return = self.Luachonbothe(board, ['auto_color'])
                card = self.get_card_value(board)
                if self.check_get_card(card):
                    # print(stocks_return)
                    return [], card, stocks_return, 3

        stocks = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        
        if stocks.__len__() > 0:
            # print(stocks, 'mmmm')
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
        
        if stocks.__len__() > 0:
            # print(stocks, stocks_return, 'nnnn')
            return stocks, None, stocks_return

        card = self.Tim_the_up(state['Board'])
        if card != None:
            stocks_return = []
            if state['Board'].stocks['auto_color'] > 0:
                stocks_return = self.Luachonbothe(state['Board'], ['auto_color'])
            
            # print(card.stocks, card.score, stocks_return, 'oooo')
            return [], card, stocks_return, 3
        


        # print(self.card_upside_down.__len__(), 'pppp')
        return [], None, []

    def NLcan(self, board):
        NL_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        NL_can = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for lnl in self.stocks.keys():
            if lnl != "auto_color":
                for the in self.card_upside_down:
                    NL_the_up[lnl] += the.stocks[lnl]
                NL_can[lnl] = NL_the_up[lnl] - self.stocks_const[lnl]
        return NL_can

    def Tranguyenlieu(self, board):
        listthebo = []
        dictnguyenlieuthua = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        nguyen_lieu_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}

        for lnl in dictnguyenlieuthua.keys():
            Nlcan = self.NLcan(board)
            if self.stocks[lnl] > 0:
                dictnguyenlieuthua[lnl] = self.stocks[lnl] - Nlcan[lnl]

        SXNL_thua= dict(sorted(dictnguyenlieuthua.items(), key=lambda x:x[1], reverse=True))
        for lnl in SXNL_thua.keys():
            listthebo.append(lnl)
        SXNLcan = dict(sorted(Nlcan.items(), key=lambda x:x[1], reverse=False))
        for lnl in SXNLcan.keys():
            if self.stocks[lnl] > 0  and (lnl not in list(SXNL_thua.keys())):
                listthebo.append(lnl)
        return listthebo

    def Luachonbothe(self, board, args):
        dict_bo = {
            "red": 0,
            "blue": 0,
            "white": 0,
            "green": 0,
            "black": 0,
            "auto_color": 0
        }
        dict_bd = self.stocks.copy()
        for x in args:
            dict_bd[x] += 1
        Tranguyenlieu = self.Tranguyenlieu(board)
        danhsachcon = Tranguyenlieu
        if sum(dict_bd.values()) > 10:
            n = sum(dict_bd.values()) - 10
            i = 0
            while n != 0:
                if dict_bd[danhsachcon[i]] != 0:
                    dict_bo[danhsachcon[i]] += 1
                    dict_bd[danhsachcon[i]] -= 1
                    n -= 1
                else:
                    i += 1

        list_bo = []
        for key in dict_bo.keys():
            while dict_bo[key] > 0:
                list_bo.append(key)
                dict_bo[key] -= 1
        return list_bo

    def Tim_the_up(self, board):
        list_card_can_check = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    list_card_can_check.append(car)

        if len(list_card_can_check) != 0:
            card = self.chon_the_gia_tri_cao(list_card_can_check)
            return card
        
        return None

    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

    def price_card(self, card):
        price = 0
        for typestock in list(card.stocks.keys()):
            price += card.stocks[typestock] - self.stocks_const[typestock]
        if price <= 0:
            return 0.1
        return price

    def get_Three_Most_Token(self, board):
        token_can_get = self.list_token_can_get(board)
        dict_most_token = {}
        dict_most_token['red'] = 0
        dict_most_token['blue'] = 0
        dict_most_token['green'] = 0
        dict_most_token['white'] = 0
        dict_most_token['black'] = 0
        list_type = ['III', 'II', 'I']
        #xác định 3 nguyên liệu phổ biến nhất
        for i in list_type:
            for card in board.dict_Card_Stocks_Show[i]:
                dict_most_token['red'] += card.stocks['red'] - self.stocks_const['red']
                dict_most_token['blue'] += card.stocks['blue'] - self.stocks_const['blue']
                dict_most_token['green'] += card.stocks['green'] - self.stocks_const['green']
                dict_most_token['white'] += card.stocks['white'] - self.stocks_const['white']
                dict_most_token['black'] += card.stocks['black'] - self.stocks_const['black']

        list_token = list(dict_most_token.keys())
        list_number_token = list(dict_most_token.values())
        dict_token_choose = {}
        count = 0

        while count < len(list_token):
            count += 1
            # for token in list_token:
            # if list_token[list_number_token.index(max(list_number_token))] in token_can_get:
            dict_token_choose[list_token[list_number_token.index(max(list_number_token))]] = max(list_number_token)
            
            list_token.remove(list_token[list_number_token.index(max(list_number_token))])
            list_number_token.remove(max(list_number_token))
        return dict_token_choose

    def get_card_to_get_noble(self, board):
        dict_important_card = {}
        dict_important_card['red'] = 0
        dict_important_card['blue'] = 0
        dict_important_card['green'] = 0
        dict_important_card['white'] = 0
        dict_important_card['black'] = 0
        dict_card_value = {}
        thecothelay = self.list_card_can_buy(board)
        target_noble = []
        #tính xem với các thẻ noble thì cần mua thêm bao nhiêu thẻ các loại để lấy được thẻ noble
        for card in board.dict_Card_Stocks_UpsiteDown['Noble']:
            dict_card_to_get = {}
            for type_card in card.stocks.keys():
                dict_card_to_get[type_card] = max(card.stocks[type_card] - self.stocks_const[type_card] , 0)
            if sum(list(dict_card_to_get.values())) > 2:
                continue
            else:
                dict_card_value[card] = dict_card_to_get
                target_noble.append(sum(list(dict_card_to_get.values())))
        #chỉ hướng đến các thẻ noble còn thiếu dưới 3 thẻ
        list_card_noble = list(dict_card_value.keys())
        noble_should_get = []
        while len(target_noble) > 0:
            index_card = target_noble.index(min(target_noble))
            noble_should_get.append(list_card_noble[index_card])
            target_noble.remove(min(target_noble))
            list_card_noble.remove(list_card_noble[index_card])
        if len(noble_should_get) > 0:
            list_card_should_get = []
            for the in thecothelay:
                if the.type_stock in list(dict_card_value[noble_should_get[0]].keys()):
                    list_card_should_get.append(the)

            return list_card_should_get

    def token_of_player(self, board):
        token_of_player = []
        for token in list(self.stocks.keys()):
            if self.stocks[token] > 0:
                token_of_player.append(token)

        return token_of_player
    
    def get_token_return(self, board, number_bo):
        '''
        #note: nếu đã úp thẻ thì trả token mà có ít tác dụng nhất trong việc lật thẻ, còn nếu chưa úp thẻ thì
        trả token kém phổ biến nhất trong các thẻ đang lật trên bàn chơi
        '''
        dict_token_not_important = {}
        token_can_return = self.token_of_player(board)
        count = 0
        bo = {}
        
        if len(self.card_upside_down) > 0:
            dict_important_token = {}
            dict_important_token['red'] = 0
            dict_important_token['blue'] = 0
            dict_important_token['green'] = 0
            dict_important_token['white'] = 0
            dict_important_token['black'] = 0
            for card in self.card_upside_down:
                dict_important_token['red'] += card.stocks['red'] - self.stocks_const['red'] - self.stocks['red']
                dict_important_token['blue'] += card.stocks['blue'] - self.stocks_const['blue'] - self.stocks['blue']
                dict_important_token['green'] += card.stocks['green'] - self.stocks_const['green'] - self.stocks['green']
                dict_important_token['white'] += card.stocks['white'] - self.stocks_const['white'] - self.stocks['white']
                dict_important_token['black'] += card.stocks['black'] - self.stocks_const['black'] - self.stocks['black']
            list_token = list(dict_important_token.keys())
            list_number_token = list(dict_important_token.values())
            
            while count < len(list_token):
                count += 1
                if list_token[list_number_token.index(min(list_number_token))] in token_can_return:
                    dict_token_not_important[list_token[list_number_token.index(min(list_number_token))]] = min(list_number_token)
                list_token.remove(list_token[list_number_token.index(min(list_number_token))])
                list_number_token.remove(min(list_number_token))
        else:
            dict_most_token = self.get_Three_Most_Token(board)
            list_token = list(dict_most_token.keys())
            list_number_token = list(dict_most_token.values())
            while count < len(list_token):
                count += 1
                if list_token[list_number_token.index(min(list_number_token))] in token_can_return:
                    dict_token_not_important[list_token[list_number_token.index(min(list_number_token))]] = min(list_number_token)
                list_token.remove(list_token[list_number_token.index(min(list_number_token))])
                list_number_token.remove(min(list_number_token))
        
        list_value = list(dict_token_not_important.values())
        list_type_token = list(dict_token_not_important.keys())
    
        list_token_return = []
        count = 0
        while count < len(dict_token_not_important):
            count += 1
            min_value = min(list_value)
            list_token_return.append(list_type_token[list_value.index(min_value)])
            list_type_token.remove(list_type_token[list_value.index(min_value)])
            list_value.remove(min_value)
        so_bo = 0
    
        index = 0
        while so_bo < number_bo:
            if self.stocks[list_token_return[index]] > 0:
                bo[list_token_return[index]] = 1
                so_bo += 1
            index += 1
        # for nguyenlieu in list_token_return:
        #     if player_04.stocks[nguyenlieu] > 0:
        #         bo[nguyenlieu] = 1
        #         break
        # return dict_token_not_important
        return bo

    def target_card(self, board):
        list_card23 = board.dict_Card_Stocks_Show['III'] + board.dict_Card_Stocks_Show['II']
        list_target_card = []

        for card in list_card23:
            sum = 0
            for token in list(card.stocks.keys()):
                sum += max(card.stocks[token] - self.stocks[token] - self.stocks_const[token], 0)
            
            if sum < 2:
                list_target_card.append(card)

        return list_target_card

    def get_important_token(self, board):
        token_can_get = self.list_token_can_get(board)
        dict_important_token = {}
        dict_important_token['red'] = 0
        dict_important_token['blue'] = 0
        dict_important_token['green'] = 0
        dict_important_token['white'] = 0
        dict_important_token['black'] = 0
        for card in list(self.card_upside_down + self.target_card(board)):
            dict_important_token['red'] += card.stocks['red'] - self.stocks_const['red'] - self.stocks['red']
            dict_important_token['blue'] += card.stocks['blue'] - self.stocks_const['blue'] - self.stocks['blue']
            dict_important_token['green'] += card.stocks['green'] - self.stocks_const['green'] - self.stocks['green']
            dict_important_token['white'] += card.stocks['white'] - self.stocks_const['white'] - self.stocks['white']
            dict_important_token['black'] += card.stocks['black'] - self.stocks_const['black'] - self.stocks['black']
        list_token = list(dict_important_token.keys())
        list_number_token = list(dict_important_token.values())
        dict_token_important = {}
        count = 0
        while count < len(list_token):
            if list_token[list_number_token.index(max(list_number_token))] in token_can_get:
                dict_token_important[list_token[list_number_token.index(max(list_number_token))]] = max(list_number_token)
            list_token.remove(list_token[list_number_token.index(max(list_number_token))])
            list_number_token.remove(max(list_number_token))
        return dict_token_important

    def get_card_value(self, board):
        dict_card_value = {}
        list_card_process = []
        list_card_get = []
        list_type_card = ['III', 'II', 'I']
        for type_card in list_type_card:
            for card in list(board.dict_Card_Stocks_Show[type_card]):
                if card.score == 0:
                    list_card_process.append(card)
                    sum = 1
                    for token in list(card.stocks.keys()):
                        if card.stocks[token] - self.stocks[token] - self.stocks_const[token]  > 0:
                            sum += card.stocks[token] - self.stocks[token] - self.stocks_const[token]
                        else:
                            sum += 0
                    
                    dict_card_value[card.id] = math.sqrt(sum+3)
                else:
                    sum = 1
                    list_card_process.append(card)
                    for token in card.stocks.keys():
                        if card.stocks[token] - self.stocks[token] - self.stocks_const[token] > 0:
                            sum += card.stocks[token]- self.stocks[token] - self.stocks_const[token]
                        else:
                            sum += 0
                    dict_card_value[card] = sum/card.score
        dict_card_process = {}
        values = list(dict_card_value.values())
        count = 0
        list_card = list_card_process
        while count < len(list_card_process):
            count += 1
            list_card_get.append(list_card_process[values.index(min(values))])
            list_card.remove(list_card[values.index(min(values))])
            values.remove(min(values))    
        return list_card_get[0]

    def list_card_can_buy(self, board):
        thecothelay = []
        if len(self.card_upside_down) > 0:
            for the in self.card_upside_down:
                if self.check_get_card(the) == True:
                    thecothelay.append(the)
        for the in board.dict_Card_Stocks_Show["III"]:
            if self.check_get_card(the) == True:
                thecothelay.append(the)
        for the in board.dict_Card_Stocks_Show["II"]:
            if self.check_get_card(the) == True:
                thecothelay.append(the)
        for the in board.dict_Card_Stocks_Show["I"]:
            if self.check_get_card(the) == True:
                thecothelay.append(the)
        return thecothelay

    def listnguyenlieulay2(self, board):
        nguyenlieucothelay2 = []
        for nguyenlieu in board.stocks.keys():
            if nguyenlieu != "auto_color" and board.stocks[nguyenlieu] > 3:
                nguyenlieucothelay2.append(nguyenlieu)
        return nguyenlieucothelay2

    def listnguyenlieucon(self, board):
        nguyenlieucon = []
        for nguyenlieu in board.stocks.keys():
            if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
                nguyenlieucon.append(nguyenlieu)
        return nguyenlieucon

    def target_noble_card(self, board):
        list_noble_card = board.dict_Card_Stocks_Show['Noble']
        dict_card_value = {}
        for card in list_noble_card:
            dict_thieu = {}
            for type_card in card.stocks.keys():
                if self.stocks_const[type_card] > card.stocks.keys():
                    dict_thieu[type_card] = 0
                else:
                    dict_thieu[type_card] = card.stocks.keys() - self.stocks_const[type_card]
            dict_card_value[card] = sum(list(dict_thieu.values()))

    def list_token_can_get(self, board):
        nguyenlieucon = []
        for nguyenlieu in board.stocks.keys():
            if board.stocks[nguyenlieu] > 0 and nguyenlieu != "auto_color":
                nguyenlieucon.append(nguyenlieu)
        return nguyenlieucon