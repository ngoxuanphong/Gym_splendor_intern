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


# 

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []


        # Hiển thị các thẻ có trên bàn
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    print("{} \tID: {} \tScore: {} \tStocks {} \tType Stocks: {}".format
                    (type_card, card1.id, card1.score, card1.stocks, card1.type_stock))










        return stocks, card, stock_return