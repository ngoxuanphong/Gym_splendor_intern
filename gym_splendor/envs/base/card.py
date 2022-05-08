class Card:
    tt = 0
    def __init__(self,id, score, dict_buy):
        self.__score = score
        self.__stocks = dict_buy
        self.__id = id
        self.stt = Card.tt+1
        Card.tt = self.stt
    @property
    def id(self):
        return self.__id
    @id.setter
    def setId(self,value):
        self.__id = value
    @property
    def score(self):
        return self.__score
    @score.setter
    def setScore(self,value):
        self.__score = value
    #Stock 
    @property
    def stocks(self):
        return self.__stocks.copy()
    @stocks.setter
    def setStocks(self,value):
        self.__stocks = value



class Card_Stock(Card):
    def __init__(self,id, type_stock, score, dict_buy):
        super().__init__(id, score, dict_buy)
        self.__type_stock = type_stock.replace("type_","")
    
    @property
    def type_stock(self):
        return self.__type_stock
    @type_stock.setter
    def setType_stock(self,value):
        self.__type_stock = value

    
class Card_Noble(Card):
    pass