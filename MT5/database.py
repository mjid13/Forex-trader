import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["Collection"]
tb = db["Status"]

'''
STATUS collection is for bot.py to save the bot state ( save and find the state) 
'''
class Status():
    def save_status(self, collection, status, time):
        collection = db[collection]
        collection.delete_many({})
        new_stat = {"Status":status, "Time":time}
        data = collection.insert_one(new_stat)
        return data

    def find_status(self, collection):
        collection = db[collection]
        data = collection.find({})
        stat = ""
        for dt in data:
            stat = dt["Status"]
        return stat

'''
SIGNALS collection is for the stragrty signals ( add, find and clear the signals )
'''
class Signals():

    def add(self, collection, ticker, volume, pct_sl, deal_type,rsi,chikou,tenkan, kijan,b_sen,a_sen):
        collection = db[collection]
        new_signal={"Ticker": ticker, "Volume": volume, "StopLoss": pct_sl, "Deal Type":deal_type,'rsi':rsi,'chikou':chikou,'tenkan':tenkan,
            "kijan":kijan,
            "b_sen":b_sen,
            'a_sen':a_sen}
        data = collection.insert(new_signal)
        return data

    def find_all(self, collection):
        tickers = {}
        collection = db[collection]
        data = collection.find()
        for dt in data:
            tickers[dt["Ticker"]] = [dt["Volume"], dt["StopLoss"]]
        return tickers

    def clear_all_signals(self, collection):
        collection = db[collection]


        return collection.delete_many({})

'''
ORDERS 
'''
class Orders():
    def save_order(self, collection, symbol, orderid, price, take_profit, stop_limit, Comment, DateTime):
        collection = db[collection]
        new_order = {"symbol": symbol, "OrderID": orderid, "price": price, "TP": take_profit, "SL": stop_limit, "Comment": Comment, "DateTime": DateTime}
        data = collection.insert(new_order)
        return data

    def clear_orders(self, collection , symbol):
        collection = db[collection]



        return collection.delete_one({'symbol':symbol})


    def find_orders(self, collection):
        tickers = []
        collection = db[collection]
        data = collection.find()
        for dt in data:
            tickers.append(dt["symbol"])
        return tickers

