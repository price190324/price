# Общие процедуры
# Импорт библиотек
#from calendar import month
#from pickle import FALSE, TRUE
#import sys
# Подключаем модуль для работы с датой/веременем
from datetime import datetime
#from datetime import timedelta
# Поделючаем модкль генерации случайных чисел
#import random

# Запись в лог-файл
def writing_log(category, message):
    try:        
        # Лог-файл
        somefile = open("log.txt", "a", encoding="utf-8")
        # Сообщение
        message = str(datetime.now().strftime('%d.%m.%Y %H:%M:%S')) + "\t" + category + "\t" + message + "\r"
        try:
            # Запись в файл и вывод на экран
            somefile.write(message)
            print(message)
        except Exception as exception:
            print(exception)
        finally:
            # Закрыть при любом раскладе!
            somefile.close()
    except Exception as exception:
        print(exception)
        writing_log("Ошибка", "writing_log\t" + str(exception))
