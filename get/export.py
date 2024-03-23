# Импорт библиотек
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# Таймер
from time import sleep        
# Чтобы засечь время выполнения
import time
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
# Функция отладки
DEBUG = False
DEBUG = True
# Подключаем модуль для работы с БД
import database
# Поделючаем общий для всего проекта модуль
import common
# Подключаем сообщения
from messages import msg
# Эти библиотеки только для порграммной оболочки
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets

# Создается новый класс ExportWindow котрый наследуется от класса QMainWindow. 
class ExportWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle("Export to Django")
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            #self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))            
                        # Создаём таблицу
            self.tableWidget = QTableWidget(self)  
            # Запрет изменения таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Устанавливаем количество колонок
            self.tableWidget.setColumnCount(10)
            # Устанавливаем заголовки таблицы
            self.tableWidget.setHorizontalHeaderLabels(["id", "URL (Карточка)", "Дата", "Продавец", "Категория", "Название", "Описание", "Цена", "Артикул", "Фотография"])
            self.tableWidget.doubleClicked.connect(lambda: self.edit_data())
            # Устанавливаем выравнивание на заголовки
            """
            tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
            tableWidget.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
            """            
            # Поле ввода строки поиска
            self.lineEdit = QLineEdit(self)            
            # Кнопка для поиска
            self.button = QPushButton(msg.filter)
            self.button.clicked.connect(lambda: self.filter_data())            
            # Кнопки
            self.pushButtonDjango = QPushButton(msg.export_to_django)
            self.pushButtonDjango.setObjectName("pushButtonDjango")
            self.pushButtonDjango.clicked.connect(lambda: self.export_to_django())
            self.pushButtonRefresh = QPushButton(msg.refresh)
            self.pushButtonRefresh.setObjectName("pushButtonRefresh")
            self.pushButtonRefresh.clicked.connect(lambda: self.select_data(""))
            self.pushButtonExit = QPushButton(msg.exit)
            self.pushButtonExit.setObjectName("pushButtonExit")
            self.pushButtonExit.clicked.connect(lambda: self.close())
            # Создаём центральный виджет
            central_widget = QWidget(self)
            # Устанавливаем центральный виджет
            self.setCentralWidget(central_widget)
            # Создаём QGridLayout -  сеточный макет который делит пространство на строки и столбцы. 
            grid_layout = QGridLayout()            
            # Устанавливаем данное размещение в центральный виджет
            central_widget.setLayout(grid_layout)               
            # Добавляем все визуальные элементы в сетку
            # int fromRow — номер ряда, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int fromColumn — номер столбца, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int rowSpan — количество рядов, ячейки которых следует объединить для размещения виджета начиная с ряда fromRow.
            # int columnSpan — количество столбцов, ячейки которых следует объединить для размещения виджета начиная со столбца fromColumn.
            grid_layout.addWidget(self.lineEdit, 0, 0, 1, 2)
            grid_layout.addWidget(self.button, 0, 2, 1 , 1)
            # Ячейка начинается с первой строки и нулевой колонки, и занимает 1 строку и 5 колонок.
            grid_layout.addWidget(self.tableWidget, 1, 0, 1, 5)                 
            grid_layout.addWidget(self.pushButtonDjango, 2, 0, 1, 1)            
            grid_layout.addWidget(self.pushButtonRefresh, 2, 1, 1, 1)            
            grid_layout.addWidget(self.pushButtonExit, 2, 2, 1, 1)            
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())  
            # Обновить данные
            self.select_data("")  
        except Exception as error:
            print(error)
            common.writing_log("Ошибка", "export\t" + str(error))
            QMessageBox.critical(self,  "Error",  str(error))  
            
    def select_data(self, where):
        try:
            # SQL-запрос
            #sql = "SELECT id, url, strftime('%d.%m.%Y %H:%M:%S', dateb), salesman, category, title, description, price, code, photo_url FROM basket " + where + " ORDER BY dateb"                
            sql = "SELECT id, url, dateb, salesman, category, title, description, price, code, photo_url FROM basket " + where + " ORDER BY dateb"                
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            result = database.fetchAll(sql)
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Заполнить таблицу
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if val != None:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))  
            # Ресайз колонок по содержимому
            self.tableWidget.resizeColumnsToContents()
            # Сброс строки поиска
            if where=="":
                self.lineEdit.setText("")
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "export\t" + str(exception))  

    def filter_data(self):
        try:
            # Сформировать строку поиска
            where = " WHERE category Like '%" +  self.lineEdit.text() + "%' OR category Like '%" +  self.lineEdit.text() + "%'"
            # Обновить данные в таблице
            self.select_data(where)            
        except Exception as exception:
            common.writing_log("Ошибка", "export\t" + str(exception))  
            QMessageBox.critical(self,  "Error",  str(exception))   

    def export_to_django(self):
        try:
            # Окно с сообщением и с двумя кнопками: Yes и No. Первая строка отображается в заголовке окна.
            # Вторая строка является текстовым сообщением и отображается в диалоговом окне.
            # Третий аргумент определяет комбинацию кнопок, появляющихся в диалоге.
            # Последний параметр - кнопка по умолчанию. Это кнопка, на которой изначально установлен фокус клавиатуры. Возвращаемое значение хранится в переменной reply.
            reply = QMessageBox.question(self, msg.warning,  msg.run + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Проверка возвращаемого значения
            if reply == QMessageBox.Yes:
                common.writing_log("Информация", "Старт экспорта в Django")
                # Перебрать всю корзину SQL-запрос
                sql = "SELECT url, dateb, salesman, category, title, description, price, code, photo_url FROM basket ORDER BY dateb"                
                # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
                result = database.fetchAll(sql)
                # Перебрать всю корзину и Заполнить таблицы category и product
                for row in result:
                    url = row[0]
                    #print(url)
                    dateb = row[1]
                    #print(dateb)
                    salesman = row[2]
                    #print(salesman)
                    category = row[3]
                    #print(category)
                    title = row[4]
                    #print(title)
                    description = row[5]
                    #print(description)
                    price = row[6]
                    if price == "cena":
                        price = '0'
                    #print(price)
                    code = row[7]
                    #print(code)
                    photo_url = row[8]
                    #print(photo_url)
                    ## SQL-запрос новая запись SQLite
                    #sql = "INSERT INTO product (url, dateb, salesman_id, category_id, title, description, price, code, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"                    
                    ## Параметры запроса
                    #parameters = [url, dateb, self.get_salesman_id(salesman), self.get_category_id(category), title, description, price, code, photo_url]
                    # SQL-запрос новая запись PostgreSQL
                    sql = "INSERT INTO product (url, dateb, salesman_id, category_id, title, description, price, code, photo_url) VALUES ('" + url + "', '" + str(dateb) + "', " + str(self.get_salesman_id(salesman)) + ", " + str(self.get_category_id(category)) + ", '" + title + "', '" + description + "', " + str(price) + ", '" + code + "', '" + photo_url +"')"                    
                    print(sql)
                    # Параметры запроса
                    parameters = []
                    # Выполнить запрос sql c параметрами parameters
                    database.executeSQL(sql, parameters)
                # Очистить корзину
                sql = "DELETE FROM basket"
                parameters= []
                # Выполнить запрос sql c параметрами parameters
                #database.executeSQL(sql, parameters)
                common.writing_log("Информация", "Экспорт в Django завершен")
            # Обновить данные в таблице
            self.select_data("")              
        except Exception as exception:
            common.writing_log("Ошибка", "export\t" + str(exception))  
            QMessageBox.critical(self,  "Error",  str(exception))   


    def get_salesman_id(self, val):   
        # Полчить id таблицы salesman, если такой записи нету то сначала добавить запись а потом получить id
        try:
            # Поиск 
            # SQL-запрос новая чтения записи
            sql = "SELECT id FROM salesman WHERE title='" + val + "'"
            # Получить результат запроса из resultSet можно с помощью метода fetchone()  
            result = database.fetchOne(sql)
            if result != None:                
                if len(result) > 0:                
                    #print("Продавец '" + val + "' уже существует")        
                    return result[0]
            else:
                ## SQL-запрос новая запись SQLite
                ##sql = "INSERT INTO salesman (title, site) VALUES (?, ?)"
                ## Параметры запроса
                #parameters = [val, ""]
                # SQL-запрос новая запись PostgreSQL
                sql = "INSERT INTO salesman  (title, site) VALUES ('" + val + "', '')"
                # Параметры запроса
                parameters = []
                # Выполнить запрос sql c параметрами parameters
                database.executeSQL(sql, parameters)
                # Поиск 
                # SQL-запрос новая чтения записи
                sql = "SELECT id FROM salesman WHERE title='" + val + "'"
                # Получить результат запроса из resultSet можно с помощью метода fetchone()   
                result = database.fetchOne(sql)
                if len(result) > 0:                
                    #print("Создан продавец '" + val + "'")         
                    return result[0]
        except Exception as exception:
            common.writing_log("Ошибка", "export\t" + str(exception))  
            QMessageBox.critical(self,  "Error",  str(exception))   

    def get_category_id(self, val):   
        # Полчить id таблицы category, если такой записи нету то сначала добавить запись а потом получить id
        try:
            # Поиск 
            # SQL-запрос новая чтения записи
            sql = "SELECT id FROM category WHERE title='" + val + "'"
            # Получить результат запроса из resultSet можно с помощью метода fetchone()  
            result = database.fetchOne(sql)
            if result != None:                
                if len(result) > 0:                
                    #print("Категория '" + val + "' уже существует")        
                    return result[0]
            else:
                ## SQL-запрос новая запись SQLite
                ##sql = "INSERT INTO category (title) VALUES (?)"
                ## Параметры запроса
                #parameters = [val]                
                # SQL-запрос новая запись PostgreSQL
                sql = "INSERT INTO category (title) VALUES ('" + val + "')"
                # Параметры запроса
                parameters = [val]
                # Выполнить запрос sql c параметрами parameters
                database.executeSQL(sql, parameters)
                # Поиск 
                # SQL-запрос новая чтения записи
                sql = "SELECT id FROM category WHERE title='" + val + "'"
                # Получить результат запроса из resultSet можно с помощью метода fetchone()   
                result = database.fetchOne(sql)
                if len(result) > 0:                
                    #print("Создана категория '" + val + "'")         
                    return result[0]
        except Exception as exception:
            common.writing_log("Ошибка", "export\t" + str(exception))  
            QMessageBox.critical(self,  "Error",  str(exception))   


