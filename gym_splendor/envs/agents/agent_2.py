from ..base.player import Player
import random
import math
from collections import Counter

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def check_card(self, card):
        card_st = card.stocks
        for stock in card_st:
            if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] > 0:
                return False
        return True
    
    


    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        list = []
        # in ra tat ca cac the co diem trên bàn và thẻ có điểm có số nguyên liệu thấp nhât
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for c in state['Board'].dict_Card_Stocks_Show[type_card]:
                    print(c.id, c.stocks, c.score, c.type_stock)

        # xem thẻ có điểm ít nguyên liệu nhất
        
        card_it = state['Board'].dict_Card_Stocks_Show['II'][0]
        
        answer = sum(card_it.stocks.values())
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble' and type_card !='I' :
                for card1 in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if sum(card1.stocks.values())/card1.score > 2 and sum(card1.stocks.values())/card1.score < 4:
                        card_it = card1 
        print(card_it.id,card_it.stocks,card_it.score)
        
        
        

        # list các thẻ lấy được
        list_thelayduoc = []
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for c in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(c):
                        list_thelayduoc.append(c)
        print(list_thelayduoc)

        
        #lấy thẻ có ít nguyên liệu nhất
        card_st = card_it.stocks
        """
        for stock in card_st:
            if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] > 1:
                if state['Board'].stocks[stock] > 0:
                    if len(stocks) < 1 and state['Board'].stocks[stock] > 4: 
                        stocks += [stock,stock]
        if len(stocks) !=2:
            for stock in card_st:
                if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] > 0:
                    if state['Board'].stocks[stock] > 0 and len(stock) < 3:
                        stocks.append(stock)
        
            for stock in state['Board'].stocks:
                if state['Board'].stocks[stock] > 0 and len(stocks) < 3:
                    if stock not in stocks and stock != "auto_color" :
                        stocks.append(stock)
        """
        # hàm lấy 3 nguyên liệu lớn nhất trên bàn
        dict_du = state['Board'].stocks
        del dict_du['auto_color']
        print("dict các sắp xếp giảm dần các thẻ trên bàn",dict_du)

        c = Counter(dict_du)
        most_common = c.most_common(3)
        stocks = [key for key, val in most_common]
        print("3 thẻ lớn nhất đã lấy",stocks)

        #stocks = sorted(dict_du, key=dict_du.get, reverse=True)[:3]

        
        print(stocks)
        print(sum(self.stocks.values()))
           
        #check xem có thẻ có thể lấy được không

        if len(list_thelayduoc) > 0:
            card = list_thelayduoc[0]
        
        # stock_return = ['red', 'red', 'red']
        soNL = sum(self.stocks.values()) + len(stocks) - 10
        if soNL == 2 and len(self.card_upside_down) < 3:
            card = card_it
            stocks = []
        else:
            for stock in self.stocks:
                if self.stocks[stock] > 0 and len(stock_return) < soNL:
                    for stock in card_st:
                        if card_st[stock] - self.stocks[stock] - self.stocks_const[stock] < 0:
                            stock_return.append(stock)
        
        # stocks = []
        return stocks, card, stock_return, 2
    

    
