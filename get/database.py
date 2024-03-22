# Импорт библиотек
from pickle import TRUE
import sys
# Подключаем модуль для SQLite
import sqlite3
# Импорт модуля Psycopg2 в программу
import psycopg2
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
# Поделючаем модкль генерации случайных чисел
import random
# Подключаем модуль для создания поделючения к БД
import connector
# Поделючаем общий для всего проекта модуль
import common
# Модуль hashlib реализует общий интерфейс для множества различных безопасных алгоритмов хеширования и дайджеста сообщений
import hashlib
# Модуль os предоставляет множество функций для работы с операционной системой, причём их поведение, как правило, не зависит от ОС, поэтому программы остаются переносимыми. 
import os
import decimal

# Создание базы данных, заполнение ее начальными данными 
def init_db():
    try:
        # Подключение к БД
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        print("База данных подключена")
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()

        ##################
        ##### basket #####
        ##################

        # Проверка наличия таблицы 
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='basket'")
        # Проверка наличия таблицы 
        cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'basket'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица basket уже существует")        
        else:
            print("Создается таблица basket")  
            create_table_query = '''CREATE TABLE basket 
                                (
                                id INTEGER NOT NULL,                                
                                url VARCHAR(255) NOT NULL,
                                dateb datetime NOT NULL,
                                salesman VARCHAR(64) NOT NULL,
                                category VARCHAR(255) NOT NULL,
                                title VARCHAR(255) NOT NULL,
                                description text NOT NULL,
                                price decimal NOT NULL,
                                code VARCHAR(255) NOT NULL,
                                photo_url VARCHAR(255) NOT NULL,                                
                                PRIMARY KEY("id" AUTOINCREMENT)
                                );'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица basket создана")       
            
        ####################
        ##### salesman #####
        ####################

        # Проверка наличия таблицы 
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='salesman'")
        # Проверка наличия таблицы 
        cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'salesman'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица salesman уже существует")        
        else:
            print("Создается таблица salesman")  
            create_table_query = '''CREATE TABLE salesman 
                (
                id INTEGER NOT NULL,                                
                title VARCHAR(255) NOT NULL UNIQUE,
                site VARCHAR(255),
                PRIMARY KEY("id" AUTOINCREMENT)
                );'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица salesman создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM salesman"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
            
        ####################
        ##### category #####
        ####################

        # Проверка наличия таблицы 
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='category'")
        # Проверка наличия таблицы 
        cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'category'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица category уже существует")        
        else:
            print("Создается таблица category")  
            create_table_query = '''CREATE TABLE category 
                (
                id INTEGER NOT NULL,                                
                title VARCHAR(255) NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT)
                );'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица category создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM category"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
       
        ###################
        ##### product #####
        ###################

        # Проверка наличия таблицы 
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product'")
        # Проверка наличия таблицы 
        cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'product'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица product уже существует")        
        else:
            print("Создается таблица product")  
            create_table_query = '''CREATE TABLE "product" 
            (
	            id	integer NOT NULL,
	            url VARCHAR(255) NOT NULL,
                dateb datetime NOT NULL,
                salesman_id bigint NOT NULL,	            
                category_id bigint NOT NULL,	            
                title VARCHAR(255) NOT NULL,
                description text NOT NULL,
                price decimal NOT NULL,
                code VARCHAR(255) NOT NULL,
                photo_url VARCHAR(255) NOT NULL,                                
	            PRIMARY KEY("id" AUTOINCREMENT),
	            FOREIGN KEY("salesman_id") REFERENCES "salesman"("id") DEFERRABLE INITIALLY DEFERRED,
	            FOREIGN KEY("category_id") REFERENCES "category"("id") DEFERRABLE INITIALLY DEFERRED
            );'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица product создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM product"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)

        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print("База данных отключена")        
    except Exception as error:
        print(error)
        
#######################
# Экспорт данных в БД #
#######################   
# Экспорт данных в БД
# header - Заголовок таблицы, data данные (список списков), название файла
def export_to_database(data):
    try:
        common.writing_log("Информация", "Экспорт в БД")
        # SQL-запрос на добавление записи
        sql = "INSERT INTO basket (url, dateb, salesman, category, title, description, price, code, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        for d in data:
            try:
                # Исходные данные
                print(str(d))            
                # Параметры запроса
                parameters = []
                # Заполнить параметры
                parameters.append(d[0])
                #print(parameters[0])
                # dateb
                parameters.append(d[1])
                #print(parameters[1])
                # salesman
                parameters.append(d[2])
                #print(parameters[2])
                # category
                parameters.append(d[3])
                #print(parameters[3])
                # title
                parameters.append(d[4])
                #print(parameters[4])
                # description
                parameters.append(d[5])
                #print(parameters[5])
                # price
                price=""
                for i in d[6]:
                    if i.isdigit(): price+=i 
                parameters.append(price)
                #parameters.append(price)
                #print(parameters[6])
                # code
                parameters.append(d[7])
                #print(parameters[7])
                # photo_url
                parameters.append(d[8])
                #print(parameters[8])
                print(str(parameters))
                # Выполнить запрос sql c параметрами parameters
                executeSQL(sql, parameters)
            except Exception as exception:
                print(exception)
                common.writing_log("Ошибка", "export_to_database\t" + str(exception))
        common.writing_log("Информация", "Экспорт в БД завершен")
    except Exception as exception:
        print(exception)
        common.writing_log("Ошибка", "export_to_database\t" + str(exception))
     
###################
# Общие процедуры #
###################

# Выполнение параметрического запроса SQL (без возврата набора данных)
def executeSQL(sql, parameters):
    try:            
        # SQL-запрос 
        #print(sql)
        # Параметры запроса
        #print(parameters)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()            
        # Включить ограничения FOREIGN KEY 
        #cursor.execute("PRAGMA foreign_keys=ON")                  
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        cursor.execute(sql, parameters)
        # Применить изменения
        conn.commit()     
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print(sql)
        return 1
    except Exception as error:
        print(error)
        return -1
    
# Возврат данных из таблицы БД (множество записей)
def fetchAll(sql):
    try:
        # print(sql)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        rows = cursor.fetchall()            
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return rows
    except Exception as error:
        print(error)

# Возврат данных из таблицы БД (одна запись)
def fetchOne(sql):
    try:
        #print(sql)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        result = cursor.fetchone()
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return result
    except Exception as error:
        print(error)
