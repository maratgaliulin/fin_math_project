import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime

# При необходимости в класс могут добавляться другие параметры и методы

def date_time_index_maker(dfr:pd.DataFrame): # функция по созданию строки типа "2023-12-14 00:00:00" из интовых данных столбцов <DATE> и <TIME>
    return datetime.strptime(dfr['Date'] + dfr['Time'], "%y%m%d%H%M%S")

class dfContainerIntraDay:
    def __init__(self, df_path):
        self.df_path = df_path  # строковое значение пути распололжения датасета
        self.curr_df = pd.read_csv(self.df_path, sep=';', dtype=str)   # инициализация pandas-датафрейма. Изначально перевожу все данные в строковый формат, т.к. выяснилось что pandas съедает нули у интов типа 001500 - распознается как 1500. Строковый формат позволяет этого избежать
        self.curr_df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']  # Замена названий столбцов типа <DATE> на тип 'Date' для правильной работы биб-ки mplfinance
        self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']] = self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']].astype('float32')  # Цифровые значения перевожу снова в float
        self.curr_df.index = pd.DatetimeIndex(self.curr_df.apply(date_time_index_maker, axis=1))  # применяю функцию date_time_index_maker к строкам датафрейма и делаю индекс из получившихся значений datetime

    # Методы как в классе dfContainer

    def show_info(self):
        print(self.curr_df.info())

    def show_describe(self):
        print(self.curr_df.describe())

    def show_head(self, num:int):
        print(self.curr_df.head(num))

    # Метод draw_graph() отрисовывает график датафрейма. start_date - дата начала графика (по умолчанию - 2022-12-01г),
    # type_graph - показывает, какой промежуток от start_date отрисовывать (если day, то 1 день, если week то 1 неделю, если month то 1 месяц)
    # fig_sz - размер области графика
    # vol - если True, график будет выводить цену и объем (при наличии соответствующих данных), если False, только цену (по умолчанию - False)

    def draw_graph(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):  # здесь добавляется переменная vol. Если ее значение True, то будет отрисовываться торговый объем. По умолчанию False.
        def draw_do(d_o: pd.DateOffset(), start_date, fig_sz, vol, type): # вспомогательная функция, отрисовывающая график в зависимости от значения type_graph (см. условия if/else ниже)
          try:
            start_date += ' 00:00:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            mpf.plot(self.curr_df.loc[stdt:end_date], type=type,mav=(3,6,9), figsize=fig_sz, volume=vol) # отрисовывает график
            plt.show()
          except:
            start_date += ' 00:15:00' # прибавляет время к строке даты
            stdt = pd.to_datetime(start_date) # превращает строку в формат datetime
            end_date = pd.to_datetime(start_date) + d_o # задает конечную дату в зависимости от значения DateOffset
            mpf.plot(self.curr_df.loc[stdt:end_date], type=type,mav=(3,6,9), figsize=fig_sz, volume=vol) # отрисовывает график
            plt.show()
    # Условный оператор в зависимости от переменной type_graph:
        if type_graph <= 8:
          draw_do(pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
        else:
          draw_do(pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')