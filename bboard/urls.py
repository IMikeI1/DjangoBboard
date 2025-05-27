from django.urls import path
from . import views
from .views import about, contacts
from django.contrib.auth.views import LogoutView
from django.db import IntegrityError
from bboard.views import filter_bboard

app_name = 'bboard'

# Основной список маршрутов
urlpatterns = [
    path('filter/', filter_bboard, name='filter'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('add/', views.add_bboard, name='add'),
    path('<slug:slug>/delete/', views.delete_bboard, name='delete'), # Просмотр одного объявления по его slug
    path('<slug:slug>/edit/', views.edit_bboard, name='edit'),
    path('<slug:slug>/', views.detail_bboard, name='detail'), # Удаление объявления по его slug
]
