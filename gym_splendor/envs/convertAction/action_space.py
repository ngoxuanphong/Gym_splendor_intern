from gym_splendor.envs.convertAction import convert as cv
import pandas as pd
import json

def amount(*arg):
    count = 0
    for i in arg:
        if i != "0":
            count += 1
    return count


def IndexPlayer(state, player):
    for i in range(len(state["Player"])):
        if player.stt == state["Player"][i].stt:
            return i


def check_get_card(stocks, stocks_const, stock_card):
    auto_color = stocks["auto_color"]
    for i in stock_card.keys():
        if stocks[i] + stocks_const[i] < stock_card[i]:
            if stocks[i] + stocks_const[i] + auto_color >= stock_card[i]:
                auto_color = stocks[i] + stocks_const[i] + \
                    auto_color - stock_card[i]
            else:
                return False
    return True


class Action_Space_State():
    def __init__(self):
        with open("gym_splendor/envs/data_action/action_space.json") as datafile:
            self.all_action = json.load(datafile)
        with open('gym_splendor/envs/Cards_Splendor.json') as datafile:
            self.all_data = json.load(datafile)
        # self.all_data = pd.read_json("gym_splendor/envs/Cards_Splendor.json")
        self.list_state = []
        self.index_list_state = []
        self.list_all_action = list(self.all_action.keys())

    def clone_all_action(self):
        return self.all_action.copy()

    def process(self):
        self.all_action["amount_stock"] = self.all_action.apply(
            lambda row: amount(row["Stock1", "Stock2", "Stock3"]), axis=1)
        self.all_action["amount_stock_return"] = self.all_action.apply(
            lambda row: amount(row["StockReturn1", "StockReturn2", "StockReturn3"]), axis=1)

    def recomend_action(self, state, player):
        data = pd.DataFrame(columns=["TypeAction", "Stock1", "Stock2", "Stock3",
                                     "Card", "StockAutoColor", "StockReturn1", "StockReturn2", "StockReturn3"])
        stock_board = state["Board"].stocks
        stock_player = player.stocks
        list_get_stock = list(cv.FilterColor(stock_board, Return_=False))
        list_push_stock = list(cv.FilterColor(stock_player, Return_=True))
        for s in list_get_stock:
            if sum(stock_player.values())+len(s) <= 10:
                  data = data.append(cv.formatGetStock(
                      s,()), ignore_index=True)

            for r_s in list_push_stock:
                if len(s) >= len(r_s) and cv.compare(s, r_s) == 0 and sum(player.stocks.values())+len(s)-len(r_s) <= 10:
                    data = data.append(cv.formatGetStock(
                        s, r_s), ignore_index=True)
        for card in state["Board"].getCardUp():
            id = cv.to_str(card.stt)
            # print(id,end=" ")
            if player.check_get_card(card):
                data = data.append(cv.getCard(id), ignore_index=True)
            if stock_board["auto_color"] > 0:
                data = data.append(cv.getUpDown(id), ignore_index=True)
            else:
                data = data.append(cv.getUpDownNoneAuto(id), ignore_index=True)
        List_Code = cv.CreateCode(data)
        list_code = []
        
        for i in List_Code:
            list_code.append(self.all_action[i]["Index"])
        return list_code

    def covertState(self, state, player):
        self.list_state = []
        self.list_state.append(state["Turn"])
        for value in state["Board"].stocks.values():
            self.list_state.append(value)
        list_card = self.formatListCard(state["Board"].getCardUp("Noble"))
        for i in list_card:
            self.list_state.append(i)
        
        index = IndexPlayer(state, player)
        for i in range(index, index+len(state["Player"])):
            vitri = i % len(state["Player"])

            self.list_state.append(state["Player"][vitri].score)

            for value in state["Player"][vitri].stocks.values():
                self.list_state.append(value)
            
            for value in state["Player"][vitri].stocks_const.values():
                self.list_state.append(value)
            list_card = self.formatListCard(state["Player"][vitri].card_open)
            for card in list_card:
                self.list_state.append(card)
            if i == index:
                # print(len(self.list_state))
                list_card = self.formatListCard(state["Player"][vitri].card_upside_down)
                for card in list_card:
                    self.list_state.append(card)
            list_card = self.formatListCard(state["Player"][vitri].card_noble)
            for card in list_card:
                self.list_state.append(card)

        if state["Victory"] == None:
            self.list_state.append(-1)
        elif state["Victory"].stt != player.stt:
            self.list_state.append(0)
        else:
            self.list_state.append(1)
        return self.list_state

    def convertListToState(self, List_State):
        stocks_board = {"red": 1, "blue": 1, "green": 1,
                        "white": 1, "black": 1, "auto_color": 1}
        stocks_player = {"red": 1, "blue": 1, "green": 1,
                         "white": 1, "black": 1, "auto_color": 1}
        stocks_const_player = {"red": 1, "blue": 1,
                               "green": 1, "white": 1, "black": 1}
        list_card = []
        turn = List_State[0]
        # Stock On Board
        vitri = 1
        iterable = sorted(list(cv.GetListStock(stocks_board)))
        for i in range(vitri, vitri+6):
            stocks_board[iterable[i-vitri]] = List_State[i]
        vitri += 6
        # Card On Board
        for i in range(vitri, vitri+90):
            if List_State[i] == 1:
                list_card.append(i-vitri+1)
        # Score player
        score_player = List_State[vitri+100]
        # Stock Player
        vitri += 101
        iterable = sorted(list(cv.GetListStock(stocks_player)))
        for i in range(vitri, vitri+6):
            stocks_player[iterable[i-vitri]] = List_State[i]
        # Stock Const Player
        vitri += 6
        iterable = sorted(list(cv.GetListStock(stocks_const_player)))
        for i in range(vitri, vitri+5):
            stocks_const_player[iterable[i-vitri]] = List_State[i]
        # Card UpSiteDown
        card_up_down = []
        vitri = 219
        for i in range(vitri, vitri+100):
            if List_State[i] == 1:
                list_card.append(i-vitri+1)
                card_up_down.append(i-vitri+1)
        # print("dichtustate: ",list_card)
        
        data = pd.DataFrame(columns=["TypeAction", "Stock1", "Stock2", "Stock3",
                                     "Card", "StockAutoColor", "StockReturn1", "StockReturn2", "StockReturn3"])
        list_get_stock = list(cv.FilterColor(stocks_board, Return_=False))
        list_push_stock = list(cv.FilterColor(stocks_player, Return_=True))
        for s in list_get_stock:
            if sum(stocks_player.values())+len(s) <= 10:
                data = data.append(cv.formatGetStock(
                    s,()), ignore_index=True)
            for r_s in list_push_stock:
                if len(s) >= len(r_s) and cv.compare(s, r_s) == 0 and sum(stocks_player.values())+len(s)-len(r_s) <= 10:
                    data = data.append(cv.formatGetStock(
                        s, r_s), ignore_index=True)
            
        for card in list_card:
            id = cv.to_str(card)
            # print(id,end = " ")
            card_stock = self.all_data[card]["stock"].copy()
            if check_get_card(stocks_player, stocks_const_player, card_stock):
                data = data.append(cv.getCard(id), ignore_index=True)
            if len(card_up_down)<3 and not (card in card_up_down):
                if stocks_board["auto_color"] > 0:
                    data = data.append(cv.getUpDown(id), ignore_index=True)
                else:
                    data = data.append(cv.getUpDownNoneAuto(id), ignore_index=True)
        
        List_Code = cv.CreateCode(data)
        list_code = []
        for i in List_Code:
            list_code.append(self.all_action[i]["Index"])
        list_code.append(1295)
        return list_code

    def formatListCard(self, arr):
        list_card = [0 for i in range(0, 100)]
        for card in arr:
            list_card[card.stt-1] = 1
        return list_card