from cgitb import small
from os import stat
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


# 

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

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

    def get_larget_stock_in_board(self, state):
        stocks = []
        for stock in state["Board"].stocks:
            if stock != "auto_color":
                if len(stocks) < 3:
                    if len(stocks) == 0 and state["Board"].stocks[stock] >= 4:
                        stocks.append(stock)
                        stocks.append(stock)
                        break
                    elif state["Board"].stocks[stock] > 0 and stock not in stocks:
                        stocks.append(stock)
        return stocks


    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        card_in_board = []
        card_co_diem = []

        # Hiển thị các thẻ có trên bàn
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    card_in_board.append(card1)
                    # print("{} \tID: {} \tScore: {} \tStocks {} \tType Stocks: {}".\
                    #     format(type_card, card1.id, card1.score, card1.stocks, card1.type_stock))
                    if card1.score != 0:
                        card_co_diem.append(card1)

        card_in_board.sort(key = lambda x: sum(list(x.stocks.values())))
        card_co_diem.sort(key = lambda x: sum(list(x.stocks.values())))
        # Nếu có thể lấy thẻ => lấy thẻ
        # Nếu không thể lấy thẻ => lấy tài nguyên có nhiều nhất trên bàn (Ưu tiên lấy 2 nếu có thể)
        for card1 in card_in_board:
            if self.check_get_card(card1):
                return [], card1, []

        # Kiểm tra tài nguyên
        # Nếu có 9 tài nguyên => úp thẻ 
        if sum(self.stocks.values()) == 9:
            # Úp thẻ đầu trong thẻ có điểm
            if self.check_upsite_down(card_co_diem[0]):
                return [], card_co_diem[0], []
        elif sum(self.stocks.values()) == 10:
            # Trả về tài nguyên bất kỳ
            for stock in state["Board"].stocks:
                if stock != "auto_color":
                    if state["Board"].stocks[stock] > 0:
                        stock_return.append(stock)
                        return [], card_co_diem[0], stock_return 
        
        # Lấy tài nguyên
        stocks = self.get_larget_stock_in_board(state)
        if sum(self.stocks.values()) + len(stocks) > 10:
            # Trả về thẻ không cần nữa
            var = sum(self.stocks.values()) + len(stocks) - 10
            while var > 0:
                for card1 in card_co_diem:
                    for stock_in_card in card1.stocks:
                        if card1.stocks[stock_in_card] - self.stocks[stock_in_card]\
                             - self.stocks_const[stock_in_card] < 0:
                             stock_return.append(stock_in_card)
                             var -= 1


        return stocks, card, stock_return