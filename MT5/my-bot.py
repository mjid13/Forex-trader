from MT5.get_data import *
from MT5.ichimoku import *
import MT5.place_orders as pl_or
from datetime import datetime
from MT5.database import Signals
import threading
from MT5 import tickers as tkr

depth = 200
ema_used = [50, 100]
signals = Signals()
tenkan1 = 0
kijan1 = 0

def find_engulfing(series):
    for i in series.index:
        if series[i] == 100:
            return i

#signals.clear_all(collection="Signals")

def ema_strgy(symbols , num):
    for symbol in symbols:
        try:
            df = get_klines_M15(symbol, utc= datetime.now(), depth=depth)
            df = get_ICH(df)
            df = get_RSI(df)

            rsi = df['RSI'][-1]
            chikou = df['chikou'][-1]
            tenkan = df['tenkan_avg'][-1]
            kijan = df['kijun_avg'][-1]
            b_sen = df['senkou_b'][-1]
            a_sen = df['senkou_a'][-1]

            df.to_csv(f"{symbol}.csv")
            df = pd.read_csv(f"{symbol}.csv")

            if int(rsi) < 50:
                print("hi 1 ")

                if (tenkan == kijan)  and tenkan > (b_sen and a_sen) :
                    print("hi if 1 ")
                    #print(symbol, last_index, close_price)
                    signals.add(collection="Signals" , ticker=symbol, volume=pl_or.entry_price(symbol,'buy'), pct_sl=pl_or.stop_loss(symbol))
                else:
                    tenkan1 = tenkan
                    kijan1 = kijan
                    print("hi else 1")
                    signals.add(collection="Signals", ticker=symbol, volume=None, pct_sl=None)
            elif int(rsi) >= 50:

                if (tenkan == kijan) and tenkan > (b_sen and a_sen) :
                    #print(symbol, last_index, close_price)
                    signals.add(collection="Signals" , ticker=symbol, volume=pl_or.entry_price(symbol,'buy'), pct_sl=pl_or.stop_loss(symbol))
                else:
                    signals.add(collection="Signals", ticker=symbol, volume=None, pct_sl=None)

        except Exception as a:
            pass

    signals.add(collection="Signals", ticker="End_" + num, volume=None, pct_sl=None)


def Xichmo_stg(symbols, num):
    for symbol in symbols:
        try:
            df = get_klines_M15(symbol, utc= datetime.now(), depth=depth)
            get_ICH(df)
            get_RSI(df)
            sell_mark = []
            buy_mark = []
            rsi    = df['RSI'][-1]
            chikou = df['chikou'][-27]
            tenkan = df['tenkan_avg'][-1]
            kijan  = df['kijun_avg'][-1]
            b_sen  = df['senkou_b'][-1]
            a_sen  = df['senkou_a'][-1]
            close_pr = df['close'][-1]
            df.to_csv(f"{symbol}.csv")
            df = pd.read_csv(f"{symbol}.csv")
            ngv = a_sen < b_sen
            pst = a_sen > b_sen


            if rsi >50 :
                if ngv:

                    t1 = (chikou and close_pr and tenkan) < (a_sen and b_sen)
                    t2 = (tenkan < kijan) and (close_pr > tenkan)
                    t3 = chikou > close_pr
                    if t1 and t2 and t3:
                        signals.add(collection="Signals", ticker=symbol, deal_type="buy", volume=pl_or.entry_price(symbol, 'buy'),pct_sl=pl_or.stop_loss(symbol,"buy"))
                        print("your ticker is ", symbol)
                        balsnce = pl_or.get_balance()
                        print(f"Entry amount : {balsnce} USDT ")
                        if balsnce >= 20:
                            pl_or.open_buy(symbol, 0.01)
                            en_price = pl_or.entry_price(symbol, "buy")
                            print(f"Place order for: {symbol}, Entry price : {en_price}")
                    else:
                        signals.add(collection="Signals", ticker=symbol, volume=None, pct_sl=None, deal_type="buy")





            else:
                print('test')
                if pst:

                    t1 = (chikou and close_pr and tenkan) > (a_sen and b_sen)
                    t2 = (tenkan > kijan) and (close_pr < tenkan)
                    t3 = chikou < close_pr

                    if t1 and t2 and t3:
                        #sell_mark.append(i)
                        signals.add(collection="Signals", ticker=symbol, deal_type="sell", volume=pl_or.entry_price(symbol, 'sell'),pct_sl=pl_or.stop_loss(symbol,"sell"))
                        print("your ticker is ", symbol)
                        balsnce = pl_or.get_balance()
                        print(f"Entry amount : {balsnce} USD ")
                        if balsnce >= 20:
                            pl_or.open_sell(symbol, 0.01)
                            en_price = pl_or.entry_price(symbol, "sell")
                            print(f"Place order for: {symbol}, Entry price : {en_price}")
                    else:
                        signals.add(collection="Signals", ticker=symbol, volume=None, pct_sl=None, deal_type="sell")




                #print("sell deals : ", len(sell_mark))
                #print("buy deals : ", len(buy_mark))

        except Exception as e :
            print(e)
    signals.add(collection="Signals", ticker="End_" + num, volume=None, pct_sl=None, deal_type=None)
    print(f"End_{num}")


#Xichmo_stg(tkr.list_1, f"{1}")
#Xichmo_stg(tkr.list_2, f"{2}")
'''
threading.Thread(target= Xichmo_stg , args= (tkr.list_1, f"list_{1}")).start()
threading.Thread(target= Xichmo_stg , args= (tkr.list_2, f"list_{2}")).start()

li = ['USDCHF']
ema_strgy(li,"1")'''

