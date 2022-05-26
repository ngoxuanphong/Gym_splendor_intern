from re import T
from ..base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
        listcard= []
        max1=0
        d=0
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        listcard.append(card)
        for card in self.card_upside_down:
            if self.check_get_card(card):
                listcard.append(card)
        for card in listcard:
            if len(listcard) >0:
              if card.score>max1: 
                  max1=card.score
        for card in listcard:
            if card.score==max1:
                return stocks, card, stock_return
        for stock in state["Board"].stocks:     
            if stock !="auto_color":
                if state["Board"].stocks[stock] > 0 and stock not in stocks:
                    stocks.append(stock)
                    if len(stocks)==3:  
                        break         
        t=sum(self.stocks.values()) + len(stocks) -10
        if t>=0:
                for i in self.stocks:
                    if i !='auto_color':
                        if self.stocks[i] >0:
                            if len(stock_return) < t:
                                stock_return.append(i)
        return stocks, card, stock_return
