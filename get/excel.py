# screen.py
# Вывод в excel списка (списка списков)
# Импорт библиотеки - https://pypi.org/project/xlwt/
import xlwt
#import os
# Поделючаем общий для всего проекта модуль
import common
# Подключаем сообщения
from messages import msg
# Экспорт данных в Excel
# header - Заголовок таблицы, data данные (список списков), название файла
def export_to_excel(header, data, file_name):
    try:
        common.writing_log("Информация", "Экспорт в Excel")
        # Убрать начальные и концевые пробеды
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                data[i][j] = data[i][j].strip()
        # Максимальная ширина столбца в Excel
        col_max_width = 65535
        # Стиль заголовка
        style_header = xlwt.easyxf('font: name Arial, color-index blue, bold on')
        # Стиль данных
        style_data = xlwt.easyxf('font: name Arial')
        # Новая книга
        wb = xlwt.Workbook()
        # Новый лист
        ws = wb.add_sheet("List")
        # Заголовок
        for i in range(0, len(header)):        
            ws.write(0, i, header[i], style_header)
        # Данные (смещение на 1 строку из-за заголовка)
        #for row in data:
        #    for elem in row:
        #        print(elem, end=' ')
        #    print()
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                #print(data[i][j])
                # Подбор ширины колонки в зависимости от длины выводимых данных
                cwidth = ws.col(j).width
                if (len(data[i][j])*367) > cwidth:
                    if len(data[i][j])*367 > col_max_width :
                        ws.col(j).width = col_max_width
                    else:
                        ws.col(j).width = (len(data[i][j])*367)
                # Запись ячейки
                ws.write(i+1, j, data[i][j], style_data)
        # Сохранить книгу
        wb.save(file_name)
        common.writing_log("Информация", "См. файл: " + str(file_name))
    except Exception as exception:
        print(exception)
        common.writing_log("Ошибка", "export_to_excel\t" + str(exception))
