from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Basket, Salesman, Category, Product, News
# Подключение форм
from .forms import SalesmanForm, CategoryForm, ProductForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        news14 = News.objects.all().order_by('-daten')[0:4]
        return render(request, "index.html", {"news14": news14, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Отчеты
@login_required
@group_required("Managers")
def report_index(request):
    try:        
        return render(request, "report/index.html")        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 1
@login_required
@group_required("Managers")
def report_1(request):
    try:
        report = Product.objects.raw("""
SELECT 1 as id, product.salesman_id, salesman.title AS salesman_title, product.category_id, category.title AS category_title, product.title,
(SELECT price FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title AND p.dateb=(SELECT MAX(dateb) FROM product d WHERE p.salesman_id=d.salesman_id AND p.category_id=d.category_id AND p.title=d.title) LIMIT 1) AS current_price,
(SELECT MAX(price) FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title) AS max_price,
(SELECT MIN(price) FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title) AS min_price,
(SELECT AVG(price) FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title) AS avg_price
FROM product LEFT JOIN salesman ON product.salesman_id = salesman.id
LEFT JOIN category ON product.category_id = category.id
GROUP BY product.salesman_id, salesman.title, product.category_id, category.title, product.title
""")
        return render(request, "report/report_1.html", {"report": report,})                
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 2
@login_required
@group_required("Managers")
def report_2(request):
    try:
        report_max10 = Product.objects.raw("""
SELECT 1 as id, salesman.title AS salesman_title, category.title AS category_title, product.title, product.price
FROM product LEFT JOIN salesman ON product.salesman_id = salesman.id
LEFT JOIN category ON product.category_id = category.id
WHERE product.price>0 AND product.dateb=(SELECT MAX(dateb) FROM product p WHERE product.salesman_id=p.salesman_id AND product.category_id=p.category_id AND product.title=p.title)
GROUP BY salesman.title, category.title, product.title, product.price
ORDER BY product.price DESC
LIMIT 10
""")
        report_min10 = Product.objects.raw("""
SELECT 1 as id, salesman.title AS salesman_title, category.title AS category_title, product.title, product.price
FROM product LEFT JOIN salesman ON product.salesman_id = salesman.id
LEFT JOIN category ON product.category_id = category.id
WHERE product.price>0 AND product.dateb=(SELECT MAX(dateb) FROM product p WHERE product.salesman_id=p.salesman_id AND product.category_id=p.category_id AND product.title=p.title)
GROUP BY salesman.title, category.title, product.title, product.price
ORDER BY product.price 
LIMIT 10
""")
        return render(request, "report/report_2.html", {"report_max10": report_max10, "report_min10": report_min10,})         
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 3
@login_required
@group_required("Managers")
def report_3(request):
    try:
        report = Product.objects.raw("""
SELECT 1 as id, product.salesman_id, salesman.title AS salesman_title, product.category_id, category.title AS category_title, product.title,
(SELECT price FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title AND p.dateb=(SELECT MAX(dateb) FROM product d WHERE p.salesman_id=d.salesman_id AND p.category_id=d.category_id AND p.title=d.title) LIMIT 1) AS current_price,
COALESCE (
(SELECT price FROM product p 
WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title 
ORDER BY p.dateb DESC
LIMIT 1 OFFSET 1
), 0) as prev_price,
CASE  
	WHEN 
		COALESCE (
		(SELECT price FROM product p 
		WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title 
		ORDER BY p.dateb DESC
		LIMIT 1 OFFSET 1
		), 0) <> 0
	THEN 
		CAST(
        (SELECT price FROM product p WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title AND p.dateb=(SELECT MAX(dateb) FROM product d WHERE p.salesman_id=d.salesman_id AND p.category_id=d.category_id AND p.title=d.title) LIMIT 1)*100 
        AS REAL)
        /
        CAST(
        COALESCE (
        (SELECT price FROM product p 
        WHERE p.salesman_id=product.salesman_id AND p.category_id=product.category_id AND p.title=product.title 
        ORDER BY p.dateb DESC
        LIMIT 1 OFFSET 1
        ), 0)
        AS REAL)
        -100
	ELSE null
END 
AS proc
FROM product LEFT JOIN salesman ON product.salesman_id = salesman.id
LEFT JOIN category ON product.category_id = category.id
GROUP BY product.salesman_id, salesman.title, product.category_id, category.title, product.title
ORDER BY salesman.title,category.title, product.title
""")
        return render(request, "report/report_3.html", {"report": report,})     
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def salesman_index(request):
    try:
        salesman = Salesman.objects.all().order_by('title')
        return render(request, "salesman/index.html", {"salesman": salesman,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def salesman_create(request):
    try:
        if request.method == "POST":
            salesman = Salesman()
            salesman.title = request.POST.get("title")
            salesman.site = request.POST.get("site")
            salesmanform = SalesmanForm(request.POST)
            if salesmanform.is_valid():
                salesman.save()
                return HttpResponseRedirect(reverse('salesman_index'))
            else:
                return render(request, "salesman/create.html", {"form": salesmanform})
        else:        
            salesmanform = SalesmanForm()
            return render(request, "salesman/create.html", {"form": salesmanform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def salesman_edit(request, id):
    try:
        salesman = Salesman.objects.get(id=id)
        if request.method == "POST":
            salesman.title = request.POST.get("title")
            salesman.site = request.POST.get("site")
            salesmanform = SalesmanForm(request.POST)
            if salesmanform.is_valid():
                salesman.save()
                return HttpResponseRedirect(reverse('salesman_index'))
            else:
                return render(request, "salesman/edit.html", {"form": salesmanform})
        else:
            # Загрузка начальных данных
            salesmanform = SalesmanForm(initial={'title': salesman.title, 'site': salesman.site, })
            return render(request, "salesman/edit.html", {"form": salesmanform})
    except Salesman.DoesNotExist:
        return HttpResponseNotFound("<h2>Salesman not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def salesman_delete(request, id):
    try:
        salesman = Salesman.objects.get(id=id)
        salesman.delete()
        return HttpResponseRedirect(reverse('salesman_index'))
    except Salesman.DoesNotExist:
        return HttpResponseNotFound("<h2>Salesman not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def salesman_read(request, id):
    try:
        salesman = Salesman.objects.get(id=id) 
        return render(request, "salesman/read.html", {"salesman": salesman})
    except Salesman.DoesNotExist:
        return HttpResponseNotFound("<h2>Salesman not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def product_index(request):
    try:
        product = Product.objects.all().order_by('category__title', 'title', 'dateb')
        return render(request, "product/index.html", {"product": product,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
#@login_required
#@group_required("Managers")
def product_list(request):
    try:
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59).strftime('%Y-%m-%d') 
        salesman = Salesman.objects.all().order_by('title')
        category = Category.objects.all().order_by('title')
        product = Product.objects.all().order_by('category__title', 'title', 'dateb')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                #print(finish_date)
                product = product.filter(dateb__range=[start_date, finish_date])
                finish_date = request.POST.get("finish_date")
                # Поиск по категории
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    category_query = Category.objects.filter(title = selected_item_category).only('id').all()
                    product = product.filter(category_id__in = category_query)
                # Поиск по продавцу
                selected_item_salesman = request.POST.get('item_salesman')
                #print(selected_item_salesman)
                if selected_item_salesman != '-----':
                    salesman_query = Salesman.objects.filter(title = selected_item_salesman).only('id').all()
                    product = product.filter(salesman_id__in = salesman_query)      
                # Поиск по названию 
                title_search = request.POST.get("title_search")
                #print(title_search)                
                if title_search != '':
                    product = product.filter(title__contains = title_search)                
                 
                return render(request, "product/list.html", {"product": product, "category": category, "selected_item_category": selected_item_category,  "salesman": salesman, "selected_item_salesman": selected_item_salesman, "start_date": start_date, "finish_date": finish_date, "title_search": title_search })    
            else:          
                return render(request, "product/list.html", {"product": product, "category": category, "salesman": salesman, "start_date": start_date, "finish_date": finish_date })
        else:
            return render(request, "product/list.html", {"product": product, "category": category, "salesman": salesman, "start_date": start_date, "finish_date": finish_date })           
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def product_create(request):
    try:
        if request.method == "POST":
            product = Product()
            product.url = request.POST.get("url")
            product.dateb = request.POST.get("dateb")
            product.salesman = Salesman.objects.filter(id=request.POST.get("salesman")).first()
            product.category = Category.objects.filter(id=request.POST.get("category")).first()
            product.title = request.POST.get("title")
            product.description = request.POST.get("description")
            product.price = request.POST.get("price")
            product.code = request.POST.get("code")
            product.photo_url = request.POST.get("photo_url")
            productform = ProductForm(request.POST)
            if productform.is_valid():
                product.save()
                return HttpResponseRedirect(reverse('product_index'))
            else:
                return render(request, "product/create.html", {"form": productform})
        else:        
            productform = ProductForm()
            return render(request, "product/create.html", {"form": productform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def product_edit(request, id):
    try:
        product = Product.objects.get(id=id)
        if request.method == "POST":
            product.url = request.POST.get("url")
            product.dateb = request.POST.get("dateb")
            product.salesman = Salesman.objects.filter(id=request.POST.get("salesman")).first()
            product.category = Category.objects.filter(id=request.POST.get("category")).first()
            product.title = request.POST.get("title")
            product.description = request.POST.get("description")
            product.price = request.POST.get("price")
            product.code = request.POST.get("code")
            product.photo_url = request.POST.get("photo_url")
            productform = ProductForm(request.POST)
            if productform.is_valid():
                product.save()
                return HttpResponseRedirect(reverse('product_index'))
            else:
                return render(request, "product/edit.html", {"form": productform})
        else:
            # Загрузка начальных данных
            productform = ProductForm(initial={'url': product.url, 'dateb': product.dateb, 'salesman': product.salesman, 'category': product.category, 'title': product.title, 'description': product.description, 'price': product.price, 'code': product.code, 'photo_url': product.photo_url, })
            return render(request, "product/edit.html", {"form": productform})
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Product not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def product_delete(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return HttpResponseRedirect(reverse('product_index'))
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Product not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def product_read(request, id):
    try:
        product = Product.objects.get(id=id) 
        return render(request, "product/read.html", {"product": product})
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Product not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
            return render(request, "news/list.html", {"news": news}) 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")

