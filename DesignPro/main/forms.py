from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Application, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Название заявки',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Изображение',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории',
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        labels = {
            'status': 'Статус заявки',
        }