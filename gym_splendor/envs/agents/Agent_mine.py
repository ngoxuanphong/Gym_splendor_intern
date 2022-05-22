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
        max1=0
        min1=10
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    a=card.stocks
                    if card.score > 0:
                        if min1 >= sum(a.values()):
                            min1=sum(a.values())
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    a=card.stocks
                    if card.score > 0:
                        if min1==sum(a.values()):
                            print(card.id, card.stocks, card.score, card.type_stock,min1)
                            card_target=card
                            card_st=card.stocks
        # Print các thẻ có trên bàn, theo thứ tự các loại thẻ I, II, III, Noble
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    print(card.id, card.stocks, card.score, card.type_stock)
                    if self.check_get_card(card):
                        listcard.append(card)
        print(listcard)
        #stocks là một dict nguyên liệu của thẻ đó
        card_st = card_target.stocks
        print(card_st)
        stocks = []

        # Kiểm tra xem nguyên liệu của thẻ cần là bao nhiêu để lấy nguyên liệu
        #Nếu thẻ cần mở có nguyên liệu cần từ 2 trở lên, lấy trước 2 nguyên liệu. Nếu nguyên liệu đó trên bàn k >3 thì lấy 1 và chuyển qua
        #trường hợp lấy 3 nguyên liệu khác nhau
        
        for card in listcard:
            if len(listcard) >0:
              if card.score>max1: 
                  max1=card.score
        for card in listcard:
            if card.score==max1:
                card_target=card
                return stocks, card_target, stock_return
        # if sum(self.stocks.values())==10:
        #     if len(listcard) >0:
        #         card_target=listcard[-1]
        #         return stocks, card_target, stock_return
        for stock in card_st:
            if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] >1:
                if state['Board'].stocks[stock] > 3:
                    stocks.append(stock)
                    stocks.append(stock)
                    d=1
                    break
                elif state['Board'].stocks[stock] <= 3:
                    stocks.append(stock)
                    break
        if d!=1: 
            for stock in card_st:        
                if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] ==1 and state['Board'].stocks[stock] >0:
                    stocks.append(stock)
                    if len(stocks)==3:  
                        break         
                    else: continue
                if (0<len(stocks)<3) and (self.stocks[stock]==0) and state['Board'].stocks[stock] >0: 
                    stocks.append(stock)
                
            t=sum(self.stocks.values()) + len(stocks) -10
            if t>=0:
                for i in self.stocks:
                    if i !='auto_color':
                        if card_st[i]<self.stocks[i] and self.stocks[i] >0:
                            if len(stock_return) < t:
                                stock_return.append(i)
        
        print(stocks)
        print(self.stocks)
        print(stock_return)
        # Trả nguyên liệu khi vượt quá 10 

        # if sum(self.stocks.values()) >10:
        #     print("Tra nguyen lieu di ban ei")
        #     for stock in card_st: 
        #         if card_st[stock]<stocks[stock] and stock!='auto_color':
        #             stock_return.append(stock)
        # if sum(self.stocks.values()) + len(stock_return) > 10:
        #     for stock in stock_return:
        #         self.stocks[stock] = self.stocks[stock] - 1
        #     state["Board"].postStock(stock_return)
        print(sum(self.stocks.values()))
        
        print(card_target.id)
        # card=card_target
        # In ra tất cả những thẻ có trên bàn, in ra thẻ có điểm nhưng tốn ít nhiên liệu nhất
        #Gán card taget là thẻ đầu tiên loại 1 trên bàn
        # if self.check_get(card):
        #     card=card_st
        #     print("ok")
        #In ra nguyên liệu mặc định của người chơi đó(nguyên liệu thẻ đã lấy)
        print(self.stocks_const)
        # stocks là một list các nguyên liệu cần ví dụ: ['red', 'red'] hoặc ['blue', 'green', 'black']
        # card là một đối tượng, gán thẳng từ bàn chơi như dòng 36
        # stock_return cũng là một list giống stocks
        d=0
        return stocks, card_target, stock_return