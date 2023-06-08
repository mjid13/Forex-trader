from database import Signals
import place_orders as pl_or
siganls = Signals()


def filter_order():
    prev_data = []
    all_lists = ["End_1", "End_2"]
    x = 0
    all_tickers = {}
    while x < 2 :
        x = 0
        data = siganls.find_all(collection="Signals")  #find all the signals in the database
        tickers = list(data.keys())    # a new list with all signals keys in the find_all->"data" variables
        if tickers != prev_data:
            for ticker in tickers:
                if ticker not in prev_data:
                    all_tickers[ticker] = data[ticker]
                if ticker in all_lists:
                    x = x + 1
        prev_data = tickers

    sorted_tickers = sorted(all_tickers.items(), key=lambda x: x[1], reverse=True)
    if sorted_tickers in all_lists:
        selected_ticker = sorted_tickers[0][0]
        if None != selected_ticker:
            print("your ticker is ", selected_ticker)
            balsnce = pl_or.get_balance()
            print(f"Entry amount : {balsnce} USDT ")
            if balsnce >= 20 :
                #pl_or.open_buy(selected_ticker, 0.01)
                en_price = pl_or.entry_price(selected_ticker, "buy")
                print(f"Place order for: {selected_ticker}, Entry price : {en_price}")

    
    
    else:
        print(f"Sorry no order placed in {sorted_tickers} !!")
    print("__________________________")



    siganls.clear_all_signals(collection="Signals")


#filter_order()

