#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:11:00 2020

@author: justin
"""

import pandas as pd
import numpy as np
import calendar
from datetime import date,timedelta,datetime
import time
import mplfinance as mpf

df=pd.read_csv(r'/home/justin/Documents/Futures/data/rawdata/DATA(1MI_TXFG0)_2020_final.csv')
df['month'] = pd.DatetimeIndex(df['Time']).month
df['Time'] = pd.to_datetime(df['Time'])
datelist = list(dict.fromkeys(df['Time'].apply(lambda x: x.strftime('%Y-%m-%d'))))
timelist = list(dict.fromkeys(df['Time'].apply(lambda y: y.strftime('%H:%M:%S'))))
timelistmonthend = timelist.copy()
del timelistmonthend[-15:]
row_list = []

def third_wed(d):
    s = date(d.year, d.month, 15)
    return s + timedelta(days=(calendar.WEDNESDAY - s.weekday()) % 7)

def volume_avg(df,vol_length):
    df['Vol_avg'] = round(df['Volume'].ewm(span=vol_length,adjust=False),2)

def one_min_enter(df,deferred_ticks,consec_ticks,nearest_kbar,nearest_kbar_brace,current_kbar_brace):
    global BuySellTimes
    BuySellTimes = 0
    global MarketPosition
    MarketPosition = 0
    global StopGainTimes
    StopGainTimes = 0
    global StopLossTimes
    StopLossTimes = 0
    global BuyPrice
    BuyPrice = 0
    global SellPrice
    SellPrice = 0
    global NetPrice
    NetPrice = 0
    global GainLossPoints
    GainLossPoints = 0
    global TotalGain
    TotalGain = 0
    global TotalWins
    TotalWins = 0
    global TotalLoss
    TotalLoss = 0
    global TotalLose
    TotalLose = 0
    KbarBuy = 0
    KbarSell = 0
    global max_consecutive_gain
    max_consecutive_gain = 0
    global max_consecutive_loss
    max_consecutive_loss = 0
    global consecutivegain
    consecutivegain = 0
    global consecutiveloss
    consecutiveloss = 0
    global max_consecutive_win
    max_consecutive_win = 0
    global max_consecutive_lose
    max_consecutive_lose = 0
    global consecutivewin
    consecutivewin = 0
    global consecutivelose
    consecutivelose = 0
    global Winrate
    global jan_gainloss
    global feb_gainloss
    global mar_gainloss
    global apr_gainloss
    global may_gainloss
    global jun_gainloss
    global jul_gainloss
    global aug_gainloss
    global sep_gainloss
    global oct_gainloss
    global nov_gainloss
    global dec_gainloss
    global lastwin
    lastwin = True
    global lastloss
    lastloss = True
    time_ec=0
    time_c=0
    for dates in datelist:
        if third_wed(datetime.strptime(dates, '%Y-%m-%d')).day == datetime.strptime(dates, '%Y-%m-%d').day:
            for time_me in timelistmonthend:
                loc_val_1m = (time_ec*285+time_c*300)+timelistmonthend.index(time_me)
                if timelistmonthend.index(time_me) < deferred_ticks:
                    KbarBuy = 0
                    KbarSell = 0
                    continue
                elif timelistmonthend.index(time_me) == 283:
                    if MarketPosition == 1:
                        MarketPosition = 0
                        SellPrice = df.loc[loc_val_1m+1,'Open']
                        GainLossPoints = SellPrice - BuyPrice
                        if GainLossPoints > 0:
                            TotalGain += GainLossPoints
                            TotalWins +=1
                            if lastwin:
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastloss = False
                                pass
                            else:
                                consecutiveloss = 0
                                consecutivelose = 0
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastwin = True
                                lastloss = False
                                pass
                        else:
                            TotalLoss += GainLossPoints
                            TotalLose +=1
                            if lastloss:
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastwin = False
                                pass
                            else:
                                consecutivegain = 0
                                consecutivewin = 0
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastloss = True
                                lastwin = False
                                pass
                        NetPrice += GainLossPoints
                        df.loc[loc_val_1m+1, 'Position'] = 'endclose'
                        df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = SellPrice
                        df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                        df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                    elif MarketPosition == -1:
                        MarketPosition = 0
                        BuyPrice = df.loc[loc_val_1m+1,'Open']
                        GainLossPoints = SellPrice - BuyPrice
                        if GainLossPoints > 0:
                            TotalGain += GainLossPoints
                            TotalWins +=1
                            if lastwin:
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastloss = False
                                pass
                            else:
                                consecutiveloss = 0
                                consecutivelose = 0
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastwin = True
                                lastloss = False
                                pass
                        else:
                            TotalLoss += GainLossPoints
                            TotalLose +=1
                            if lastloss:
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastwin = False
                                pass
                            else:
                                consecutivegain = 0
                                consecutivewin = 0
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastloss = True
                                lastwin = False
                                pass
                        NetPrice += GainLossPoints
                        df.loc[loc_val_1m+1, 'Position'] = 'endclose'
                        df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = BuyPrice
                        df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                        df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                    else:
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                else:
                    if MarketPosition == 0 and timelistmonthend.index(time_me) > deferred_ticks and timelistmonthend.index(time_me) < 254:
                        for c in range(0,consec_ticks-1):
                            if df.loc[loc_val_1m-c,'Close'] > df.loc[loc_val_1m-c,'Open'] and df.loc[loc_val_1m-c,'Close'] > df.loc[loc_val_1m-c-1,'Close'] and df.loc[loc_val_1m-c,'Open'] > df.loc[loc_val_1m-c-1,'Open']:
                                KbarBuy +=1
                                pass
                        for d in range(0,consec_ticks-1):
                            if df.loc[loc_val_1m-d,'Close'] < df.loc[loc_val_1m-d,'Open'] and df.loc[loc_val_1m-d,'Close'] < df.loc[loc_val_1m-d-1,'Close'] and df.loc[loc_val_1m-d,'Open'] < df.loc[loc_val_1m-d-1,'Open']:
                                KbarSell +=1
                                pass
                        if KbarBuy == (consec_ticks-1):
                            BuySellTimes +=1
                            MarketPosition = 1
                            BuyPrice = df.loc[loc_val_1m+1,'Open']
                            df.loc[loc_val_1m+1, 'Position'] = 1
                            df.loc[loc_val_1m+1, 'BuyPurchasePrice'] = BuyPrice
                            KbarBuy = 0
                            KbarSell = 0
                            previous_stop_point = current_stop_point = df.loc[loc_val_1m,'Close'] - current_kbar_brace
                            continue
                        elif KbarSell == (consec_ticks-1):
                            BuySellTimes +=1
                            MarketPosition = -1
                            SellPrice = df.loc[loc_val_1m+1,'Open']
                            df.loc[loc_val_1m+1, 'Position'] = -1
                            df.loc[loc_val_1m+1, 'SellPurchasePrice'] = SellPrice
                            previous_stop_point = current_stop_point = df.loc[loc_val_1m,'Close'] + current_kbar_brace
                            KbarBuy = 0
                            KbarSell = 0
                            continue
                        else:
                            KbarBuy = 0
                            KbarSell = 0
                            continue
                    elif MarketPosition == 1:
                        recent_low = df.loc[loc_val_1m-nearest_kbar:loc_val_1m,'Low'].values.min() - nearest_kbar_brace
                        current_stop_point = df.loc[loc_val_1m,'Close'] - current_kbar_brace
                        if df.loc[loc_val_1m,'Close'] < max(recent_low,current_stop_point,previous_stop_point):
                            MarketPosition = 0
                            SellPrice = df.loc[loc_val_1m+1,'Open']
                            GainLossPoints = SellPrice - BuyPrice
                            if GainLossPoints > 0:
                                TotalGain += GainLossPoints
                                TotalWins +=1
                                if lastwin:
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastloss = False
                                    pass
                                else:
                                    consecutiveloss = 0
                                    consecutivelose = 0
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastwin = True
                                    lastloss = False
                                    pass
                            else:
                                TotalLoss += GainLossPoints
                                TotalLose +=1
                                if lastloss:
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastwin = False
                                    pass
                                else:
                                    consecutivegain = 0
                                    consecutivewin = 0
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastloss = True
                                    lastwin = False
                                    pass
                            NetPrice += GainLossPoints
                            df.loc[loc_val_1m+1, 'Position'] = 0
                            df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = SellPrice
                            df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                            df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                            continue
                        else:
                            df.loc[loc_val_1m, 'Exit Point'] = max(recent_low,current_stop_point,previous_stop_point)
                            previous_stop_point = max(recent_low,current_stop_point,previous_stop_point)
                            continue
                    elif MarketPosition == -1:
                        recent_high = df.loc[loc_val_1m-nearest_kbar:loc_val_1m,'High'].values.max() + nearest_kbar_brace
                        current_stop_point = df.loc[loc_val_1m,'Close'] + current_kbar_brace
                        if df.loc[loc_val_1m,'Close'] > min(recent_high,current_stop_point,previous_stop_point):
                            MarketPosition = 0
                            BuyPrice = df.loc[loc_val_1m+1,'Open']
                            GainLossPoints = SellPrice - BuyPrice
                            if GainLossPoints > 0:
                                TotalGain += GainLossPoints
                                TotalWins +=1
                                if lastwin:
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastloss = False
                                    pass
                                else:
                                    consecutiveloss = 0
                                    consecutivelose = 0
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastwin = True
                                    lastloss = False
                                    pass
                            else:
                                TotalLoss += GainLossPoints
                                TotalLose +=1
                                if lastloss:
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastwin = False
                                    pass
                                else:
                                    consecutivegain = 0
                                    consecutivewin = 0
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastloss = True
                                    lastwin = False
                                    pass
                            NetPrice += GainLossPoints
                            df.loc[loc_val_1m+1, 'Position'] = 0
                            df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = BuyPrice
                            df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                            df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                            continue
                        else:
                            df.loc[loc_val_1m, 'Exit Point'] = min(recent_high,current_stop_point,previous_stop_point)
                            previous_stop_point = min(recent_high,current_stop_point,previous_stop_point)
                            continue
                    else:
                        KbarBuy = 0
                        KbarSell = 0
                        continue
            time_ec+=1
        else:
            for time_nor in timelist:
                loc_val_1m = (time_ec*285+time_c*300)+timelist.index(time_nor)
                if timelist.index(time_nor) < deferred_ticks:
                    KbarBuy = 0
                    KbarSell = 0
                    continue
                elif timelist.index(time_nor) == 298:
                    if MarketPosition == 1:
                        MarketPosition = 0
                        SellPrice = df.loc[loc_val_1m+1,'Open']
                        GainLossPoints = SellPrice - BuyPrice
                        if GainLossPoints > 0:
                            TotalGain += GainLossPoints
                            TotalWins +=1
                            if lastwin:
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastloss = False
                                pass
                            else:
                                consecutiveloss = 0
                                consecutivelose = 0
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastwin = True
                                lastloss = False
                                pass
                        else:
                            TotalLoss += GainLossPoints
                            TotalLose +=1
                            if lastloss:
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastwin = False
                                pass
                            else:
                                consecutivegain = 0
                                consecutivewin = 0
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastloss = True
                                lastwin = False
                                pass
                        NetPrice += GainLossPoints
                        df.loc[loc_val_1m+1, 'Position'] = 'endclose'
                        df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = SellPrice
                        df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                        df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                    elif MarketPosition == -1:
                        MarketPosition = 0
                        BuyPrice = df.loc[loc_val_1m+1,'Open']
                        GainLossPoints = SellPrice - BuyPrice
                        if GainLossPoints > 0:
                            TotalGain += GainLossPoints
                            TotalWins +=1
                            if lastwin:
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastloss = False
                                pass
                            else:
                                consecutiveloss = 0
                                consecutivelose = 0
                                consecutivegain += GainLossPoints
                                consecutivewin +=1
                                max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                lastwin = True
                                lastloss = False
                                pass
                        else:
                            TotalLoss += GainLossPoints
                            TotalLose +=1
                            if lastloss:
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastwin = False
                                pass
                            else:
                                consecutivegain = 0
                                consecutivewin = 0
                                consecutiveloss +=GainLossPoints
                                consecutivelose +=1
                                max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                lastloss = True
                                lastwin = False
                                pass
                        NetPrice += GainLossPoints
                        df.loc[loc_val_1m+1, 'Position'] = 'endclose'
                        df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = BuyPrice
                        df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                        df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                    else:
                        KbarBuy = 0
                        KbarSell = 0
                        continue
                else:
                    if MarketPosition == 0 and timelist.index(time_nor) > deferred_ticks and timelist.index(time_nor) < 269:
                        for c in range(0,consec_ticks-1):
                            if df.loc[loc_val_1m-c,'Close'] > df.loc[loc_val_1m-c,'Open'] and df.loc[loc_val_1m-c,'Close'] > df.loc[loc_val_1m-c-1,'Close'] and df.loc[loc_val_1m-c,'Open'] > df.loc[loc_val_1m-c-1,'Open']:
                                KbarBuy +=1
                                pass
                        for d in range(0,consec_ticks-1):
                            if df.loc[loc_val_1m-d,'Close'] < df.loc[loc_val_1m-d,'Open'] and df.loc[loc_val_1m-d,'Close'] < df.loc[loc_val_1m-d-1,'Close'] and df.loc[loc_val_1m-d,'Open'] < df.loc[loc_val_1m-d-1,'Open']:
                                KbarSell +=1
                                pass
                        if KbarBuy == (consec_ticks-1):
                            BuySellTimes +=1
                            MarketPosition = 1
                            BuyPrice = df.loc[loc_val_1m+1,'Open']
                            df.loc[loc_val_1m+1, 'Position'] = 1
                            df.loc[loc_val_1m+1, 'BuyPurchasePrice'] = BuyPrice
                            KbarBuy = 0
                            KbarSell = 0
                            previous_stop_point = current_stop_point = df.loc[loc_val_1m,'Close'] - current_kbar_brace
                            continue
                        elif KbarSell == (consec_ticks-1):
                            BuySellTimes +=1
                            MarketPosition = -1
                            SellPrice = df.loc[loc_val_1m+1,'Open']
                            df.loc[loc_val_1m+1, 'Position'] = -1
                            df.loc[loc_val_1m+1, 'SellPurchasePrice'] = SellPrice
                            previous_stop_point = current_stop_point = df.loc[loc_val_1m,'Close'] + current_kbar_brace
                            KbarBuy = 0
                            KbarSell = 0
                            continue
                        else:
                            KbarBuy = 0
                            KbarSell = 0
                            continue
                    elif MarketPosition == 1:
                        recent_low = df.loc[loc_val_1m-nearest_kbar:loc_val_1m,'Low'].values.min() - nearest_kbar_brace
                        current_stop_point = df.loc[loc_val_1m,'Close'] - current_kbar_brace
                        if df.loc[loc_val_1m,'Close'] < max(recent_low,current_stop_point,previous_stop_point):
                            MarketPosition = 0
                            SellPrice = df.loc[loc_val_1m+1,'Open']
                            GainLossPoints = SellPrice - BuyPrice
                            if GainLossPoints > 0:
                                TotalGain += GainLossPoints
                                TotalWins +=1
                                if lastwin:
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastloss = False
                                    pass
                                else:
                                    consecutiveloss = 0
                                    consecutivelose = 0
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastwin = True
                                    lastloss = False
                                    pass
                            else:
                                TotalLoss += GainLossPoints
                                TotalLose +=1
                                if lastloss:
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastwin = False
                                    pass
                                else:
                                    consecutivegain = 0
                                    consecutivewin = 0
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastloss = True
                                    lastwin = False
                                    pass
                            NetPrice += GainLossPoints
                            df.loc[loc_val_1m+1, 'Position'] = 0
                            df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = SellPrice
                            df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                            df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                            continue
                        else:
                            df.loc[loc_val_1m, 'Exit Point'] = max(recent_low,current_stop_point,previous_stop_point)
                            previous_stop_point = max(recent_low,current_stop_point,previous_stop_point)
                            continue
                    elif MarketPosition == -1:
                        recent_high = df.loc[loc_val_1m-nearest_kbar:loc_val_1m,'High'].values.max() + nearest_kbar_brace
                        current_stop_point = df.loc[loc_val_1m,'Close'] + current_kbar_brace
                        if df.loc[loc_val_1m,'Close'] > min(recent_high,current_stop_point,previous_stop_point):
                            MarketPosition = 0
                            BuyPrice = df.loc[loc_val_1m+1,'Open']
                            GainLossPoints = SellPrice - BuyPrice
                            if GainLossPoints > 0:
                                TotalGain += GainLossPoints
                                TotalWins +=1
                                if lastwin:
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastloss = False
                                    pass
                                else:
                                    consecutiveloss = 0
                                    consecutivelose = 0
                                    consecutivegain += GainLossPoints
                                    consecutivewin +=1
                                    max_consecutive_gain = max(consecutivegain,max_consecutive_gain)
                                    max_consecutive_win = max(consecutivewin,max_consecutive_win)
                                    lastwin = True
                                    lastloss = False
                                    pass
                            else:
                                TotalLoss += GainLossPoints
                                TotalLose +=1
                                if lastloss:
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastwin = False
                                    pass
                                else:
                                    consecutivegain = 0
                                    consecutivewin = 0
                                    consecutiveloss +=GainLossPoints
                                    consecutivelose +=1
                                    max_consecutive_loss = min(consecutiveloss,max_consecutive_loss)
                                    max_consecutive_lose = max(consecutivelose,max_consecutive_lose)
                                    lastloss = True
                                    lastwin = False
                                    pass
                            NetPrice += GainLossPoints
                            df.loc[loc_val_1m+1, 'Position'] = 0
                            df.loc[loc_val_1m+1, 'ClosePurchasePrice'] = BuyPrice
                            df.loc[loc_val_1m+1, 'GainLoss'] = GainLossPoints
                            df.loc[loc_val_1m+1, 'NetPrice'] = NetPrice
                            continue
                        else:
                            df.loc[loc_val_1m, 'Exit Point'] = min(recent_high,current_stop_point,previous_stop_point)
                            previous_stop_point = min(recent_high,current_stop_point,previous_stop_point)
                            continue
                    else:
                        KbarBuy = 0
                        KbarSell = 0
                        continue
            time_c+=1
    jan_gainloss = df[df['month']==1]['GainLoss'].sum()
    feb_gainloss = df[df['month']==2]['GainLoss'].sum()
    mar_gainloss = df[df['month']==3]['GainLoss'].sum()
    apr_gainloss = df[df['month']==4]['GainLoss'].sum()
    may_gainloss = df[df['month']==5]['GainLoss'].sum()
    jun_gainloss = df[df['month']==6]['GainLoss'].sum()
    jul_gainloss = df[df['month']==7]['GainLoss'].sum()
    aug_gainloss = df[df['month']==8]['GainLoss'].sum()
    sep_gainloss = df[df['month']==9]['GainLoss'].sum()
    oct_gainloss = df[df['month']==10]['GainLoss'].sum()
    nov_gainloss = df[df['month']==11]['GainLoss'].sum()
    dec_gainloss = df[df['month']==12]['GainLoss'].sum()
    if BuySellTimes == 0:
        Winrate = 0
    else:
        Winrate = round(TotalWins/BuySellTimes,4)

def one_min_backtest():
    start_time=time.time()
    testtimes = 0
    b1, b2, b3 = 5, 65, 5
    b4 = (b2-b1)/b3
    c1, c2, c3 = 2, 6, 1
    c4 = (c2-c1)/c3
    d1, d2, d3 = 3, 11, 1
    d4 = (d2-d1)/d3
    e1, e2, e3 = 2, 12, 2
    e4 = (e2-e1)/e3
    f1, f2, f3 = 10, 30, 5
    f4 = (f2-f1)/f3
    totaltesttimes = b4*c4*d4*e4*f4
    for dft in range(b1,b2,b3):
        for constk in range(c1,c2,c3):
            for nrkb in range(d1,d2,d3):
                for nrkbbrace in range(e1,e2,e3):
                    for crkbbrace in range(f1,f2,f3):
                                            one_time=time.time()
                                            df2 = df.copy()
                                            one_min_enter(df2,dft,constk,nrkb,nrkbbrace,crkbbrace)
                                            resultcolumns = dict({'deferred_ticks':dft,'consec_ticks':constk,'Nearest_K_bar':nrkb,'Nearest_K_bar_brace':nrkbbrace,'Current_K_bar_brace':crkbbrace,'Total times traded':BuySellTimes,'Total net gain(loss)':NetPrice,'Total gains':TotalGain,'Total losses':TotalLoss,'Total stop gains':StopGainTimes,'Total stop losses':StopLossTimes,'Max consecutive win times':max_consecutive_win,'Max consecutive gains':max_consecutive_gain,'Max consecutive lose times':max_consecutive_lose,'Max consecutive losses':max_consecutive_loss,'Jan_Gain_Loss':jan_gainloss,'Feb_Gain_Loss':feb_gainloss,'March_Gain_Loss':mar_gainloss,'April_Gain_Loss':apr_gainloss,'May_Gain_Loss':may_gainloss,'June_Gain_Loss':jun_gainloss,'July_Gain_Loss':jul_gainloss,'August_Gain_Loss':aug_gainloss,'September_Gain_Loss':sep_gainloss,'October_Gain_Loss':oct_gainloss,'November_Gain_Loss:':nov_gainloss,'December_Gain_Loss':dec_gainloss,'Win rate':Winrate})
                                            row_list.append(resultcolumns)
                                            testtimes +=1
                                            print('{} times results out of {}'.format(testtimes,totaltesttimes))
                                            take_one_time=time.time()-one_time
                                            print('This result took:',round(take_one_time,4),'seconds')
    df3 = pd.DataFrame(row_list)
    df3.to_csv (r'/home/justin/Documents/Futures/data/2020_1m_enter.csv', index=False, header=True)
    take_time=time.time()-start_time
    print('Total Time:',round(take_time,4),'seconds')
    
one_min_backtest()

start_time=time.time()
one_min_enter(df,10,2,9,4,15)
take_time=time.time()-start_time
print('Total Time:',round(take_time,4),'seconds')
df.to_csv (r'/home/justin/Documents/Futures/data/2020_1min_enter_testresult_forlook.csv', index=False, header=True)

import datetime
df = df.set_index('Time')
df2 = df[['Open','High','Low','Close','Volume']]
year1 = 2020

for month1 in range(7,8):
    for day1 in range(1,32):
        try:
            startdate = datetime.datetime(year=year1,month=month1,day=day1,hour=8,minute=48)
            enddate = datetime.datetime(year=year1,month=month1,day=day1,hour=13,minute=45)
            try:
                # mpf_mc=mpf.make_marketcolors(up='r',down='g')
                # mpf_s  = mpf.make_mpf_style(marketcolors=mpf_mc)
                df3 = df.loc[startdate.strftime('20%y-%m-%d %H:%M'):enddate.strftime('20%y-%m-%d %H:%M')]
                df4 = df2.loc[startdate.strftime('20%y-%m-%d %H:%M'):enddate.strftime('20%y-%m-%d %H:%M')]
                exitpoints = df3['Exit Point']
                buypoints = df3['BuyPurchasePrice']
                sellpoints = df3['SellPurchasePrice']
                closepoints = df3['ClosePurchasePrice']
                try:
                    apds = [ mpf.make_addplot(exitpoints,linestyle='dashdot'),
                             mpf.make_addplot(buypoints,scatter=True,markersize=50,marker='^',color='blue'),
                             mpf.make_addplot(sellpoints,scatter=True,markersize=50,marker='v',color='orange'),
                             mpf.make_addplot(closepoints,scatter=True,markersize=50,marker='<',color='grey')
                           ]
                    fig_axis = mpf.plot(df4,type='candle',addplot=apds,datetime_format='%m-%d %H:%M',figratio=(24,16),volume=True,style='yahoo',panel_ratios=(4,1))
                except ValueError:
                    try:
                        apds = [ mpf.make_addplot(exitpoints,linestyle='dashdot'),
                                 mpf.make_addplot(buypoints,scatter=True,markersize=50,marker='^',color='blue'),
                                 mpf.make_addplot(closepoints,scatter=True,markersize=50,marker='<',color='grey')
                                ]
                        fig_axis = mpf.plot(df4,type='candle',addplot=apds,datetime_format='%m-%d %H:%M',figratio=(24,16),volume=True,style='yahoo',panel_ratios=(4,1))
                    except ValueError:
                        try:
                            apds = [ mpf.make_addplot(exitpoints,linestyle='dashdot'),
                                     mpf.make_addplot(sellpoints,scatter=True,markersize=50,marker='v',color='orange'),
                                     mpf.make_addplot(closepoints,scatter=True,markersize=50,marker='<',color='grey')
                                   ]
                            fig_axis = mpf.plot(df4,type='candle',addplot=apds,datetime_format='%m-%d %H:%M',figratio=(24,16),volume=True,style='yahoo',panel_ratios=(4,1))
                        except ValueError:
                            try:
                                fig_axis = mpf.plot(df4,type='candle',datetime_format='%m-%d %H:%M',figratio=(24,16),volume=True,style='yahoo',panel_ratios=(4,1))
                            except ValueError:
                                pass
            except IndexError:
                pass
        except ValueError:
            pass

