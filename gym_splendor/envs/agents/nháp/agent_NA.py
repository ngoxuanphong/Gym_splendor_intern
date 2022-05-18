from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        if self.hanh_dong(state['Board'], state) == None:
            return [], None, []
        
        a = self.hanh_dong(state['Board'], state)
        if a[0] == '3':
            stocks = self.list_nl_con(state['Board'])
            temp = self.lua_chon_bo_the(state['Board'], stocks[0], stocks[1], stocks[2])
            stocks_return = []
            for key in temp.keys():
                if temp[key] != 0:
                    for i in range(temp[key]):
                        stocks_return.append(key)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            print(stocks, stocks_return)
            return stocks, [], stocks_return

        if a[0] == '2':
            stocks = [a[1:], a[1:]]
            temp = self.lua_chon_bo_the(state['Board'], a[1:], a[1:])
            stocks_return = []
            for key in temp.keys():
                if temp[key] != 0:
                    for i in range(temp[key]):
                        stocks_return.append(key)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            print(stocks, stocks_return)
            return stocks, [], stocks_return
        
        if a[0] == 'U':
            for the in self.list_the_co_the_up(state['Board']):
                if the._Card__id == a[1:]:
                    temp = self.lua_chon_bo_the(state['Board'], 'auto_color')
                    stocks_return = []
                    for key in temp.keys():
                        if temp[key] != 0:
                            for i in range(temp[key]):
                                stocks_return.append(key)
                    
                    return [], the, stocks_return
        
        if a[0] == 'M':
            for the in self.list_the_co_the_mua(state['Board']):
                if the._Card__id == a[1:]:
                    return [], the, []

        return [], None, []

    def hanh_dong(self, board, state):
        a = self.dict_up(board)
        if self.dict_mo(board) != None:
            a.update(self.dict_mo(board))
        if self.dict_lay_2(board, state) != None:
            a.update(self.dict_lay_2(board, state))
        if self.dict_lay_3(board) != None:
            a.update(self.dict_lay_3(board))
        
        b = {k:v for k,v in sorted(
            a.items(), key = lambda item: item[1], reverse=True
        )}

        if len(b) > 0:
            return (list(b.keys()))[0]
        else:
            return None

    def dict_lay_3(self, board):
        a = {}
        if self.list_nl_con(board).__len__() > 2:
            b = self.lua_chon_bo_the(board, self.list_nl_con(board)[0], self.list_nl_con(board)[1], self.list_nl_con(board)[2])
            chi_phi = 0
            if b != None:
                for nguyenlieu in b.keys():
                    chi_phi += self.cham_diem(board, nguyenlieu) * b[nguyenlieu]
            
            a = {'3':(self.cham_diem(board, self.list_nl_con(board)[0])
                + self.cham_diem(board, self.list_nl_con(board)[1])+self.cham_diem(board, self.list_nl_con(board)[2]) - chi_phi)}

        return a

    def dict_lay_2(self, board, state):
        dict_lay_2 = {}
        a = self.lua_chon_bo_the(board, 'auto_color', 'auto_color')
        chi_phi = 0
        if a != None:
            for nguyenlieu in a.keys():
                chi_phi += a[nguyenlieu] * self.cham_diem(board, nguyenlieu)
            
        for nguyenlieu in self.list_lay_2(board, state):
            dict_lay_2['2' + str(nguyenlieu)] = self.cham_diem(board, nguyenlieu) * 2 - chi_phi
        
        return dict_lay_2

    def lua_chon_bo_the(self, board, *args):
        dict_bo = {
        "red": 0, "blue": 0, "white": 0, "green": 0, "black": 0, "auto_color": 0
        }

        dict_bd = deepcopy(self._Player__stocks)

        for x in args:
            dict_bd[x] += 1

        diem_nl = {}
        for nl in dict_bd.keys():
            diem_nl[nl] = self.cham_diem(board, nl)
        
        abc = {k:v for k,v in sorted(
            diem_nl.items(), key = lambda item: item[1], reverse=True
        )}

        danh_sach_con = list(abc.keys())

        if sum(dict_bd.values()) > 10:
            n = sum(dict_bd.values()) - 10
            i = 0
            while n != 0:
                if dict_bd[danh_sach_con[i]] != 0:
                    dict_bo[danh_sach_con[i]] += 1
                    dict_bd[danh_sach_con[i]] -= 1
                    n -= 1
                else:
                    i += 1
        
        return dict_bo

    def list_nl_con(self, board):
        nl = {}
        for nguyenlieu in board._Board__dict_Card_Stocks_Show['III'][0]._Card__stocks.keys():
            if board._Board__stocks[nguyenlieu] > 0:
                nl[nguyenlieu] = self.cham_diem(board, nguyenlieu)
        
        a = {k:v for k,v in sorted(
            nl.items(), key=lambda item: item[1], reverse=True
        )}

        return list(a.keys())

    def dict_up(self, board):
        if self._Player__card_upside_down.__len__() >= 3:
            return {}
        
        dict_up = {}
        for the in self.list_the_co_the_up(board):
            dict_up['U'+str(the._Card__id)] = self.cham_diem(board, the._Card_Stock__type_stock) / sum(the._Card__stocks.values()) + self.cham_diem(board, 'auto_color') * min(1, board._Board__stocks['auto_color'])
            if the == self.the_t2(board):
                return {'U' + str(the._Card__id): self.cham_diem(board, the._Card_Stock__type_stock) / sum(the._Card__stocks.values()) + self.cham_diem(board, 'auto_color') * min(1, board._Board__stocks['auto_color'])}
            
            return dict_up

    def dict_mo(self, board):
        dict_mo = {}
        for the in self.list_the_co_the_mua(board):
            chi_phi = 0
            for nguyenlieu in the._Card__stocks.keys():
                if the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] > self._Player__stocks[nguyenlieu]:
                    chi_phi += (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - 
                                self._Player__stocks[nguyenlieu]) * self.cham_diem(board, 'auto_color')
                    chi_phi += self._Player__stocks[nguyenlieu] * self.cham_diem(board, nguyenlieu)
                
                else:
                    chi_phi += (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu]) * self.cham_diem(board, nguyenlieu)

            dict_mo['M' + str(the._Card__id)] = the._Card__score - chi_phi
        
        return dict_mo

    def cham_diem(self, board, nglieu):
        dict_nl = {}
        for nguyenlieu in board._Board__dict_Card_Stocks_Show['III'][0]._Card__stocks.keys():
            the = self.the_t2(board)
            so_nl_thieu = 0

            for nl in the._Card__stocks.keys():
                so_nl_thieu += max(0, the._Card__stocks[nl] - self._Player__stocks_const[nl])
            
            diem = (the._Card__score / so_nl_thieu - the._Card__score / (so_nl_thieu + 1)) * max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu])) / so_nl_thieu
            dict_nl[nguyenlieu] = diem
        
        dict_nl['auto_color'] = max(dict_nl.values()) * (1 - len(self._Player__card_upside_down) * 0.33)
        return dict_nl[nglieu]

    def list_lay_2(self, board, state):
        nl = []
        for nguyenlieu in board._Board__dict_Card_Stocks_Show['III'][0]._Card__stocks.keys():
            if self.check_input_stock([nguyenlieu, nguyenlieu], state) != 0:
                nl.append(nguyenlieu)

        return nl

    def the_t2(self, board):
        diem_max = 0
        the_max = None
        for the in self.danh_sach_the(board):
            if the not in self.list_the_co_the_mua(board):
                so_nl_thieu = 0
                tong_nl_can = 0
                for nguyenlieu in the._Card__stocks.keys():
                    tong_nl_can = max(0, the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu]) + tong_nl_can
                    if max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu])) > so_nl_thieu:
                        so_nl_thieu = max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu]))
                
                diem = min(15 - self._Player__score, the._Card__score) / (1 + so_nl_thieu)

                diem += diem*(self.nl_nn_III(board)[the._Card_Stock__type_stock] - 0.2)

                if tong_nl_can > 10:
                    diem = 0
                
                if diem > diem_max:
                    diem_max = diem
                    the_max = the

        return the_max

    def danh_sach_the(self, board):
        danh_sach_the = []
        danh_sach_the.extend(self._Player__card_upside_down)
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['III'])
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['II'])
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['I'])

        return danh_sach_the

    def list_the_co_the_up(self, board):
        a = []
        a.extend(board._Board__dict_Card_Stocks_Show['III'])
        a.extend(board._Board__dict_Card_Stocks_Show['II'])
        a.extend(board._Board__dict_Card_Stocks_Show['I'])

        return a

    def list_the_co_the_mua(self, board):
        a = self.danh_sach_the(board)
        b = []
        for the in a:
            if self.check_get_card(the):
                b.append(the)

        return b

    def nl_nn_III(self, board):
        dict_nl = {
        "red" :0, "blue":0, "white":0, "green":0, "black":0,
        }

        for cap in board._Board__dict_Card_Stocks_Show.keys():
            for the in board._Board__dict_Card_Stocks_Show[cap]:
                for nlieu in the._Card__stocks.keys():
                    dict_nl[nlieu] += the._Card__stocks[nlieu]

        for the in self._Player__card_upside_down:
            for nlieu in the._Card__stocks.keys():
                dict_nl[nlieu] += the._Card__stocks[nlieu]
        
        max_ = 0
        key = ''

        dict_static = {}
        for i in dict_nl.keys():
            dict_static[i] = dict_nl[i] / sum(dict_nl.values())

        return dict_static