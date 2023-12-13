import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# При необходимости в класс могут добавляться другие параметры и методы

def date_time_index_maker(dfr:pd.DataFrame): # функция по созданию строки типа "2023-12-14 00:00:00" из интовых данных столбцов <DATE> и <TIME>

    return pd.to_datetime(dfr['Date'][4:] + '-' + dfr['Date'][2:4] + '-' + dfr['Date'][0:2] + ' ' + dfr['Time'][0:2] + ':' + dfr['Time'][2:4] + ':' + dfr['Time'][4:])

class dfContainerIntraDay:
    def __init__(self, df_path):
        self.df_path = df_path  # строковое значение пути распололжения датасета
        self.curr_df = pd.read_csv(self.df_path, sep=';', dtype=str)   # инициализация pandas-датафрейма. Изначально перевожу все данные в строковый формат, т.к. выяснилось что pandas съедает нули у интов типа 001500 - распознается как 1500. Строковый формат позволяет этого избежать 
        self.curr_df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']  # Замена названий столбцов типа <DATE> на тип 'Date' для правильной работы биб-ки mplfinance
        self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']] = self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']].astype('float32')  # Цифровые значения перевожу снова в float

        self.curr_df.index = self.curr_df.apply(date_time_index_maker, axis=1)  # применяю функцию date_time_index_maker к строкам датафрейма и делаю индекс из получившихся значений datetime

    # Методы как в классе dfContainer

    def show_info(self):
        print(self.curr_df.info())

    def show_describe(self):
        print(self.curr_df.describe())

    def show_head(self, num:int):
        print(self.curr_df.head(num))

    def draw_graph(self, end_date:str, start_date='', fig_sz = (8,8), vol=False):  # здесь добавляется переменная vol. Если ее значение True, то будет отрисовываться торговый объем. По умолчанию False.
        if(start_date != ''):
            mpf.plot(self.curr_df.loc[pd.to_datetime(start_date):pd.to_datetime(end_date)], type='candle',mav=(3,6,9), figsize=fig_sz, volume=vol)
            plt.show()

        else:
            mpf.plot(self.curr_df.loc[:pd.to_datetime(end_date)], type='candle',mav=(3,6,9), figsize=fig_sz, volume=vol)
            plt.show()
