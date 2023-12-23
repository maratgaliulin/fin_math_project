import pandas as pd
from datetime import datetime
from .draw_date_offset_graph import draw_do
from .rsi import relative_strength
import numpy as np

# При необходимости в класс могут добавляться другие параметры и методы

def date_time_index_maker(dfr:pd.DataFrame): # функция по созданию строки типа "2023-12-14 00:00:00" из интовых данных столбцов <DATE> и <TIME>
    return datetime.strptime(dfr['Date'] + dfr['Time'], "%y%m%d%H%M%S")

def func_upper_zone_limit(df:pd.DataFrame):
   return np.array_split(np.linspace(df['daily_low'], df['daily_high'], 10), 5)[4][0]

def func_lower_zone_limit(df:pd.DataFrame):
   return np.array_split(np.linspace(df['daily_low'], df['daily_high'], 10), 5)[0][1]

def diff_calc(df:pd.DataFrame):
   result = (df['High'] - df['upper_zone_limit'])/(df['High'] - df['Low'] + 0.00000001) * df['Volume']
   neg_result = (df['Low'] - df['lower_zone_limit']) / (df['High'] - df['Low'] + 0.00000001) * df['Volume']
   if result > 0:
      return result
   elif neg_result < 0:
      return neg_result
   else:
      return 0.0
   

class dfContainerIntraDay:
    def __init__(self, df_path, period = 10):
        self.df_path = df_path  # строковое значение пути распололжения датасета
        self.period = period
        self.curr_df = pd.read_csv(self.df_path, sep=';', dtype=str)   # инициализация pandas-датафрейма. Изначально перевожу все данные в строковый формат, т.к. выяснилось что pandas съедает нули у интов типа 001500 - распознается как 1500. Строковый формат позволяет этого избежать
        self.curr_df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']  # Замена названий столбцов типа <DATE> на тип 'Date' для правильной работы биб-ки mplfinance
        self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']] = self.curr_df[['Open', 'High', 'Low', 'Close', 'Volume']].astype('float32')  # Цифровые значения перевожу снова в float
        self.curr_df.index = pd.DatetimeIndex(self.curr_df.apply(date_time_index_maker, axis=1))  # применяю функцию date_time_index_maker к строкам датафрейма и делаю индекс из получившихся значений datetime
        self.curr_df['Date'] = self.curr_df.index.date
        self.curr_df['Upper'] = self.curr_df['High'].rolling(self.period).max()
        self.curr_df['Lower'] = self.curr_df['Low'].rolling(self.period).min()
        self.curr_df['Middle'] = (self.curr_df['Upper'] + self.curr_df['Lower']) / 2
        self.curr_df['rsi'] = relative_strength(self.curr_df['Close'],n=7)
        self.minimax = pd.DataFrame(self.curr_df[['High', 'Low']].groupby(self.curr_df.index.date, as_index=True).agg({'High': 'max', 'Low': 'min'}))
        self.curr_df['daily_high'] = self.curr_df['Date'].map(self.minimax['High'])
        self.curr_df['daily_low'] = self.curr_df['Date'].map(self.minimax['Low'])
        self.curr_df['upper_zone_limit'] = self.curr_df.apply(func_upper_zone_limit, axis=1)
        self.curr_df['lower_zone_limit'] = self.curr_df.apply(func_lower_zone_limit, axis=1)
        self.curr_df['candle_LZ'] = self.curr_df.apply(diff_calc, axis=1)

    # Методы как в классе dfContainer

    def show_info(self):
        print(self.curr_df.info())

    def show_describe(self):
        print(self.curr_df.describe())

    def show_head(self, num:int):
        print(self.curr_df.head(num))

    def write_to_file(self):
      self.curr_df.to_csv('test.csv')

    def minimax_write_to_file(self):
      self.minimax.to_csv('minimax.csv')

    # Метод draw_graph() отрисовывает график датафрейма. start_date - дата начала графика (по умолчанию - 2022-12-01г),
    # type_graph - показывает, какой промежуток от start_date отрисовывать (если day, то 1 день, если week то 1 неделю, если month то 1 месяц)
    # fig_sz - размер области графика
    # vol - если True, график будет выводить цену и объем (при наличии соответствующих данных), если False, только цену (по умолчанию - False)

    def draw_graph(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):  # здесь добавляется переменная vol. Если ее значение True, то будет отрисовываться торговый объем. По умолчанию False.
    
    # Так как класс начал разрастаться, перенес функцию draw_do() в отдельный файл
        
    # Условный оператор в зависимости от переменной type_graph:
        if type_graph <= 8:
          draw_do(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
        else:
          draw_do(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')
