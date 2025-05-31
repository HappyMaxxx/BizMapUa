from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'id_username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and not self.is_valid():
            self.data = self.data.copy() 
            self.data['password1'] = ''  
            self.data['password2'] = '' 


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class BuisnesCreationForm(forms.ModelForm):
    class Meta:
        model = Businesse
        fields = ['region', 'city', 'name', 'description', 'email', 'phone', 'insta', 'category', 'tags']
        
        labels = {
            'region': 'Регіон',
            'city': 'Місто',
            'name': 'Назва',
            'description': 'Опис',
            'email': 'Електронна пошта',
            'phone': 'Телефон',
            'insta': 'Інстаграм',
            'category': 'Категорія',
            'tags': 'Теги'
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'insta': forms.TextInput(attrs={'class': 'form-control'}),
        }

        required = {
            'tags': False,
            'insta': False,
        }