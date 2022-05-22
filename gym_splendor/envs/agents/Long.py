from cgitb import small
from pickletools import TAKEN_FROM_ARGUMENT1
from ..base.player import Player
import random
import math


# Note:
# Board:
#            dict_Card_Stocks_Show: Truy cập các thẻ đang ở trên bàn
#            Stocks: nguyên liệu
# 
# 
# Player: 1 object
# Attribute: điểm: self.score
#            nguyên liệu: self.stocks    
#            nguyên liệu mặc định: self.stocks_const
#            thẻ đã mở (thẻ tính điểm): self.card_open
#            thẻ đang úp: self.card_upside_down
#            thẻ noble: self.noble
#
#
# Card: 1 object
# Attribute:    ID:
#               score:
#               stocks:
#               type_stock
#
#
# state: dictionary
#               Turn
#               Board
#               Player (Người chơi khác)
#               truy cập: state["Board"].Các_method_và_attribute_trong_class_Board
#
#


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.pathway = None
        self.tier1 = 0


    def check_get_card_no_auto_color(self, Card):
        if self.checkthehople(Card) == False:
            return False
        for i in Card.stocks.keys():
            if self.stocks[i] + self.stocks_const[i] < Card.stocks[i]:
                if self.stocks[i] + self.stocks_const[i] >= Card.stocks[i]:
                    continue
                else:
                    return False
        return True

    
    def get_stock_for_target_card(self, card_tg, state, stocks):
        card_st=card_tg.stocks
        if len(stocks) == 0:
            for stock in card_st:
                if card_st[stock] - self.stocks[stock]- self.stocks_const[stock] > 1 \
                    and state['Board'].stocks[stock] > 0:
                    if len(stocks) < 1:
                        if state['Board'].stocks[stock] > 3:
                            stocks.append(stock)
                            stocks.append(stock)
                        elif state['Board'].stocks[stock] < 4:
                            stocks.append(stock)
                elif card_st[stock] - self.stocks[stock] - self.stocks_const[stock] > 0 \
                    and state['Board'].stocks[stock] > 0:
                    if len(stocks) < 3:
                        if len(stocks) == 2 and stocks[0] == stocks[1]:
                            pass
                        else:
                            if stock not in stocks:
                                stocks.append(stock) 
        else:
            for stock in card_st:
                if card_st[stock]- self.stocks[stock]\
                    - self.stocks_const[stock] > 0 \
                        and state['Board'].stocks[stock] > 0:
                    if stock not in stocks and len(stocks) < 2:
                        stocks.append(stock)
        return stocks


    def return_stock_not_in_target_card(self, target_list, num):
        stock_return = []
        for target_card in target_list:
            while num > 0:
                stock_in_card = target_card.stocks
                for stock in stock_in_card:
                    if target_card.stocks[stock] == 0 and self.stocks[stock] > 1:
                        stock_return.append(stock)
                        num -= 1
        return stock_return




    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        print("Turn: {}".format(state["Turn"]))
        path_way = None


        # Hiển thị các thẻ có trên bàn
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    print("{} \tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format\
                    (type_card, card1.id, card1.score, card1.stocks, card1.type_stock))


        # Hiển thị các thẻ đã lật và nguyên liệu đang có
        if len(self.card_open) != 0:
            print("Các thẻ đã lật của Long: ")
            for i in self.card_open:
                print("Score: {} {} {}".format(i.score, i.id, i.type_stock), end = ",")
        else:
            print("Long chưa lật thẻ nào")
        print("\nNguyên liệu hữu hạn: {}".format(self.stocks))
        print("Nguyên liệu vĩnh viễn: {}".format(self.stocks_const))

        # Hiển thị các thẻ đang úp
        if len(self.card_upside_down) != 0:
            print("Các thẻ đang úp của Long là: ")    
            for i in self.card_upside_down:
                print("Score: {} {} {} {}".format(i.score, i.id, i.type_stock, i.stocks))
        else:
            print("Long chưa úp thẻ nào")
       

        # Lấy thông tin thẻ loại 2 và 3 để xác định lối chơi là d/d/t hay l/l/t
        sum_d_d = 0
        sum_l_l = 0
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble" and type_card != "I":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    if card1.score >= 2:
                        for stock_in_card in card1.stocks:
                            if stock_in_card in ["red", "black"]:
                                sum_d_d += card1.stocks[stock_in_card]
                            elif stock_in_card in ["green", "blue"]:
                                sum_l_l += card1.stocks[stock_in_card]
       

        # Xác định lối chơi
        if sum_d_d > sum_l_l and state["Turn"] < 5:
            self.pathway = True
        elif sum_d_d <= sum_l_l and state["Turn"] < 5:
            self.pathway = False
        print(" ---------- Pathway ----------- : {}".format(self.pathway))
        if self.pathway:    
            # Chơi tam tấu d/d/t
            # Chơi style 1-2-3-4-5 hoặc 2-2-2-4-5
            # Lấy 3 đến 4 thẻ loại I (Trong đó có thể 1 thẻ 1 điểm)
            # Tạo 1 list các thẻ cần lấy
            
            
            
            # -------------------------------------------------------------------------------------------
            # Tạo list các thẻ cần lấy cho tam tấu d/d/t
            needed_card_l = []
            

            # -------------------------------------------------------------------------------
            # Tier I
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_I = []

            for card1 in state["Board"].dict_Card_Stocks_Show["I"]:
                if card1.type_stock == "black":
                   needed_card_black.append(card1)
                elif card1.type_stock == "red":
                    needed_card_red.append(card1)
                elif card1.type_stock == "white":
                    needed_card_white.append(card1)
            
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_black.sort(key = lambda x: x.score, reverse=True)
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: x.score, reverse=True)
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: x.score, reverse=True)
            needed_card_l_I = needed_card_white + needed_card_black + needed_card_red
            needed_card_l_I.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_l_I.sort(key = lambda x: x.score, reverse=True)
            
            # Tier II
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_II = []
            for card1 in state["Board"].dict_Card_Stocks_Show["II"]:
                if card1.score > 0:    
                    if card1.type_stock == "black" and sum(card1.stocks.values()) in [5,6]:
                        needed_card_black.append(card1)
                    elif card1.type_stock == "red" and sum(card1.stocks.values()) in [5,6,8]:
                        needed_card_red.append(card1)
                    elif card1.type_stock == "white":
                        needed_card_white.append(card1)
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_black.sort(key = lambda x: x.score, reverse=True)
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: x.score, reverse=True)
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: x.score, reverse=True)
            needed_card_l_II = needed_card_white + needed_card_black + needed_card_red
            needed_card_l_II.sort(key = lambda x: x.score, reverse=True)


            # Tier III
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_III = []
            for card1 in state["Board"].dict_Card_Stocks_Show["III"]:
                if card1.score > 3:    
                    if card1.type_stock == "black" and sum(card1.stocks.values()) in [10, 7]:
                        needed_card_black.append(card1)
                    elif card1.type_stock == "white":
                        needed_card_white.append(card1)
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_l_III = needed_card_white + needed_card_black + needed_card_red


            needed_card_l_II_III = needed_card_l_II + needed_card_l_III
            needed_card_l_II_III.sort(key = lambda x: x.score / sum(list(x.stocks.values())), reverse=True)
            needed_card_l = self.card_upside_down + needed_card_l_II_III + needed_card_l_I
            needed_card_l.sort(key = lambda x: x.score)
            needed_card_l.sort(key = lambda x: sum(list(x.stocks.values())))


            for card_in_list in needed_card_l_I:
                print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format\
                (card_in_list.id, card_in_list.score, card_in_list.stocks, card_in_list.type_stock))            

            for card_in_list in needed_card_l_II_III:
                print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format\
                (card_in_list.id, card_in_list.score, card_in_list.stocks, card_in_list.type_stock))            
            # -------------------------------------------------------------------------------

          
            # -------------------------------------------------------------------------------------------
            # Nếu có 9 tài nguyên, úp thẻ tiếp theo trong needed_card
            sum_self_st = 0
            for i in self.stocks:
                    sum_self_st += self.stocks[i]
            if sum_self_st == 9:
                # Úp thẻ
                if self.check_upsite_down(needed_card_l[0]):
                    return [], needed_card_l[0], []
            # Nếu có 10 tài nguyên, kiểm tra xem có lấy được thẻ nào trên bàn hay không?
            elif sum_self_st == 10:
                for card3 in needed_card_l:
                    if self.check_get_card_no_auto_color(card3) or self.check_get_card(card3):
                        return [], card3, []
                for type_card in state["Board"].dict_Card_Stocks_Show:
                            if type_card != "Noble":
                                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                                    if self.check_get_card_no_auto_color(card1) or self.check_get_card(card1):
                                            return [], card1, []
            # -------------------------------------------------------------------------------


            # -------------------------------------------------------------------------------
            # Nếu có nhiều hơn 4 thẻ loại 1, không lấy thẻ loại 1 nữa
            num_tier1 = 0
            for card4 in self.card_open + self.card_upside_down:
                if card4.score < 2:
                        num_tier1 += 1
            if num_tier1 > 4:
                needed_card_l_I = []
                print("----------- Kết thúc tier1 -------------")
            # -------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------
            # Kiểm tra xem có thẻ loại I có 1 điểm mà có type stock trong ["đen", "đỏ", "trắng"]
            if len(needed_card_l_I) != 0:
                for card1 in needed_card_l_I:
                    if card1.score == 1 and (card1.type_stock in ["red", "black", "white"]) and self.score != 1:
                        # Úp thẻ
                        if self.check_upsite_down(card1) \
                            and len(self.card_upside_down) == 0 and self.score == 0:
                            return stocks, card1, stock_return

                        if self.check_upsite_down(card1) and self.score == 0 \
                            and self.card_upside_down[0].score != 1:
                            return stocks, card1, stock_return
            # -------------------------------------------------------------------------------


            # -------------------------------------------------------------------------------
            # Nếu có thẻ đang úp điểm = 1, lấy tài nguyên để mở thẻ đó
            if len(self.card_upside_down) != 0:
                target_card = self.card_upside_down[0]
                if self.check_get_card(target_card):
                    print("Đã lấy thẻ đang úp 1 điểm")
                    card = target_card
                    stocks = []
                    stock_return = []
                    return stocks, card, stock_return
                else:    
                    # Lấy tài nguyên để mở thẻ đó
                    # Lấy 2 tài nguyên nếu cần và nếu có thể, nếu không thể lấy 2, lấy mỗi 
                    # loại 1 tài nguyên theo các thẻ trong list các thẻ cần lấy (needed card)
                    stocks = self.get_stock_for_target_card(target_card, state, stocks)
                    if (len(stocks) == 2 and stocks[0] != stocks[1]) or len(stocks) < 2:
                        for card1 in needed_card_l_I:
                            stocks = self.get_stock_for_target_card(card1, state, stocks)
                        for card in needed_card_l_II_III:
                            stocks = self.get_stock_for_target_card(card, state, stocks)
                    # Nếu hết tài nguyên, úp thẻ trong need_card
                    if len(stocks) == 0:
                        if len(needed_card_l_I) != 0 and self.check_upsite_down(needed_card_l_I[0]):
                            return stocks, needed_card_l_I[0], []
                        if len(needed_card_l_II_III) != 0 and self.check_upsite_down(needed_card_l_II_III[0]):
                            return stocks, needed_card_l_II_III[0], []

                    # Nếu thừa nguyên liệu, trả về nguyên liệu KHÔNG có trong target card
                    if len(stocks) + sum_self_st > 10:
                        # Trả về nguyên liệu không trong target card
                        stock_return = self.return_stock_not_in_target_card\
                            (needed_card_l_I, len(stocks) - sum_self_st > 10)
            # -------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------
            # Không có thẻ đang úp điểm = 1 loại 1, target đến thẻ đầu tiên trong needed_card_list
            else:
                if len(needed_card_l_I) > 0:
                    target_list = needed_card_l_I
                else:
                    target_list = needed_card_l
                target_list += self.card_upside_down

                if len(target_list) != 0 and self.check_get_card(target_list[0]):
                    card = target_list[0]
                    stocks = []
                    stock_return = []
                    return stocks, card, stock_return
                else:    
                    # Lấy tài nguyên để mở thẻ đó
                    # Lấy 2 tài nguyên nếu cần và nếu có thể, nếu không thể lấy 2, lấy mỗi 
                    # loại 1 tài nguyên theo các thẻ trong list các thẻ cần lấy (needed card)
                    if len(target_list) != 0:
                        stocks = self.get_stock_for_target_card(target_list[0], state, stocks)
                    else:
                        stocks = self.get_stock_for_target_card(state["Board"].dict_Card_Stocks_Show["II"][0], state, stocks)
                    if (len(stocks) == 2 and stocks[0] != stocks[1]) or len(stocks) < 2:
                        for card in needed_card_l_I:
                            stocks = self.get_stock_for_target_card(card, state, stocks)
                        for card in needed_card_l_II_III:
                            stocks = self.get_stock_for_target_card(card, state, stocks)
                    # Nếu hết tài nguyên, úp thẻ trong need_card_I
                    # Hoặc nếu hết tài nguyên, úp thẻ trong need_card
                    # Úp thẻ
                    if len(stocks) == 0:
                        if len(needed_card_l_I) != 0 and self.check_upsite_down(needed_card_l_I[0]):
                            return stocks, needed_card_l_I[0], []
                        if len(needed_card_l_II_III) != 0 and self.check_upsite_down(needed_card_l_II_III[0]):
                            return stocks, needed_card_l_II_III[0], []

                    # Nếu thừa nguyên liệu, trả về nguyên liệu KHÔNG có trong target card
                    if len(stocks) + sum_self_st > 10:
                        # Trả về nguyên liệu không trong target card
                        stock_return = self.return_stock_not_in_target_card(target_list, len(stocks) - sum_self_st > 10)
            # -------------------------------------------------------------------------------

        else: 
            # Chơi tam tấu l/l/t
            # Chơi style 1-2-3-4-5 hoặc 2-2-2-4-5
            # Lưu ý với tam tấu l/l/t thì thẻ red loại III có thể lấy vì toàn cần lam/lục và 1 chút đỏ
            # Lấy 3 đến 4 thẻ loại I (Trong đó có thể 1 thẻ 1 điểm)
            # Tạo 1 list các thẻ cần lấy
            
            
            # -------------------------------------------------------------------------------------------
            # Tạo list các thẻ cần lấy cho tam tấu d/d/t
# Tạo list các thẻ cần lấy cho tam tấu d/d/t
            needed_card_l = []
            

            # -------------------------------------------------------------------------------
            # Tier I
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_I = []

            for card1 in state["Board"].dict_Card_Stocks_Show["I"]:
                if card1.type_stock == "black":
                   needed_card_black.append(card1)
                elif card1.type_stock == "red":
                    needed_card_red.append(card1)
                elif card1.type_stock == "white":
                    needed_card_white.append(card1)
            
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_black.sort(key = lambda x: x.score, reverse=True)
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: x.score, reverse=True)
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: x.score, reverse=True)
            needed_card_l_I = needed_card_white + needed_card_black + needed_card_red
            needed_card_l_I.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_l_I.sort(key = lambda x: x.score, reverse=True)
            
            # Tier II
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_II = []
            for card1 in state["Board"].dict_Card_Stocks_Show["II"]:
                if card1.score > 0:    
                    if card1.type_stock == "black" and sum(card1.stocks.values()) in [5,6]:
                        needed_card_black.append(card1)
                    elif card1.type_stock == "red" and sum(card1.stocks.values()) in [5,6,8]:
                        needed_card_red.append(card1)
                    elif card1.type_stock == "white":
                        needed_card_white.append(card1)
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_black.sort(key = lambda x: x.score, reverse=True)
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: x.score, reverse=True)
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: x.score, reverse=True)
            needed_card_l_II = needed_card_white + needed_card_black + needed_card_red
            needed_card_l_II.sort(key = lambda x: x.score, reverse=True)


            # Tier III
            needed_card_black = []
            needed_card_red = []
            needed_card_white = []
            needed_card_l_III = []
            for card1 in state["Board"].dict_Card_Stocks_Show["III"]:
                if card1.score > 3:    
                    if card1.type_stock == "black" and sum(card1.stocks.values()) in [10, 7]:
                        needed_card_black.append(card1)
                    elif card1.type_stock == "white":
                        needed_card_white.append(card1)
            needed_card_black.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_red.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_white.sort(key = lambda x: sum(list(x.stocks.values())))
            needed_card_l_III = needed_card_white + needed_card_black + needed_card_red


            needed_card_l_II_III = needed_card_l_II + needed_card_l_III
            needed_card_l_II_III.sort(key = lambda x: x.score / sum(list(x.stocks.values())), reverse=True)
            needed_card_l = self.card_upside_down + needed_card_l_II_III + needed_card_l_I
            needed_card_l.sort(key = lambda x: x.score)
            needed_card_l.sort(key = lambda x: sum(list(x.stocks.values())))


            for card_in_list in needed_card_l_I:
                print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format\
                (card_in_list.id, card_in_list.score, card_in_list.stocks, card_in_list.type_stock))            

            for card_in_list in needed_card_l_II_III:
                print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format\
                (card_in_list.id, card_in_list.score, card_in_list.stocks, card_in_list.type_stock))            
            # -------------------------------------------------------------------------------

          
            # -------------------------------------------------------------------------------------------
            # Nếu có 9 tài nguyên, úp thẻ tiếp theo trong needed_card
            sum_self_st = 0
            for i in self.stocks:
                    sum_self_st += self.stocks[i]
            if sum_self_st == 9:
                # Úp thẻ
                if self.check_upsite_down(needed_card_l[0]):
                    return [], needed_card_l[0], []
            # Nếu có 10 tài nguyên, kiểm tra xem có lấy được thẻ nào trên bàn hay không?
            elif sum_self_st == 10:
                for card3 in needed_card_l:
                    if self.check_get_card_no_auto_color(card3) or self.check_get_card(card3):
                        return [], card3, []
                for type_card in state["Board"].dict_Card_Stocks_Show:
                            if type_card != "Noble":
                                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                                    if self.check_get_card_no_auto_color(card1) or self.check_get_card(card1):
                                            return [], card1, []
            # -------------------------------------------------------------------------------


            # -------------------------------------------------------------------------------
            # Nếu có nhiều hơn 4 thẻ loại 1, không lấy thẻ loại 1 nữa
            num_tier1 = 0
            for card4 in self.card_open + self.card_upside_down:
                if card4.score < 2:
                        num_tier1 += 1
            if num_tier1 > 4:
                needed_card_l_I = []
                print("----------- Kết thúc tier1 -------------")
            # -------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------
            # Kiểm tra xem có thẻ loại I có 1 điểm mà có type stock trong ["đen", "đỏ", "trắng"]
            if len(needed_card_l_I) != 0:
                for card1 in needed_card_l_I:
                    if card1.score == 1 and (card1.type_stock in ["red", "black", "white"]) and self.score != 1:
                        # Úp thẻ
                        if self.check_upsite_down(card1) \
                            and len(self.card_upside_down) == 0 and self.score == 0:
                            return stocks, card1, stock_return

                        if self.check_upsite_down(card1) and self.score == 0 \
                            and self.card_upside_down[0].score != 1:
                            return stocks, card1, stock_return
            # -------------------------------------------------------------------------------


            # -------------------------------------------------------------------------------
            # Nếu có thẻ đang úp điểm = 1, lấy tài nguyên để mở thẻ đó
            if len(self.card_upside_down) != 0:
                target_card = self.card_upside_down[0]
                if self.check_get_card(target_card):
                    print("Đã lấy thẻ đang úp 1 điểm")
                    card = target_card
                    stocks = []
                    stock_return = []
                    return stocks, card, stock_return
                else:    
                    # Lấy tài nguyên để mở thẻ đó
                    # Lấy 2 tài nguyên nếu cần và nếu có thể, nếu không thể lấy 2, lấy mỗi 
                    # loại 1 tài nguyên theo các thẻ trong list các thẻ cần lấy (needed card)
                    stocks = self.get_stock_for_target_card(target_card, state, stocks)
                    if (len(stocks) == 2 and stocks[0] != stocks[1]) or len(stocks) < 2:
                        for card1 in needed_card_l_I:
                            stocks = self.get_stock_for_target_card(card1, state, stocks)
                        for card in needed_card_l_II_III:
                            stocks = self.get_stock_for_target_card(card, state, stocks)
                    # Nếu hết tài nguyên, úp thẻ trong need_card
                    if len(stocks) == 0:
                        if len(needed_card_l_I) != 0 and self.check_upsite_down(needed_card_l_I[0]):
                            return stocks, needed_card_l_I[0], []
                        if len(needed_card_l_II_III) != 0 and self.check_upsite_down(needed_card_l_II_III[0]):
                            return stocks, needed_card_l_II_III[0], []

                    # Nếu thừa nguyên liệu, trả về nguyên liệu KHÔNG có trong target card
                    if len(stocks) + sum_self_st > 10:
                        # Trả về nguyên liệu không trong target card
                        stock_return = self.return_stock_not_in_target_card\
                            (needed_card_l_I, len(stocks) - sum_self_st > 10)
            # -------------------------------------------------------------------------------







        return stocks, card, stock_return