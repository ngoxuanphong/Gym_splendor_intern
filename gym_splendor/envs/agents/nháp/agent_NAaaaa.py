from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        if self.hanh_dong(state['Board'], state) == None:
            
            stocks = []
            for i in range(min(3, 10-sum(self._Player__stocks.values()))):
                temp_list = [mau for mau in state['Board']._Board__stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board']._Board__stocks[mau] > 0]
                if temp_list.__len__() > 0:
                    stocks.append(random.choice(temp_list))
            # print('1111', stocks)
            return stocks, None, []
        
        a = self.hanh_dong(state['Board'], state)
        if a != None and a[0] != None and a[0] == '3':
            stocks_ = self.list_nl_con(state['Board'])
            stocks = [stocks_[0], stocks_[1], stocks_[2]]
            temp = self.lua_chon_bo_the(state['Board'], stocks[0], stocks[1], stocks[2])
            stocks_return = []

            if temp != None:
                for key in temp.keys():
                    if temp[key] != 0:
                        for i in range(temp[key]):
                            stocks_return.append(key)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            # print('2222', stocks, stocks_return)
            return stocks, None, stocks_return

        if a != None and a[0] != None and a[0] == '2':
            stocks = [str(a[1:]), str(a[1:])]
            temp = self.lua_chon_bo_the(state['Board'], a[1:], a[1:])
            stocks_return = []
            if temp != None:
                for key in temp.keys():
                    if temp[key] != 0:
                        for i in range(temp[key]):
                            stocks_return.append(key)
            
            nl_trung_nhau = list(set(stocks) & set(stocks_return))
            for i in nl_trung_nhau:
                stocks.remove(i)
                stocks_return.remove(i)
            # print(nl_trung_nhau)
            # print('3333', stocks, stocks_return)
            if stocks == stocks_return:
                return [], None, []
            return stocks, None, stocks_return
        
        if a != None and a[0] != None and a[0] == 'U':
            for the in self.list_the_co_the_up(state['Board']):
                if the._Card__id == a[1:]:
                    temp = self.lua_chon_bo_the(state['Board'], 'auto_color')
                    stocks_return = []

                    if temp != None:
                        for key in temp.keys():
                            if temp[key] != 0:
                                for i in range(temp[key]):
                                    stocks_return.append(key)
                    # print('4444', stocks_return)
                    return [], the, stocks_return
        
        if a != None and a[0] != None and a[0] == 'M':
            for the in self.list_the_co_the_mua(state['Board']):
                if the._Card__id == a[1:]:
                    # print('5555')
                    return [], the, []

        stocks = []
        for i in range(min(3, 10-sum(self._Player__stocks.values()))):
            temp_list = [mau for mau in state['Board']._Board__stocks.keys() if mau not in (['auto_color'] + stocks) and state['Board']._Board__stocks[mau] > 0]
            if temp_list.__len__() > 0:
                stocks.append(random.choice(temp_list))
        # print('6666', stocks)
        return stocks, None, []

    def hanh_dong(self, board, state):
        a = self.dict_up(board)

        dict_mo = self.dict_mo(board)
        if dict_mo != None:
            a.update(dict_mo)
        
        dict_lay_2 = self.dict_lay_2(board, state)
        if dict_lay_2 != None:
            a.update(dict_lay_2)

        dict_lay_3 = self.dict_lay_3(board)
        if dict_lay_3 != None:
            a.update(dict_lay_3)
        
        b = {k:v for k,v in sorted(
            a.items(), key = lambda item: item[1], reverse=True
        )}

        if len(b) > 0:
            return (list(b.keys()))[0]
        else:
            return None

    def dict_lay_3(self, board):
        a = {}
        list_nl_con = self.list_nl_con(board)
        if list_nl_con.__len__() > 2:
            b = self.lua_chon_bo_the(board, list_nl_con[0], list_nl_con[1], list_nl_con[2])
            chi_phi = 0
            if b != None:
                for nguyenlieu in b.keys():
                    chi_phi += self.cham_diem(board, nguyenlieu) * b[nguyenlieu]
            
            a = {'3':(self.cham_diem(board, list_nl_con[0])
                + self.cham_diem(board, list_nl_con[1])+self.cham_diem(board, list_nl_con[2]) - chi_phi)}
        
        if a == {}:
            return None

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
        
        if dict_lay_2 == {}:
            return None

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
            diem_nl.items(), key = lambda item: item[1], reverse=False
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

        dict_bo_cuoi = {k:v for k,v in dict_bo.items() if v != 0}

        if list(dict_bo_cuoi.keys()).__len__() == 0:
            return None
        
        return dict_bo_cuoi

    def list_nl_con(self, board):
        nl = {}
        temp = ['red', 'blue', 'green', 'white', 'black']
        for nguyenlieu in temp:
            if board._Board__stocks[nguyenlieu] > 0:
                nl[nguyenlieu] = self.cham_diem(board, nguyenlieu)

        a = {k:v for k,v in sorted(
            nl.items(), key=lambda item: item[1], reverse=True
        )}

        return list(a.keys())

    def dict_up(self, board):
        if self._Player__card_upside_down.__len__() >= 3:
            return {}

        list_co_the_up = self.list_the_co_the_up(board)
        dict_up = {}
        thet2 = self.the_t2(board)
        for the in list_co_the_up:
            dict_up['U'+str(the._Card__id)] = self.cham_diem(board, the._Card_Stock__type_stock) / sum(the._Card__stocks.values()) + self.cham_diem(board, 'auto_color') * min(1, board._Board__stocks['auto_color'])
            if the == thet2:
                return {'U' + str(the._Card__id): self.cham_diem(board, the._Card_Stock__type_stock) / sum(the._Card__stocks.values()) + self.cham_diem(board, 'auto_color') * min(1, board._Board__stocks['auto_color'])}
        
        return dict_up

    def dict_mo(self, board):
        dict_mo = {}
        list_the_can_buy = self.list_the_co_the_mua(board)
        temp = ['red', 'blue', 'green', 'white', 'black']
        for the in list_the_can_buy:
            chi_phi = 0
            for nguyenlieu in temp:
                if the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] > self._Player__stocks[nguyenlieu]:
                    chi_phi += (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu]) * self.cham_diem(board, 'auto_color')
                    chi_phi += self._Player__stocks[nguyenlieu] * self.cham_diem(board, nguyenlieu)
                else:
                    chi_phi += (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu]) * self.cham_diem(board, nguyenlieu)

            dict_mo['M' + str(the._Card__id)] = the._Card__score - chi_phi
        
        if dict_mo == {}:
            return None
        
        return dict_mo

    def cham_diem(self, board, nglieu):
        dict_nl = {}
        temp = ['red', 'blue', 'green', 'white', 'black']
        the = self.the_t2(board)
        for nguyenlieu in temp:
            so_nl_thieu = 0

            for nl in temp:
                so_nl_thieu += max(0, the._Card__stocks[nl] - self._Player__stocks_const[nl])

            diem = (the._Card__score / so_nl_thieu - the._Card__score / (so_nl_thieu + 1)) * max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu])) / so_nl_thieu
            dict_nl[nguyenlieu] = diem
        
        dict_nl['auto_color'] = max(dict_nl.values()) * (1 - len(self._Player__card_upside_down) * 0.33)
        return dict_nl[nglieu]

    def list_lay_2(self, board, state):
        nl = []
        temp = ['red', 'blue', 'green', 'white', 'black']
        for nguyenlieu in temp:
            if self.check_input_stock_no_print([nguyenlieu, nguyenlieu], state) != 0:
                nl.append(nguyenlieu)

        return nl

    def the_t2(self, board):
        diem_max = 0
        the_max = None
        list_the = self.danh_sach_the(board)
        list_the_can_buy = self.list_the_co_the_mua(board)
        nl_nn_3 = self.nl_nn_III(board)

        for the in list_the:
            if the not in list_the_can_buy:
                the_max = the
                break

        for the in list_the:
            if the not in list_the_can_buy:
                so_nl_thieu = 0
                tong_nl_can = 0
                for nguyenlieu in the._Card__stocks.keys():
                    tong_nl_can += max(0, the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu])
                    if max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu])) > so_nl_thieu:
                        so_nl_thieu = max(0, (the._Card__stocks[nguyenlieu] - self._Player__stocks_const[nguyenlieu] - self._Player__stocks[nguyenlieu]))

                diem = min(15 - self._Player__score, the._Card__score) / (1 + so_nl_thieu)
                diem += diem*(nl_nn_3[the._Card_Stock__type_stock] - 0.2)
                
                if tong_nl_can > 10:
                    diem = 0
                
                if diem > diem_max:
                    diem_max = diem
                    the_max = the

        return the_max

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

    def danh_sach_the(self, board):
        danh_sach_the = []
        danh_sach_the.extend(self._Player__card_upside_down)
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['III'])
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['II'])
        danh_sach_the.extend(board._Board__dict_Card_Stocks_Show['I'])

        return danh_sach_the

    def nl_nn_III(self, board):
        dict_nl = {
        "red" :0, "blue":0, "white":0, "green":0, "black":0,
        }

        for type_card in board._Board__dict_Card_Stocks_Show.keys():
            for the in board._Board__dict_Card_Stocks_Show[type_card]:
                for nlieu in the._Card__stocks.keys():
                    dict_nl[nlieu] += the._Card__stocks[nlieu]
        
        dict_static = {}
        tong = sum(dict_nl.values())
        for i in dict_nl.keys():
            dict_static[i] = dict_nl[i] / tong

        return dict_static