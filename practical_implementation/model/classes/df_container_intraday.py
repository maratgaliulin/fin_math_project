import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def date_time_index_maker(dfr:pd.DataFrame):
    return pd.to_datetime(dfr['Date'][4:] + '-' + dfr['Date'][2:4] + '-' + dfr['Date'][0:2] + ' ' + dfr['Time'][0:2] + ':' + dfr['Time'][2:4] + ':' + dfr['Time'][4:])

class dfContainerIntraDay:
    def __init__(self, df_path):
        self.df_path = df_path
        self.curr_df = pd.read_csv(self.df_path, sep=';', dtype=str)
        self.curr_df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']] = self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']].astype('float32')

        self.curr_df.index = self.curr_df.apply(date_time_index_maker, axis=1)

    def show_info(self):
        print(self.curr_df.info())

    def show_describe(self):
        print(self.curr_df.describe())

    def show_head(self, num:int):
        print(self.curr_df.head(num))

    def draw_graph(self, end_date:str, start_date='', fig_sz = (8,8), vol=False):
        if(start_date != ''):
            mpf.plot(self.curr_df.loc[pd.to_datetime(start_date):pd.to_datetime(end_date)], type='candle',mav=(3,6,9), figsize=fig_sz, volume=vol)
            plt.show()

        else:
            mpf.plot(self.curr_df.loc[:pd.to_datetime(end_date)], type='candle',mav=(3,6,9), figsize=fig_sz, volume=vol)
            plt.show()
