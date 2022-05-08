import copy
from gym_splendor.envs.base import error

class Board:
    def __init__(self):
        self.name = "Board"
        self.max_init_stock = 7
        self.__stocks = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "black": 0,
            "white": 0,
            "auto_color": 5,
        }
        self.__dict_Card_Stocks_Show = {
            'I': [],
            'II': [],
            'III': [],
            'Noble': []
        }
        self.__dict_Card_Stocks_UpsiteDown = {
            'I': [],
            'II': [],
            'III': [],
            'Noble': []
        }
    @property
    def stocks(self):
        return self.__stocks.copy()
    # @stocks.setter
    def Stocks(self,value):
        token = 0
        if value == 4:
            token = 7
        if value == 3:
            token = 5
        if value == 2:
            token = 4
        self.max_init_stock = token
        for key in self.__stocks.keys():
            if key != "auto_color":
                self.__stocks[key] = token
    @property
    def dict_Card_Stocks_Show(self):
        return copy.deepcopy(self.__dict_Card_Stocks_Show)
    # @dict_Card_Stocks_Show.setter
    def setDict_Card_Stocks_Show(self,new_dict):
        self.__dict_Card_Stocks_Show.update(new_dict)


    @property
    def dict_Card_Stocks_UpsiteDown(self):
        return  copy.deepcopy(self.__dict_Card_Stocks_UpsiteDown)
    # @dict_Card_Stocks_UpsiteDown.setter
    def setDict_Card_Stocks_UpsiteDown(self,new_dict):
        self.__dict_Card_Stocks_UpsiteDown.update(new_dict)


# Xóa thẻ trong trồng úp
    def deleteCardInUpsiteDown(self, key, card_stock):
        try:
            self.__dict_Card_Stocks_UpsiteDown[key].remove(card_stock)
        except:
            pass      
        return self
    
    def deleteCardNoble(self, CardNoble):
        card = self.equal(CardNoble,"Noble")
        # print(card)
        self.__dict_Card_Stocks_Show["Noble"].remove(card)


# Thêm thẻ Nguyên liệu
    def appendUpCard(self, key, card_stock):
        try:
            self.__dict_Card_Stocks_Show[key].append(card_stock)
            self.deleteCardInUpsiteDown(key, card_stock)
        except:
            error.RecommendColor("Hết thẻ rồi, Không thêm nguyên liệu được nữa đâu")
        return self

# Xóa thẻ trên bàn chơi
    def deleteUpCard(self, key, card_stock):
        try:
            a = self.__dict_Card_Stocks_UpsiteDown[key][0]
        except:
            a = None

        if a != None:
            self.__dict_Card_Stocks_Show[key] = [a if i.id == card_stock.id else i for i in self.__dict_Card_Stocks_Show[key] ]
            self.deleteCardInUpsiteDown(key,a)
        else:
            card = self.equal(card_stock,key)
            self.__dict_Card_Stocks_Show[key].remove(card)

            
    def equal(self, card_, field):
        for card in self.__dict_Card_Stocks_Show[field]:
                if card_.id == card.id:
                    return card

# Lấy thông tin các thẻ trên bàn
    def getInforCards(self):
        return self.__dict_Card_Stocks_Show

# Trả lại thẻ
    def getStock(self, stock_return):
        for stock in stock_return:
            self.__stocks[stock] -=1
        return self

    def postStock(self, stock_return):
        for stock in stock_return:
            self.__stocks[stock] +=1
        return self
    def hien_the(self):
        for i in self.__dict_Card_Stocks_Show.keys():
            print(i,end=": ")
            for j in self.__dict_Card_Stocks_Show[i]:
                print(j.id, end=" ")
            print()