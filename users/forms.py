from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput

# Кастомизированная форма регистрации пользователя, расширяющая стандартную UserCreationForm
class RegistrationForm(UserCreationForm):
    # Поле для ввода логина с пользовательским сообщением об ошибке
    username = forms.CharField(label="Логин",
                               error_messages= {
                                   "required": "Пожалуйста, введите логин"
                               } )
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Эл. почта")
    password1 = forms.CharField(label="Пароль", widget=PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль",
                                widget=forms.PasswordInput,
                                error_messages= {
                                    "required": "Пожалуйста, введите пароль"
                                })

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",) # Указываем, какие поля пользователь может редактировать
        
# Форма редактирования профиля пользователя

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        # Настройка отображения виджетов (CSS, readonly для username)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }