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


        # Hiển thị các thẻ đã lật và nguyên liệu đang có
        if len(self.card_open) != 0:
            print("Các thẻ đã lật của Long: ")
            for i in self.card_open:
                print("Score: {}".format(i.score), end = ",")
        else:
            print("Long chưa lật thẻ nào")
        print("\nNguyên liệu hữu hạn: {}".format(self.stocks))
        print("Nguyên liệu vĩnh viễn: {}".format(self.stocks_const))

        # Hiển thị các thẻ đang úp
        if len(self.card_upside_down) != 0:
            print("Các thẻ đang úp của Long là: ")    
            for i in self.card_upside_down:
                print("Score: {}".format(i.score))
       

        # Kiểm tra xem có thẻ loại I có giá trị 1 điểm hay không? Nếu có => úp thẻ
        # Chỉ úp thẻ loại I khi chua có điểm, 1 ván lấy duy nhất 1 thẻ 1 điểm loại I
        if self.score < 1 and len(self.card_upside_down) == 0:
            for type_card in state["Board"].dict_Card_Stocks_Show:
                if type_card == "I":
                    for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                        if card1.score == 1:
                            if self.check_upsite_down(card1):
                                stocks = stock_return = []
                                card = card1
                                return stocks, card, stock_return
            
        # Nếu đã úp thẻ loại I có 1 điểm
        if len(self.card_upside_down) != 0 and self.card_upside_down[0].score == 1:
            target_card = self.card_upside_down[0]
            # Nếu có thể mở thẻ đó
            if self.check_get_card(target_card):
                stocks = stock_return = []
                card = target_card
                return stocks, card, stock_return
            else:
                # Lấy tài nguyên để mở thẻ đang úp (LƯU Ý ĐANG CÓ 1 THẺ VÀNG)
                








        return stocks, card, stock_return