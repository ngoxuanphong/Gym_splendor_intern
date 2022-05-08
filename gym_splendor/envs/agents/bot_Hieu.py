from base import player
import numpy as np
import math
from scipy.stats import hmean
import pandas as pd
player_01 = player.Player("3", 0)
#DONE
def action(board, arr_player):
    file_card_point = pd.read_csv('file_card_point.csv')
    return turn(board, player_01, file_card_point)

def turn(board, player, file_card_point):
    '''hàm này trả ra action trong turn '''
    the_co_the_lay = list_card_can_buy(board, player)

    target_card = create_target_card(board, player, file_card_point)
    if target_card in the_co_the_lay:
        return player.getCard(target_card, board)

    pick_token = value_function2(board, player_01)
    dict_value_stock_const = value_function1(board, player_01)
    value_get_card = [-1, -1]

    if len(the_co_the_lay) > 0:
        value_get_card = [Q_function(board, player_01, 'get_card', the_co_the_lay[0], [], dict_value_stock_const), the_co_the_lay[0]]
        for card in the_co_the_lay[1:]:
            val_get_card = Q_function(board, player_01, 'get_card', card, [], dict_value_stock_const)
            if val_get_card > value_get_card[0]:
                value_get_card = [val_get_card, card]
    
    if value_get_card[0] >= sum(item[1] for item in pick_token):
        return player_01.getCard(value_get_card[1], board)
    else:
        if len(pick_token) > 1:
            dict_bo = create_dict_return(board, player_01, sum(player_01.stocks.values()) + 3 - 10)
            return player_01.getThreeStocks(pick_token[0][0], pick_token[1][0], pick_token[2][0], board, dict_bo)
        elif len(pick_token) > 0:
            return player_01.getOneStock(pick_token[0][0], board, create_dict_return(board, player_01, sum(player_01.stocks.values()) + 2 - 10))
    return board

#DONE
def check_probability_get_card(card, player):
    dict_stock_need = {'red':0, 'blue':0, 'green':0, 'white':0, 'black':0}
    for type_stock in dict_stock_need.keys():
        dict_stock_need[type_stock] = max(min(card.stocks[type_stock] - player.stocks[type_stock] - player.stocks_const[type_stock], card.stocks[type_stock]),0)
    stock_need = sum(dict_stock_need.values())
    probability_get_card = (sum(card.stocks.values()) - sum(dict_stock_need.values()))/sum(card.stocks.values())
    return probability_get_card

#DONE
def create_target_card(board, player, file_card_point):
    '''
    hàm này trả ra danh sách thẻ mình hướng đến, có thể là 1 hoặc n thẻ, hoặc list thẻ theo thứ tự
    '''
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III']
    list_card_point = create_list_card_point(board, player, file_card_point)
    probability_card = np.array(list_card_point)/np.sum(np.array(list_card_point))    
    #nếu muốn lấy nhiều thẻ hơn, sửa thành np.random.choice(list_card_show, number_card, probability_card)
    target_card = np.random.choice(list_card_show,p=probability_card)
    return target_card

#DOING
def create_list_card_point(board, player, file_card_point):
    '''
    hàm này cập nhật lại giá trị của thẻ dựa trên kết quả tích lũy các ván chơi và thêm sự đánh giá tình hình hiện tại, cần viết thêm vì cái này chưa có gì
    '''
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III']
    list_card_point = []
    for card in list_card_show:
        #đoạn này cần thêm yếu tố đánh giá nội tại của người chơi đối với các thẻ
        card_point = float(file_card_point[file_card_point["ID"]==card.id]["Score"])
        # card_point = 1
        list_card_point.append(card_point)
    return list_card_point

#DOING
def create_dict_return(board, player, number_bo):
    '''
    hàm này tạo ra dict token cần trả lại khi số token có quá 10
    '''
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

#DOING
def value_function1(board, player):
    '''
    hàm này tính giá trị của cái loại thẻ trong việc lấy thẻ noble
    '''
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
                dict_value_stock_const[type_stock] = dict_value_stock_const[type_stock] + D**(C + 1 - A)
    return dict_value_stock_const

#DOING
def value_function2(board, player):
    '''
    tính giá trị của các token khi được bốc 3 loại token hay 1 loại token, cần xem xét thêm trường hợp bàn không đủ 3 loại token thì thế nào
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

#DOING
def value_function3(board, player):
    '''
    hàm này tính giá trị của việc úp thẻ, cần tối ưu thêm
    '''
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
            val = D**(C1+gold-A) - D**(C1-A) + C1*card.score/(2*A)
            try:
                if val > choice[1]:
                    choice = [card, val]
            except:
                choice = [card, val]

    return choice
#DOING
def Q_function(board, player, action, card, pick_token, dict_value_stock_const):
    '''
    hàm này tính giá trị đanh giá người chơi theo quy ước, cần sửa thêm để tối ưu
    '''
    Q_value = 0
    if action == 'get_card':
        Q_value = player.score +  sum(player.stocks_const.values()) + dict_value_stock_const[card.type_stock] + 2 + 2*card.score
    elif action == 'get_token':
        Q_value = player.score +  sum(player.stocks_const.values()) + sum(item[1] for item in pick_token)
    return Q_value
#DONE
def list_card_can_buy(board, player):
    '''
    hàm này đưa ra danh sách các thẻ ăn được ngay
    '''
    the_co_thelay = []
    list_card_show = board.dict_Card_Stocks_Show['I'] + board.dict_Card_Stocks_Show['II'] + board.dict_Card_Stocks_Show['III'] + player.card_upside_down
    for the in list_card_show:
        if player.checkGetCard(the) == True:
            the_co_thelay.append(the)
    return the_co_thelay