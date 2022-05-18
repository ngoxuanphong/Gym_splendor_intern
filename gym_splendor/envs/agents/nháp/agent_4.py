from ..base.player import Player
import random
import math
import numpy as np


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    loaithe = ['I', 'II', 'III', 'Noble']
    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        board = state['Board']
        return stocks, card, stock_return


    def thecotheup(self, board):
        for tile in np.arange(2,3.5,0.1):
            for Loaithe in board.dict_Card_Stocks_Show.keys():
                for card in board.dict_Card_Stocks_Show[Loaithe]:
                    if (sum(card.stocks.values()) / card.score) > diem :
                        if self.check_upsite_down(card):
                            return card

    def thecothemo(self, board):
        listthecothemo = []
        if len(self.card_upside_down) > 0:
            for card in self.card_upside_down:
                if self.check_get_card(card):
                    listthecothemo.append(card)
        for Loaithe in board.dict_Card_Stocks_Show.keys():
            if Loaithe != "Noble":
                for card in board.dict_Card_Stocks_Show[Loaithe]:
                        if self.check_get_card(card) == True:
                            listthecothemo.append(card)
        return listthecothemo

    #sap xep cac the co the mo va co diem
    def SXthecothemo(self, board):
        soluongnguyenlieucan = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for danhgia in np.arange(0,4,0.1):
            for the in thecothemo(self,board):
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
        for lnl in NLtheup1(self,board):
            if NLtheup1(self,board)[lnl] >= 2:
                if self.check_input_stock(board, lnl):
                    OneNguyenlieucothelay.append(lnl)
        return OneNguyenlieucothelay

    def Lay3NLtheup1(self, board):
        listcacNLnenlay = []
        for lnl in NLtheup1(self, board):
            if NLtheup1(self, board)[lnl] > 0 and board.stocks[lnl] > 0:
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
        return dict(sorted(Nguyenlieucan(self, board).items(), key=lambda x:x[1], reverse=True))

    def laymotnguyenlieu(self, board):
        OneNguyenlieucothelay = []
        if sum(self.stocks.values()) <= 8:
            for lnl in dictsapxepnguyenlieu(self, board):
                if dictsapxepnguyenlieu(self, board)[lnl] >= 2:
                    if self.check_input_stock(self, board, lnl):
                        OneNguyenlieucothelay.append(lnl)
        return OneNguyenlieucothelay

    def layBaNguyenlieu(self, board):
        listcacNLnenlay = []
        for lnl in dictsapxepnguyenlieu(self, board):
            if dictsapxepnguyenlieu(self, board)[lnl] > 0 and board.stocks[lnl] > 0:
                listcacNLnenlay.append(lnl)
        return listcacNLnenlay

    def Laythehotro(self, board):
        listNLcan = []
        listthehotro = []
        listthehotrolay = []
        for lnl in dictsapxepnguyenlieu(self, board):
            if dictsapxepnguyenlieu(self, board)[lnl] > 0:
                listNLcan.append(lnl)
        for the in thecothemo(self, board):
            if the.type_stock in listNLcan:
                listthehotro.append(the)
        for the in listthehotro:
            if self.check_get_card(the) == True:
                listthehotrolay.append(the)
        return listthehotrolay

    def Laythebinhthuong(self, board):
        a = []
        if len(thecothemo(self, board)) > 0:
            the = thecothemo(self, board)[0]
            for card in thecothemo(self, board):
                NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
                for lnl in NLcanmo1the.keys():
                    NLcanmo1the[lnl] = card.stocks[lnl] - self.stocks_const[lnl]
                a.append(sum(NLcanmo1the.values()))
            x = min(a)
            for card in thecothemo(self, board):
                NLcanmo1the = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
                for lnl in NLcanmo1the.keys():
                    NLcanmo1the[lnl] = card.stocks[lnl] - self.stocks_const[lnl]
                if a == sum(NLcanmo1the.values()):
                    return card
        return None
        
    def SXNLtrenban(self, board):
        listNLcan = layBaNguyenlieu(self, board)
        NLtrenban = board.stocks.copy()
        for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
            if lnl != "auto_color":
                if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(self, board)):
                    listNLcan.append(lnl)
        return listNLcan
    def Lay1NLbatky(self, board):
        ln = []
        NLtrenban = board.stocks.copy()
        for lnl in NLtrenban.keys():
            if lnl != "auto_color":
                if NLtrenban[lnl] >=4:
                    if self.check_input_stock(self, board, lnl):
                        ln.append(lnl)
        return ln
    def L3NLtrong2(self, board):
        listNLcan = layBaNguyenlieu(self, board)
        if len(layBaNguyenlieu(self, board)) == 2:
            NLtrenban = board.stocks.copy()
            for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
                if lnl != "auto_color":
                    if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(self, board)):
                        listNLcan.append(lnl)
        return listNLcan

    def L3NLtrong1(self, board):
        listNLcan = layBaNguyenlieu(self, board)
        if len(layBaNguyenlieu(self, board)) == 1:
            NLtrenban = board.stocks.copy()
            for lnl in (dict(sorted(NLtrenban.items(), key=lambda x:x[1], reverse=False))).keys():
                if lnl != "auto_color":
                    if board.stocks[lnl] > 0 and (lnl not in layBaNguyenlieu(self, board)):
                        listNLcan.append(lnl)
        return listNLcan 

    #Nguyen lieu can cua the up tru cho stocks count
    def NLcan(self, board):
        NL_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        NL_can = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        for lnl in self.stocks.keys():
            if lnl != "auto_color":
                for the in self.card_upside_down:
                    NL_the_up[lnl] += the.stocks[lnl]
                NL_can[lnl] = NL_the_up[lnl] - self.stocks_const[lnl]
        return NL_can

    def Tranguyenlieu(self,board):
        listthebo = []
        dictnguyenlieuthua = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}
        nguyen_lieu_the_up = {"red": 0, "blue": 0, "green": 0, "white": 0, "black": 0,}

        for lnl in dictnguyenlieuthua.keys():
            if self.stocks[lnl] > 0:
                dictnguyenlieuthua[lnl] = self.stocks[lnl] - NLcan(self,board)[lnl]

        SXNL_thua= dict(sorted(dictnguyenlieuthua.items(), key=lambda x:x[1], reverse=True))
        for lnl in SXNL_thua.keys():
            listthebo.append(lnl)
        SXNLcan = dict(sorted(NLcan(self,board).items(), key=lambda x:x[1], reverse=False))
        for lnl in SXNLcan.keys():
            if self.stocks[lnl] > 0  and (lnl not in list(SXNL_thua.keys())):
                listthebo.append(lnl)
        return listthebo

    def Luachonbothe(board, *args):
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
        danhsachcon = Tranguyenlieu(self,board)
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
        return dict_bo

    def laythenoble(self,board):
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
        for the in thecothemo(self,board):
            if the.type_stock in NLcanchotheNoble:
                the_taget_noble.append(the)
        return the_taget_noble