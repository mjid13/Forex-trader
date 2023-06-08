import sys
import datetime
import threading
import tickers as tkr , EMA_strg as strgy , filter_data as dataFl
import time

min15_lis = [0, 15, 30, 45]
min30_lis = [0, 30]
min5_lis = []
for i in range(0, 60, 5):
    min5_lis.append(i)

def server_tm():

    while True:
        rel_time = datetime.datetime.now()
        min_ = rel_time.strftime("%M")
        min_ = int(min_)
        sec_ = rel_time.strftime("%S")
        sec_ = int(sec_)
        if min_ in min30_lis and sec_ == 5:
            print("\nis going will for", min_, "min")
            print("Searching for opportunities ..30M..")
            # run strategy
            strgy.Xichmo_stg(tkr.list_1, str(1), '30M')
            strgy.Xichmo_stg(tkr.list_2, str(2), '30M')
            #time.sleep(20)
            #dataFl.filter_order()
        if min_ in min15_lis and sec_ == 5:
            print("\nis going will for", min_, "min")
            print("Searching for opportunities ..15M..")
            # run strategy
            strgy.Xichmo_stg(tkr.list_1, str(1), '15M')
            strgy.Xichmo_stg(tkr.list_2, str(2), '15M')
            #time.sleep(20)
            #dataFl.filter_order()

        else:
            r = "." * sec_
            sys.stdout.flush()
            print("\rwhiting",min_,r, end="" )


''' 
       if min_ in min5_lis and sec_ == 5:
            print("\nis going will for", min_, "min")
            print("Searching for opportunities ..5M..")
            # run strategy
            strgy.Xichmo_stg(tkr.list_1, str(1), '5M')
            strgy.Xichmo_stg(tkr.list_2, str(2), '5M')
            #time.sleep(20)
            #dataFl.filter_order()

            '''


