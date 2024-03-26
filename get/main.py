# Импорт библиотек
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# Поделючаем общий для всего проекта модуль
import common
# Подключаем сообщения
from messages import msg
# Подключаем модуль для работы с БД
import database
# Подключаем другие модули (инициализация, другие окона...)
import month, aquilon, moydom, imperial, export

# Эти библиотеки только для порграммной оболочки
from PyQt5.QtWidgets import * 
import sys

# Создается новый класс MainWindow котрый наследуется от класса QMainWindow. 
class MainWindow(QMainWindow):
    # Класс MainWindow наследуется от класса QWidget. Это означает, что мы вызываем два конструктора:
    # первый для класса MainWindow и второй для родительского класса.
    # Функция super() возвращает родительский объект MainWindow с классом, и мы вызываем его конструктор.    
    def __init__(self):
        super().__init__()       
        # Создание GUI делегируется методу initUI().
        self.initUI()
    def initUI(self):
        try:
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 400, 300)
            # Заголовок окна
            self.setWindowTitle("Scraping")            
            # Кнопки
            self.pushButtonMonth = QPushButton("12 Месяцев")
            self.pushButtonMonth.clicked.connect(lambda: self.open_month())
            self.pushButtonAquilon = QPushButton("Аквилон")
            self.pushButtonAquilon.clicked.connect(lambda: self.open_aquilon())
            self.pushButtonMoydom = QPushButton("Мой Дом")
            self.pushButtonMoydom.clicked.connect(lambda: self.open_moydom())
            self.pushButtonImperial = QPushButton("Империал")
            self.pushButtonImperial.clicked.connect(lambda: self.open_imperial())
            self.pushButtonExport = QPushButton(msg.export_to_django)
            self.pushButtonExport.clicked.connect(lambda: self.open_export())
            self.pushButtonCancel = QPushButton(msg.cancel)
            self.pushButtonCancel.clicked.connect(lambda: self.close())
            # Создаём центральный виджет
            central_widget = QWidget(self)
            # Устанавливаем центральный виджет
            self.setCentralWidget(central_widget)
            # Создаём QGridLayout -  сеточный макет который делит пространство на строки и столбцы. 
            grid_layout = QGridLayout()            
            # Устанавливаем данное размещение в центральный виджет
            central_widget.setLayout(grid_layout)               
            ## Добавляем все визуальные элементы в сетку
            ## int fromRow — номер ряда, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            ## int fromColumn — номер столбца, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            ## int rowSpan — количество рядов, ячейки которых следует объединить для размещения виджета начиная с ряда fromRow.
            ## int columnSpan — количество столбцов, ячейки которых следует объединить для размещения виджета начиная со столбца fromColumn.
            ## Ячейка начинается с первой строки и нулевой колонки, и занимает 1 строку и 4 колонки.            
            grid_layout.addWidget(self.pushButtonMonth, 0, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonAquilon, 1, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonMoydom, 2, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonImperial, 3, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonExport, 4, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonCancel, 5, 0, 1, 1)
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())            
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))

    # Запуск окна
    def open_month(self):
        try:
            # Вызов дочернего окна 
            self.month_window = month.MonthWindow()  
            self.month_window.show() 
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))       
            
    # Запуск окна
    def open_aquilon(self):
        try:
            # Вызов дочернего окна 
            self.aquilon_window = aquilon.AquilonhWindow()  
            self.aquilon_window.show() 
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))  
            
    # Запуск окна
    def open_moydom(self):
        try:
            # Вызов дочернего окна 
            self.moydom_window = moydom.MoydomWindow()  
            self.moydom_window.show() 
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))   
            
    # Запуск окна
    def open_imperial(self):
        try:
            # Вызов дочернего окна 
            self.imperial_window = imperial.ImperialWindow()  
            self.imperial_window.show() 
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))   

    # Запуск окна
    def open_export(self):
        try:
            # Вызов дочернего окна 
            self.imperial_export = export.ExportWindow()  
            self.imperial_export.show() 
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))   

# Главная функция, которая вызывает остальные функции
# Скрипт начинает работать с вызова главной функции main(), соответственно если функцию main()
# закомментировать вызова функций не произойдет. Когда нет никакого управления потоком или
# главной функции, весь программный код выполняется немедленно, во время импортирования модуля.
if __name__ == '__main__':
    try:
        # Инициализация таблиц базы данных (сделать один раз)
        database.init_db() 
        # Создаются объекты application и MainWindow. 
        app = QApplication(sys.argv)
        main_window = MainWindow()
        # Показать окно
        main_window.show()
        # Запускается основной цикл.
        sys.exit(app.exec_())  
        #Запуск с консоли
        #run()
    except Exception as exception:
        #print(exception)
        common.writing_log("Ошибка", "main\t" + str(exception))








