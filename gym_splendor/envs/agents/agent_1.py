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

        # Print các thẻ có trên bàn, theo thứ tự các loại thẻ I, II, III, Noble
        for type_card in state['Board'].dict_Card_Stocks_Show:
            if type_card != 'Noble':
                for card in state['Board'].dict_Card_Stocks_Show[type_card]:
                    print(card.id, card.stocks, card.score, card.type_stock)


        #Gán card taget :để lấy nguyên liệu là card loại 1 và stt đầu tiên(vì nó là một list)
        #stocks là một dict nguyên liệu của thẻ đó
        card_st = state['Board'].dict_Card_Stocks_Show['I'][0].stocks
        print(card_st)
        stocks = []

        # Kiểm tra xem nguyên liệu của thẻ cần là bao nhiêu để lấy nguyên liệu
        for stock in card_st:
            if card_st[stock] - self.stocks[stock] > 0:
                if len(stocks) < 3: # Do mỗi turn chỉ được lấy tối đa 3 nguyên liệu, nên <3
                    stocks.append(stock)
        print(stocks)

        #Gán card taget là thẻ đầu tiên loại 1 trên bàn
        card = state['Board'].dict_Card_Stocks_Show['I'][0]

        #In ra nguyên liệu mặc định của người chơi đó(nguyên liệu thẻ đã lấy)
        print(self.stocks_const)


        # stocks là một list các nguyên liệu cần ví dụ: ['red', 'red'] hoặc ['blue', 'green', 'black']
        # card là một đối tượng, gán thẳng từ bàn chơi như dòng 36
        # stock_return cũng là một list giống stocks
        return stocks, card, stock_return
    