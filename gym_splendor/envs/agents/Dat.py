
from gym_splendor.envs.base.board import Board
from ..base.player import Player
import random
import math

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
        
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if card.score >0:
                        if sum(card.stocks.values()) / card.score <= max_value:
                            max_value = sum(card.stocks.values()) / card.score           
                    else:
                        continue
            
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if card.score >0:
                        if sum(card.stocks.values()) / card.score==max_value:
                            card_selected_best_1 = card
                            card_stocks_best_1 = card.stocks
                          #  print(card.stocks, card.score, card.type_stock)

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
                        card_selected_best_2 = card
                        card_stocks_best_2 = card.stocks
                      #  print(card.stocks, card.score, card.type_stock)
                        break

        #list of available card to choose                    
        list_card_id_avai = []
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    if self.check_get_card(card):
                        list_card_id_avai.append(card.id)

        # print(list_card_id_avai)
        #list all card on board
        list_card_id_on_board = []
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    list_card_id_on_board.append(card.id)
        #select the optimal card to take
        if self.check_get_card(card_selected_best_1):
            card_selected = card_selected_best_1
            card_stocks = card_stocks_best_1
        elif self.check_get_card(card_selected_best_2):
            card_selected = card_selected_best_2
            card_stocks = card_stocks_best_2
        elif len(list_card_id_avai) >0:
    
            for type_card in state['Board'].dict_Card_Stocks_Show:
                if type_card != 'Noble':
                    for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                        if card.id==list_card_id_avai[0]:
                            card_selected = card
                            card_stocks = card.stocks
        else:
            random_num = random.randint(0,len(list_card_id_on_board)-1)
            for type_card in state['Board'].dict_Card_Stocks_Show:
                if type_card != 'Noble':
                    for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                        if card.id==list_card_id_on_board[random_num]:
                            card_selected = card
                            card_stocks = card.stocks
           

      #  print("Thẻ đã target:")
      #  print(card_stocks,card_selected.score,card_selected.id)
        
        
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

            #      
            for stock in state['Board'].stocks: 
                # print(stock)          
                if stock != 'auto_color' and sum(self.stocks.values())+len(stocks)-len(stock_return)>10 :
                    if stock in stocks and card_stocks[stock]<1 and len(stock_return) <3:
                        stock_return.append(stock)
                    if card_stocks[stock]<1 and len(stock_return) <3 and self.stocks[stock]>0 and self.stocks[stock] + self.stocks_const[stock]-card_stocks[stock]>0:
                            
                        stock_return.append(stock)
                    elif len(stock_return) <3 and self.stocks[stock]>0 and self.stocks[stock] + self.stocks_const[stock]-card_stocks[stock]>0:
                        stock_return.append(stock)
        

        card = card_selected                    




        
        return stocks, card, stock_return