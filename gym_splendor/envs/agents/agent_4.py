from ..base.player import Player
import random
import math
from collections import Counter


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []

        list_build_IV=[]
        dict_tn_target = {}#loại thẻ noble chỉ có 2 tài nguyên
        count_type_tn_build_IV = {'red': 0, 'blue': 0, 'green': 0, 'black': 0,
                                  'white': 0}  # loại thẻ noble có 3 tài nguyên
        tn_target = [] # tài nguyên chọn để build thực sự.
        list_tnvv_III = []
        list_tnvv_II = []
        list_tnvv_I = []

        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card == 'Noble':
                list_tn_target_ = []
                for card in state['Board'].dict_Card_Stocks_Show['Noble']:
                    count_card_tn_eval_2 = 0
                    for k in card.stocks.keys():
                        if card.stocks[k] > 0:
                            count_card_tn_eval_2 +=1

                    if count_card_tn_eval_2 == 2:
                        for k in card.stocks.keys():
                            if card.stocks[k] > 0:
                                list_tn_target_.append(k)
                        dict_tn_target = dict((x, list_tn_target_.count(x)) for x in set(list_tn_target_))
                    else:
                        list_build_IV.append(card.stocks)
                for tn_build_each_card_IV in list_build_IV:
                    if tn_build_each_card_IV['red'] > 0:
                        count_type_tn_build_IV['red'] += 1
                    if tn_build_each_card_IV['blue'] > 0:
                        count_type_tn_build_IV['blue'] += 1
                    if tn_build_each_card_IV['green'] > 0:
                        count_type_tn_build_IV['green'] += 1
                    if tn_build_each_card_IV['black'] > 0:
                        count_type_tn_build_IV['black'] += 1
                    if tn_build_each_card_IV['white'] > 0:
                        count_type_tn_build_IV['white'] += 1

                print("######################################################")
                dict_tn_target = dict(sorted(dict_tn_target.items(), key=lambda x: x[1], reverse=True))
                count_type_tn_build_IV = dict(sorted(count_type_tn_build_IV.items(), key=lambda x: x[1], reverse=True))
                print(dict_tn_target)  # loại thẻ noble chỉ có 2 tài nguyên
                print(count_type_tn_build_IV)  # loại thẻ có 3 tài nguyên

                #chọn tài nguyên, ưu tiên loại tài nguyên trong thẻ có 2 tài nguyên
                #xét thẻ có 2 tài nguyên

                if len(dict_tn_target) != 0:
                    if len(dict_tn_target) == 2:
                        tn_target.append(x for x in dict_tn_target.keys())
                    else: # nếu len(dict_tn_target) > 2
                        #nếu tất cả giá trị = 1 thì xét sang list kia
                        for k,v in dict_tn_target.items():
                            if not v != 1:
                                while (len(tn_target) <= 3):
                                    for m in count_type_tn_build_IV.keys():
                                        tn_target.append(m)
                            else:
                                for m in dict_tn_target.keys():
                                    if len(tn_target) <=3:
                                        tn_target.append(m)
                #else:
                 #   for

            print("-------------------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&--------------------------")
            print(tn_target)


        return stocks, card, stock_return
def check_max_value_dict(dic):
    max_value = max(dic.values())
    max_keys = [k for k, v in dic.items() if v == max_value]
    return max_keys#, max_value

