from ..base.player import Player
import random
import math

# Note:
# Board
#           dict_Card_Stocks_Show: Truy cập các thẻ đang ở trên bàn
#           Stocks: nguyên liệu
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







class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def check_card_target(self, card_target):
        card_target_stock = card_target.stocks
        for stock in card_target_stock:
            if self.stocks[stock] + self.stocks_const[stock] - card_target_stock[stock] < 0:
              #  print("Can't get target card!")
                return False
      #  print("Can get target card!")
        return True       


    def random_return_stock(self, ret_number):
        stock_return = []
        for stock in self.stocks:
            if len(stock_return) < ret_number and self.stocks[stock] > 0:
                stock_return.append(stock)

        return stock_return


    def action(self, state):
        list_card_can_get = []
        stocks = []
        card = None
        stock_return = []

        # Print các thẻ có trên bàn, theo thứ tự các loại thẻ I, II, III, Noble
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #           #  print(card.id, card.stocks, card.score, card.type_stock)

        # --------------------------------------------------------------------------------
        # Target buổi 2: in tất cả các thẻ có trên bàn và thẻ CÓ ĐIỂM nhưng cần trả ít nguyên liệu nhất
        # Task 1: In ra tất cả các thẻ
        # --------------------------------------------------------------------------------
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                  #  print(card.id, card.stocks, card.score, card.type_stock)

        # Task 2: In ra thẻ có điểm và cần ít tài nguyên nhất
        len_value = 15
        needed_card = None
        for type_card in state["Board"].dict_Card_Stocks_Show:
            if type_card != "Noble":
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if card.score > 0:
                        if sum(card.stocks.values()) <= len_value:
                            needed_card = card
                            len_value = sum(card.stocks.values())
                        elif sum(card.stocks.values()) == len_value and card.score >= needed_card.score:
                            needed_card = card
                            len_value = sum(card.stocks.values())                
      #  print("\n------------------------------------------------------")
      #  print("Needed Card: ID: {}, Stock: {}, Score: {}, Type Stock: {}".format(needed_card.id, needed_card.stocks, needed_card.score, needed_card.type_stock))
      #  print("------------------------------------------------------\n")
        # ---------------------------------------------------------------------------------
        # Task 2: Bốc tài nguyên sao cho lấy được cái thẻ needed card phía trên
        # --------------------------------------------------------------------------------



        # ------------ Hoàn thành 16/5 ------------------------------------------
        # Bốc tài nguyên
        # a1: Kiểm tra xem tài nguyên cần để mua thẻ có cái nào >= 2 không?, nếu không => nhảy đến a3
            # a2: Nếu có => Kiểm tra tài nguyên đó trên bàn có >= 4 không?, có => bốc 2 tài nguyên
                # a3: Nếu không: kiểm tra xem tài nguyên trên bàn có 3 loại tài nguyên cần có của thẻ không? nếu có => bốc 3 thẻ
                    # Trong trường hợp không bốc đủ 3 thẻ (do trên bàn hết tài nguyên) => bốc ngẫu nhiên sao cho đủ 3 thẻ tài nguyên

        # # a1: Kiểm tra xem tài nguyên cần để mua thẻ có cái nào >= 2 không?, nếu không => nhảy đến (1)
        # if any(x >= 2 for x in needed_card.stocks.values()):
        #   #  print("True")
        #     # a2: Nếu có => Kiểm tra tài nguyên đó trên bàn có >= 4 không?, có => bốc 2 tài nguyên
        #     for stock_in_card in needed_card.stocks:
        #         if needed_card.stocks[stock_in_card] >= 2 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 2:
        #             break
        #     if state["Board"].stocks[stock_in_card] >= 4:
        #         stocks.append(stock_in_card)
        #         stocks.append(stock_in_card)
        #     # a3: Nếu không: kiểm tra xem tài nguyên trên bàn có 3 loại tài nguyên cần có của thẻ không? nếu có => bốc 3 thẻ
        #     else:
        #         for stock_in_card in needed_card.stocks:
        #             if needed_card.stocks[stock_in_card] > 0 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 1:
        #                 if len(stocks) < 3 and state["Board"].stocks[stock_in_card] > 0:
        #                     stocks.append(stock_in_card)
        #         # Trong trường hợp không bốc đủ 3 thẻ (do trên bàn hết tài nguyên) => bốc ngẫu nhiên sao cho đủ 3 thẻ tài nguyên
        #         for stock_in_board in state["Board"].stocks:
        #             if len(stocks) < 3 and state["Board"].stocks[stock_in_board] > 0 and stock_in_board not in stocks:
        #                 stocks.append(stock_in_board)
        # else: 
        #     for stock_in_card in needed_card.stocks:
        #             if needed_card.stocks[stock_in_card] > 0 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 1:
        #                 if len(stocks) < 3 and state["Board"].stocks[stock_in_card] > 0:
        #                     stocks.append(stock_in_card)
        #     # Trong trường hợp không bốc đủ 3 thẻ (do trên bàn hết tài nguyên) => bốc ngẫu nhiên sao cho đủ 3 thẻ tài nguyên
        #     for stock_in_board in state["Board"].stocks:
        #         if len(stocks) < 3 and state["Board"].stocks[stock_in_board] > 0 and stock_in_board not in stocks:
        #             stocks.append(stock_in_board)
        # # ------------------------------------------------------------------------------------------

        # Trả về tài nguyên ngẫu nhiên nếu thừa
        if len(stocks) + len(self.stocks) > 10:
            stock_return = self.random_return_stock(len(stocks) + len(self.stocks) - 10)
        # ------------ Hoàn thành 16/5 ------------------------------------------




        # --------------------------------------------------------------------------------------------------------------
        if self.check_card_target(needed_card):
                    card = needed_card
                    stocks = []
        # --------------------------------------------------------------------------------------------------------------

                
        
        # Print số lượng tài nguyên đang có trên bàn:
      #  print("Resource in board:")
        # for stock_in_board_key in state["Board"].stocks:
          #  print("{}: {}".format(stock_in_board_key, state["Board"].stocks[stock_in_board_key]))
        
        # Print các tài nguyên vĩnh viễn đang có
      #  print("Tai nguyen vinh vien {}".format(self.stocks_const))
        
        # Print các tài nguyên hữu hạn
      #  print("Tai nguyen huu han {}".format(self.stocks))

        # Gán card taget :để lấy nguyên liệu là card loại 1 và stt đầu tiên(vì nó là một list)
        # stocks là một dict nguyên liệu của thẻ đó

        # In ra nguyên liệu mặc định của người chơi đó(nguyên liệu thẻ đã lấy)
      #  print(self.stocks_const)
   

        # Buoi 3:

        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for one_card in state['Board'].dict_Card_Stocks_Show[type_card]: 
                    if self.check_card_target(one_card):
                        list_card_can_get.append(one_card)

        # --------------------------------------------------------------------------------------------------------------
        # Tạo list các thẻ có thể lấy, sau đó lấy thẻ đầu tiên trong list đó
        if len(list_card_can_get) == 0:
            # Bốc tài nguyên    
            # a1: Kiểm tra xem tài nguyên cần để mua thẻ có cái nào >= 2 không?, nếu không => nhảy đến (1)
            if any(x >= 2 for x in needed_card.stocks.values()):
              #  print("True")
                # a2: Nếu có => Kiểm tra tài nguyên đó trên bàn có >= 4 không?, có => bốc 2 tài nguyên
                for stock_in_card in needed_card.stocks:
                    if needed_card.stocks[stock_in_card] >= 2 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 2:
                        break
                if state["Board"].stocks[stock_in_card] >= 4:
                    stocks.append(stock_in_card)
                    stocks.append(stock_in_card)
                # a3: Nếu không: kiểm tra xem tài nguyên trên bàn có 3 loại tài nguyên cần có của thẻ không? nếu có => bốc 3 thẻ
                else:
                    for stock_in_card in needed_card.stocks:
                        if needed_card.stocks[stock_in_card] > 0 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 1:
                            if len(stocks) < 3 and state["Board"].stocks[stock_in_card] > 0:
                                stocks.append(stock_in_card)
                    # Trong trường hợp không bốc đủ 3 thẻ (do trên bàn hết tài nguyên) => bốc ngẫu nhiên sao cho đủ 3 thẻ tài nguyên
                    for stock_in_board in state["Board"].stocks:
                        if len(stocks) < 3 and state["Board"].stocks[stock_in_board] > 0 and stock_in_board not in stocks:
                            stocks.append(stock_in_board)
            else: 
                for stock_in_card in needed_card.stocks:
                        if needed_card.stocks[stock_in_card] > 0 and needed_card.stocks[stock_in_card] - (self.stocks[stock_in_card] + self.stocks_const[stock_in_card]) >= 1:
                            if len(stocks) < 3 and state["Board"].stocks[stock_in_card] > 0:
                                stocks.append(stock_in_card)
                # Trong trường hợp không bốc đủ 3 thẻ (do trên bàn hết tài nguyên) => bốc ngẫu nhiên sao cho đủ 3 thẻ tài nguyên
                for stock_in_board in state["Board"].stocks:
                    if len(stocks) < 3 and state["Board"].stocks[stock_in_board] > 0 and stock_in_board not in stocks:
                        stocks.append(stock_in_board)
            # ------------------------------------------------------------------------------------------

        else:
            card = list_card_can_get[0]
        # stocks là một list các nguyên liệu cần ví dụ: ['red', 'red'] hoặc ['blue', 'green', 'black']
        # card là một đối tượng, gán thẳng từ bàn chơi như dòng 36
        # stock_return cũng là một list giống stocks


        return stocks, card, stock_return
    