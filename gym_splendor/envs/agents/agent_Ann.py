from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        dict_the_lay_ngay = self.dict_the_lay_ngay_func(state['Board'])
        mau_the_quan_trong = self.mau_the_quan_trong_func(state['Board'])

        sl_the_lay_ngay = sum([dict_the_lay_ngay[mau].__len__() for mau in dict_the_lay_ngay.keys()])
        if sl_the_lay_ngay != 0:
            for sub_list in mau_the_quan_trong:
                for mau in sub_list:
                    if dict_the_lay_ngay[mau].__len__() != 0:
                        card = self.chon_the_gia_tri_cao(dict_the_lay_ngay[mau])

                        # print('1111')
                        return [], card, []
            
            list_the_lay_ngay = []
            for mau in dict_the_lay_ngay.keys():
                if dict_the_lay_ngay[mau].__len__() != 0:
                    list_the_lay_ngay += dict_the_lay_ngay[mau]

            card = self.chon_the_gia_tri_cao(list_the_lay_ngay)
            if card.score > 0:

                # print('2222')
                return [], card, []
        
        list_co_the_lay = self.the_co_the_lay_func(state['Board'], mau_the_quan_trong)
        if list_co_the_lay.__len__() != 0:
            target = list_co_the_lay[0]
            stocks = []
            mau_target_thieu = [mau for mau in target['nl_thieu'].keys() if mau != 'auto_color' and target['nl_thieu'][mau] != 0]

            if mau_target_thieu.__len__() == 1:
                if target['nl_thieu'][mau_target_thieu[0]] >= 2 and state['Board'].stocks[mau_target_thieu[0]] >= 4:
                    stocks = [mau_target_thieu[0], mau_target_thieu[0]]
                    stocks_return = self.Tim_nl_tra(target['the'], stocks)
                    
                    nl_trung_nhau = list(set(stocks) & set(stocks_return))
                    for i in nl_trung_nhau:
                        stocks.remove(i)
                        stocks_return.remove(i)
                    
                    # print('3333')
                    return stocks, None, stocks_return
            
            temp_list_abcxyz = []
            for ele in list_co_the_lay:
                for mau in ele['the'].stocks.keys():
                    if ele['nl_thieu'][mau] != 0 and mau not in temp_list_abcxyz:
                        temp_list_abcxyz.append(mau)
            
            if temp_list_abcxyz.__len__() <= 3:
                stocks = deepcopy(temp_list_abcxyz)
            else:
                while stocks.__len__() < 3:
                    mau_choice = random.choice(temp_list_abcxyz)
                    stocks.append(mau_choice)
                    temp_list_abcxyz.remove(mau_choice)
            
            if stocks.__len__() == 3:
                stocks_return = self.Tim_nl_tra(target['the'], stocks)

                nl_trung_nhau = list(set(stocks) & set(stocks_return))
                for i in nl_trung_nhau:
                    stocks.remove(i)
                    stocks_return.remove(i)
                
                # print('4444')
                return stocks, None, stocks_return

            nn = 3 - stocks.__len__()
            for i in range(nn):
                temp_list_mau = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
                if temp_list_mau.__len__() != 0:
                    mau_choice = random.choice(temp_list_mau)
                    stocks.append(mau_choice)

            stocks_return = self.Tim_nl_tra(target['the'], stocks)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            
            # print('5555')
            return stocks, None, stocks_return

        if  (state['Board'].stocks['auto_color'] > 0 and self.card_upside_down.__len__() < 3) or (self.card_upside_down.__len__() < 3 and sum(state['Board'].stocks.values()) == state['Board'].stocks['auto_color']):
            card_up = self.Tim_the_up(state['Board'], mau_the_quan_trong)
            stocks_return = []
            if card_up != None:
                stocks_return = self.Tim_nl_tra(card_up, ['auto_color'])

                # print('6666')
                return [], card_up, stocks_return
        
        stocks = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        
        if stocks.__len__() > 0:
            # print('7777')
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
        
        # print('8888')
        return stocks, None, stocks_return

    def Tim_the_up(self, board, mau_the_quan_trong):
        list_card_can_check = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        list_card_can_check.append(car)
        
        list_check_1 = []
        for mau in mau_the_quan_trong[0]:
            for car in list_card_can_check:
                if car.type_stock == mau:
                    list_check_1.append(car)
        
        list_check_1_2 = []
        for mau in mau_the_quan_trong[1]:
            for car in list_card_can_check:
                if car.type_stock == mau:
                    list_check_1_2.append(car)
        
        list_check_2 = [car for car in list_card_can_check if car not in (list_check_1+list_check_1_2)]

        list_check = [list_check_1, list_check_1_2, list_check_2]
        for i in range(3):
            if list_check[i].__len__() != 0:
                card = self.chon_the_gia_tri_cao(list_check[i])
                return card

        return None

    def Tim_nl_tra(self, card, stocks):
        nl_hien_tai = deepcopy(self.stocks)
        for i in stocks:
            nl_hien_tai[i] += 1
        
        snl = sum(list(nl_hien_tai.values()))
        if snl <= 10:
            return []

        list_stock_return = []
        nl_thua = snl - 10

        dict_nl_thua_temp = {}
        for mau in card.stocks.keys():
            if nl_hien_tai[mau] + self.stocks_const[mau] > card.stocks[mau] and nl_hien_tai[mau] > 0:
                dict_nl_thua_temp[mau] = min(nl_hien_tai[mau], nl_hien_tai[mau] + self.stocks_const[mau] - card.stocks[mau])

        dict_nl_thua = {k:v for k,v in sorted(dict_nl_thua_temp.items(), key = lambda item: item[1], reverse=True)}
        for i in range(nl_thua):
            for mau in dict_nl_thua.keys():
                if dict_nl_thua[mau] != 0:
                    dict_nl_thua[mau] -= 1
                    nl_hien_tai[mau] -= 1
                    dict_nl_thua_temp = deepcopy(dict_nl_thua)
                    dict_nl_thua = {k:v for k,v in sorted(dict_nl_thua_temp.items(), key = lambda item: item[1], reverse=True)}
                    list_stock_return.append(mau)
                    break
        
        if list_stock_return.__len__() != nl_thua:
            nl_hien_tai.pop('auto_color')
            nl_tra_them = nl_thua - list_stock_return.__len__()
            for i in range(nl_tra_them):
                a = max(nl_hien_tai.values())
                for mau in nl_hien_tai.keys():
                    if nl_hien_tai[mau] == a:
                        nl_hien_tai[mau] -= 1
                        list_stock_return.append(mau)
                        break
        
        return list_stock_return

    def the_co_the_lay_func(self, board, mau_the_quan_trong):
        list_card_can_check = []
        for car in self.card_upside_down:
            if not self.check_get_card(car):
                list_card_can_check.append(car)

        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        list_card_can_check.append(car)
        
        list_check_1 = []
        for mau in mau_the_quan_trong[0]:
            for car in list_card_can_check:
                if car.type_stock == mau:
                    list_check_1.append(car)
        
        list_check_1_2 = []
        for mau in mau_the_quan_trong[1]:
            for car in list_card_can_check:
                if car.type_stock == mau:
                    list_check_1_2.append(car)
        
        list_check_2 = [car for car in list_card_can_check if car not in (list_check_1+list_check_1_2)]
        
        temp = ["red", "blue", "green", "white", "black"]
        list_thu_nhat = []
        for car in (list_check_1+list_check_1_2+list_check_2):
            nl_vc_thieu = {}
            for mau in temp:
                nl_vc_thieu[mau] = max(0, car.stocks[mau] - self.stocks_const[mau])
            
            if sum(nl_vc_thieu.values()) > 10:
                continue

            nl_thieu = {}
            nl_thieu['auto_color'] = 0
            for mau in temp:
                nl_thieu[mau] = max(0, car.stocks[mau] - self.stocks_const[mau] - self.stocks[mau])

            if self.stocks['auto_color'] != 0:
                a = self.stocks['auto_color']
                for i in range(a):
                    loai_nl_thieu = [mau for mau in temp if nl_thieu[mau] > 0]
                    dict_temp = {}
                    for mau in loai_nl_thieu:
                        if board.stocks[mau] == 0:
                            dict_temp[mau] = -10 - nl_thieu[mau]
                        else:
                            dict_temp[mau] = board.stocks[mau] - nl_thieu[mau]

                    dict_tempp = {k:v for k,v in sorted(
                        dict_temp.items(), key=lambda item:item[1], reverse=False
                    )}

                    nl_thieu[list(dict_tempp.keys())[0]] -= 1

            loai_mau_thieu = [mau for mau in temp if nl_thieu[mau] > 0]
            list_board_nl = [mau for mau in temp if board.stocks[mau] > 0]
            list_temp = list(set(loai_mau_thieu) & set(list_board_nl))
            if list_temp.__len__() > 0:
                list_thu_nhat.append({
                    'the': car,
                    'nl_thieu': nl_thieu
                })

        list_check_11 = [ele for ele in list_thu_nhat if ele['the'] in list_check_1]
        list_check_11_2 = [ele for ele in list_thu_nhat if ele['the'] in list_check_1_2]
        list_check_22 = [ele for ele in list_thu_nhat if ele not in (list_check_11+list_check_11_2)]
        list_check_11.sort(key = lambda a: sum(a['nl_thieu'].values()))
        list_check_11_2.sort(key = lambda a: sum(a['nl_thieu'].values()))
        list_check_22.sort(key = lambda a: sum(a['nl_thieu'].values()))

        list_thu_hai = list_check_11 + list_check_11_2 + list_check_22
        for ele in list_thu_hai:
            for mau in temp:
                if mau not in list_board_nl:
                    ele['nl_thieu'][mau] = 0

        return list_thu_hai

    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

    def mau_the_quan_trong_func(self, board):
        if board.dict_Card_Stocks_Show['Noble'].__len__() == 0:
            return [[], []]

        temp = ["red", "blue", "green", "white", "black"]

        sl_bien = {}
        for mau in temp:
            list_temp = [car.stocks[mau] for car in board.dict_Card_Stocks_Show['Noble']]
            max_ = max(list_temp)
            if max_ > 0:
                sl_bien[mau] = max_

        mau_dat_sl_bien = []
        for mau in sl_bien.keys():
            if self.stocks_const[mau] >= sl_bien[mau]:
                mau_dat_sl_bien.append(mau)
        
        if mau_dat_sl_bien.__len__() == 0:
            mau_can_lay_1 = list(sl_bien.keys())
            mau_can_lay_2 = []
        elif mau_dat_sl_bien.__len__() == 1:
            mau_can_lay_1 = []
            for car in board.dict_Card_Stocks_Show['Noble']:
                if car.stocks[mau_dat_sl_bien[0]] != 0:
                    for mau in temp:
                        if mau not in (mau_dat_sl_bien + mau_can_lay_1) and car.stocks[mau] > 0:
                            mau_can_lay_1.append(mau)
            
            mau_can_lay_2 = [mau for mau in sl_bien.keys() if mau not in (mau_dat_sl_bien + mau_can_lay_1)]
        else:
            mau_can_lay_1 = []
            a = mau_dat_sl_bien.__len__()
            for i in range(a):
                for j in range(i+1,a):
                    mau1 = mau_dat_sl_bien[i]
                    mau2 = mau_dat_sl_bien[j]
                    for car in board.dict_Card_Stocks_Show['Noble']:
                        if car.stocks[mau1] != 0 and car.stocks[mau2] != 0:
                            for mau in temp:
                                if mau not in (mau_dat_sl_bien + mau_can_lay_1) and car.stocks[mau] > 0:
                                    mau_can_lay_1.append(mau)
                    
            mau_can_lay_2 = [mau for mau in sl_bien.keys() if mau not in (mau_dat_sl_bien + mau_can_lay_1)]

        mau_can_lay_1_sorted = self.sap_xep_mau_func(mau_can_lay_1, sl_bien)
        mau_can_lay_2_sorted = self.sap_xep_mau_func(mau_can_lay_2, sl_bien)

        mau_quan_trong = [mau_can_lay_1_sorted, mau_can_lay_2_sorted]
        return mau_quan_trong

    def sap_xep_mau_func(self, list_mau, sl_bien):
        if list_mau.__len__() == 0:
            return []

        dict_mau = {}
        for mau in list_mau:
            dict_mau[mau] = sl_bien[mau] - self.stocks_const[mau]
        
        dict_mau_sorted = {a:b for a,b in sorted(
            dict_mau.items(), key=lambda item:item[1], reverse=False
        )}

        return list(dict_mau_sorted.keys())

    def dict_the_lay_ngay_func(self, board):
        dict_card = {
            'red': [], 'blue': [], 'green': [], 'white': [], 'black': []
        }

        for card in self.card_upside_down:
            if self.check_get_card(card):
                dict_card[card.type_stock].append(card)

        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board.dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        dict_card[card.type_stock].append(card)

        return dict_card