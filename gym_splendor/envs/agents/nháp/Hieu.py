from typing import get_type_hints
from numpy.core.fromnumeric import sort
from base import player
import random
import math
from scipy.stats import hmean

player_07 = player.Player("test", 0)
def action(board, arr_player):
    return turn(board, player_07)

def turn(board, player_07):
    the_co_the_lay = list_card_can_buy(board, player_07)
    print(the_co_the_lay)
    pick_token = value_function2(board, player_07)
    pick_gold = value_function3(board, player_07)
    dict_value_stock_const = value_function1(board, player_07)
    value_get_card = [-1, -1]
    if len(the_co_the_lay) > 0:
        value_get_card = [Q_function(board, player_07, 'get_card', the_co_the_lay[0], [], dict_value_stock_const), the_co_the_lay[0]]
        for card in the_co_the_lay[1:]:
            val_get_card = Q_function(board, player_07, 'get_card', card, [], dict_value_stock_const)
            if val_get_card > value_get_card[0]:
                value_get_card = [val_get_card, card]
    # print(pick_token)
    # print(type(pick_token[0][1]), pick_token[0][1])
    dict_action = {'pick_gold':pick_gold[1], 'pick_token':sum(item[1] for item in pick_token), 'get_card':value_get_card[0]}
    sort_action = sorted(dict_action.items(),reverse= True, key = lambda x : x[1])
    if sort_action[0][0] == 'pick_gold':
        print('toang1')
        # print(player_07.stocks)
        # print(board.stocks)
        dict_bo = create_dict_return(board, player_07, sum(player_07.stocks.values()) + 1 - 10)
        # print(dict_bo)
        # print(pick_gold)
        return player_07.getUpsideDown(pick_gold[0], board, dict_bo)
    elif sort_action[0][0] == 'get_card':
        print('toang4')
        return player_07.getCard(value_get_card[1], board)
    else:
        if len(pick_token) > 1:
            print('toang2')
            dict_bo = create_dict_return(board, player_07, sum(player_07.stocks.values()) + 3 - 10)
            # print(dict_bo)
            # print(pick_token)
            # print(board.stocks)
            return player_07.getThreeStocks(pick_token[0][0], pick_token[1][0], pick_token[2][0], board, dict_bo)
        elif len(pick_token) > 0:
            print('toang3')
            # dict_bo = create_dict_return(board, player_07, sum(player_07.stocks.values()) + 2 - 10)
                # print(dict_bo)
                # print(pick_token)
                # print(board.stocks)
            return player_07.getOneStock(pick_token[0][0], board, create_dict_return(board, player_07, sum(player_07.stocks.values()) + 2 - 10))
    print('NO ACTION')
    return board


def create_dict_return(board, player, number_bo):
    dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    dict_value_stock2 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + player.card_upside_down
    for card in list_card_show:
        A = sum(card.stocks.values())/2
        B = card.score
        D = B**(1/A)
        C = 0
        for type_stock in dict_value_stock1.keys():
            C += min(player.stocks_const[type_stock] + player.stocks[type_stock], card.stocks[type_stock])
        for type_stock in dict_value_stock1.keys():
            if D > 0:
                if card.stocks[type_stock] > 0 and player.stocks[type_stock] > 0:
                    dict_value_stock1[type_stock] = dict_value_stock1[type_stock] + D**(C-A) - D**(C - 1 - A) 
                if card.stocks[type_stock] > 0 and player.stocks[type_stock] > 1:
                    dict_value_stock2[type_stock] = dict_value_stock2[type_stock] + D**(C-A) - D**(C - 2 - A)
    for type_stock in dict_value_stock1.keys():
        if player.stocks[type_stock] == 0:
            dict_value_stock1[type_stock] = 100
    id = 0
    pick_return = sorted(dict_value_stock1.items(), key = lambda x : x[1])
    dict_bo = {}
    while number_bo > 0:
        dict_bo[pick_return[id][0]] = 1
        id += 1
        number_bo -= 1
    return dict_bo

def value_function1(board, player):
    dict_value_stock_const = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    for card in board.dict_Card_Stocks_Show['Noble']:
        A = sum(card.stocks.values())/2
        B = 3
        D = B**(1/A)
        C = 0
        for type_stock in dict_value_stock_const.keys():
            C += min(player.stocks_const[type_stock], card.stocks[type_stock])
        for type_stock in dict_value_stock_const.keys():
            if card.stocks[type_stock] > 0:
                dict_value_stock_const[type_stock] = dict_value_stock_const[type_stock] + D**(C + 1 - A)*C/(2*A)
    
    return dict_value_stock_const

def value_function2(board, player):
    '''
    tính giá trị của các token khi được bốc 1 hoặc 2 cái
    '''

    dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    dict_value_stock2 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    dict_number_card_stock = {'red':1, 'blue':1, 'green':1, 'white':1, 'black':1}
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + player.card_upside_down
    for card in list_card_show:
        C1 = 0
        for type_stock in dict_value_stock1.keys():
            C1 += min(player.stocks[type_stock] + player.stocks_const[type_stock], card.stocks[type_stock])
        A = sum(card.stocks.values())/2
        B = card.score*C1/sum(card.stocks.values())
        D = B**(1/A)
        
        for type_stock in dict_value_stock1.keys():
            if card.stocks[type_stock] > 0 and board.stocks[type_stock] > 0:
                dict_number_card_stock[type_stock] = dict_number_card_stock[type_stock] + 1
                if B > 0:
                    dict_value_stock1[type_stock] = dict_value_stock1[type_stock] + D**(C1 + 1 - A)
                    if board.stocks[type_stock] > 3:
                        dict_value_stock2[type_stock] = dict_value_stock2[type_stock] + D**(C1+ 2 - A)
    for type_stock in dict_value_stock1.keys():
        dict_value_stock1[type_stock] /= dict_number_card_stock[type_stock]
        dict_value_stock2[type_stock] /= dict_number_card_stock[type_stock]
    pick3 = sorted(dict_value_stock1.items(),reverse= True, key = lambda x : x[1])[:3]
    pick2 = sorted(dict_value_stock1.items(), reverse= True, key = lambda x : x[1])[0]
    # print(pick3)
    # print(pick2)
    if pick2[1] > sum(item[1] for item in pick3):
        return [pick2]
    else:
        if board.stocks[pick3[2][0]] > 0:
            return pick3
        else:
            return {}

def value_function3(board, player):
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III']
    dict_value_stock1 = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    choice = [list_card_show[0], -100]
    if len(player.card_upside_down) == 3:
        return choice
    gold = min(1,board.stocks['auto_color'])
    for card in list_card_show:
        C1 = 0
        for type_stock in dict_value_stock1.keys():
            C1 += min(player.stocks[type_stock] + player.stocks_const[type_stock], card.stocks[type_stock])
        A = sum(card.stocks.values())/2
        B = card.score*C1/sum(card.stocks.values())
        if B > 0:
            D = B**(1/A)
            val = D**(C1+gold-A) 
            #- D**(C1-A) + C1*card.score/(2*A)
            try:
                if val > choice[1]:
                    choice = [card, val]
            except:
                choice = [card, val]

    return choice






def Q_function(board, player, action, card, pick_token, dict_value_stock_const):
    Q_value = 0
    if action == 'get_card':
        Q_value = player.score +  sum(player.stocks_const.values()) + dict_value_stock_const[card.type_stock] + 2 + 2*card.score
        # print('Q_value: ', Q_value)
        
    elif action == 'get_token':
        Q_value = player.score +  sum(player.stocks_const.values()) + sum(item[1] for item in pick_token)
    return Q_value

def list_card_can_buy(board, player):
    thecothelay = []
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + player.card_upside_down
    for the in list_card_show:
        if player.checkGetCard(the) == True:
            thecothelay.append(the)
    return thecothelay