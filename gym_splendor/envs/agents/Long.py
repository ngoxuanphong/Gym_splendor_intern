from cgitb import small
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
        card_type_list_reverse = ["III", "II", "I"]
        so_the_co_diem_tren_ban = 0
        so_the_khong_co_diem_tren_ban = 0
        the_co_diem_l = []
        the_khong_co_diem_l = []

        # Hiển thị các thẻ đã lật và nguyên liệu đang có
        print("Các thẻ đã lật của Long: ")
        if len(self.card_open) != 0:
            for i in self.card_open:
                print("Score: {}".format(i.score), end=", ")
        print("\nNguyên liệu hữu hạn: {}".format(self.stocks))
        print("Nguyên liệu vĩnh viễn: {}".format(self.stocks_const))

        # Lấy danh sách các thẻ có điểm và không có điểm
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    if card1.score > 0:
                        # Không lấy thẻ 1 điểm cần 8 tài nguyên
                        if card1.score == 1 and sum(card1.stocks.values()) >= 7:
                            continue
                        # Không lấy các thẻ 3 điểm cần 14 tài nguyên
                        if card1.score == 3 and sum(card1.stocks.values()) == 14:
                            continue
                        so_the_co_diem_tren_ban += 1
                        the_co_diem_l.append(card1)
                    else:
                        so_the_khong_co_diem_tren_ban += 1
                        the_khong_co_diem_l.append(card1)
        

        # Hiển thị các thẻ có trên bàn
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card1 in state["Board"].dict_Card_Stocks_Show[type_card]:
                    print("{} \tID: {} \tScore: {} \tStocks {} \tType Stocks: {}".format(type_card, card1.id, card1.score, card1.stocks, card1.type_stock))

        # Sap xep cac the co diem theo thu tu uu tien (score/stock lớn đứng đầu)
        the_co_diem_l.sort(key=lambda a: a.score/sum(a.stocks.values()), reverse=True)

        # Sap xep cac the khong co diem theo thu tu the can it tai nguyen nhat
        the_khong_co_diem_l.sort(key=lambda a: sum(a.stocks.values()))


        # Hiển thị các thẻ có điểm và không có điểm
        print("The co diem:")
        for card_co_diem in the_co_diem_l:
            print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format(card_co_diem.id, card_co_diem.score, card_co_diem.stocks, card_co_diem.type_stock))
        print("The khong co diem:")
        for card_khong_diem in the_khong_co_diem_l:
            print("\tID: {} \tScore: {} \tStocks {} \t Type Stocks: {}".format(card_khong_diem.id, card_khong_diem.score, card_khong_diem.stocks, card_khong_diem.type_stock))


        # Kiểm tra xem có thể lấy thẻ nào trong các thẻ (ưu tiên thẻ có điểm trước)
        for card2 in the_co_diem_l:
            if self.check_get_card(card2):
                card = card2
                stocks = []
                stock_return = []
                return stocks, card, stock_return
        else:
            for card2 in the_khong_co_diem_l:
                if self.check_get_card(card2):
                    card = card2
                    stocks = []
                    stock_return = []
                    return stocks, card, stock_return          
        
        # Nếu không thể lấy thẻ, lấy tài nguyên
        # lấy tài nguyên có số lượng nhiều nhất trên bàn
        # Tìm tài nguyên có số lượng nhiều nhất
        max_stock = max(list(state["Board"].stocks.values())[1:])
        # Nếu số lượng tài nguyên nhiều nhất >= 4 => bốc luôn =))
        if max_stock >= 4:
            for stock_in_board in state["Board"].stocks:
                if stock_in_board != "auto_color":
                    if state["Board"].stocks[stock_in_board] == max_stock:
                        # Chú ý phần trả về tài nguyên nếu thừa sẽ xử lý sau
                        stocks.append(stock_in_board)
                        stocks.append(stock_in_board)
        # Nếu số lượng tài nguyên nhiều nhất < 4 => 
        # Bốc 3 loại tài nguyên nhiều nhất trên bàn
        else:
            stock_can_get_l = [3,2,1]
            # while len(stocks) < 3:      # Đang bị kẹt chỗ này, fix lẹ
            for stock_can_get in stock_can_get_l:
                for stock_in_board in state["Board"].stocks:
                    if stock_in_board != "auto_color":
                        if state["Board"].stocks[stock_in_board] == stock_can_get and stock_in_board not in stocks:
                            stocks.append(stock_in_board)


        check_return_len = sum(self.stocks.values()) + len(stocks) - 10
        print("check return length: {}".format(check_return_len))
        print("length: {}".format(check_return_len + 10))

        # Nếu vượt quá 10 tài nguyên, trả lại tài nguyên mình có ít nhất
        smallest_l = [1,2,3]
        while check_return_len > 0:
            for smallest in smallest_l:
                for stock_of_me in self.stocks:
                    if self.stocks[stock_of_me] > 0 and self.stocks[stock_of_me] == smallest:
                        stock_return.append(stock_of_me)
                        check_return_len -= 1
            
        return stocks, card, stock_return