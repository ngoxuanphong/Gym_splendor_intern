from base.board import Board
from base import player
import random
import operator
player_03 = player.Player("TheGod", 0)


def action(board,  state=None,action_space = None):
    return moiturn(board)


def danhsachthe(board):
    danhsachthe = []
    danhsachthe.extend(player_03.card_upside_down)
    danhsachthe.extend(board.dict_Card_Stocks_Show["III"])
    danhsachthe.extend(board.dict_Card_Stocks_Show["II"])
    danhsachthe.extend(board.dict_Card_Stocks_Show["I"])
    return danhsachthe

# hàm trả nl:


def Luachonbothe(board, *args):
    dict_bo = {
        "red": 0,
        "blue": 0,
        "white": 0,
        "green": 0,
        "black": 0,
        "auto_color": 0
    }
    # Copy Nguyên liệu ban đầu
    dict_bd = player_03.stocks.copy()
    # Thêm Nguyên liệu
    for x in args:
        dict_bd[x] += 1
    # Kiểm tra nguyên liệu còn
    diemnl = {}
    for nl in dict_bd.keys():
        diemnl[nl] = chamdiem(board, nl)
    abc = {k: v for k, v in sorted(
        diemnl.items(), key=lambda item: item[1], reverse=True)}
    danhsachcon = list(abc.keys())
    # Thực hiện bỏ thẻ. Đk bỏ thẻ là bỏ lần lượt.
    if sum(dict_bd.values()) > 10:
        n = sum(dict_bd.values()) - 10
        i = 0
        while n != 0:
            if dict_bd[danhsachcon[i]] != 0:
                dict_bo[danhsachcon[i]] += 1
                dict_bd[danhsachcon[i]] -= 1
                n -= 1
            else:
                i += 1
    return dict_bo

# thẻ có thể úp


def listthecotheup(board):
    a = []
    a.extend(board.dict_Card_Stocks_Show["III"])
    a.extend(board.dict_Card_Stocks_Show["II"])
    a.extend(board.dict_Card_Stocks_Show["I"])
    return a

# thẻ có thể mua


def listcothemua(board):
    a = danhsachthe(board)
    b = []
    for the in a:
        if player_03.checkGetCard(the) == True:
            b.append(the)
    return b

# nguyên liệu có thể lấy 2


def listlay2(board):
    nl = []
    for nguyenlieu in board.dict_Card_Stocks_Show["III"][0].stocks.keys():
        if player_03.checkOneStock(board, nguyenlieu) == True:
            nl.append(nguyenlieu)
    return nl

# nguyên liệu trên bàn


def listnlcon(board):
    nl = {}
    for nguyenlieu in board.dict_Card_Stocks_Show["III"][0].stocks.keys():
        if board.stocks[nguyenlieu] > 0:
            nl[nguyenlieu] = chamdiem(board, nguyenlieu)
    a = {k: v for k, v in sorted(
        nl.items(), key=lambda item: item[1], reverse=True)}
    return list(a.keys())

# thẻ đáng lấy thứ 2


def thet2(board):
    diemmax = 0
    themax = None
    for the in danhsachthe(board):
        if the not in listcothemua(board):
            sonlthieu = 0
            tongnlcan = 0
            for nguyenlieu in the.stocks.keys():
                tongnlcan = max(0, the.stocks[nguyenlieu] - player_03.stocks_const[nguyenlieu]) + tongnlcan
                if max(0, (the.stocks[nguyenlieu]-player_03.stocks_const[nguyenlieu]-player_03.stocks[nguyenlieu])) > sonlthieu:
                    sonlthieu = max(0, (the.stocks[nguyenlieu]-player_03.stocks_const[nguyenlieu]-player_03.stocks[nguyenlieu]))
            diem = min(15-player_03.score,the.score)/(1+sonlthieu)
            # if the.type_stock == nlnhieunhatIII(board)["key"]:
                # print(diem*nlnhieunhatIII(board)["persent"])
            diem += diem*(nlnhieunhatIII(board)[the.type_stock]-0.2)
            if tongnlcan > 10:
                diem = 0
            if diem > diemmax:
                diemmax = diem
                themax = the
    return themax

# Lấy số nguyên liệu cần nhiều nhất trên bàn

def nlnhieunhatIII(board):
    dict_nl = {
        "red" :0,
        "blue":0,
        "white":0,
        "green":0,
        "black":0,
    }
   
    # if len(player_03.card_upside_down) > 1:
    #     for the in player_03.card_upside_down:
    #         for nlieu in the.stocks.keys():
    #             dict_nl[nlieu]+= the.stocks[nlieu]
    # else:
    for cap in board.dict_Card_Stocks_Show.keys():
        # if cap = "Noble":
            for the in board.dict_Card_Stocks_Show[cap]:
                for nlieu in the.stocks.keys():
                    dict_nl[nlieu]+= the.stocks[nlieu]
    for the in player_03.card_upside_down:
        for nlieu in the.stocks.keys():
            dict_nl[nlieu]+= the.stocks[nlieu]
    max = 0
    key = ''
    dict_static = {}
    for i in dict_nl.keys():
        dict_static[i] = dict_nl[i]/sum(dict_nl.values())
        # if dict_nl[i]>max:
        #     max = dict_nl[i]
        #     key = i


    return dict_static


# chấm điểm nguyên liệu


def chamdiem(board, nglieu):
    dictnl = {}
    for nguyenlieu in board.dict_Card_Stocks_Show["III"][0].stocks.keys():
        the = thet2(board)
        sonlthieu = 0
        for nl in the.stocks.keys():
            sonlthieu += max(0, the.stocks[nl] - player_03.stocks_const[nl])
        diem = (the.score/(sonlthieu)- the.score/(sonlthieu+1)) * max(0,(the.stocks[nguyenlieu]-player_03.stocks_const[nguyenlieu]-player_03.stocks[nguyenlieu]))/sonlthieu
        dictnl[nguyenlieu] = diem
    dictnl["auto_color"] = max(dictnl.values())*(1 - len(player_03.card_upside_down) * 0.33)
    return dictnl[nglieu]

# chấm điểm thẻ úp


def dictup(board):
    if player_03.checkUpsiteDown() != True:
        return {}
    else:
        dictup = {}
        for the in listthecotheup(board):
            dictup["U" + str(the.id)] = chamdiem(board, the.type_stock)/sum(the.stocks.values()) + chamdiem(board, "auto_color") * min(1, board.stocks["auto_color"])
            if the == thet2(board):
                return {"U" + str(the.id): chamdiem(board, the.type_stock)/sum(the.stocks.values()) + chamdiem(board, "auto_color") * min(1, board.stocks["auto_color"])}
        return dictup

# chấm điểm thẻ có thể mở


def dictmo(board):
    dictmo = {}
    for the in listcothemua(board):
        chiphi = 0
        for nguyenlieu in the.stocks.keys():
            if the.stocks[nguyenlieu] - player_03.stocks_const[nguyenlieu] > player_03.stocks[nguyenlieu]:
                chiphi += (the.stocks[nguyenlieu] - player_03.stocks_const[nguyenlieu] -
                           player_03.stocks[nguyenlieu]) * chamdiem(board, "auto_color")
                chiphi += player_03.stocks[nguyenlieu] * \
                    chamdiem(board, nguyenlieu)
            else:
                chiphi += (the.stocks[nguyenlieu] -
                           player_03.stocks_const[nguyenlieu]) * chamdiem(board, nguyenlieu)
        dictmo["M" + str(the.id)] = (the.score)-chiphi
    return dictmo

# chấm điểm lấy 2


def dictlay2(board):
    dictlay2 = {}
    a = Luachonbothe(board, "auto_color", "auto_color")
    chiphi = 0
    if a != None:
        for nguyenlieu in a.keys():
            chiphi += a[nguyenlieu] * chamdiem(board, nguyenlieu)
    for nguyenlieu in listlay2(board):
        dictlay2["2" + str(nguyenlieu)] = chamdiem(board,
                                                   nguyenlieu) * 2 - chiphi
    return dictlay2

# chấm điểm lấy 3


def dictlay3(board):
    a = {}
    if len(listnlcon(board)) > 2:
        b = Luachonbothe(board, listnlcon(board)[0], listnlcon(
            board)[1], listnlcon(board)[2])
        chiphi = 0
        if b != None:
            for nguyenlieu in b.keys():
                chiphi += chamdiem(board, nguyenlieu)*b[nguyenlieu]
        a = {"3": (chamdiem(board, listnlcon(board)[
                   0])+chamdiem(board, listnlcon(board)[1])+chamdiem(board, listnlcon(board)[2])-chiphi)}
    return a

# tìm hành động nhiều điểm nhất


def hanhdong(board):
    a = dictup(board)
    if dictmo(board) != None:
        a.update(dictmo(board))
    if dictlay2(board) != None:
        a.update(dictlay2(board))
    if dictlay3(board) != None:
        a.update(dictlay3(board))
    b = {k: v for k, v in sorted(
        a.items(), key=lambda item: item[1], reverse=True)}
    # print(b)
    if len(b) > 0:
        return (list(b.keys()))[0]
    else:
        return None


def moiturn(board):
    # print(nlnhieunhatIII(board))
    if hanhdong(board) == None:
        return board
    a = hanhdong(board)
    # print("Action :",a)
    # print(player_03.stocks)
    if a[0] == "3":
        return player_03.getThreeStocks(listnlcon(board)[0], listnlcon(board)[1], listnlcon(board)[2], board, Luachonbothe(board, listnlcon(board)[0], listnlcon(board)[1], listnlcon(board)[2]))
    if a[0] == "2":
        return player_03.getOneStock(a[1:], board, Luachonbothe(board, a[1:], a[1:]))
    if a[0] == "U":
        for the in listthecotheup(board):
            if the.id == a[1:]:
                return player_03.getUpsideDown(the, board, Luachonbothe(board, "auto_color"))
    if a[0] == "M":
        for the in listcothemua(board):
            if the.id == a[1:]:
                return player_03.getCard(the, board)
    return board