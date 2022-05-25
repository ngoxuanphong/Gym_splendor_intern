from ..base.player import Player
from ..base.board import Board
from ..base.card import Card
import random
import math
from collections import Counter
from copy import deepcopy

class Agent(Player, Card, Board):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        # gán
        board = state['Board']
        tn_target_final = self.tai_nguyen_target_func(state['Board'])
        the_lay_ngay = self.dict_the_lay_ngay_func(board)  # dict
        mau_the_quan_trong = self.mau_the_quan_trong_func(state['Board'])
        print("list the lay ngay : ", the_lay_ngay)
        #chọn thẻ lấy ngay
        mau_the_vinh_vien_da_so_huu = {
            'red': 0, 'blue': 0, 'green': 0, 'white': 0, 'black': 0}
        for mau_the,ds_the in the_lay_ngay.items():
            if mau_the in tn_target_final :
                for car in ds_the:
                    if car.type_stock == mau_the and mau_the_vinh_vien_da_so_huu[mau_the] <=3:
                        card = car
                        mau_the_vinh_vien_da_so_huu[car.type_stock] +=1
                        return None, card, None#---------------------------------------------------------------

        #tim nguyen lieu tra
        list_co_the_lay = self.the_co_the_lay_func(state['Board'], mau_the_quan_trong)
        if list_co_the_lay.__len__() != 0:
            target = list_co_the_lay[0]
            mau_target_thieu = [mau for mau in target['nl_thieu'].keys() if
                                mau != 'auto_color' and target['nl_thieu'][mau] != 0]

            if mau_target_thieu.__len__() == 1:
                if target['nl_thieu'][mau_target_thieu[0]] >= 2 and state['Board'].stocks[mau_target_thieu[0]] >= 4:
                    stocks = [mau_target_thieu[0], mau_target_thieu[0]]
                    stocks_return = self.Tim_nl_tra(target['the'], stocks)
                    print(stocks, stocks_return)
                    nl_trung_nhau = list(set(stocks) & set(stocks_return))
                    for i in nl_trung_nhau:
                        stocks.remove(i)
                        stocks_return.remove(i)
                    print(stocks, stocks_return, '1111')
                    return stocks, None, stocks_return

            temp_list_jasdhg = []
            for ele in list_co_the_lay:
                for mau in ele['the'].stocks.keys():
                    if ele['nl_thieu'][mau] != 0 and mau not in temp_list_jasdhg:
                        temp_list_jasdhg.append(mau)

            # print('asfsadfsdfsfsd', temp_list_jasdhg)

            if temp_list_jasdhg.__len__() <= 3:
                stocks = deepcopy(temp_list_jasdhg)
            else:
                while stocks.__len__() < 3:
                    sdg = random.choice(temp_list_jasdhg)
                    stocks.append(sdg)
                    temp_list_jasdhg.remove(sdg)

            if stocks.__len__() == 3:
                stocks_return = self.Tim_nl_tra(target['the'], stocks)
                print(stocks, stocks_return)
                nl_trung_nhau = list(set(stocks) & set(stocks_return))
                for i in nl_trung_nhau:
                    stocks.remove(i)
                    stocks_return.remove(i)
                print(stocks, stocks_return, '2222')
                return stocks, None, stocks_return

            nn = 3 - stocks.__len__()
            for i in range(nn):
                temp_list_mau = [mau for mau in state['Board'].stocks.keys() if
                                 mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
                if temp_list_mau.__len__() != 0:
                    mau_choice = random.choice(temp_list_mau)
                    stocks.append(mau_choice)

            stocks_return = self.Tim_nl_tra(target['the'], stocks)
            print(stocks, stocks_return)
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            print(stocks, stocks_return, '3333')
            return stocks, None, stocks_return
        if (state['Board'].stocks['auto_color'] > 0 and self.card_upside_down.__len__() < 3) or (
            self.card_upside_down.__len__() < 3 and sum(state['Board'].stocks.values()) ==
            state['Board'].stocks['auto_color']):
            card_up = self.Tim_the_up(state['Board'], mau_the_quan_trong)
            if card_up != None:
                stocks_return = []
                if card_up != None:
                    stocks_return = self.Tim_nl_tra(card_up, ['auto_color'])
                print(stocks_return, card_up, '4444')
                return [], card_up, stocks_return



        stocks = []
        for i in range(min(3, 10 - sum(self.stocks.values()))):
            temp_list = [mau for mau in state['Board'].stocks.keys() if
                             mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        print(stocks, '5555')
        if stocks.__len__() > 0:
            return stocks, None, []

        for i in range(3):
            temp_list = [mau for mau in state['Board'].stocks.keys() if
                        mau not in (['auto_color'] + stocks) and state['Board'].stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))

        stocks_return = []
        nl_thua = max(sum(self.stocks.values()) + stocks.__len__() - 10, 0)
        pl_st = deepcopy(self.stocks)
        for i in range(nl_thua):
            temp_list = [mau for mau in pl_st.keys() if mau != 'auto_color' and pl_st[mau] > 0]
            dfghjk = random.choice(temp_list)
            stocks_return.append(dfghjk)
            pl_st[dfghjk] -= 1
        print(stocks, stocks_return, '6666', self.card_upside_down.__len__())
        return stocks, None, stocks_return

            #kiểm tra xem có mua được thẻ không=>list thẻ có thể mua

               # list_the_up_can_mo = []
                #for card in self.card_upside_down:
                 #   if not self.check_get_card(card):
                  #      #list_the_up_can_mo
                   #     print(" ")


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

        list_check_2 = [car for car in list_card_can_check if car not in (list_check_1 + list_check_1_2)]

        list_check = [list_check_1, list_check_1_2, list_check_2]
        for i in range(3):
            if list_check[i].__len__() != 0:
                card = self.chon_the_gia_tri_cao(list_check[i])
                return card

        return None
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
    def tai_nguyen_target_func(self, board):
        # lấy list tài nguyên target cho toàn trận từ hàng noble.
        noble_3_tn_tam = []
        noble_2_tn = {}  # các loại tài nguyên xuất hiện trong thẻ noble chỉ có 2 tài nguyên_và số thẻ mà nó nằm trong
        noble_3_tn = {'red': 0, 'blue': 0, 'green': 0, 'black': 0,
                      'white': 0}  # các loại tài nguyên xuất hiện trong thẻ noble chỉ có 3 tài nguyên
        # số thẻ mà nó nằm trong
        tn_target_final = []  # tài nguyên chọn để build thực sự.

        for type_card in board.dict_Card_Stocks_Show:
            if type_card == 'Noble':
                list_tn_target_ = []
                for card in board.dict_Card_Stocks_Show['Noble']:
                    # tìm các thẻ noble chứa 2 tn build
                    count_card_tn_eval_2 = 0
                    for k in card.stocks.keys():
                        if card.stocks[k] > 0:
                            count_card_tn_eval_2 += 1

                    if count_card_tn_eval_2 == 2:
                        for k in card.stocks.keys():
                            if card.stocks[k] > 0:
                                list_tn_target_.append(k)
                        noble_2_tn = dict((x, list_tn_target_.count(x)) for x in set(list_tn_target_))
                    else:
                        noble_3_tn_tam.append(card.stocks)
                # lưu tất cả loại tài nguyên của thẻ noble có 3 tài nguyên build vào noble_3_tn
                for tn_build_each_card_IV in noble_3_tn_tam:
                    if tn_build_each_card_IV['red'] > 0:
                        noble_3_tn['red'] += 1
                    if tn_build_each_card_IV['blue'] > 0:
                        noble_3_tn['blue'] += 1
                    if tn_build_each_card_IV['green'] > 0:
                        noble_3_tn['green'] += 1
                    if tn_build_each_card_IV['black'] > 0:
                        noble_3_tn['black'] += 1
                    if tn_build_each_card_IV['white'] > 0:
                        noble_3_tn['white'] += 1

                noble_2_tn = dict(sorted(noble_2_tn.items(), key=lambda x: x[1], reverse=True))
                noble_3_tn = dict(sorted(noble_3_tn.items(), key=lambda x: x[1], reverse=True))
                print("noble_2_tn", noble_2_tn)  # loại thẻ noble chỉ có 2 tài nguyên
                print("noble_3_tn", noble_3_tn)  # loại thẻ noble chỉ có 3 tài nguyên

                # ưu tiền target tài nguyên theo các thẻ noble chỉ có 2 loại tài nguyên build và có loại tài nguyên xuất hiện trong noble_3_tn

                if len(noble_2_tn) != 0:
                    if len(noble_2_tn) == 2:  # chỉ có 1 thẻ noble 2 tn build
                        for x in noble_2_tn.keys():
                            tn_target_final.append(x)
                    else:  # nếu len(noble_2_tn) > 2, tức có >= 2 thẻ noble 2 tn build
                        # nếu tất cả giá trị = 1 thì xét sang list kia
                        if list(noble_2_tn.values())[0] == 1:  # list chứa toàn value = 1
                            for k in noble_2_tn.keys():
                                if k in noble_3_tn.keys():
                                    if len(tn_target_final) < 3:
                                        tn_target_final.append(k)
                        else:
                            for m in noble_2_tn.keys():
                                if noble_2_tn[m] >= 2 and len(tn_target_final) < 3:
                                    tn_target_final.append(m)
                            if len(tn_target_final) < 3:
                                for k in noble_3_tn.keys():
                                    if k in tn_target_final:
                                        continue
                                    else:
                                        if len(tn_target_final) < 3:
                                            tn_target_final.append(k)
                print("tn_target_final : ",
                      tn_target_final)

                ####################cần tối ưu: giả sử noble_2_tn có value= [2,1,1,1]. Sau khi lấy key của value 2
                # ta cần truy cập đến thẻ chứa tài nguyên key=2 để lấy nốt cái tài nguyên còn lại
        return tn_target_final

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
            if nl_hien_tai[mau] + self.stocks_const[mau] > card.stocks[mau]:
                dict_nl_thua_temp[mau] = nl_hien_tai[mau] + self.stocks_const[mau] - card.stocks[mau]

        dict_nl_thua = {k: v for k, v in sorted(dict_nl_thua_temp.items(), key=lambda item: item[1], reverse=True)}
        for i in range(nl_thua):
            for mau in dict_nl_thua.keys():
                if dict_nl_thua[mau] != 0:
                    dict_nl_thua[mau] -= 1
                    nl_hien_tai[mau] -= 1
                    dict_nl_thua_temp = deepcopy(dict_nl_thua)
                    dict_nl_thua = {k: v for k, v in
                                    sorted(dict_nl_thua_temp.items(), key=lambda item: item[1], reverse=True)}
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
                for j in range(i + 1, a):
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

        list_check_2 = [car for car in list_card_can_check if car not in (list_check_1 + list_check_1_2)]

        temp = ["red", "blue", "green", "white", "black"]
        list_thu_nhat = []
        for car in (list_check_1 + list_check_1_2 + list_check_2):
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

                    dict_tempp = {k: v for k, v in sorted(
                        dict_temp.items(), key=lambda item: item[1], reverse=False
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
        list_check_22 = [ele for ele in list_thu_nhat if ele not in (list_check_11 + list_check_11_2)]
        list_check_11.sort(key=lambda a: sum(a['nl_thieu'].values()))
        list_check_11_2.sort(key=lambda a: sum(a['nl_thieu'].values()))
        list_check_22.sort(key=lambda a: sum(a['nl_thieu'].values()))

        list_thu_hai = list_check_11 + list_check_11_2 + list_check_22
        for ele in list_thu_hai:
            for mau in temp:
                if mau not in list_board_nl:
                    ele['nl_thieu'][mau] = 0

        return list_thu_hai

    def sap_xep_mau_func(self, list_mau, sl_bien):
        if list_mau.__len__() == 0:
            return []

        dict_mau = {}
        for mau in list_mau:
            dict_mau[mau] = sl_bien[mau] - self.stocks_const[mau]

        dict_mau_sorted = {a: b for a, b in sorted(
            dict_mau.items(), key=lambda item: item[1], reverse=False
        )}

        return list(dict_mau_sorted.keys())
    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

