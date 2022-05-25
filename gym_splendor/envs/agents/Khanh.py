from ..base.player import Player
import random
import math

import copy
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []

        list_card_can_buy = self.list_card_can_buy(state['Board'])
        if list_card_can_buy.__len__() != 0:
            return [], list_card_can_buy[0], [] 

        list_card_target = []
        list_card = []
        for key in state['Board'].dict_Card_Stocks_Show.keys():
            if key != 'Noble' :
                for j in state["Board"].dict_Card_Stocks_Show[key]:
                    if j.score > 1 and 2 >= (sum(j.stocks.values())/j.score) and(sum(j.stocks.values())/j.score) >= 1.75 :
                        list_card_target.append(j)
        for key in state['Board'].dict_Card_Stocks_Show.keys():
            if key != 'Noble' :
                for j in state["Board"].dict_Card_Stocks_Show[key]:
                    if j.score >= 1 and  (sum(j.stocks.values())/j.score) <= 4 and (sum(j.stocks.values())/j.score)> 1.75 and sum(j.stocks.values())<= 9 :
                        list_card_target.append(j)
                    elif j.score >= 1:
                        list_card_target.append(j)
                
        list_card_target.sort(key=lambda x: (sum(x.stocks.values())/(x.score)))
        if (self.card_upside_down == 3 and sum(self.stocks.values()) == 10) or (sum(state['Board'].stocks.values())-state["Board"].stocks['auto_color'] == 0) :
            if list_card_can_buy.__len__() != 0:
                return [], list_card_can_buy[0], []    
        for i in list_card_target:
            #print(i.id, i.stocks,i.type_stock)
            break
        #print('-----------')
        #print(list_card_target[0].score,list_card_target[0].stocks,list_card_target[0].type_stock)
        if len(self.card_upside_down) < 3:
            for i in self.card_upside_down:
                #print(i.id ,i.type_stock,i.stocks)
                break
            for i in range(0,1):
                if len(self.card_upside_down) == 0 : 
                    return [],list_card_target[0],i
            if len(self.card_upside_down)> 0 :
                self.card_upside_down.sort(key=lambda x: (sum(x.stocks.values())/(x.score+1)))
                list_card = self.list_card_of_target(state['Board'],self.card_upside_down)
                #print("!!!!!!!")
                for i in list_card:
                    #print(i.id,i.score, i.stocks,i.type_stock)
                    break
                #print('_-------------')
                
                for i in range(0,1):
                    if 'III' not in self.card_upside_down[0].id and 'II' not in self.card_upside_down[0].id: 
                        return [],list_card_target[0],i
                for i in range(0,2):
                    if len(list_card) != 0 and len(self.card_upside_down) <= 2 :
                        target = list_card[i]
                        return [],target,[]     
            
        else:
            for i in self.card_upside_down:
                #print(i.id ,i.type_stock,i.stocks)
                break
            self.card_upside_down.sort(key=lambda x: (sum(x.stocks.values())/(x.score+1)))
            for i in range(0,3):
                #print(self.card_upside_down[i].id,self.card_upside_down[i].stocks)
                break
            target  = self.card_upside_down[1]
            target1 = self.card_upside_down[2]
            target2 = self.card_upside_down[0]

            if self.check_get_card(target2) == True :
                return [],target2,[]
            elif self.check_get_card(target1) == True:
                return [],target1,[]
            elif self.check_get_card(target) == True :
                return [],target,[]
            
            stocks_get = self.lack_of_stocks(target)
            # lay tai nguyen 
            stocks = [key for key in stocks_get if stocks_get[key] != 0 and state['Board'].stocks[key] != 0]               
            for key in stocks_get :
                if stocks_get[key] != 0 and stocks_get[key] >= 2 and state['Board'].stocks[key] >= 4 :
                    stocks = [key,key]
                if stocks_get[key] != 0 and state['Board'].stocks[key] == 0 :
                    stocks_get1 = self.lack_of_stocks(target1)
                    stocks = [key1 for key1 in stocks_get1 if stocks_get1[key1] != 0 and state['Board'].stocks[key1] != 0]
                    for key1 in stocks_get1 :
                        if stocks_get1[key1] != 0 and stocks_get1[key1] >= 2 and state['Board'].stocks[key1] >= 4 :
                            stocks = [key1,key1]
                        if stocks_get1[key1] != 0 and state['Board'].stocks[key1] == 0 :
                            target2 = list_card_target[0]
                            stocks_get2 = self.lack_of_stocks(target2)
                            stocks = [key2 for key2 in stocks_get2 if stocks_get2[key2] != 0 and state['Board'].stocks[key2] != 0]
                            for key2 in stocks_get2 :
                                if stocks_get2[key2] != 0 and stocks_get2[key2] >= 2 and state['Board'].stocks[key2] >= 4 :
                                    stocks = [key2,key2]
                                if (stocks_get2[key2] != 0 and state['Board'].stocks[key2] == 0) :
                                    for i,val in state['Board'].stocks.items():
                                        if len(stocks) == 3 :
                                            break 
                                        if val != 0 and i != "auto_color" :
                                            stocks.append(i) 
                                    for i in stocks : 
                                        if stocks.count(i) >=2 and len(stocks) == 3 and (state['Board'].stocks[i]>=4):
                                            stocks = [i,i]
                                            break 
                                        if stocks.count(i) >=2 and len(stocks) == 3 and len(set(stocks)) == 2 and (state['Board'].stocks[i]) <4:
                                            stocks.remove(i)
                                            break
            # lay tai nguyen 
            if len(stocks) == 1 and (sum(state['Board'].stocks.values())-state["Board"].stocks['auto_color'] >= 3)  :
                for i in self.card_upside_down:
                    if len(stocks) == 3 :
                        break
                    for key1,vall in self.lack_of_stocks(i).items():
                        if key1 not in stocks and self.lack_of_stocks(i)[key1] != 0 and state['Board'].stocks[key1] != 0 and len(stocks) < 3:
                            stocks.append(key1)                    
                for j in list_card:
                    if len(stocks) == 3 :
                        break   
                    for key2,vval in self.lack_of_stocks(j).items():
                        if key2 not in stocks and self.lack_of_stocks(i)[key2] != 0 and state['Board'].stocks[key2] != 0 and len(stocks) < 3:
                            stocks.append(key2)                 
                for k in list_card_can_buy:
                    if len(stocks) == 3 :
                        break   
                    for key3,vvall in self.lack_of_stocks(k).items():                     
                        if key3 not in stocks and self.lack_of_stocks(i)[key3] != 0 and state['Board'].stocks[key3] != 0 and len(stocks) < 3:
                            stocks.append(key3)
                for i in stocks : 
                    if stocks.count(i) >=2 and len(stocks) == 3 :
                        stocks = [i,i]
                        break
            if len(stocks) == 2 and sum(self.stocks.values()) < 10 and len(set(stocks))== 2 :
                for i,val in state['Board'].stocks.items():
                    if len(stocks) == 3 :
                        break 
                    if val != 0 and i != "auto_color" and i not in stocks:
                        stocks.append(i) 
            if len(stocks) == 2 and sum(self.stocks.values()) < 10 and len(set(stocks)) == 1 :
                for i,val in state['Board'].stocks.items():
                    if len(stocks) == 3 :
                        break 
                    if val < 4 and i != "auto_color" and i  in stocks:
                        stocks.remove(i) 

            fmax_key = max(stocks_get, key= stocks_get.get) 
            stocks_get1 = self.lack_of_stocks(target1)
            fmax_key2  = max(stocks_get1,key = stocks_get1.get)
            stocks_get2 = self.lack_of_stocks(list_card_target[0])
            fmax_key3 = max(stocks_get2,key = stocks_get2.get)
            stocks_return = self.return_stocks(stocks,fmax_key,fmax_key2,fmax_key3)                     
            return stocks,None, stocks_return
        
    def return_stocks(self, stocks_get,cars,carr,carrr):
        my_stocks = self.stocks
        stocks_return = []
        for key in stocks_get:
            my_stocks[key] += 1
        if sum(my_stocks.values()) > 10:
            n = sum(my_stocks.values())-10
            for i in range(n):
                for key in my_stocks.keys():
                    if key !=cars :
                        if my_stocks[key] >= 1  :
                            stocks_return += [key]
                            my_stocks[key] -= 1
                            break
        else:
            stocks_return = []
        return stocks_return
    
    
    def lack_of_stocks(self, _card):
        price = _card.stocks # dict, 5 keys
        my_stocks = {}
        for key in self.stocks_const.keys():
            my_stocks[key] = self.stocks[key] + self.stocks_const[key]

        my_stocks['auto_color'] = self.stocks['auto_color']

        lack_of_stocks = {}
        for key in price.keys():
            lack_of_stocks[key] = max(0, price[key] - my_stocks[key])

        n = my_stocks['auto_color']

        for i in range(n):
            if sum(lack_of_stocks.values()) == 0:
                break
            for key in lack_of_stocks.keys():
                if lack_of_stocks[key] != 0:
                    lack_of_stocks[key] -= 1
                    break
        return lack_of_stocks
    def list_card_of_target(self,boar ,card) : #return list of card support the card type = "III"
        list_card = []

        for key in boar.dict_Card_Stocks_Show.keys():
            if key != 'Noble' :
                for j in boar.dict_Card_Stocks_Show[key]:
                    if  card[0].stocks[j.type_stock] > 0 and j != card[0] and sum(j.stocks.values())<=9 and key != "III" :
                        list_card.append(j)
                        
        if len(list_card) == 0 :
            for key in boar.dict_Card_Stocks_Show.keys():
                if key != 'Noble' :
                    for j in boar.dict_Card_Stocks_Show[key]:
                        if card[0].stocks[j.type_stock] > 0:
                            list_card.append(j)
                        else:
                            list_card.append(j)

        if 0 < len(list_card) < 2 : 
            for key in boar.dict_Card_Stocks_Show.keys():
                if key != 'Noble' :
                    for j in boar.dict_Card_Stocks_Show[key]:
                        if card[0].stocks[j.type_stock] ==0 and list_card[0].stocks[j.type_stock] >0 :
                            list_card.append(j)
        return list_card

    def list_card_can_buy(self, board):
        _temp = []
        for key in board.dict_Card_Stocks_Show.keys():
            if key != 'Noble':
                for card in board.dict_Card_Stocks_Show[key]:
                    if self.check_get_card(card):
                        _temp.append(card)
        
        for card in self.card_upside_down:
            if self.check_get_card(card):
                _temp.append(card)

        return _temp