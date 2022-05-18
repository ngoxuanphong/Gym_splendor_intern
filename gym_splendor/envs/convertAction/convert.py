import pandas as pd
from itertools import chain, combinations,combinations_with_replacement

def GetListStock(dict_):
  for key,value in dict_.items():
    if value != 0 :
      yield key

def checkListHopLeReturn(stock,list_stock):
  dict_stock = stock.copy()
  for s in list_stock:
    dict_stock[s] -=1
    if dict_stock[s] <0:
      return False
  return True

def checkListHopLeGet(stock,list_stock,scale):
  dict_stock = stock.copy()
  for s in list_stock:
    if scale == 2 and dict_stock[s] <4:
      return False
    dict_stock[s] -=1
    if dict_stock[s] <0:
      return False
  return True

def PowerSet(iterable):
    list_combinations = list()
    for n in range(4):
        list_combinations += list(combinations_with_replacement(iterable, n))
    return list_combinations

def FilterColor(stocks,Return_=False):
  iterable = sorted(list(GetListStock(stocks)))
  list_color = PowerSet(iterable)
  for input in list_color[1:]:
    amount_stock = len(input)
    if Return_==False:
      if not("auto_color" in input) :
        types_stock = len(list(set(input)))
        scale = amount_stock/types_stock
        if scale==1 or scale==2:
          if checkListHopLeGet(stocks,input,scale)==True:
            yield input
    else:
      if checkListHopLeReturn(stocks,input)==True:
            yield input

def compare(arr1,arr2):
  count = 0
  for i in arr2:
    if i in arr1:
      count +=1
  return count

def formatGetStock(s,r_s):
  dict_color = {"Card":"00","StockAutoColor":"0","TypeAction":"G"}
  for i in range(0,3):
    try: 
      dict_color["Stock"+str(i+1)] = s[i]
    except:
      dict_color["Stock"+str(i+1)] = "0"
  for i in range(0,3):
    try: 
      dict_color["StockReturn"+str(i+1)] = r_s[i]
    except:
      dict_color["StockReturn"+str(i+1)] = "0"
  return dict_color

def getCard(id):
  dict_color = {"Card":id,"StockAutoColor":"0","TypeAction":"O"}
  for i in range(3):
    dict_color["Stock"+str(i+1)] = "0"
    dict_color["StockReturn"+str(i+1)] = "0"
  return dict_color

def getUpDown(id):
  dict_color = {"Card":id,"StockAutoColor":"1","TypeAction":"U"}
  for i in range(3):
    dict_color["Stock"+str(i+1)] = "0"
    dict_color["StockReturn"+str(i+1)] = "0"
  return dict_color

def getUpDownNoneAuto(id):
  dict_color = {"Card":id,"StockAutoColor":"0","TypeAction":"U"}
  for i in range(3):
    dict_color["Stock"+str(i+1)] = "0"
    dict_color["StockReturn"+str(i+1)] = "0"
  return dict_color

def getUpDown_return_stock(id,stock):
  dict_color = {"Card":id,"StockAutoColor":"1","TypeAction":"U"}
  for i in range(3):
    dict_color["Stock"+str(i+1)] = "0"
    dict_color["StockReturn"+str(i+1)] = "0"
  dict_color["StockReturn1"] = stock
  return dict_color

def to_str(i):
  if i < 10:
    return "0"+str(i)
  else:
    return str(i)
  
def CreateAll():
  data = pd.DataFrame(columns = ["TypeAction","Stock1","Stock2","Stock3","Card","StockAutoColor","StockReturn1","StockReturn2","StockReturn3"])
  stocks = {"red":7,"blue":7,"green":7,"white":7,"black":7,"auto_color":5}
  list_get_stock = list(FilterColor(stocks,False))
  list_push_stock = list(FilterColor(stocks,True))
  for s in list_get_stock:
    data = data.append(formatGetStock(s,()), ignore_index=True)
    for r_s in list_push_stock:
      if len(s) >= len(r_s) and compare(s,r_s) == 0:
        data = data.append(formatGetStock(s,r_s),ignore_index=True)
  for i in range(1,91):
    id = to_str(i)
    data = data.append(getCard(id),ignore_index=True)
    data = data.append(getUpDown(id),ignore_index=True)
    data = data.append(getUpDownNoneAuto(id),ignore_index=True)
    for stock in stocks:
      data = data.append(getUpDown_return_stock(id,stock),ignore_index=True)
  data = data.append(getCard("00"),ignore_index=True)
  ma = CreateCode(data)
  data = data.set_index([pd.Index(ma)],[""])
  data.to_json("../data_action/action_space.json",orient="index")
  return data
def CreateCode(data):
  df = data.replace("auto_color",'1').replace("black",'2').replace("blue",'3').replace("green","4").replace("red","5").replace("white",'6')
  arr = []
  for row in range(len(df["Stock1"])):
    s = ""
    for column in df:
      s += df[column][row]
    arr.append(s)
  data["Index"] = [ i for i in range(len(df["Stock1"]))]
  return arr