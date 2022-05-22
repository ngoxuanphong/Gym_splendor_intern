# from Gym_splendor_intern.gym_splendor.envs.base.board import Board
from numpy import append
from ..base.player import Player
import random
import math
# BOARD
#dict_Card_Stocks_Show: thể hiện thẻ đang mở trên bàn chơi
#stocks: nguyên liệu
# PLAYER
# self.score: Điểm 
# self.stocks: Nguyên liệu
# self.stocks_const: xem nguyên liệu vĩnh viễn mặc định
# self.card_open:thẻ đã mở
# self.card_upside_down: thẻ đang up 
# self.card_noble: thẻ quý tộc
# CARD ( id, stocks, score, type_stock)
# AGENT(self, state):
#   State={"Turn":            ,
#          "Board":...........,
#           "Player":..........}
# RETURN:stocks, card, stock_return
# Các ý tưởng code bot:(Lấy các loại thẻ/ Target thẻ trên bàn/ Lấy NL bất kỳ --> lấy thẻ có thể lấy )
# 1. def_check_card(): Kiểm tra có lấy được hay không?
#     True-> card = card_target
#     False-> Card = None



class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, state):
        stocks = []
        card = None
        stock_return = []
# Tìm thẻ target: những thẻ đang mở trên bàn có điểm, -> có sum stocks min-> điểm cao nhất 
        C=[]
        D=[]
        for card_type in state['Board'].dict_Card_Stocks_Show:
            for i in state['Board'].dict_Card_Stocks_Show[card_type]:
                EE=[]
                if i.score>0 and card_type!= "Noble" :
                # if i.score>0 and card_type!= "Noble" and card_type!= 'I':
                    C.append(i)
                    # auto_color = self.__stocks["auto_color"]
                    for stock in i.stocks:
                        if i.stocks[stock]- self.stocks[stock]- self.stocks_const[stock]> 0:
                            EE.append(i.stocks[stock]- self.stocks[stock]- self.stocks_const[stock])
                        else:
                            EE.append(0)
                        # print(card.id,card.stocks,card.score, card.type_stock)
                    if sum(EE)- self.stocks["auto_color"] <0:
                        D.append(0)
                    else:
                        D.append(sum(EE)- self.stocks["auto_color"])
                    # for stock in card:
                    #     # print(card[stock])
        # print("do loi -------",(type(card)))
        # print(len(C),len(D))
        diem=0
        card_tg={}

        for i in range(0,len(D),1):
           
            if D[i]==min(D):
                if C[i].score>diem:
                    diem=C[i].score
                    card_tg=C[i]
        # C=[]
        # D=[]
        # for card_type in state['Board'].dict_Card_Stocks_Show:
        #     for i in state['Board'].dict_Card_Stocks_Show[card_type]:
        #         if i.score>0 and card_type!= "Noble":
        #             C.append(i)
        #             # a=i.stocks
        #             # print(card.id,card.stocks,card.score, card.type_stock)
        #             D.append(sum(i.stocks.values()))
        #             # for stock in card:
        #             #     # print(card[stock])
        # # print("do loi -------",(type(card)))
        # diem=0
        # card_tg={}

        # for i in range(0,len(D),1):
           
        #     if D[i]==min(D):
        #         if C[i].score>diem:
        #             diem=C[i].score
        #             card_tg=C[i]
                
        # print("the target",card_tg.stocks,card_tg.score,card_tg.type_stock)       
        # print(D)
        
        
#  Lấy stocks theo thẻ target  
        p=0
        card_st=card_tg.stocks
        for stock in card_st:
            p=1
            if card_st[stock]- self.stocks[stock]- self.stocks_const[stock]> 1 and state['Board'].stocks[stock]>0:
                
                if len(stocks)<1:
                    # print("sai",state['Board'].stocks[stock])
                    if state['Board'].stocks[stock] >3:
                        stocks.append(stock)
                        stocks.append(stock)
                    elif state['Board'].stocks[stock] <4:
                        stocks.append(stock)
            elif card_st[stock]- self.stocks[stock]- self.stocks_const[stock]>0 and state['Board'].stocks[stock]>0:
                if len(stocks) < 3:
                    if len(stocks)==2 and stocks[0]==stocks[1]:
                        pass
                    else:
                        stocks.append(stock) 
                # if len(stocks)==0:

        for stock in state['Board'].stocks:
            p=1
            if len(stocks) < 3 and stock not in stocks and stock != 'auto_color' :
                if len(stocks)==2 and stocks[0]==stocks[1]:
                    pass
                elif state['Board'].stocks[stock]>0:
                    stocks.append(stock)
         
        
# Upthe khi  tren tay có 10 nguyen lieu 
        if sum(self.stocks.values())==10 and self.check_upsite_down(card_tg):
            diemm=100
            p = 3
            AA=[]
            card=card_tg
            for i in self.stocks:
            
                if len(stock_return)<2 and 0<self.stocks[i]<diemm and i != 'auto_color':
                    diemm = self.stocks[i]
                    AA.append(i)
            # print(AA,"kokoko")
            stock_return.append(AA[-1])
        # print(stock_return,"leuleu")
        
        if len(stocks)<1 and self.check_upsite_down(card_tg):
            p=3
            if sum(self.stocks.values())<10:
                pass
#  Tạo list thẻ có thể lấy
        List_card_can_take =self.check_list_card_can_take(state)
        # print(List_card_can_take,'aoila')
        a=1000
        diemmm=0
        List_card_can_take_2=[]
        for Card in List_card_can_take:
            if sum(Card.stocks.values())<a and Card.score>diemmm:
                a= sum(Card.stocks.values())
                diemmm=Card.score
                List_card_can_take_2.append(Card)
            elif Card.score>diemmm:
                a= sum(Card.stocks.values())
                diemmm=Card.score
                List_card_can_take_2.append(Card)
            elif sum(Card.stocks.values())<a:
                a= sum(Card.stocks.values())
                diemmm=Card.score
                List_card_can_take_2.append(Card)
            # print(List_card_can_take_2,'kkkkk')
        if len(List_card_can_take_2)>0 :
            
            p=2
            if self.check_get_card(List_card_can_take_2[len(List_card_can_take_2)-1]):
                stocks=[]
                card=List_card_can_take_2[len(List_card_can_take_2)-1]
                # print(stocks, card.id, stock_return)
                # return stocks, card, stock_return,2
            # print('hhhhhh')
       
        


        elif len(stocks)>0:
            stock_return=[]
            p=1
            for stock in state['Board'].stocks: 
                # print(stock)          
                if stock != 'auto_color' and sum(self.stocks.values())+len(stocks)-len(stock_return)>10 :
                    if stock in stocks and card_st[stock]<1 and len(stock_return) <3:
                        stock_return.append(stock)
                    if card_st[stock]<1 and len(stock_return) <3 and self.stocks[stock]>0 and self.stocks[stock] + self.stocks_const[stock]-card_st[stock]>0:
                            # print(self.stocks[stock],"babab")
                        stock_return.append(stock)
                    elif len(stock_return) <3 and self.stocks[stock]>0 and self.stocks[stock] + self.stocks_const[stock]-card_st[stock]>0:
                        stock_return.append(stock)

        # print(stock_return,"tl")     
        # print('imissu',sum(self.stocks.values()))
        # print('imissu',len(stocks))  
        # print('so the dang up', len(self.card_upside_down))
        # print(self.stocks,"NL player")
        try:
            # print(card.stocks, card.id)
            pass
        except:
            pass
        # print(state['Board'].stocks,"NL ban choi")
        # print(self.name)
        # print("return",stocks, card, stock_return,p)
        try:
            # print(self.check_input_stock(stocks,state),"kiem tra dau vao")
            pass
        except:
            pass

        # card= state['Board'].dict_Card_Stocks_Show['I'][0]
        return stocks, card, stock_return,p

    # def check_card_can_take(self,card):
    #     price= card.stocks
    #     NL_vang = self.stocks['auto_color']
    #     for stock in price:
    #         if self.stocks[stock]+ self.stocks_const[stock]+ NL_vang- price[stock]>=0:
    #             NL_vang=

    #             # if self.stocks[stock]+ self.stocks_const[stock]- price[stock]+NL_vang>=0:
    #             #     NL_vang = self.stocks[stock]+ self.stocks_const[stock]- price[stock]+NL_vang
    #             # else:   
    #             return False
    #     return True
    
    def check_list_card_can_take(self,state):
        List_card_can_take=[]
        # print(List_card_can_take, 'hahahaha')
        for card_type in state['Board'].dict_Card_Stocks_Show:
            if card_type != 'Noble' :
                # and card_type != 'I'
                for Card in state['Board'].dict_Card_Stocks_Show[card_type]:
                    if self.check_get_card(Card):
                        List_card_can_take.append(Card)
        for Card in self.card_upside_down:
            if self.check_get_card(Card):
                List_card_can_take.append(Card)
        
        # print(List_card_can_take,"List_card_can_take")
        return List_card_can_take

                


                


        



        
        
    