from database import Orders
import MetaTrader5 as mt5
from datetime import datetime
orders = Orders()




if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()
#class Pla
def get_positions():
    positions = mt5.positions_get()
    symbols= []
    for position in positions:
        symbols.append(position.symbol)

    return symbols

# calculate the stop loss price
def stop_loss(symbol,dell):
    if dell == "sell":
        price = mt5.symbol_info_tick(symbol).ask
        point = price * 0.002
        stop_loss = round(price + point,5)
        return stop_loss
    elif dell == "buy":
        price = mt5.symbol_info_tick(symbol).ask
        point = price * 0.002
        stop_loss = round(price - point,5)
        return stop_loss


# calculate the take profit price
def take_profit(symbol,dell):
    if dell == "sell":
        price = mt5.symbol_info_tick(symbol).ask
        point = price * 0.006
        tp_price = round(price - point,5)
        return tp_price
    elif dell == "buy":
        price = mt5.symbol_info_tick(symbol).ask
        point = price * 0.006
        tp_price = round(price + point,5)
        return tp_price


# get the entry price
def entry_price(sympol, type):
    sympol_info = mt5.symbol_info(sympol)

    if type == "sell":
        return sympol_info.bid
    elif type == "buy":
        return sympol_info.ask

# it use to open an buy order with all details
def open_buy(symbol, lot):
    # get the information about the symbol
    symbol_info = mt5.symbol_info(symbol)

    # check if can find the symbol information
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        quit()

    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print(f"symbol_select({symbol}) failed, exit")
            quit()


    deviation = 20
    price = mt5.symbol_info_tick(symbol).ask
    request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": stop_loss(symbol,"buy"),
            "tp": take_profit(symbol,"buy"),
            "deviation": deviation ,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
    }



    # send a trading request
    buy_result = mt5.order_send(request)

    if buy_result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(buy_result.retcode))


    #save the order details in the database
    orders.save_order(collection="Buy_orders",
                                 symbol=symbol,
                                 orderid=buy_result.order,
                                 price=buy_result.ask,
                                 take_profit=take_profit(symbol,"buy"),
                                 stop_limit=stop_loss(symbol,"buy"),
                                 Comment=buy_result.comment,
                                 DateTime = datetime.now())
    return buy_result



def close_buy(symbol):
    position_id = 0
    lot = 0
    # create a close request
    Xorders = mt5.positions_get(symbol=symbol)
    if Xorders is None:
        print("No orders on GBPUSD, error code={}".format(mt5.last_error()))
    for order in Xorders:
        position_id = order.identifier
        lot = order.volume



    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send failed, retcode={}".format(result.retcode))
    else:
        print("position #{} closed, {}".format(position_id, result))



def open_sell(symbol, lot):
    # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")

        quit()

    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print(f"symbol_select({symbol}) failed, exit")

            quit()

    account_info_dict = mt5.account_info()._asdict()
    margin = account_info_dict["margin_free"]

    request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "sl": stop_loss(symbol,"sell"),
            "tp": take_profit(symbol,"sell"),
            "deviation": 20,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # send a trading request
    global sell_result
    sell_result = mt5.order_send(request)


    if sell_result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(sell_result.retcode))


    data = orders.save_order(collection="Sell_orders",
                                 symbol=symbol,
                                 orderid=sell_result.order,
                                 price=sell_result.ask,
                                 take_profit=take_profit(symbol,"sell"),
                                 stop_limit=stop_loss(symbol,"sell"),
                                 Comment=sell_result.comment,
                                 DateTime = datetime.now())
    return data

def close_sell(symbol):
    position_id = 0
    lot = 0
    # create a close request
    Xorders = mt5.positions_get(symbol=symbol)
    print(Xorders)
    if Xorders is None:
        print("No orders on GBPUSD, error code={}1133602573".format(mt5.last_error()))
    for order in Xorders:
        position_id = order.identifier
        lot = order.volume

    deviation = 20
    price = mt5.symbol_info_tick(symbol).ask
    request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "position": position_id,
            "price": price,
            "deviation": deviation ,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
    else:
        print("4. position #{} closed, {}".format(position_id, result))



def get_balance():
    authorized = mt5.login(50514149, password="gqmil5tn")
    if authorized != None:
        account_info_dict = mt5.account_info()._asdict()
        return int(account_info_dict['balance'])

    else:
        print("failed to connect to trade account 25115284 with password=gqz0343lbdm, error code =", mt5.last_error())


def risk_mang(balance):
    if balance in range(0,100):
        lot = 0
        deals = 0
        return lot , deals
    elif balance in range(100,300):
        lot = 0.01
        deals = 1
        return lot , deals
    elif balance in range(300,500):
        lot = 0.01
        deals = 2
        return lot , deals

    elif balance in range(500,700):
        lot = 0.01
        deals = 3
        return lot , deals

    elif balance in range(700, 900):
        lot = 0.01
        deals = 4
        return lot , deals

    elif balance in range(900, 3000):
        lot = 0.01
        deals = 5
        return lot , deals

    elif balance in range(3000, 6000):
        lot = 0.03
        deals = 4
        return lot , deals

    else:
        lot = 0.05
        deals = 4
        return lot , deals




x= get_balance()
print(x)

z = open_buy('EURGBP',0.01)
x= entry_price('EURGBP','sell')
print(z.order)

x = get_positions()
print(x)
'''
x =stop_loss('USDCHF','buy')
print(x)
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
print()
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

x =0
Xorders=mt5.positions_get(symbol='EURJPY')
if Xorders is None:
    print("No orders on GBPUSD, error code={}".format(mt5.last_error()))
else:
    print("Total orders on GBPUSD:",len(Xorders))
    # display all active orders
    for order in Xorders:
        print(order)
print(x)


'''
