"""
URL configuration for price project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from scraping import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('report/index/', views.report_index, name='report_index'),
    #path('growth_decline-chart/', views.growth_decline_chart, name='growth_decline-chart'),
    path('report/report_1/', views.report_1, name='report_1'),
    path('report/report_2/', views.report_2, name='report_2'),
    path('report/report_3/', views.report_3, name='report_3'),
    
    #path('basket/index/', views.basket_index, name='basket_index'),
    #path('basket/create/', views.basket_create, name='basket_create'),
    #path('basket/edit/<int:id>/', views.basket_edit, name='basket_edit'),
    #path('basket/delete/<int:id>/', views.basket_delete, name='basket_delete'),
    #path('basket/read/<int:id>/', views.basket_read, name='basket_read'),

    path('salesman/index/', views.salesman_index, name='salesman_index'),
    path('salesman/create/', views.salesman_create, name='salesman_create'),
    path('salesman/edit/<int:id>/', views.salesman_edit, name='salesman_edit'),
    path('salesman/delete/<int:id>/', views.salesman_delete, name='salesman_delete'),
    path('salesman/read/<int:id>/', views.salesman_read, name='salesman_read'),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),

    path('product/index/', views.product_index, name='product_index'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:id>/', views.product_delete, name='product_delete'),
    path('product/read/<int:id>/', views.product_read, name='product_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

