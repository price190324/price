from django.contrib import admin

from .models import Basket, Salesman, Category, Product, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Basket)
admin.site.register(Salesman)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(News)



