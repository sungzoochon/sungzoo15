import time
import pyupbit
import datetime
import numpy as np
access = "dNlYFPozFWnpa6gtT7OuOjLFbx7iD65qCkWVxxTg"
secret = "nzhg0ah7Lh3XX2nKlUxBY904RBoSbpBHMrf8pGrZ"
upbit = pyupbit.Upbit(access, secret)
def get_ror(k=0.5,coin = "KRW-BTC"):
  try:
    df = pyupbit.get_ohlcv(coin, count=3)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range']

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)
    ror = df['ror'].cumprod()[-2]
    return ror
  except Exception as e:
        return "error"
def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time
def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
def get_high(coin = "KRW-BTC"):
  try:
    df = pyupbit.get_ohlcv(coin, count=1)
    df['ror'] = df['high']
    ror = df['ror'].cumprod()[0]
    return ror
  except Exception as e:
        return "error"
coini ="BTC"
coin = "KRW-"+ coini
buy_price =[4915,0]
buy_list = ["XTZ","BTC"]
bought_list = []
asd = 0
i = 0
ticker = []
temp = pyupbit.get_tickers()
for i in range (0,len(temp)):
  time.sleep(0.1)    
  if "KRW" in temp[i]:
      string = temp[i]
      string = string.replace("KRW-","")
      if get_current_price("KRW-"+string) > 2500:
       ticker.append(string)
target_list = [0 for i in range(len(ticker))]
while True:
 try:
  start_time = get_start_time(coin) + datetime.timedelta(minutes=90)
  end_time = start_time + datetime.timedelta(days=1)- datetime.timedelta(minutes=85)
  break
 except Exception as e:
  continue
while True:
    try:
     if i < len(ticker): 
         now = datetime.datetime.now()
         coini = ticker[i]
         coin = "KRW-"+ticker[i]
         if start_time < now < end_time: 
            if buy_list.count("") != 0 and get_balance("KRW") > 5000:
             if coini not in bought_list:
              current_price = get_current_price(coin)
              if target_list[i] == 0:
                target_list[i] = get_target_price(coin,0.5)
              if asd == 0:
               if target_list[i] < current_price <= target_list[i] * 1.05:
                 money = get_balance("KRW")/buy_price.count(0)
                 upbit.buy_market_order(coin, money * 0.9995)
                 for i in range(0,2):
                  if buy_list[i] == "":
                   buy_list[i] = coini
                   buy_price[i] = current_price
                   break
                  else:
                   continue
                 bought_list.append(coini)  
              if asd == 1:
               if target_list[i] < current_price <= target_list[i] * 1.05 and current_price * 1.3 >= get_high(coin):
                 money = get_balance("KRW")/buy_price.count(0)
                 upbit.buy_market_order(coin, money * 0.9995)
                 for i in range(0,2):
                  if buy_list[i] == "":
                   buy_list[i] = coini
                   buy_price[i] = current_price
                   break
                  else:
                   continue
                 bought_list.append(coini)
            for n in range(0,2):
              if buy_list[n] != "" and buy_price[n] != 0: 
               btc = get_balance(buy_list[n])  
               if btc > 0:
                current_price = get_current_price("KRW-"+buy_list[n])
                if buy_price[n] * 1.05  < current_price:              
                 upbit.sell_market_order("KRW-"+buy_list[n], btc)
                 buy_price[n] = 0
                 break
                if buy_price[n] * 0.98 > current_price:
                 upbit.sell_market_order("KRW-"+buy_list[n], btc)
                 buy_price[n] = 0
                 break
            if now.hour == 16:
             if asd == 1: 
              for i in range(0,2):
                 if buy_price[n] == 0:
                   buy_list[n] = ""
              asd = 0  
              bought_list = []
         else:
            i = 0
            if asd == 0:
              ticker = []
              temp = []
              temp = pyupbit.get_tickers()
              for i in range (0,len(temp)):
               time.sleep(0.1)
               if "KRW" in temp[i]:
                 string = temp[i]
                 string = string.replace("KRW-","")
                 if get_current_price("KRW-"+string) > 2500:
                  ticker.append(string)
              for n in range(0,2):
               btc = get_balance(buy_list[n]) 
               if btc != 0:
                upbit.sell_market_order("KRW-"+buy_list[n], btc)
              target_list = [0 for i in range(len(ticker))]
              buy_list = ["",""]
              buy_price = [0,0]
              bought_list = []
              asd = 1
            while True:
              try: 
               start_time = get_start_time(coin) + datetime.timedelta(minutes=90)
               end_time = start_time + datetime.timedelta(days=1)- datetime.timedelta(minutes=85)
               break
              except Exception as e:
               continue
         i = i + 1 
     else:
      i = 0
    except Exception as e:
     print(e)                    
     i = i + 1
