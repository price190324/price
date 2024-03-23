# Импорт библиотек
# Подключаем модуль ODBCL
from asyncio.windows_events import NULL
# Подключаем модуль для SQLite
import sqlite3
# Импорт модуля Psycopg2 в программу
import psycopg2

from PyQt5.QtWidgets import QMessageBox

# Создание соединения с базой данных с указанием конкретной схемы
def get_connection():
    try:
        #conn = sqlite3.connect('scraping.sqlite3')
        #conn = sqlite3.connect('C:/django/2023-2024/price/db.sqlite3')
        #conn = psycopg2.connect(user="customer", password="customer", host="127.0.0.1", port="5432", database="price") 
        conn = psycopg2.connect("postgres://price_admin:49c1nP4FWyzYTAuAXelSTuJ5rGbjGJUZ@dpg-cnv63nn79t8c73d58mc0-a.frankfurt-postgres.render.com/price_8g0n", sslmode="require")

        return conn  
    except Exception as error:
        print(error)
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(str(error))
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()