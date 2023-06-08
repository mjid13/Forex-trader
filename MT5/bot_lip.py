import numpy as np
import talib as tb
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mp



tickers =["BTCUSDT"]

for ticker in tickers:
    df = pd.read_csv("5m.csv")
    print(df)
    df["Date"] = pd.to_datetime(df["Date"], unit="ns")
    df = df.set_index("Date")
    sma_15 = tb.SMA(df["Close"], timeperiod = 15)
    pos =0
    sell_mark = []
    buy_mark = []
    for i in range(len(df)):
        if sma_15[i] < df["Close"][i] and pos ==0 :
            print(i)
            sell_mark.append(i)
            pos =1
        if sma_15[i] > df["Close"][i] and pos ==1 :
            buy_mark.append(i)
            pos =0
    #print(sell_mark)
    for i in sell_mark:
        plt.plot(i,df["Close"][i], marker= "^")
    for i in buy_mark:
        plt.plot(i,df["Close"][i], marker= "v")

    mp.plot(df, type="candle", style="yahoo", volume=False, title="hi", ylabel="Price (USDT)")

    '''
    #************************************
    df["Close"].plot()
    sma_15.plot()
    plt.legend()
    plt.show()
'''
    df["Close"].plot(label = "hi" , color = "red")
    df["Open"].plot()
    plt.plot([0,len(df)],[1.30 ,1.34]) # ______________________ خط أفقي _____________
    plt.plot([0,1.34]) # _______________ خط عمودي ___________
    plt.plot(10,1.3 , marker="0") # _________علامات ( ^,v,o) _____________
    plt.legend()

    plt.show()

    #*****************************************************
