import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

print(mt5.BOOK_TYPE_BUY_MARKET)