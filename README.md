## 1. Цель краткосрочной исследовательской работы – анализ движения цен валютных пар (3-4 наиболее ликвидных) внутри временных зон, соответствующих повышению активности на крупных торговых площадках

## 2. Задачи:
### а. Сбор сырых данных по ценам и торговым объемам валютных пар на форексе
### б. Определение целевых временных зон (ЦВЗ) – временные интервалы внутри дня по московскому времени, совпадающие с наибольшей активностью крупнейших мировых валютных торговых площадок
### в. Анализ движения цены внутри ЦВЗ в различных таймфреймах (5мин, 15мин, 30мин, 60мин, дневной и недельный таймфреймы) – торговые объемы, уровни, точки притяжения цены и т.д.
### г. Подключение алгоритмов машинного обучения (scikit learn и т.д.) для определения направления движения цены

## Папка classes будет содержать все классы для работы
## Класс dfContainer нужен для модификации датасета: переводит строковое значение даты/времени в формат datetime, делает его индексом, добавляет столбец Close (необходим для работы библиотеки mplfinance)
## Методы класса включают:
### show_info - выводит информацию о датасете
### show_describe - выводит стат.данные по датасету
### draw_graph - рисует графики по вводным параметрам