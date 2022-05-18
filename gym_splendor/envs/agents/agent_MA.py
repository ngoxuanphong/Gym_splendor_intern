from ..base.player import Player
import random
from copy import deepcopy

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        dict_type_card_show = self.statistic_type_card(state['Board'])
        blue_green_white = dict_type_card_show['blue'] + dict_type_card_show['green'] + dict_type_card_show['white']
        black_red_white = dict_type_card_show['black'] + dict_type_card_show['red'] + dict_type_card_show['white']
        if blue_green_white > black_red_white:
            sub_color = ['blue', 'green', 'white']
        else:
            sub_color = ['white', 'black', 'red']
        # print('sub_color turn {} {}'.format(turn, sub_color))
        lst_theaim = []
        # turn < = 5
        dict_value = {}
        for key in ['III', 'II', 'I']:
            if key != 'Noble':
                state['Board'].dict_Card_Stocks_Show[key].sort(reverse=True, key=lambda x:x.score)
                # neu lay duoc the nao => lay luon
                for card_ in state['Board'].dict_Card_Stocks_Show[key]:
                    if card_.score >=4:
                        if self.check_get_card(card_):
                            # print('1. minh lay the ', card_.score, card_.stocks)
                            return [], card_, []
                    elif card_.score == 3:
                        if self.check_get_card(card_):
                            # print('1. minh lay the ', card_.score, card_.stocks)
                            return [], card_, []
                    elif card_.score == 2:
                        if self.check_get_card(card_):
                            # print('1. minh lay the ', card_.score, card_.stocks)
                            return [], card_, []
                    elif card_.score == 1:
                        if self.check_get_card(card_):
                            # print('1. minh lay the ', card_.score, card_.stocks)
                            return [], card_, []
                    else:
                        if self.check_get_card(card_):
                            # print('1. minh lay the ', card_.score, card_.stocks)
                            return [], card_, []

        # neu turn < 10 : chi aim the I
        for key in state['Board'].dict_Card_Stocks_Show.keys():
            if state['Turn'] <= 17:
                # lay tai nguyen dua vao gia trị cua the
                if key == "I":
                    for card in state['Board'].dict_Card_Stocks_Show[key]:
                        dict_value[card] = self.statistic_card_value(state['Board'], card, sub_color)
            else:
                if key != 'Noble':
                    for card in state['Board'].dict_Card_Stocks_Show[key]:
                        dict_value[card] = self.statistic_card_value(state['Board'], card, sub_color)

        # lay the co value nho nhat
        card_aim = self.sorted_dict_n(dict_value, 5, descending=False)
        for card_aim_key in card_aim.keys():
            # print("card aim: ", key_.score, key_.type_stock, key_.stocks)
            if card_aim_key.score >= 2:
                # up the nay
                if self.check_upsite_down(card_aim_key):
                    # print('2. minh up the ', card_aim_key.score, card_aim_key.stocks)
                    nl_bo = self.nlbo(card_aim_key, ['auto_color'])
                    # print(nl_bo, '1111')
                    return [], card_aim_key, nl_bo, 3
                else:
                    lst_theaim.append(card_aim_key)
            else:
                # lay nguyen lieu cho the nayf
                # print('3. them the vao the aim ', card_aim_key.score, card_aim_key.stocks)
                lst_theaim.append(card_aim_key)
                # print('3.1 lst the aim ', lst_theaim)

        # lay tai nguyen minh dang co - so sanh voi tai nguyen can de lay the
        # suy ra tai nguyen can lay
        if len(self.card_upside_down) >= 1:
            theup_recent = self.card_upside_down[0]
        else:
            # print('out of index 6', lst_theaim, len(lst_theaim))
            theup_recent = lst_theaim[0]

        # print('3.2 the dang huong toi ', theup_recent.score, theup_recent.stocks)
        lst_nl_dangco = self.stocks.copy()
        for i, j in self.stocks_const.items():
            lst_nl_dangco[i] += j
        # print('4. nl dang co cua minh ', lst_nl_dangco)

        dict_nl_canlay = {}
        for stock_type, stock_num in theup_recent.stocks.items():
            if stock_type in lst_nl_dangco:
                if stock_num > lst_nl_dangco[stock_type]:
                    dict_nl_canlay[stock_type] = stock_num - lst_nl_dangco[stock_type]
            else:
                dict_nl_canlay[stock_type] = stock_num

        # print('5. nl can lay cua minh ', dict_nl_canlay)

        ## check neu co > 3 loai nguyen lieu => lay
        lst_nl_canlay_keys = list(dict_nl_canlay.keys())
        # print('5.2 list nl key can lay ', lst_nl_canlay_keys)
        if len(lst_nl_canlay_keys) >= 3:
            nl_lay = [lst_nl_canlay_keys[i] for i in range(3) if state['Board'].stocks[lst_nl_canlay_keys[i]] > 0]
            nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]])
            if len(nl_lay) == 3:
                # print('1111')
                # print(nl_lay, nl_bo)
                # print(nl_lay, nl_bo, '2222aa')
                return [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]], None, nl_bo
            else:
                lst_temp = []
                for nl_key, nl_value in state['Board'].stocks.items():
                    if nl_key not in lst_nl_canlay_keys and nl_value != 0 and nl_key != 'auto_color':
                        lst_temp.append(nl_key)
                # print('6.1 nl con co the lay ', lst_temp)
                for nl in lst_temp:
                    if nl not in lst_nl_canlay_keys:
                        lst_nl_canlay_keys.append(nl)

                lst_nl_can_lay_temp = lst_nl_canlay_keys.copy()
                lst_nl_canlay_keys = [nl for nl in lst_nl_can_lay_temp if state['Board'].stocks[nl] > 0]
                
                if len(lst_nl_canlay_keys) >= 3:
                    nl_lay = [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]]
                    nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]])
                    # print('2222')
                    # print(nl_lay, nl_bo)
                    return nl_lay, None, nl_bo

                if len(lst_nl_canlay_keys) == 2:
                    nl_lay = [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1]]
                    nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1]])
                    # print('3333')
                    # print(nl_lay, nl_bo)
                    return nl_lay, None, nl_bo

        ## check neu co < 3 loai => pick random 1 cai tu nguyen lieu con it tren ban
        else:
            nl_hiem = self.tim_nl_hiem(state['Board'], n=5)
            lst_nl_se_lay = self.check_nl_can_lay(lst_nl_canlay_keys, nl_hiem)
            # print('7 list nl se lay ', lst_nl_se_lay)
            if len(lst_nl_se_lay) >= 3:
                nl_lay = [lst_nl_canlay_keys[i] for i in range(3) if state['Board'].stocks[lst_nl_canlay_keys[i]] > 0]
                nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]])
                if len(nl_lay) == 3:
                    # print('4444')
                    # print(nl_lay, nl_bo)
                    return [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]], None, nl_bo
                else:
                    lst_temp = []
                    for nl_key, nl_value in state['Board'].stocks.items():
                        if nl_key not in list(lst_nl_se_lay.keys()) and nl_value != 0 and nl_key != 'auto_color':
                            lst_temp.append(nl_key)
                    # print('7.2 nl con co the lay ', lst_temp)
                    for nl in lst_temp:
                        if nl not in lst_nl_se_lay:
                            lst_nl_se_lay.append(nl)
                    for nl in lst_nl_se_lay:
                        if state['Board'].stocks[nl] == 0:
                            lst_nl_se_lay.remove(nl)
                    
                    if len(lst_nl_canlay_keys) >= 3:
                        nl_lay = [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]]
                        nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1], lst_nl_canlay_keys[2]])
                        # print('5555')
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo

                    if len(lst_nl_canlay_keys) == 2:
                        nl_lay = [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1]]
                        nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_canlay_keys[0], lst_nl_canlay_keys[1]])
                        # print('6666')
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo

            elif len(lst_nl_se_lay) >= 1:
                if state['Board'].stocks[lst_nl_se_lay[0]] >= 4:
                    nl_lay = [lst_nl_se_lay[0], lst_nl_se_lay[0]]
                    nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [lst_nl_se_lay[0],lst_nl_se_lay[0]])
                    # print('7777')
                    # print(nl_lay, nl_bo)
                    return nl_lay, None, nl_bo

                else:
                    # print('8.1. minh lay 3 nl')
                    lst_temp = []
                    for nl_key, nl_value in state['Board'].stocks.items():
                        if nl_key not in lst_nl_se_lay and nl_value != 0 and nl_key != 'auto_color':
                            lst_temp.append(nl_key)
                    # print('8.2 nl con co the lay ', lst_temp)
                    for nl in lst_temp:
                        if nl not in lst_nl_se_lay:
                            lst_nl_se_lay.append(nl)

                    for nl in lst_nl_se_lay:
                        if state['Board'].stocks[nl] == 0:
                            lst_nl_se_lay.remove(nl)
                    
                    try:
                        lst_nl_se_lay.remove('auto_color')
                    except:
                        pass

                    # print('8.3 minh lay 3 nl la ', lst_nl_se_lay[:4])
                    if len(lst_nl_se_lay) >= 3:
                        nl_lay = [lst_nl_se_lay[i] for i in range(3) if state['Board'].stocks[lst_nl_se_lay[i]] > 0]
                        nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), nl_lay)
                        # print('8888')
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo

                    if len(self.lay_1nl_co_the(state['Board'])) >= 1 and state['Board'].stocks[self.lay_1nl_co_the(state['Board'])[0]] >= 4:
                        nl_lay = [self.lay_1nl_co_the(state['Board'])[0], self.lay_1nl_co_the(state['Board'])[0]]
                        nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [self.lay_1nl_co_the(state['Board'])[0], self.lay_1nl_co_the(state['Board'])[0]])
                        # print('9999')
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo
                        
                    elif len(self.lay_3nl_co_the(state['Board'])) >= 3 and len([self.lay_3nl_co_the(state['Board'])[i] for i in range(3) if state['Board'].stocks[self.lay_3nl_co_the(state['Board'])[i]] > 0]) >= 3:
                        nl_lay = [self.lay_3nl_co_the(state['Board'])[0], self.lay_3nl_co_the(state['Board'])[1] ,self.lay_3nl_co_the(state['Board'])[2]]
                        nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [self.lay_3nl_co_the(state['Board'])[0], self.lay_3nl_co_the(state['Board'])[1] ,self.lay_3nl_co_the(state['Board'])[2]])
                        # print('aaaa')
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo
                        
                    elif self.lay_duynhat_1nl(state['Board']) != None:
                        if state['Board'].stocks[self.lay_duynhat_1nl(state['Board'])] > 0:
                            nl_lay = [self.lay_duynhat_1nl(state['Board'])]
                            nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [self.lay_duynhat_1nl(state['Board'])])
                            # print('bbbb')
                            # print(nl_lay, nl_bo)
                            return nl_lay, None, nl_bo
                            
                        else:
                            nl_lay = []
                            for i in range(min(3, 10-sum(self.stocks.values()))):
                                mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                                if len(mau_lay) > 0:
                                    nl_lay.append(random.choice(mau_lay))
                            
                            if nl_lay.__len__() > 0:
                                # print('cccc')
                                # print(nl_lay)
                                return nl_lay, None, []

                            for i in range(3):
                                mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                                if len(mau_lay) > 0:
                                    nl_lay.append(random.choice(mau_lay))

                            nl_bo = []
                            nl_thua = max(sum(self.stocks.values()) + nl_lay.__len__() - 10, 0)
                            pl_st = deepcopy(self.stocks)
                            for i in range(nl_thua):
                                mau_bo = [key for key in pl_st.keys() if key != 'auto_color' and pl_st[key] > 0]
                                mau_choice = random.choice(mau_bo)
                                nl_bo.append(mau_choice)
                                pl_st[mau_choice] -= 1
                            # print('dddd')
                            # print(nl_lay, nl_bo)
                            return nl_lay, None, nl_bo
                    else:
                        nl_lay = []
                        for i in range(min(3, 10-sum(self.stocks.values()))):
                            mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                            if len(mau_lay) > 0:
                                nl_lay.append(random.choice(mau_lay))
                        
                        if nl_lay.__len__() > 0:
                            # print('eeee')
                            # print(nl_lay)
                            return nl_lay, None, []

                        for i in range(3):
                            mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                            if len(mau_lay) > 0:
                                nl_lay.append(random.choice(mau_lay))

                        nl_bo = []
                        nl_thua = max(sum(self.stocks.values()) + nl_lay.__len__() - 10, 0)
                        pl_st = deepcopy(self.stocks)
                        for i in range(nl_thua):
                            mau_bo = [key for key in pl_st.keys() if key != 'auto_color' and pl_st[key] > 0]
                            mau_choice = random.choice(mau_bo)
                            nl_bo.append(mau_choice)
                            pl_st[mau_choice] -= 1
                        # print('ffff')    
                        # print(nl_lay, nl_bo)
                        return nl_lay, None, nl_bo

        if self.lay_duynhat_1nl(state['Board']) != None:
            if state['Board'].stocks[self.lay_duynhat_1nl(state['Board'])] > 0:
                nl_lay = [self.lay_duynhat_1nl(state['Board'])]
                nl_bo = self.nlbo(self.Tim_the_up(state['Board'], None), [self.lay_duynhat_1nl(state['Board'])])
                # print('gggg')
                # print(nl_lay, nl_bo)
                return nl_lay, None, nl_bo
            
            else:
                nl_lay = []
                for i in range(min(3, 10-sum(self.stocks.values()))):
                    mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                    if len(mau_lay) > 0:
                        nl_lay.append(random.choice(mau_lay))
                        
                if nl_lay.__len__() > 0:
                    # print('hhhh')
                    # print(nl_lay)
                    return nl_lay, None, []

                for i in range(3):
                    mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
                    if len(mau_lay) > 0:
                        nl_lay.append(random.choice(mau_lay))

                nl_bo = []
                nl_thua = max(sum(self.stocks.values()) + nl_lay.__len__() - 10, 0)
                pl_st = deepcopy(self.stocks)
                for i in range(nl_thua):
                    mau_bo = [key for key in pl_st.keys() if key != 'auto_color' and pl_st[key] > 0]
                    mau_choice = random.choice(mau_bo)
                    nl_bo.append(mau_choice)
                    pl_st[mau_choice] -= 1
                # print('iiii')  
                # print(nl_lay, nl_bo)          
                return nl_lay, None, nl_bo

        nl_lay = []
        for i in range(min(3, 10-sum(self.stocks.values()))):
            mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
            if len(mau_lay) > 0:
                nl_lay.append(random.choice(mau_lay))
                        
        if nl_lay.__len__() > 0:
            # print('kkkk')
            # print(nl_lay)
            return nl_lay, None, []

        for i in range(3):
            mau_lay = [key for key in state['Board'].stocks.keys() if key not in (['auto_color'] + nl_lay) and state['Board'].stocks[key] > 0]
            if len(mau_lay) > 0:
                nl_lay.append(random.choice(mau_lay))

        nl_bo = []
        nl_thua = max(sum(self.stocks.values()) + nl_lay.__len__() - 10, 0)
        pl_st = deepcopy(self.stocks)
        for i in range(nl_thua):
            mau_bo = [key for key in pl_st.keys() if key != 'auto_color' and pl_st[key] > 0]
            mau_choice = random.choice(mau_bo)
            nl_bo.append(mau_choice)
            pl_st[mau_choice] -= 1
        # print('llll')    
        # print(nl_lay, nl_bo)                
        return nl_lay, None, nl_bo

    def lay_duynhat_1nl(self, board):
        for stock_key, stock_value in board.stocks.items():
            if stock_value >= 1 and stock_key != 'auto_color':
                return stock_key
        
        return None

    def lay_1nl_co_the(self, board):
        lay1stock = []
        for stock_key, stock_value in board.stocks.items():
            if stock_value > 3 and stock_key != 'auto_color':
                lay1stock.append(stock_key)
        return lay1stock

    def lay_3nl_co_the(self, board):
        lay3stocks = []
        for stock_key, stock_value in board.stocks.items():
            if stock_value >= 1 and stock_key != 'auto_color':
                lay3stocks.append(stock_key)
        return lay3stocks

    def bo_nl(self, lst_aim_card):
        lst_nl_dang_co = self.stocks.copy()
        dict_co_the_bo = {}
        for key_stock, value_stock in lst_nl_dang_co.items():
            if key_stock not in list(lst_aim_card.keys()):
                dict_co_the_bo[key_stock] = value_stock
                if value_stock >= 3:
                    return dict_co_the_bo

        for key_stock, value_stock in lst_nl_dang_co.items():
            if key_stock not in list(dict_co_the_bo.keys()):
                if value_stock > lst_nl_dang_co[key_stock]:
                    dict_co_the_bo[key_stock] = value_stock - lst_nl_dang_co[key_stock]

        return dict_co_the_bo

    def check_nl_can_lay(self, nl_can_lay, nl_hiem):
        final_list_nl = []
        for nl_hime_ in nl_hiem:
            if nl_hime_ in nl_can_lay and nl_hime_ != 'auto_color':
                final_list_nl.append(nl_hime_)

        for key in nl_can_lay:
            if key != 'auto_color' and key not in nl_can_lay:
                nl_can_lay.append(key)

        remove_dup = []
        for nl in nl_can_lay:
            if nl not in remove_dup and nl != 'auto_color':
                remove_dup.append(nl)
                
        return remove_dup

    def tim_nl_hiem(self, board, n):
        dict_board_stock_remove_autocolor = {}
        for stock_key, stock_value in board.stocks.items():
            if stock_key != 'auto_color':
                dict_board_stock_remove_autocolor[stock_key] = stock_value
        # print('5.1 nl hiem bo auto color ', dict_board_stock_remove_autocolor)
        lst = list(self.sorted_dict_n(dict_board_stock_remove_autocolor, n=n, descending=False).keys())
        return lst

    def sorted_dict_n(self, dictionary, n, descending=None):
        final = {}
        ilistofTuples = sorted(dictionary.items(), key=lambda x: x[1])

        if descending == True:
            lst = ilistofTuples[:n]
            for elem in lst:
                final[elem[0]] = elem[1]
        elif descending == False:
            lst = ilistofTuples[::-1][:n]
            for elem in lst:
                final[elem[0]] = elem[1]
        return final
    
    def Tim_the_up(self, board, mau_the_quan_trong):
        list_card_can_check = []
        for type_card in board.dict_Card_Stocks_Show.keys():
            if type_card != 'Noble':
                for car in board.dict_Card_Stocks_Show[type_card]:
                    if not self.check_get_card(car):
                        list_card_can_check.append(car)

        if len(list_card_can_check) != 0:
            card = self.chon_the_gia_tri_cao(list_card_can_check)
            return card
        
        return None
        
    def chon_the_gia_tri_cao(self, list_the):
        value_cards = [car.score / sum(list(car.stocks.values())) for car in list_the]
        max_value = max(value_cards)

        return list_the[value_cards.index(max_value)]

    def statistic_card_value(self, board, card, sub_color):
        # note : giá trị / giá cả ( số điểm / số nguyên liệu cần - số nl const stocks)
        const_stocks = self.stocks_const.copy()
        count_soluongnl = 0
        real_value = {}
        if card.type_stock in sub_color:
            for key, value in card.stocks.items():
                if key in list(const_stocks.keys()):
                    if const_stocks[key] < value:
                        real_value[key] = value - const_stocks[key]
                else:
                    real_value[key] = value
        tong_nl_thuc = sum(real_value.values())

        if card.type_stock in sub_color:
            for key, value in real_value.items():
                if value > 0:
                    count_soluongnl += 1
        # index 1 = tong so nguyen lieu can / so luong nguyen lieu ( can nho )
        index1 = tong_nl_thuc / (count_soluongnl + 1)

        # index2 = tong so tai nguyen / tong so diem ( can nho )
        index2 = tong_nl_thuc / (card.score + 1)

        # index3 = ty le tai nguyen tren ban
        # index3.1 = so luong tai nguyen 1 can tren the / so luong tai nguyen 1 dang co tren ban ( can nho )
        lst_index3 = []
        for key_stock, number_stock in card.stocks.items():
            num_stock_avai_board = board.stocks[key_stock]
            if num_stock_avai_board > 0:
                lst_index3.append(number_stock / num_stock_avai_board)
        index3 = sum(lst_index3) / (len(lst_index3)+0.01)

        # index = trung binh 3 index
        index = (0.95 * index1 + 0.05 * index2 + 0.05 * index3)
        return index

    def statistic_stock_in_card_show(self, board):
        dict_nl = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
        }
        for key in board.dict_Card_Stocks_Show.keys():
            for card in board.dict_Card_Stocks_Show[key]:
                for nl in dict_nl.keys():
                    dict_nl[nl] += card.stocks[nl]
        return dict_nl

    def statistic_type_card(self, board):
        dict_nl = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0,
        }
        for key in board.dict_Card_Stocks_Show.keys():
            if key != "Noble":
                for card in board.dict_Card_Stocks_Show[key]:
                    dict_nl[card.type_stock] += 1
        return dict_nl

    def nlbo(self, card, stocks):
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