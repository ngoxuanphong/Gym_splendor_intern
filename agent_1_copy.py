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

    def check_get_card(self, Card):
        card_st = Card.stocks
        print('okokokokokok')
        for stock in card_st:
            if self.stocks[stock]+ self.stocks_const[stock]-card_st[stock] < 0:
                return False
        return True
    def list_card_available(self,Card):
        
    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             print(card.stocks, card.score, card.type_stock)
        #             print(sum(card.stocks.values()))
        print("Thẻ có điểm có ít nguyên liệu:")
        
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
                        card_new = card
                        card_st = card.stocks
                        print(card.stocks, card.score, card.type_stock)
                        break
        print("Thẻ đã target:")
        print(card_st)       
        print(stocks)
        print(sum(self.stocks.value()))
        

        stocks = []
        for stock in card_st:
                       
            if card_st[stock] - self.stocks[stock] -self.stocks_const[stock] >=2 and len(stocks)==0 and state['Board'].stocks[stock] >=4:
               
                stocks +=[stock, stock]
                break
            else:
                if card_st[stock] - self.stocks[stock] -self.stocks_const[stock] >0 :
                    if len(stocks) <3:
                        stocks.append(stock)           
        
        if self.check_get_card(card_new):
            card = card_new
        return stocks, card, stock_return