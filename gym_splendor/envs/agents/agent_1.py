from multiprocessing.sharedctypes import Value

from numpy import true_divide

from gym_splendor.envs.base.card import Card_Stock
from ..base.player import Player
import random
import math

# self: Truy cập những thông tin hiện tại của bản thân như score, stock, thẻ
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    # def check_get(self, card):
    #     card_st=card.stocks
    #     for stock in card_st:
    #         if card_st[stock]-self.stocks[stock]-self.stocks_const[stock]>0:
    #             return False
    #     return True 
    #     return card

    def action(self, state):
        global d
        stocks = []
        card = None
        stock_return = []
        listcard=[]
        d=0
        min1=10
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             a=card.stocks
        #             if card.score > 0:
        #                 if min1 >= sum(a.values()):
        #                     min1=sum(a.values())
        # for type_card in state['Board'].dict_Card_Stocks_Show:
        #     if type_card != 'Noble':
        #         for card in state['Board'].dict_Card_Stocks_Show[type_card]:
        #             a=card.stocks
        #             if card.score > 0:
        #                 if min1==sum(a.values()):
        #                     print(card.id, card.stocks, card.score, card.type_stock,min1)
        #                     card_st=card.stocks
        # Print các thẻ có trên bàn, theo thứ tự các loại thẻ I, II, III, Noble
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    print(card.id, card.stocks, card.score, card.type_stock)
                    # if self.check_get(card):
                    #     listcard.append(card)
        
        # print(listcard)
        #Gán card taget :để lấy nguyên liệu là card loại 1 và stt đầu tiên(vì nó là một list)
        #stocks là một dict nguyên liệu của thẻ đó
        card_st = state['Board'].dict_Card_Stocks_Show['II'][0].stocks
        print(card_st)
        stocks = []

        # Kiểm tra xem nguyên liệu của thẻ cần là bao nhiêu để lấy nguyên liệu
        for stock in card_st:
            if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] >1:
                stocks.append(stock)
                stocks.append(stock)
                d=1
                break
        if d!=1: 
            for stock in card_st:        
                if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] ==1:
                    stocks.append(stock)
                    if len(stocks)==3: 
                        break
        if d!=1:            
            for stock in card_st:
                if (0<len(stocks)<3) and (card_st[stock]==0): 
                    stocks.append(stock)
        d=0
        print(stocks)
        print(sum(self.stocks.values()))
        if sum(self.stocks.values()) >10 :
            for stock in card_st: 
                if card_st[stock]<stocks[stock]:
                    stock_return.append(
                        
                    )
        print(sum(self.stocks.values()))
        # In ra tất cả những thẻ có trên bàn, in ra thẻ có điểm nhưng tốn ít nhiên liệu nhất
        #Gán card taget là thẻ đầu tiên loại 1 trên bàn
        card = state['Board'].dict_Card_Stocks_Show['II'][0]
        # if self.check_get(card):
        #     card=card_st
        #     print("ok")
        #In ra nguyên liệu mặc định của người chơi đó(nguyên liệu thẻ đã lấy)
        print(self.stocks_const)
        # stocks là một list các nguyên liệu cần ví dụ: ['red', 'red'] hoặc ['blue', 'green', 'black']
        # card là một đối tượng, gán thẳng từ bàn chơi như dòng 36
        # stock_return cũng là một list giống stocks
        return stocks, card, stock_return