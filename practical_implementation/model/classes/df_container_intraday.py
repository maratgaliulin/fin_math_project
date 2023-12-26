import pandas as pd
from datetime import datetime
from .graph_types.draw_date_offset_graph import draw_do
from .graph_types.base_graph import draw_basic_graph
from .graph_types.graph_rsi import draw_graph_rsi
from .graph_types.graph_ema import draw_graph_ema
from .rsi import relative_strength
import numpy as np

# При необходимости в класс могут добавляться другие параметры и методы

def date_time_index_maker(dfr:pd.DataFrame): # функция по созданию строки типа "2023-12-14 00:00:00" из интовых данных столбцов <DATE> и <TIME>
    return datetime.strptime(dfr['Date'] + dfr['Time'], "%y%m%d%H%M%S")

def func_upper_zone_limit(df:pd.DataFrame):
   return np.array_split(np.linspace(df['daily_low'], df['daily_high'], 10), 5)[4][0]

def func_lower_zone_limit(df:pd.DataFrame):
   return np.array_split(np.linspace(df['daily_low'], df['daily_high'], 10), 5)[0][1]

def pos_diff_calc(df:pd.DataFrame):
   result = (df['High'] - df['upper_zone_limit'])/(df['High'] - df['Low'] + 0.00000001) * df['Volume']   
   if result > 0:
      return result   
   else:
      return 0.0
   
def neg_diff_calc(df:pd.DataFrame):   
   neg_result = (df['Low'] - df['lower_zone_limit']) / (df['High'] - df['Low'] + 0.00000001) * df['Volume']
   if neg_result < 0:
      return neg_result
   else:
      return 0.0
   
def between_diff_calc(df:pd.DataFrame):   
   
   candle_len = df['High'] - df['Low']
   upper_border = df['upper_zone_limit'] - df['High']
   lower_border = df['Low'] - df['lower_zone_limit']

   if df['Open'] < df['Close']:
      if upper_border >= 0 and lower_border >= 0:
         between_res = (candle_len) / (candle_len + 0.00000001) * df['Volume']
      elif upper_border <= 0 and lower_border >= 0:
         between_res = (df['upper_zone_limit'] - df['Low']) / (candle_len + 0.00000001) * df['Volume']
      elif upper_border >= 0 and lower_border <= 0:
         between_res = (df['High'] - df['lower_zone_limit']) / (candle_len + 0.00000001) * df['Volume']
      else: 
         between_res = 0.0

   elif df['Open'] > df['Close']:
      if upper_border >= 0 and lower_border >= 0:
         between_res = -(candle_len) / (candle_len + 0.00000001) * df['Volume']
      elif upper_border <= 0 and lower_border >= 0:
         between_res = -(df['upper_zone_limit'] - df['Low']) / (candle_len + 0.00000001) * df['Volume']
      elif upper_border >= 0 and lower_border <= 0:
         between_res = -(df['High'] - df['lower_zone_limit']) / (candle_len + 0.00000001) * df['Volume']
      else: 
         between_res = 0.0
   else: 
         between_res = 0.0
   
   return between_res
   

class dfContainerIntraDay:
    def __init__(self, df_path, period = 10, benchmark=50000):
        self.df_path = df_path  # строковое значение пути распололжения датасета
        self.period = period
        self.benchmark = benchmark
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

        self.curr_df['low_vol_cumulation'] = self.curr_df.apply(neg_diff_calc, axis=1)
        self.curr_df['low_vol_cumulation'].replace(0.0, np.nan, inplace=True)
        self.curr_df['low_vol_cumsum'] = self.curr_df['low_vol_cumulation'].cumsum(axis=0, skipna=True)
        self.curr_df['low_vol_cumsum_%_50_000'] = self.curr_df['low_vol_cumsum'] % self.benchmark
        self.curr_df['low_vol_cumsum_%_TrueFalse'] = self.curr_df['low_vol_cumsum_%_50_000'] <= 7000

        self.curr_df['between_vol_cumulation'] = self.curr_df.apply(between_diff_calc, axis=1)
        self.curr_df['between_vol_cumulation'].replace(0.0, np.nan, inplace=True)
        self.curr_df['between_vol_cumsum'] = self.curr_df['between_vol_cumulation'].cumsum(axis=0, skipna=True)
        self.curr_df['between_vol_cumsum_%_50_000'] = self.curr_df['between_vol_cumsum'] % (self.benchmark * 2)
        self.curr_df['between_vol_cumsum_%_TrueFalse'] = self.curr_df['between_vol_cumsum_%_50_000'] <= 7000

        self.curr_df['high_vol_cumulation'] = self.curr_df.apply(pos_diff_calc, axis=1)
        self.curr_df['high_vol_cumulation'].replace(0.0, np.nan, inplace=True)
        self.curr_df['high_vol_cumsum'] = self.curr_df['high_vol_cumulation'].cumsum(axis=0, skipna=True)
        self.curr_df['high_vol_cumsum_%_50_000'] = self.curr_df['high_vol_cumsum'] % self.benchmark
        self.curr_df['high_vol_cumsum_%_TrueFalse'] = self.curr_df['high_vol_cumsum_%_50_000'] <= 7000

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
      
    def negative_write_to_file(self):
      self.negative.to_csv('negative.csv')

    # Метод draw_graph() отрисовывает график датафрейма. start_date - дата начала графика (по умолчанию - 2022-12-01г),
    # type_graph - показывает, какой промежуток от start_date отрисовывать (если day, то 1 день, если week то 1 неделю, если month то 1 месяц)
    # fig_sz - размер области графика
    # vol - если True, график будет выводить цену и объем (при наличии соответствующих данных), если False, только цену (по умолчанию - False)
      
    def basic_graph(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):
       if type_graph <= 8:
          draw_basic_graph(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
       else:
          draw_basic_graph(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')  

    def graph_rsi(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):
       if type_graph <= 8:
          draw_graph_rsi(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
       else:
          draw_graph_rsi(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')  

    def graph_ema(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):
       if type_graph <= 8:
          draw_graph_ema(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
       else:
          draw_graph_ema(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')  

    def draw_full_graph(self, start_date='2022-12-01', fig_sz = (8,8), vol=False, type_graph=1):  # здесь добавляется переменная vol. Если ее значение True, то будет отрисовываться торговый объем. По умолчанию False.
        if type_graph <= 8:
          draw_do(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'candle')
        else:
          draw_do(self.curr_df, pd.DateOffset(type_graph), start_date, fig_sz, vol, 'line')

