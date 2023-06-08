
def get_ICH(df):
    #Tenkan Sen
    tenkan_max = df['high'].rolling(window = 9, min_periods = 0).max()
    tenkan_min = df['low'].rolling(window = 9, min_periods = 0).min()
    df['tenkan_avg'] = (tenkan_max + tenkan_min) / 2

    #Kijun Sen
    kijun_max = df['high'].rolling(window = 26, min_periods = 0).max()
    kijun_min = df['low'].rolling(window = 26, min_periods = 0).min()
    df['kijun_avg'] = (kijun_max + kijun_min) / 2

    #Senkou Span A
    #(Kijun + Tenkan) / 2 Shifted ahead by 26 periods
    df['senkou_a'] = ((df['kijun_avg'] + df['tenkan_avg']) / 2).shift(26)

    #Senkou Span B
    #52 period High + Low / 2
    senkou_b_max = df['high'].rolling(window = 52, min_periods = 0).max()
    senkou_b_min = df['low'].rolling(window = 52, min_periods = 0).min()
    df['senkou_b'] = ((senkou_b_max + senkou_b_min) / 2).shift(52)

    #Chikou Span
    #Current close shifted -26
    df['chikou'] = (df['close']).shift(-26)


    #Plotting Ichimoku

    #m_plots = ['kijun_avg', 'tenkan_avg',df[df.columns[5:]] ]

    return df



def get_RSI(df, periods=14, ema=True):

    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    df['RSI'] = rsi
    return df
