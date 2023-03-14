import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np
import os
from datetime import date, datetime, timezone, tzinfo
import time, schedule
import numpy as np
import requests
from math import floor
import matplotlib.pyplot as plt
import ta as tl
import math
import functools
from pandas import DataFrame
import warnings
from io import StringIO
from pathlib import Path
from scipy.signal import argrelextrema
from collections import deque
import itertools
import talib.abstract as tt
import talib
warnings.filterwarnings("ignore")
symbol = "ETH/BUSD"  # Binance 
pos_size =1
timeframe = "15m"
 


# API TANIMLAMALARI
account_binance = ccxt.binance({
    "apiKey": '',
    "secret": '',
    "enableRateLimit": True,
    'options': {
        'defaultType': 'future'
    }
})


# fibo_ratios = []
# prd = 15
# dir = 0
# max_array_size = 10
# OldPh = 0
# oldPl = 0
# zigzag = []
# enable236 = True
# enable382 = True
# enable500 = True
# enable618 = True
# enable786 = True
# fibo_ratios.append(0.000)
# if enable236:
#         fibo_ratios.append(0.236)
# if enable382:
#         fibo_ratios.append(0.382)
# if enable500:
#         fibo_ratios.append(0.500)
# if enable618:
#         fibo_ratios.append(0.618)
# if enable786:
#         fibo_ratios.append(0.786)
# for x in range(1, 6):
#     fibo_ratios.append(x)
#     fibo_ratios.append(x + 0.272)
#     fibo_ratios.append(x + 0.414)
#     fibo_ratios.append(x + 0.618)
while True: 

    try:
        
        orderTime = datetime.utcnow()
        ohlcvLB = account_binance.fetch_ohlcv(symbol, timeframe)
        dfLB = pd.DataFrame(ohlcvLB, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        indiPoint = pd.DataFrame(columns=['time'])
        if len(ohlcvLB):
            dfLB['time'] = pd.to_datetime(dfLB['time'], unit='ms')

            def get_zigzag(df: pd.DataFrame, period: int):
                zigzag_pattern = []
                direction = 0
                changed = False
                for idx in range(1, len(df)):
                    highest_high = df['high'][:idx].rolling(period).max().iloc[-1]
                    lowest_low = df['low'][:idx].rolling(period).min().iloc[-1]


                    new_high = df.high[idx] >= highest_high
                    new_low = df.low[idx] <= lowest_low

                    if new_high and not new_low:
                        if direction != 1:
                            direction = 1
                            changed = True
                        elif direction == 1:
                            changed = False
                    elif not new_high and new_low:
                        if direction != -1:
                            direction = -1
                            changed = True
                        elif direction == -1:
                            changed = False

                    if new_high or new_low:
                        if changed or len(zigzag_pattern)==0:
                            if direction == 1:
                                pat = ['H', df.high[idx], idx]
                                zigzag_pattern.append(pat)
                            elif direction == -1:
                                pat = ['L', df.low[idx], idx]
                                zigzag_pattern.append(pat)
                        else:
                            if direction == 1 and df.high[idx] > zigzag_pattern[-1][1]:
                                pat = ['H', df.high[idx], idx]
                                zigzag_pattern[-1] = pat
                            elif direction == -1 and df.low[idx] < zigzag_pattern[-1][1]:
                                pat = ['L', df.low[idx], idx]
                                zigzag_pattern[-1] = pat
                            else:
                                pass
                return zigzag_pattern
            
            zigzag = get_zigzag(dfLB,15)
            # def controlZigzag():
            #     if len(zigzag) > 10:
            #         zigzag.pop(0)
            #         controlZigzag()
            #     else:
            #         return zigzag
            # controlZigzag()









                





                
                        

        
    except Exception as e:
        print(e)
        continue


