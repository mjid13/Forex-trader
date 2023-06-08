
import MetaTrader5 as mt5
import pandas as pd
from pytz import timezone


pd.options.mode.chained_assignment = None

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def get_klines_M5(pair, utc, depth):
    eastern = timezone('US/Eastern')
    utc_from = eastern.localize(utc)
    klines = mt5.copy_rates_from(pair, mt5.TIMEFRAME_M5, utc_from, depth)
    df = pd.DataFrame(klines)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index("time")
    return df



def get_klines_M15(pair, utc, depth):
    eastern = timezone('US/Eastern')
    utc_from = eastern.localize(utc)
    klines = mt5.copy_rates_from(pair, mt5.TIMEFRAME_M15, utc_from, depth)
    df = pd.DataFrame(klines)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index("time")

    return df

def get_klines_M30(pair, utc, depth):
    eastern = timezone('US/Eastern')
    utc_from = eastern.localize(utc)
    klines = mt5.copy_rates_from(pair, mt5.TIMEFRAME_M30, utc_from, depth)
    df = pd.DataFrame(klines)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index("time")
    return df

def get_klines_H1(pair, utc, depth):
    eastern = timezone('US/Eastern')
    utc_from = eastern.localize(utc)
    klines = mt5.copy_rates_from(pair, mt5.TIMEFRAME_H1, utc_from, depth)
    df = pd.DataFrame(klines)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index("time")
    return df

def get_klines_H4(pair, utc, depth):
    eastern = timezone('US/Eastern')
    utc_from = eastern.localize(utc)
    klines = mt5.copy_rates_from(pair, mt5.TIMEFRAME_H4, utc_from, depth)
    df = pd.DataFrame(klines)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.set_index("time")
    return df

