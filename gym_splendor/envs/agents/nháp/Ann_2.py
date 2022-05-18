from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state=None,action_space = None):
        #print('Boardadsadasdasda', state['Board']._Board__dict_Card_Stocks_Show['I'][0].__dict__.keys())
        dict_the_lay_ngay = self.dict_the_lay_ngay_func(state['Board'])

        mau_the_quan_trong = self.mau_the_quan_trong_func(state['Board'])

        temp = [dict_the_lay_ngay[mau].__len__() for mau in dict_the_lay_ngay.keys()]
        sl_the_lay_ngay = sum(temp)

        if sl_the_lay_ngay != 0:
            for mau in mau_the_quan_trong:
                if dict_the_lay_ngay[mau].__len__() != 0:
                    card = self.chon_the_gia_tri_cao(dict_the_lay_ngay[mau])
                    return [], card, []

            list_the_lay_ngay = []
            for mau in dict_the_lay_ngay.keys():
                if dict_the_lay_ngay[mau].__len__() != 0:
                    list_the_lay_ngay += dict_the_lay_ngay[mau]

            card = self.chon_the_gia_tri_cao(list_the_lay_ngay)
            if card._Card__score != 0:
                return [], card, []

        list_co_the_lay = self.the_co_the_lay(state['Board'], mau_the_quan_trong)
        if list_co_the_lay.__len__() != 0:
            target = list_co_the_lay[0]
            if sum(target['nl_thieu'].values()) == 1 and target['nl_thieu']['auto_color'] == 1  \
                and target['the'] not in self._Player__card_upside_down \
                and self._Player__card_upside_down.__len__() <= 2   \
                and state['Board']._Board__stocks['auto_color'] > 0:
                stocks_return = self.Tim_nl_tra(target['the'], ['auto_color'])
                return [], target['the'], stocks_return

            stocks = []
            mau_target_thieu = [mau for mau in target['nl_thieu'].keys() if mau != 'auto_color' and target['nl_thieu'][mau] != 0]

            if mau_target_thieu.__len__() == 1:
                if target['nl_thieu'][mau_target_thieu[0]] >= 2 and state['Board']._Board__stocks[mau_target_thieu[0]] >= 4:
                    stocks = [mau_target_thieu[0], mau_target_thieu[0]]
                    stocks_return = self.Tim_nl_tra(target['the'], stocks)
                    #print(stocks, stocks_return)
                    nl_trung_nhau = list(set(stocks) & set(stocks_return))
                    for i in nl_trung_nhau:
                        stocks.remove(i)
                        stocks_return.remove(i)
                    #print(stocks, stocks_return)
                    return stocks, None, stocks_return
            
            for ele in list_co_the_lay:
                for mau in ele['the']._Card__stocks.keys():
                    if ele['nl_thieu'][mau] != 0 and mau not in stocks:
                        stocks.append(mau)
                        break

                if stocks.__len__() == 3:
                    break

            if stocks.__len__() == 3:
                stocks_return = self.Tim_nl_tra(target['the'], stocks)
                #print(stocks, stocks_return)
                nl_trung_nhau = list(set(stocks) & set(stocks_return))
                for i in nl_trung_nhau:
                    stocks.remove(i)
                    stocks_return.remove(i)
                #print(stocks, stocks_return)
                return stocks, None, stocks_return, 1
            
            nn = 3 - stocks.__len__()
            for i in range(nn):
                temp_list_mau = [mau for mau in state['Board']._Board__stocks.keys() if mau != (['auto_color'] + stocks) and state['Board']._Board__stocks[mau] != 0]
                if temp_list_mau.__len__() != 0:
                    mau_choice = random.choice(temp_list_mau)
                    stocks.append(mau_choice)
            
            stocks_return = self.Tim_nl_tra(target['the'], stocks)
            #print(stocks, stocks_return)
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            #print(stocks, stocks_return)
            return stocks, None, stocks_return, 1
        
        stocks = []
        for i in range(min(3, 10-sum(self._Player__stocks.values()))):
            temp_list = [mau for mau in state['Board']._Board__stocks.keys() if mau != 'auto_color' and mau not in stocks]
            if temp_list.__len__() != 0:
                stocks.append(random.choice(temp_list))
        #print(stocks, 'asdasdasdasda')
        return stocks, None, []

    def Tim_nl_tra(self, card, stocks):
        nl_hien_tai = deepcopy(self._Player__stocks)
        for i in stocks:
            nl_hien_tai[i] += 1

        snl = sum(list(nl_hien_tai.values()))
        if snl <= 10:
            return []

        list_stock_return = []
        nl_thua = snl - 10

        dict_nl_thua_temp = {}
        for mau in card._Card__stocks.keys():
            if nl_hien_tai[mau] + self._Player__stocks_const[mau] > card._Card__stocks[mau]:
                dict_nl_thua_temp[mau] = nl_hien_tai[mau] + self._Player__stocks_const[mau] - card._Card__stocks[mau]

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
            for i in range(nl_thua-list_stock_return):
                a = max(nl_hien_tai.values())
                for mau in nl_hien_tai.keys():
                    if mau != 'auto_color' and nl_hien_tai[mau] == a:
                        nl_hien_tai[mau] -= 1
                        list_stock_return.append(mau)
                        break

        return list_stock_return

    def the_co_the_lay(self, board, mau_the_quan_trong):
        list_card_can_check = []
        for car in self._Player__card_upside_down:
            if not self.check_get_card(car):
                list_card_can_check.append(car)
        
        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board._Board__dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        list_card_can_check.append(car)

        list_check_1 = []
        for mau in mau_the_quan_trong:
            for car in list_card_can_check:
                if car._Card_Stock__type_stock == mau:
                    list_check_1.append(car)

        list_check_2 = [car for car in list_card_can_check if car not in list_check_1]
        list_card_can_check = list_check_1 + list_check_2

        list_tra_ve = []
        temp = ["red", "blue", "green", "white", "black"]
        for car in list_card_can_check:
            nl_thieu = {}
            nl_thieu['auto_color'] = 0
            for mau in temp:
                nl_thieu[mau] = max(0, car._Card__stocks[mau] - self._Player__stocks_const[mau] - self._Player__stocks[mau])
            
            if self._Player__stocks['auto_color'] != 0:
                a = self._Player__stocks['auto_color']
                for i in range(a):
                    loai_mau_thieu = [mau for mau in temp if nl_thieu[mau] != 0]
                    dap_ung = True
                    for mau in loai_mau_thieu:
                        if board._Board__stocks[mau] < nl_thieu[mau]:
                            dap_ung = False
                            nl_thieu[mau] -= 1
                            break
                    if dap_ung:
                        du_da = {}
                        for mau in loai_mau_thieu:
                            du_da[mau] = board._Board__stocks[mau] - nl_thieu[mau]

                        min_ = min(du_da.values())
                        for mau in loai_mau_thieu:
                            if du_da[mau] == min_:
                                nl_thieu[mau] -= 1
                                break
            
            nl_vc_thieu = {}
            for mau in temp:
                nl_vc_thieu[mau] = max(0, car._Card__stocks[mau] - self._Player__stocks_const[mau])
            
            kha_nang = True
            if sum(nl_vc_thieu.values()) > (10-self._Player__stocks['auto_color']):
                kha_nang = False
            else:
                nl_nh_thieu = {}
                for mau in temp:
                    nl_nh_thieu[mau] = max(0, nl_thieu[mau] - board._Board__stocks[mau])
                
                if sum(nl_nh_thieu.values()) > 1:
                    kha_nang = False
                else:
                    if sum(nl_nh_thieu.values()) == 1:
                        if board._Board__stocks["auto_color"] != 0:
                            for mau in temp:
                                if nl_nh_thieu[mau] != 0:
                                    nl_thieu[mau] -= 1
                                    nl_thieu['auto_color'] = 1
                                    break
                        else:
                            kha_nang = False
        
            if kha_nang:
                list_tra_ve.append({
                    'the': car,
                    'nl_thieu': nl_thieu
                })
        
        if list_tra_ve.__len__() == 0:
            return []

        list_check_11 = [ele for ele in list_tra_ve if ele['the'] in list_check_1]
        list_check_22 = [ele for ele in list_tra_ve if ele not in list_check_11]

        list_check_11.sort(key = lambda a: sum(a['nl_thieu'].values()))
        list_check_22.sort(key = lambda a: sum(a['nl_thieu'].values()))

        return list_check_11 + list_check_22

    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car._Card__score / sum(list(car._Card__stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

    def mau_the_quan_trong_func(self, board):
        if board._Board__dict_Card_Stocks_Show['Noble'].__len__() == 0:
            return []

        sl_bien = {
        "red": 0, "blue": 0, "green": 0, "black": 0, "white": 0
        }

        temp = ["red", "blue", "green", "white", "black"]

        for mau in temp:
            list_temp = [car._Card__stocks[mau] for car in board._Board__dict_Card_Stocks_Show['Noble']]
            max_ = max(list_temp)

            if max_ > 0:
                sl_bien[mau] = max_
        
        mau_dat_sl_bien = []
        for mau in sl_bien.keys():
            if self._Player__stocks_const[mau] >= sl_bien[mau]:
                mau_dat_sl_bien.append(mau)

        # Chia case
        if mau_dat_sl_bien.__len__() == 0:
            mau_can_lay_1 = list(sl_bien.keys())
            mau_can_lay_2 = []
        elif mau_dat_sl_bien.__len__() == 1:
            mau_can_lay_1 = []
            for car in board._Board__dict_Card_Stocks_Show['Noble']:
                if car._Card__stocks[mau_dat_sl_bien[0]] != 0:
                    for mau in temp:
                        if mau != mau_dat_sl_bien[0] and car._Card__stocks[mau] > 0:
                            if mau not in mau_can_lay_1:
                                mau_can_lay_1.append(mau)
            mau_can_lay_2 = [color for color in sl_bien.keys() if color not in mau_dat_sl_bien and color not in mau_can_lay_1]
        else:
            mau_can_lay_1 = []
            a = mau_dat_sl_bien.__len__()

            for i in range(a):
                for j in range(i+1,a):
                    mau1 = mau_dat_sl_bien[i]
                    mau2 = mau_dat_sl_bien[j]
                    for car in board._Board__dict_Card_Stocks_Show['Noble']:
                        if car._Card__stocks[mau1] != 0 and car._Card__stocks[mau2] != 0:
                            for mau in temp:
                                if mau != mau1 and mau != mau2 and car._Card__stocks[mau] != 0:
                                    if mau not in mau_can_lay_1:
                                        mau_can_lay_1.append(mau)

            mau_can_lay_2 = [color for color in sl_bien.keys() if color not in mau_dat_sl_bien and color not in mau_can_lay_1]

        # Sắp xếp
        mau_can_lay_1_sort = self.sap_xep(mau_can_lay_1, sl_bien)
        mau_can_lay_2_sort = self.sap_xep(mau_can_lay_2, sl_bien)

        mau_quan_trong = []
        mau_quan_trong += mau_can_lay_1_sort
        if mau_can_lay_2.__len__() != 0:
            mau_quan_trong += mau_can_lay_2_sort

        return mau_quan_trong

    def sap_xep(self, list_mau, sl_bien):
        if list_mau.__len__() == 0:
            return []

        dict_mau = {}
        for mau in list_mau:
            dict_mau[mau] = sl_bien[mau] - self._Player__stocks_const[mau]
        
        dict_mau_sorted = {k:v for k,v in sorted(dict_mau.items(), key=lambda item: item[1], reverse=False)}

        return list(dict_mau_sorted.keys())

    def dict_the_lay_ngay_func(self, board):
        dict_card = {
            'red': [], 'blue': [], 'green': [], 'white': [], 'black': []
        }

        for card in self._Player__card_upside_down:
            if self.check_get_card(card):
                dict_card[card._Card_Stock__type_stock].append(card)

        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for card in board._Board__dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        dict_card[card._Card_Stock__type_stock].append(card)

        return dict_card