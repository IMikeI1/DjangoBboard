from django.urls import path
from . import views

# Пространство имён приложения для использования в шаблонах и ссылках
app_name = 'users'

# Список маршрутов URL данного приложения
urlpatterns = [
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/done/', views.register_done, name='register_done'),
]
