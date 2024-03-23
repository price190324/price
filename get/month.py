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
# Заголовок в Excel
HEADER = ["URL (Карточка)", "Дата", "Продавец", "Категория", "Название", "Описание", "Цена", "Артикул", "Фотография"]
# Функция отладки
DEBUG = False
#DEBUG = True
# Элемент класса Firefox, Chrome, Edge.
#driver = webdriver.Firefox()
driver = webdriver.Chrome()
#driver = None
# Подключаем модуль для работы с БД
import database
# Поделючаем общий для всего проекта модуль
import common
# Поделючаем модуль для работы в Excel
import excel
# Подключаем сообщения
from messages import msg
# Эти библиотеки только для порграммной оболочки
from PyQt5.QtWidgets import * 

# Общие "глобальные" переменные (со значениями по умолчанию), здесь не меняются, меняются в set_variables() для консольного или в главной форме для оконного
def glob():
    # start_url основной страницы (не менять!)
    start_url="https://12.kz/categories/smesi-rastvory"
    # Стартовая страница (не менять!)
    start_page = 1
    # Финишная страница (не менять!)
    finish_page = 5
    # Пауза для загрузки страницы с данными (не менять!)
    pause_data_page = 3
    # Пауза для загрузки страницы (не менять!)
    pause_load_page = 5
    # Пауза для переключения между страницами (не менять!)
    pause_flipping = 1
    # Список для экспорта в Excel (не менять!)
    data = []      

# Получение дополнительной информации по ссылке url
def details(url):
    try:       
        # Для контроля
        common.writing_log("Информация", "Старт парсинга " + str(url))
        # Метод driver.get перенаправляет к странице URL в параметре.
        # WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), 
        # прежде чем передать контроль вашему тесту или скрипту. 
        driver.get(url)
        # Задержка по времени т.к. это всплвающе окно и ему надо отработать
        common.writing_log("Информация", "Старт паузы для карточки")
        sleep(glob.pause_data_page)
        #common.writing_log("Информация", "Продолжить после паузы")
        row = []    # Одна запись
        row.append(url)     # Добавить url для контроля
        print(url)
        # Дата
        row.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # Продавец
        row.append("12 месяцев")
        # Поиск информации
        try:
            # Категория /html/body/div[5]/main/div/div[3]/div[2]/div[5]/a/span
            #kategoriya = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[2]/div[5]/a/span")
            kategoriya = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[2]/div[5]/a/span")
            row.append(kategoriya.text)
            print(kategoriya.text)
        except Exception as exception:
            row.append("kategoriya")
            #kategoriya = "kategoriya"
            print(exception)
        try:
            # Название/html/body/div[5]/main/div/div[3]/div[2]/div[6]/span
            #nazvanie = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[2]/div[6]/span")
            #row.append(nazvanie.text)
            nazvanie = driver.find_element(By.TAG_NAME, "h1")  
            row.append(nazvanie.text)
            print(nazvanie.text)
        except Exception as exception: 
            row.append("nazvanie")
            #nazvanie = "nazvanie"
            print(exception)
        try:
            #Описание /html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[2]/div/div/div[1]
            description = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[2]/div/div/div[1]")
            #description = driver.find_element(By.CSS_SELECTOR, "tab-content details-tabs-deacription clear tab-content-active")
            if description != None:
                row.append(description.text)
                print(description.text)
            else:
                row.append("description")
                #description = "description"
        except Exception as exception: 
            row.append("description")
            #description = "description"
            print(exception)
        try:
            #Цена /html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[7]/div[1]/div[2]/div/div[1]/div/div/div[1]
            #cena = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[7]/div[1]/div[2]/div/div[1]/div/div/div[1]")
            cena = driver.find_element(By.CLASS_NAME, "price-number")
            if cena != None:
                row.append(cena.text)
                print(cena.text)
            else:
                row.append("cena")
                #cena = "cena"
        except Exception as exception: 
            row.append("cena")
            #cena = "cena"
            print(exception)
        try:
            # Артикул /html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]
            artikul = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]")
            #artikul = driver.find_element(By.CLASS_NAME, "details-row details-sku")
            if artikul != None:
                row.append(artikul.text)
                print(artikul.text)
            else:
                row.append("artikul")
                #artikul = "artikul"
        except Exception as exception: 
            row.append("artikul")
            #artikul = "artikul"
            print(exception)
        try:
            # Фотография /html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[1]/div/figure/a/img
            img = driver.find_element(By.XPATH, "/html/body/div[5]/main/div/div[3]/div[3]/div[1]/div[1]/div[1]/div/figure/a/img")
            row.append(img.get_attribute("src"))
            print(img.get_attribute("src"))
        except Exception as exception: 
            row.append("img")
            #img = "img"
            print(exception)
        #exit(0)
            
        ##table = driver.find_elements(By.CLASS_NAME, "table table-striped")
        ##table = driver.find_elements(By.XPATH, "/html/body/main/div[4]/div[2]/div[3]/div[3]/div[2]/div/table")
        #tds = driver.find_elements(By.TAG_NAME, "td")
        #for td in tds:
        #    row.append(td.text)        
        common.writing_log("Данные", str(row))
        # Возврат на предыдущую страницу
        driver.back()
        common.writing_log("Информация", "Возврат на предыдущую страницу")
        return row
    except Exception as exception:        
        print(exception)
        #row = [] 
        common.writing_log("Ошибка", "details\t" + str(exception))
        

def parsing(url):
    try:
        # Метод driver.get перенаправляет к странице URL в параметре.
        # WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), 
        # прежде чем передать контроль вашему тесту или скрипту. 
        driver.get(url)
        # Задержка по времени для загрузки страницы
        common.writing_log("Информация", "Старт паузы для загрузки страницы")
        sleep(glob.pause_load_page)
        #common.writing_log("Информация", "Продолжить после паузы")
        # Поиск ссылок
        links = driver.find_elements(By.TAG_NAME, "a")
        # Набор ссылок на карточки, пример ссылки на карточки https://12.kz/products/0040142
        my_links = []
        for link in links:
            if str(link.get_attribute('href'))[0:23]=="https://12.kz/products/":
                if my_links.count(str(link.get_attribute('href')))==0:
                    my_links.append(str(link.get_attribute('href')))
                    print(link.get_attribute('href'))            
        #print(my_links)
        # Перебор всех ссылок
        for i in range(len(my_links)):     
            try:
                #print(my_links[i])
                glob.data.append(details(my_links[i]))
                if (len(glob.data) > 0):
                    common.writing_log("Информация", "Создана запись № " + str(len(glob.data)))
                # Сохранить каждую 1000 записей
                if (len(glob.data) % 1000 == 0):
                    # Вызов: заголовок таблицы, данные, название файла
                    current_date_time = datetime.now().strftime('%Y%m%d%H%M%S')
                    excel.export_to_excel(HEADER, glob.data, "month12.kz." + str(current_date_time) + ".xls")
                # Если это отладка достаточно будет по три карточки
                if DEBUG == True:
                    if (len(glob.data) % 3 == 0):
                        break # Счетчик на время тестирования
            except Exception as exception:
                #print(exception)
                common.writing_log("Ошибка", "parsing for link in links\t" + str(exception))
        # В завершение, окно браузера закрывается. Вы можете также вызывать метод quit вместо close. 
        # Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. 
        #driver.quit()
    except Exception as exception:
        print(exception)
        common.writing_log("Ошибка", "parsing\t" + str(exception))

# Запуск процесса
def run():    
    try:
        # Установить переменные (используется в консольном приложении, в оконном получается из формы)
        #set_variables()
        # Время старта
        start = time.time()
        # Записать праметры
        common.writing_log("Информация", "Старт")
        common.writing_log("Информация", "URL основной страницы " + str(glob.start_url))
        common.writing_log("Информация", "Стартовая страница " + str(glob.start_page))
        common.writing_log("Информация", "Финишная страница " + str(glob.finish_page))
        common.writing_log("Информация", "Пауза для загрузки страницы " + str(glob.pause_load_page))
        common.writing_log("Информация", "Пауза для переключения между страницами " + str(glob.pause_flipping))
        common.writing_log("Информация", "Пауза для загрузки страницы с данными " + str(glob.pause_data_page))
        common.writing_log("Информация", "DEBUG " + str(DEBUG))
        # Метод driver.get перенаправляет к странице URL в параметре.
        # WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), 
        # прежде чем передать контроль вашему тесту или скрипту. 
        driver.get(glob.start_url)
        # Задержка по времени для загрузки страницы
        common.writing_log("Информация", "Старт паузы для первоначальной загрузки страницы")
        sleep(glob.pause_load_page)
        #common.writing_log("Информация", "Продолжить после паузы")                
        # Собственно цикл перебора страниц
        for i in range(glob.finish_page-glob.start_page + 1):             
            # Нажатие кнопки "Next" для перехода на следующую страницу
            try:
                # Парсинг страницы
                common.writing_log("Информация", "Переход на страницу " + str(glob.start_url + "?page=" + str(glob.start_page + i)))                
                parsing(glob.start_url + "?page=" + str(glob.start_page + i) )      
            except Exception as exception:
                print(exception)
                common.writing_log("Ошибка", "main for i in range(glob.finish_page-glob.start_page)\t" +  str(exception))
        # Экспорт в Excel
        # Вызов: заголовок таблицы, данные, название файла
        current_date_time = datetime.now().strftime('%Y%m%d%H%M%S')
        excel.export_to_excel(HEADER, glob.data, "month12.kz.range(" +str(glob.start_page) + "-" + str(glob.finish_page) + ")_" +str(current_date_time) + ".xls")
        # Экспорт в БД
        database.export_to_database(glob.data)
        # Затраченное время
        common.writing_log("Информация", "Затраченное время:" + str(time.time() - start) + " секунд")
        # В завершение, окно браузера закрывается. Вы можете также вызывать метод quit вместо close. 
        # Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. 
        driver.quit()
        exit(0)
    except Exception as exception:
        #print(exception)
        common.writing_log("Ошибка", "main\t" + str(exception))

# Создается новый класс MonthWindow котрый наследуется от класса QMainWindow. 
class MonthWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 600, 400)
            # Заголовок окна
            self.setWindowTitle("month12.kz")
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            #self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))            
            # GroupBox настроек
            self.groupBox_settings = QGroupBox("Settings")
            #self.groupBox_settings.setMaximumHeight(200)
            self.grid_layout_filter = QGridLayout()
            self.groupBox_settings.setLayout(self.grid_layout_filter)
            # Метки
            self.label_start_url = QLabel("URL основной страницы")
            self.label_start_page = QLabel("Стартовая страница")
            self.label_finish_page = QLabel("Финишная страница") 
            self.label_pause_data_page = QLabel("Пауза для загрузки страницы с данными")
            self.label_pause_load_page = QLabel("Пауза для загрузки страницы")
            self.label_pause_flipping = QLabel("Пауза для переключения между страницами")
            # Поля ввода данных
            self.lineEdit_start_url = QLineEdit(self)
            self.lineEdit_start_url.setText("https://12.kz/categories/smesi-rastvory")
            self.spinBox_start_page = QSpinBox(self)
            self.spinBox_start_page.setMinimum(1)
            self.spinBox_start_page.setMaximum(100000)
            self.spinBox_start_page.setFixedWidth(100)
            self.spinBox_start_page.setValue(1)
            self.spinBox_finish_page = QSpinBox(self)
            self.spinBox_finish_page.setMinimum(1)
            self.spinBox_finish_page.setMaximum(100000)
            self.spinBox_finish_page.setFixedWidth(100)
            self.spinBox_finish_page.setValue(5)
            self.doubleSpinBox_pause_data_page = QDoubleSpinBox(self)
            self.doubleSpinBox_pause_data_page.setMinimum(0.1)
            self.doubleSpinBox_pause_data_page.setMaximum(60)
            self.doubleSpinBox_pause_data_page.setDecimals(1)
            self.doubleSpinBox_pause_data_page.setSingleStep(0.1) 
            self.doubleSpinBox_pause_data_page.setFixedWidth(100)
            self.doubleSpinBox_pause_data_page.setValue(0.5)
            self.doubleSpinBox_pause_load_page = QDoubleSpinBox(self)
            self.doubleSpinBox_pause_load_page.setMinimum(0.1)
            self.doubleSpinBox_pause_load_page.setMaximum(60)
            self.doubleSpinBox_pause_load_page.setDecimals(1)
            self.doubleSpinBox_pause_load_page.setSingleStep(0.1) 
            self.doubleSpinBox_pause_load_page.setFixedWidth(100)
            self.doubleSpinBox_pause_load_page.setValue(1.0)
            self.doubleSpinBox_pause_flipping = QDoubleSpinBox(self)
            self.doubleSpinBox_pause_flipping.setMinimum(0.1)
            self.doubleSpinBox_pause_flipping.setMaximum(60)
            self.doubleSpinBox_pause_flipping.setDecimals(1)
            self.doubleSpinBox_pause_flipping.setSingleStep(0.1) 
            self.doubleSpinBox_pause_flipping.setFixedWidth(100)
            self.doubleSpinBox_pause_flipping.setValue(0.5)
            # Добавляем визуальные элементы в сетку
            self.grid_layout_filter.addWidget(self.label_start_url, 0, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_start_url, 0, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_start_page, 1, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.spinBox_start_page, 1, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_finish_page, 2, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.spinBox_finish_page, 2, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_pause_data_page, 3, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.doubleSpinBox_pause_data_page, 3, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_pause_load_page, 4, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.doubleSpinBox_pause_load_page, 4, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_pause_flipping, 5, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.doubleSpinBox_pause_flipping, 5, 1, 1, 1)
            # Кнопки
            self.pushButtonFilter = QPushButton("Выполнить")
            self.pushButtonFilter.clicked.connect(lambda: self.set_var_and_run())
            self.pushButtonCancel = QPushButton("Отмена")
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
            grid_layout.addWidget(self.groupBox_settings, 0, 0, 1, 2)
            grid_layout.addWidget(self.pushButtonFilter, 1, 0, 1, 1)
            grid_layout.addWidget(self.pushButtonCancel, 1, 1, 1, 1)
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())     
        except Exception as error:
            print(error)
            common.writing_log("Ошибка", "main\t" + str(error))
            QMessageBox.critical(self,  "Error",  str(error))  
            
    # Установка настроек и запуск процесса
    def set_var_and_run(self):
        try:            
            # Установка настроек
            glob.start_url = self.lineEdit_start_url.text()
            glob.start_page = self.spinBox_start_page.value()
            glob.finish_page = self.spinBox_finish_page.value()
            glob.pause_load_page = self.doubleSpinBox_pause_load_page.value()
            glob.pause_flipping = self.doubleSpinBox_pause_flipping.value()
            glob.pause_data_page = self.doubleSpinBox_pause_data_page.value()
            glob.data = []    
            #driver = webdriver.Chrome()
            # Запуск процесса
            run()
        except Exception as exception:
            #print(exception)
            common.writing_log("Ошибка", "main\t" + str(exception))  

   





