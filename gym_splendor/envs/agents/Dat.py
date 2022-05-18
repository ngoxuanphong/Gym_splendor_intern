
from gym_splendor.envs.base.board import Board
from ..base.player import Player
import random
import math
#board
#dict_card_stocks_show: thẻ mở
#stocks: nguyen liệu

#player
#score: self.score
#nguyên liệu: self.stocks
#nguyên liệu mặc định: self.stocks_const
#thẻ đã mở: self.card_open
#thẻ đã úp: self.card_upsidedown
#thẻ noble: self.card_noble

#card
#id: mã của thẻ vd:[I][0]
#stocks: nguyên liệu cần để lấy thẻ
#score: điểm ghi trên thẻ
#type.stocks: nguyên liệu mặc định của thẻ

# Agent(self,state)
#State = {'Turn':...,"Board":...,"Player":...}
#btap: in ra tất cả các thẻ có trên bàn, in ra thẻ có điểm mà trả ít nguyên liệu.
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def check_get_card_ok(self, Card, state):
        stocks = Card.stocks
        for stock in stocks:
            if state["Board"].stocks[stock]+ self.stocks[stock]+ self.stocks_const[stock]-stocks[stock] < 0:
                return False
        return True
    
    def action(self, state):
        stocks = []
        card = None
        stock_return = []

        max_value = 10
        
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             if card.score >0:
        #                 if sum(card.stocks.values()) / card.score <= max_value:
        #                     max_value = sum(card.stocks.values()) / card.score           
        #             else:
        #                 continue
            
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             if card.score >0:
        #                 if sum(card.stocks.values()) / card.score==max_value:
        #                     card_selected = card
        #                     card_stocks = card.stocks
        #                     print(card.stocks, card.score, card.type_stock)

        #Choose the best card in the board 
        min = 10
        score_max = 0
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if card.score >0 and  sum(card.stocks.values()) <= min:
                        min = sum(card.stocks.values())
                   
                    else:
                        continue

                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if sum(card.stocks.values())==min and card.score >0 :
                        if card.score > score_max:
                            score_max = card.score
                        else:
                            continue

                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if sum(card.stocks.values())==min and card.score == score_max :
                        card_selected_best = card
                        card_stocks_best = card.stocks
                        print(card.stocks, card.score, card.type_stock)
                        break

        #list of available card to choose                    
        list_card_id_avai = []
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card_ok(card,state):
                        list_card_id_avai.append(card.id)

        print(list_card_id_avai)

        #select the optimal card to take
        if self.check_get_card_ok(card_selected_best,state):
            card_selected = card_selected_best
            card_stocks = card_stocks_best
        elif len(list_card_id_avai) >0:
            for type_card in state['Board'].dict_Card_Stocks_Show:
                if type_card != 'Noble':
                    for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                        if card.id==list_card_id_avai[0]:
                            card_selected = card
                            card_stocks = card.stocks
        else:
            index1 = ['I',"II",'III']
            index2 = [0,1,2,3]
            index1_1 = random.randint(0,2)
            index1_2 = random.randint(0,3)
            card_selected = state['Board'].dict_Card_Stocks_Show[index1[index1_1]][index2[index1_2]]
            card_stocks = state['Board'].dict_Card_Stocks_Show[index1[index1_1]][index2[index1_2]].stocks

        print("Thẻ đã target:")
        print(card_stocks,card_selected.score,card_selected.id)
        
        
        #get resource
        stocks = []
        direct = 0
        for stock in card_stocks:
                       
            if card_stocks[stock] - self.stocks[stock] -self.stocks_const[stock] >=2 and len(stocks)==0 and state['Board'].stocks[stock] >=4:
                direct = 1
                stocks +=[stock, stock]
                break
            else:
                if card_stocks[stock] - self.stocks[stock] -self.stocks_const[stock] > 0 :
                    if len(stocks) <3:
                        stocks.append(stock)      
                        direct = 2
                    else:
                        continue       
        
        stock_temp = self.stocks
        if direct==2:

            for stock in state['Board'].stocks:
                if stock not in stocks and stock !='auto_color':
                    if len(stocks) <3 and state['Board'].stocks[stock] > 0:
                        stocks.append(stock)

            for st in stocks:
                    stock_temp[st] = stock_temp[st] + 1


            for st in stock_temp :
                if sum(stock_temp.values()) > 10:
                    if st != 'auto_color':
                        if card_stocks[st] - stock_temp[st] < 0:
                            stock_temp[st] -=1
                            
                            if st in stocks:
                                stock_return.append(st)
                                stocks.remove(st)
            
                            else:
                                stock_return.append(st)
                                self.stocks[st] -=1
                        else:
                            continue     
                else:
                    break     
        


        # print("Stocks đã lấy:")
        # print(stocks)
        # print(self.stocks)
        # print("Lượng nguyên liệu đang có trên bàn:", end=" ")
        # print(sum(self.stocks.values()))
        # print(stock_return)
        # print("Thẻ đã chọn:")
        
        card = card_selected                    




        
        return stocks, card, stock_return