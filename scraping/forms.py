from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput, CheckboxInput
from .models import Basket, Salesman, Category, Product, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Продавец
class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['title', 'site',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
            'site': TextInput(attrs={"size":"100"}),            
        }

# Категория товара
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

# Товар
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('url', 'dateb', 'salesman', 'category', 'title', 'description', 'price', 'code', 'photo_url')
        widgets = {
            'url': TextInput(attrs={"size":"100"}),
            'dateb': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'salesman': forms.Select(attrs={'class': 'chosen'}),
            'category': forms.Select(attrs={'class': 'chosen'}),            
            'title': TextInput(attrs={"size":"100"}),
            'description': Textarea(attrs={'cols': 100, 'rows': 5}),    
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'code': TextInput(attrs={"size":"100"}),
            'photo_url': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'salesman': _('salesman'),            
            'category': _('category_title'),            
        }
        # Метод-валидатор для поля dateb
    def clean_dateb(self):        
        if isinstance(self.cleaned_data['dateb'], datetime.date) == True:
            data = self.cleaned_data['dateb']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
