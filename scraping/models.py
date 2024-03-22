from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django import forms

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Корзина 
class Basket(models.Model):
    url = models.CharField(_('url'), max_length=255)
    dateb = models.DateTimeField(_('dateb'))
    salesman = models.CharField(_('salesman'), max_length=64)
    category = models.CharField(_('category'), max_length=255)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    code = models.CharField(_('code'), max_length=255)
    photo_url = models.CharField(_('photo_url'), max_length=255)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'basket'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dateb']),
        ]
        # Сортировка по умолчанию
        ordering = ['dateb']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}: {}".format(self.category, self.title, self.price)

# Продавец
class Salesman(models.Model):
    title = models.CharField(_('salesman_title'), max_length=255, unique=True)
    site = models.CharField(_('site'), max_length=255, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'salesman'
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}".format(self.title)

# Категория товара
class Category(models.Model):
    title = models.CharField(_('category_title'), max_length=255, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}".format(self.title)

# Товар 
class Product(models.Model):
    url = models.CharField(_('url'), max_length=255)
    dateb = models.DateTimeField(_('dateb'))
    salesman = models.ForeignKey(Salesman, related_name='product_salesman', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    title = models.CharField(_('product_title'), max_length=255)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    code = models.CharField(_('code'), max_length=255)
    photo_url = models.CharField(_('photo_url'), max_length=255)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'product'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dateb']),
            models.Index(fields=['salesman']),
            models.Index(fields=['category']),
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['dateb']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}: {}".format(self.category, self.title, self.price)

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
