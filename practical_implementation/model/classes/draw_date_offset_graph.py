import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from .mpf_styles import binance_dark


def draw_do(df:pd.DataFrame, d_o: pd.DateOffset(), start_date, fig_sz, vol, type): # вспомогательная функция, отрисовывающая график в зависимости от значения type_graph (см. условия if/else ниже)
          try:
            start_date += ' 00:00:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            DCU = df[['Upper']].loc[stdt:end_date]
            DCM = df[['Middle']].loc[stdt:end_date]
            DCL = df[['Lower']].loc[stdt:end_date]
            Plot_RSI = df['rsi'].loc[stdt:end_date]
            Daily_High_Limit = df['daily_high'].loc[stdt:end_date]
            Daily_Low_Limit = df['daily_low'].loc[stdt:end_date]
            Upper_Zone_Limit = df['upper_zone_limit'].loc[stdt:end_date]
            Lower_Zone_Limit = df['lower_zone_limit'].loc[stdt:end_date]
            apds = [
                mpf.make_addplot(DCU,color='#2962FF',panel=0),
                mpf.make_addplot(DCM,color='#FF6D00',panel=0),
                mpf.make_addplot(DCL,color='#2962FF',panel=0),

                mpf.make_addplot(Daily_High_Limit,color='#00aa14',panel=0),
                mpf.make_addplot(Daily_Low_Limit,color='#b60431',panel=0),

                mpf.make_addplot(Upper_Zone_Limit,color='#00aa14',panel=0),
                mpf.make_addplot(Lower_Zone_Limit,color='#b60431',panel=0),

                mpf.make_addplot(Plot_RSI,panel=2,color='lime',ylim=(10,90),secondary_y=True),
            ]
            mpf.plot(df.loc[stdt:end_date], type=type, figsize=fig_sz, volume=vol, style=binance_dark, addplot=apds) # отрисовывает график
            plt.show()
          except:
            start_date += ' 00:15:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            DCU = df[['Upper']].loc[stdt:end_date]
            DCM = df[['Middle']].loc[stdt:end_date]
            DCL = df[['Lower']].loc[stdt:end_date]
            Plot_RSI = df['rsi'].loc[stdt:end_date]
            Daily_High_Limit = df['daily_high'].loc[stdt:end_date]
            Daily_Low_Limit = df['daily_low'].loc[stdt:end_date]
            Upper_Zone_Limit = df['upper_zone_limit'].loc[stdt:end_date]
            Lower_Zone_Limit = df['lower_zone_limit'].loc[stdt:end_date]
            apds = [
                mpf.make_addplot(DCU,color='#2962FF',panel=0),
                mpf.make_addplot(DCM,color='#FF6D00',panel=0),
                mpf.make_addplot(DCL,color='#2962FF',panel=0),

                mpf.make_addplot(Daily_High_Limit,color='#00aa14',panel=0),
                mpf.make_addplot(Daily_Low_Limit,color='#b60431',panel=0),

                mpf.make_addplot(Upper_Zone_Limit,color='#00aa14',panel=0),
                mpf.make_addplot(Lower_Zone_Limit,color='#b60431',panel=0),

                mpf.make_addplot(Plot_RSI,panel=2,color='lime',ylim=(10,90),secondary_y=True),
            ]
            mpf.plot(df.loc[stdt:end_date], type=type, figsize=fig_sz, volume=vol, style=binance_dark, addplot=apds) # отрисовывает график
            plt.show()