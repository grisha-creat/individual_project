# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Придумайте логин'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Улучшаем тексты подсказок
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'

class UserUpdateForm(forms.ModelForm):
    """Форма обновления данных пользователя"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля"""
    class Meta:
        model = Profile
        fields = [ 'location', 'birth_date', 'avatar', 
                 'email_notifications', 'dark_mode']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }