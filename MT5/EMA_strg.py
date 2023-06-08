from get_data import *
from ichimoku import *
import place_orders as pl_or
from datetime import datetime
from database import Signals
import threading
import tickers as tkr

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


def Xichmo_stg(symbols, num, fream):
    deals = pl_or.get_positions()

    for symbol in symbols:
        try:

            #if fream == '5M':
            #    df = get_klines_M5(symbol, utc=datetime.now(), depth=depth)
            if fream == '15M':
                df = get_klines_M15(symbol, utc=datetime.now(), depth=depth)
            elif fream == '1H':
                df = get_klines_H1(symbol, utc=datetime.now(), depth=depth)
            elif fream == '4H':
                df = get_klines_H4(symbol, utc=datetime.now(), depth=depth)
            else:
                df = get_klines_M30(symbol, utc=datetime.now(), depth=depth)

            get_ICH(df)
            get_RSI(df)
            rsi    = df['RSI'][-1]
            chikou = df['chikou'][-27]
            tenkan = df['tenkan_avg'][-1]
            kijan  = df['kijun_avg'][-1]
            b_sen  = df['senkou_b'][-1]
            a_sen  = df['senkou_a'][-1]
            _b_sen  = df['senkou_b'][-27]
            _a_sen  = df['senkou_a'][-27]
            close_pr = df['close'][-1]
            #df.to_csv(f"{symbol}.csv")
            ngv = a_sen < b_sen
            pst = a_sen > b_sen

            buy_lis = pl_or.orders.find_orders('Buy_orders')
            sell_lis = pl_or.orders.find_orders('Sell_orders')

            if rsi >50 :
                if ngv:
                    t1 = (close_pr and tenkan) > (a_sen and b_sen)
                    t2 = (close_pr > tenkan > kijan)
                    t3 = chikou > (_a_sen and _b_sen)
                    if t1 and t2 and t3:
                        if symbol in deals:
                                print(f'------------------------------ Buy Deal already Done! {symbol}--------------------------')
                        else:
                            buy_lis.append(symbol)
                            print(f'------------------------------ Buy Deal Done! {symbol}--------------------------')
                            print("your ticker is ", symbol)
                            balsnce = pl_or.get_balance()
                            print(f"Entry amount : {balsnce} USDT ")
                            if balsnce >= 20:
                                pl_or.open_buy(symbol, 0.01)
                                en_price = pl_or.entry_price(symbol, "buy")
                                print(f"Place order for: {symbol}, Entry price : {en_price}")
                                print('======================================================================================')
                    else:
                        print("----------> ",symbol,">buy deal not done !! <----------")
            else:

                if pst:
                    t1 = (close_pr and tenkan) < (a_sen and b_sen)
                    t2 = (close_pr < tenkan < kijan)
                    t3 = chikou < (_a_sen and _b_sen)
                    if t1 and t2 and t3:
                        if symbol in deals:
                            print(f'------------------------------ sell Deal already Done! {symbol}--------------------------')
                        else:
                            print(f'------------------------------ sell Deal Done! {symbol}--------------------------')
                            print("your ticker is ", symbol)
                            balsnce = pl_or.get_balance()
                            print(f"Entry amount : {balsnce} USDT ")
                            if balsnce >= 20:
                                pl_or.open_sell(symbol, 0.01)
                                en_price = pl_or.entry_price(symbol, "sell")
                                print(f"Place order for: {symbol}, Entry price : {en_price}")
                                print('======================================================================================')
                    else:
                        print("----------> ",symbol,">sell deal not done !! <----------")

            if symbol in deals:
                if symbol in sell_lis:
                    if close_pr > kijan:
                        try:
                            print(f'------------------------------ Sell Deal Close! {symbol}--------------------------')
                            pl_or.close_sell(symbol)
                            pl_or.orders.clear_orders('Sell_orders', symbol)

                        except:
                            print(f"-------------------- Can't Close Sell Desl {symbol} ------------------")
                            print(f'{symbol} sell deal may closed before')
                            pl_or.orders.clear_orders('Sell_orders', symbol)
                elif symbol in buy_lis:
                    if close_pr < kijan:
                        try:
                            print(f'------------------------------ Buy Deal Close! {symbol}--------------------------')
                            pl_or.close_buy(symbol)
                            pl_or.orders.clear_orders('Buy_orders', symbol)
                        except:
                            print(f"-------------------- Can't Close Sell Desl {symbol} ------------------")
                            print(f'{symbol} buy deal may closed before')
                            pl_or.orders.clear_orders('Buy_orders', symbol)
                else:
                    print("--------------------- Can't find the order ----------------------")

        except Exception as e :
            print(e)

    print(f"End_{num}")


#Xichmo_stg(tkr.list_1, f"{1}",'4H')
#Xichmo_stg(tkr.list_2, f"{2}",'4H')
'''
threading.Thread(target= Xichmo_stg , args= (tkr.list_1, f"list_{1}")).start()
threading.Thread(target= Xichmo_stg , args= (tkr.list_2, f"list_{2}")).start()

li = ['USDCHF']
ema_strgy(li,"1")'''
