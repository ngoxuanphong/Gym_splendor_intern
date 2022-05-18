from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        thecothemo = self.thecothemo(state['Board'])
        
        if len(thecothemo) > 0:
            x = []
            for the in thecothemo:
                if self.score + the.score >= 15:
                    x.append(the)

            for diem in range(5, 0, -1):
                for card in x:
                    if card.score == diem:
                        # print(card.stocks, card.score, '1111')
                        return [], card, []

        thecothemocuanguoichoi = self.thecothemocuanguoichoi(state['Board'], state['Player'])
        for i in thecothemocuanguoichoi:
            id = 0
            if id == state['Player'].index(self):
                continue
            if len(i) > 0:
                x = []
                for the in i:
                    if state['Player'][id].score + the.score >= 15:
                        x.append(the)
            
                for diem in range(5, 0, -1):
                    for card in x:
                        if card.score == diem:
                            if self.check_upsite_down(card):
                                stocks_return = []
                                if state['Board'].stocks['auto_color'] > 0:
                                    stocks_return = self.Luachonbothe(state['Board'], ['auto_color'])

                                # print(card.stocks, card.score, '2222')
                                return [], card, stocks_return, 3

            id += 1

        latthedangup = self.latthedangup(state['Board'])
        if len(latthedangup) > 0:
            for diem in range(5, 0, -1):
                for card in latthedangup:
                    if card.score == diem:
                        
                        # print(card.stocks, card.score, '3333')
                        return [], card, []

        laythenoble = self.laythenoble(state['Board'])
        if laythenoble.__len__() > 0:
            card = laythenoble[0]
            # print(card.stocks, card.score, '3333')
            return [], card, []

        arr_player = [pl for pl in state['Player'] if pl != self]
        if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
            if len(self.card_upside_down) == 0:
                thecotheup = self.thecotheup(state['Board'])
                if len(thecotheup) > 0:
                    if self.check_upsite_down(thecotheup[0]):
                        card = thecotheup[0]
                        stocks_return = []
                        if state['Board'].stocks['auto_color'] > 0:
                            stocks_return = self.Luachonbothe(state['Board'], ['auto_color'])

                        # print(card.stocks, card.score, stocks_return, '4444')
                        return [], card, stocks_return, 3

        if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
            lay1NLtheup1 = self.lay1NLtheup1(state['Board'])
            if len(lay1NLtheup1) > 0:
                color = lay1NLtheup1
                if len(color) > 0:
                    stocks_get = [color[0], color[0]]
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, '5555')
                    return stocks_get, None, stocks_return
        
        if arr_player[0].score <= 13 and arr_player[1].score <= 13 and arr_player[2].score <= 13:
            if sum(self.stocks.values()) <= 8:
                Lay3NLtheup1 = self.Lay3NLtheup1(state['Board'])
                if len(Lay3NLtheup1) >= 3:
                    tp_ = [mau for mau in Lay3NLtheup1[0:3] if state['Board'].stocks[mau] > 0]
                    if len(tp_) == 3:
                        stocks_return = self.Luachonbothe(state['Board'], tp_)
                        # print(tp_, stocks_return, '6666')
                        return tp_, None, stocks_return

        if arr_player[0].score <= 12 and arr_player[1].score <= 12 and arr_player[2].score <= 12:
            if sum(self.stocks.values()) <= 8:
                layBaNguyenlieu = self.layBaNguyenlieu(state['Board'])
                if len(layBaNguyenlieu) >= 3:
                    tp_ = [mau for mau in layBaNguyenlieu[0:3] if state['Board'].stocks[mau] > 0]
                    if len(tp_) == 3:
                        stocks_return = self.Luachonbothe(state['Board'], tp_)
                        # print(tp_, stocks_return, '7777')
                        return tp_, None, stocks_return

        if arr_player[0].score <= 12 and arr_player[1].score <= 12 and arr_player[2].score <= 12:
            if sum(self.stocks.values()) <= 9:
                color = self.laymotnguyenlieu(state['Board'])
                if len(color) > 0:
                    stocks_get = [color[0], color[0]]
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, '8888')
                    return stocks_get, None, stocks_return
        
        if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12:
            SXthecothemo = self.SXthecothemo(state['Board'])
            if SXthecothemo != None:
                card = SXthecothemo
                # print(card.stocks, card.score, '9999')
                return [], card, []
        
        thecothemo = self.thecothemo(state['Board'])
        if len(thecothemo) > 0:
            for diem in range(5, 0, -1):
                for card in thecothemo:
                    if card.score == diem:
                        # print(card.stocks, card.score, '0000')
                        return [], card, []

        lay1NLtheup1 = self.lay1NLtheup1(state['Board'])
        if len(lay1NLtheup1) > 0:
            if sum(self.stocks.values()) <= 9:
                color = lay1NLtheup1
                stocks_get = [color[0], color[0]]
                stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                # print(stocks_get, stocks_return, 'aaaa')
                return stocks_get, None, stocks_return

        Lay3NLtheup1 = self.Lay3NLtheup1(state['Board'])
        if sum(self.stocks.values()) <= 8:
            if len(Lay3NLtheup1) >= 3:
                stocks_get = [mau for mau in Lay3NLtheup1[0:3] if state['Board'].stocks[mau] > 0]
                if stocks_get.__len__() == 3:
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, 'bbbb')
                    return stocks_get, None, stocks_return

        layBaNguyenlieu = self.layBaNguyenlieu(state['Board'])
        if sum(self.stocks.values()) <= 8 and layBaNguyenlieu.__len__() >= 3:
            stocks_get = [mau for mau in layBaNguyenlieu[0:3] if state['Board'].stocks[mau] > 0]
            if stocks_get.__len__() == 3:
                stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                # print(stocks_get, stocks_return, 'cccc')
                return stocks_get, None, stocks_return

        if sum(self.stocks.values()) <= 9:
            color = self.laymotnguyenlieu(state['Board'])
            if len(color) > 0:
                stocks_get = [color[0], color[0]]
                stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                # print(stocks_get, stocks_return, 'dddd')
                return stocks_get, None, stocks_return

        Laythehotro = self.Laythehotro(state['Board'])
        if Laythehotro.__len__() > 0:
            card = Laythehotro[0]
            # print(card.stocks, card.score, 'eeee')
            return [], Laythehotro[0], []

        if sum(self.stocks.values()) <= 8:
            L3NLtrong2 = self.L3NLtrong2(state['Board'])
            if len(L3NLtrong2) >= 3:
                stocks_get = [mau for mau in L3NLtrong2[0:3] if state['Board'].stocks[mau] > 0]
                if stocks_get == 3:
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, 'ffff')
                    return stocks_get, None, stocks_return

        thecotheup = self.thecotheup(state['Board'])
        if len(thecotheup) > 0:
            if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12:
                if self.check_upsite_down(thecotheup[0]):
                    card = thecotheup[0]
                    stocks_return = []
                    if state['Board'].stocks['auto_color'] > 0:
                        stocks_return = self.Luachonbothe(state['Board'], ['auto_color'])
                    # print(card.stocks, card.score, stocks_return, 'gggg')
                    return [], card, [], 3
        
        if sum(self.stocks.values()) <= 9:
            L3NLtrong1 = self.L3NLtrong1(state['Board'])
            if len(L3NLtrong1) >= 3:
                stocks_get = [mau for mau in L3NLtrong1[0:3] if state['Board'].stocks[mau] > 0]
                if stocks_get == 3:
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, 'hhhh')
                    return stocks_get, None, stocks_return

        if sum(self.stocks.values()) <= 7:
            SXNLtrenban = self.SXNLtrenban(state['Board'])
            if len(SXNLtrenban) >= 3:
                stocks_get = [mau for mau in SXNLtrenban[0:3] if state['Board'].stocks[mau] > 0]
                if stocks_get == 3:
                    stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                    # print(stocks_get, stocks_return, 'jjjj')
                    return stocks_get, None, stocks_return

        if sum(self.stocks.values()) <= 8:
            Lay1NLbatky = self.Lay1NLbatky(state['Board'])
            if len(Lay1NLbatky) > 0:
                mau_lay = Lay1NLbatky[0]
                stocks_get = [mau_lay, mau_lay]
                stocks_return = self.Luachonbothe(state['Board'], stocks_get)
                # print(stocks_get, stocks_return, 'kkkk')
                return stocks_get, None, stocks_return


        if arr_player[0].score <=12 and arr_player[1].score <=12 and arr_player[2].score <=12:
            thecothemo = self.thecothemo(state['Board'])
            if len(thecothemo) > 0:
                Laythebinhthuong = self.Laythebinhthuong(state['Board'])
                if Laythebinhthuong != None:
                    card = Laythebinhthuong
                    # print(card.stocks, card.score, stocks_return, 'llll')
                    return [], card, []

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
        


        # print(self.card_upside_down.__len__())
        # print('pppp')
        return [], None, []

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

    def thecotheup(self, board):
        listthecotheup = []
        for Loaithe in board.dict_Card_Stocks_Show.keys():
            if Loaithe != 'Noble':
                for card in board.dict_Card_Stocks_Show[Loaithe]:
                    if card.score == 3 and sum(card.stocks.values()) == 6:
                        listthecotheup.append(card)
                    if card.score == 4 and sum(card.stocks.values()) == 7:
                        listthecotheup.append(card)
                    if card.score == 2 and sum(card.stocks.values()) == 5:
                        listthecotheup.append(card)
                    if card.score == 5 and sum(card.stocks.values()) == 10:
                        listthecotheup.append(card)            
                    if card.score == 1 and sum(card.stocks.values()) == 4:
                        listthecotheup.append(card)
                    if card.score == 2 and sum(card.stocks.values()) == 7:
                        listthecotheup.append(card)
                    if card.score == 2 and sum(card.stocks.values()) == 8:
                        listthecotheup.append(card)

        return listthecotheup

    def latthedangup(self, board):
        listthecothemuadangup = []
        if len(self.card_upside_down) > 0:
            for card in self.card_upside_down:
                if self.check_get_card(card):
                    listthecothemuadangup.append(card)

        return listthecothemuadangup

    def thecothemo(self, board):
        listthecothemo = []
        if len(self.card_upside_down) > 0:
            for card in self.card_upside_down:
                if self.check_get_card(card):
                    listthecothemo.append(card)

        for Loaithe in board.dict_Card_Stocks_Show.keys():
            if Loaithe != "Noble":
                for card in board.dict_Card_Stocks_Show[Loaithe]:
                        if self.check_get_card(card):
                            listthecothemo.append(card)

        return listthecothemo

    def thecothemocuanguoichoi(self, board, arr_player):
        listnguoichoi = []
        for nguoichoi in range(len(arr_player)):
            listthecothemo = []
            for Loaithe in board.dict_Card_Stocks_Show.keys():
                if Loaithe != "Noble":
                    for card in board.dict_Card_Stocks_Show[Loaithe]:
                            if arr_player[nguoichoi].check_get_card(card):
                                listthecothemo.append(card)
            listnguoichoi.append(listthecothemo)

        return listnguoichoi

    def SXthecothemo(self, board):
        x = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4]
        soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for danhgia in x:
            thecothemo = self.thecothemo(board)
            for the in thecothemo:
                if the.score > 0:
                    sumNL = 0
                    for lnl in soluongnguyenlieucan.keys():
                        sumNL += the.stocks[lnl] - self.stocks_const[lnl]
                        if sumNL / the.score < danhgia:
                            return the    

        return None

    def NLtheup1(self, board):
        soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for lnl in soluongnguyenlieucan.keys():
            if len(self.card_upside_down) > 0:
                the = self.card_upside_down[0]
                soluongnguyenlieucan[lnl] += the.stocks[lnl] 
                soluongnguyenlieucan[lnl] -= self.stocks[lnl] + self.stocks_const[lnl]
        SXNL = dict(sorted(soluongnguyenlieucan.items(), key=lambda x:x[1], reverse=True))
        return SXNL

    def lay1NLtheup1(self, board):
        OneNguyenlieucothelay = []
        nl_theup = self.NLtheup1(board)
        for lnl in nl_theup:
            if nl_theup[lnl] >= 2:
                if board.stocks[lnl] > 3:
                    OneNguyenlieucothelay.append(lnl)

        return OneNguyenlieucothelay

    def Lay3NLtheup1(self, board):
        listcacNLnenlay = []
        nl_theup = self.NLtheup1(board)
        for lnl in nl_theup:
            if nl_theup[lnl] > 0 and board.stocks[lnl] > 0:
                listcacNLnenlay.append(lnl)
        return listcacNLnenlay

    def Nguyenlieucan(self, board):
        soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for lnl in soluongnguyenlieucan.keys():
            for the in self.card_upside_down:
                soluongnguyenlieucan[lnl] += the.stocks[lnl] 
            soluongnguyenlieucan[lnl] -= self.stocks[lnl] + self.stocks_const[lnl] 
        return soluongnguyenlieucan

    def dictsapxepnguyenlieu(self, board):
        return dict(sorted(self.Nguyenlieucan(board).items(), key=lambda x:x[1], reverse=True))
    
    def laymotnguyenlieu(self, board):
        OneNguyenlieucothelay = []
        if sum(self.stocks.values()) <= 8:
            dictsapxepnguyenlieu = self.dictsapxepnguyenlieu(board)
            for lnl in dictsapxepnguyenlieu:
                if dictsapxepnguyenlieu[lnl] >= 2:
                    if board.stocks[lnl] > 3:
                        OneNguyenlieucothelay.append(lnl)
        return OneNguyenlieucothelay

    def layBaNguyenlieu(self, board):
        listcacNLnenlay = []
        dictsapxepnguyenlieu = self.dictsapxepnguyenlieu(board)
        for lnl in dictsapxepnguyenlieu:
            if dictsapxepnguyenlieu[lnl] > 0 and board.stocks[lnl] > 0:
                listcacNLnenlay.append(lnl)
        return listcacNLnenlay

    def Laythehotro(self, board):
        listNLcan = []
        listthehotro = []
        listthehotrolay = []
        dictsapxepnguyenlieu = self.dictsapxepnguyenlieu(board)
        for lnl in dictsapxepnguyenlieu:
            if dictsapxepnguyenlieu[lnl] > 0:
                listNLcan.append(lnl)
        thecothemo = self.thecothemo(board)
        for the in thecothemo:
            if the.type_stock in listNLcan:
                listthehotro.append(the)
        for the in listthehotro:
            if self.check_get_card(the) == True:
                listthehotrolay.append(the)
        return listthehotrolay

    def Laythebinhthuong(self, board):
        a = []
        thecothemo = self.thecothemo(board)
        if len(thecothemo) > 0:
            the = thecothemo[0]
            for card in thecothemo:
                NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
                for lnl in NLcanmo1the.keys():
                    NLcanmo1the[lnl] = card.stocks[lnl] - self.stocks_const[lnl]
                a.append(sum(NLcanmo1the.values()))
            x = min(a)
            for card in thecothemo:
                NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
                for lnl in NLcanmo1the.keys():
                    NLcanmo1the[lnl] = card.stocks[lnl] - self.stocks_const[lnl]
                if a == sum(NLcanmo1the.values()):
                    return card
        return None

    def SXNLtrenban(self, board):
        layBaNguyenlieu = self.layBaNguyenlieu(board)
        listNLcan = layBaNguyenlieu.copy()
        NLtrenban = board.stocks.copy()
        for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
            if lnl != "auto_color":
                if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu):
                    listNLcan.append(lnl)
        return listNLcan

    def Lay1NLbatky(self, board):
        ln = []
        NLtrenban = board.stocks.copy()
        for lnl in NLtrenban.keys():
            if lnl != "auto_color":
                if NLtrenban[lnl] >=4:
                    if board.stocks[lnl] > 3:
                        ln.append(lnl)
        return ln

    def L3NLtrong2(self, board):
        listNLcan = self.layBaNguyenlieu(board)
        layBaNguyenlieu = self.layBaNguyenlieu(board)
        if len(layBaNguyenlieu) == 2:
            NLtrenban = board.stocks.copy()
            for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
                if lnl != "auto_color":
                    if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu):
                        listNLcan.append(lnl)
        return listNLcan

    def L3NLtrong1(self, board):
        listNLcan = self.layBaNguyenlieu(board)
        layBaNguyenlieu = self.layBaNguyenlieu(board)
        if len(layBaNguyenlieu) == 1:
            NLtrenban = board.stocks.copy()
            for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
                if lnl != "auto_color":
                    if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu):
                        listNLcan.append(lnl)
        return listNLcan

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

    def laythenoble(self, board):
        theNoblenenlay = []
        NLcanchotheNoble = []
        for the in board.dict_Card_Stocks_Show["Noble"]:
            x = 0
            for lnl in the.stocks.keys():
                if the.stocks[lnl] > 0:
                    x += the.stocks[lnl] - self.stocks_const[lnl]
            if x <= 1:
                theNoblenenlay.append(the)
        for the in theNoblenenlay:
            for lnl in the.stocks.keys():
                if (the.stocks[lnl] - self.stocks_const[lnl]) > 0:
                    NLcanchotheNoble.append(lnl)
        the_taget_noble = []
        thecothemo = self.thecothemo(board)
        for the in thecothemo:
            if the.type_stock in NLcanchotheNoble:
                the_taget_noble.append(the)
        return the_taget_noble