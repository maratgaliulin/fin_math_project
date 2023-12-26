import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from ..mpf_styles import binance_dark
from ..cumsum_truefalse import cumsum_true_false


def draw_basic_graph(df:pd.DataFrame, d_o: pd.DateOffset(), start_date, fig_sz, vol, type): # вспомогательная функция, отрисовывающая график в зависимости от значения type_graph (см. условия if/else ниже)
          try:
            start_date += ' 00:00:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            mpf.plot(df.loc[stdt:end_date], type=type, figsize=fig_sz, volume=vol, style=binance_dark) # отрисовывает график
            plt.show()
          except:
            start_date += ' 00:15:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            mpf.plot(df.loc[stdt:end_date], type=type, figsize=fig_sz, volume=vol, style=binance_dark) # отрисовывает график
            plt.show()