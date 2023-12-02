import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

class dfContainer:
    def __init__(self, df_path):
        self.df_path = df_path
        self.curr_df = pd.read_csv(self.df_path, index_col='Date')
        self.curr_df['Close'] = self.curr_df['Price']
        self.curr_df.index = pd.to_datetime(self.curr_df.index)

    def show_info(self):
        print(self.curr_df.info())

    def show_describe(self):
        print(self.curr_df.describe())

    def draw_graph(self, end_date:str, start_date='', fig_sz = (8,8)):
        if(start_date != ''):
            mpf.plot(self.curr_df.loc[pd.to_datetime(end_date, format='%Y-%m-%d'):pd.to_datetime(start_date, format='%Y-%m-%d')], type='candle',mav=(3,6,9), figsize=fig_sz)
            plt.show()

        else:
            mpf.plot(self.curr_df.loc[:pd.to_datetime(end_date)], type='candle',mav=(3,6,9), figsize=fig_sz)
            plt.show()
