from django.urls import path
from .views import (about, contacts, index,
                    add_bboard, delete_bboard, edit_bboard, detail_bboard, filter_bboard)
from django.contrib.auth.views import LogoutView

app_name = 'bboard'

urlpatterns = [
    path('', index, name='index'),
    path('filter/', filter_bboard, name='filter'),
    path('search/', index, name='search-form'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', add_bboard, name='add'),
    path('<slug:slug>/', detail_bboard, name='detail'),
    path('<slug:slug>/edit/', edit_bboard, name='edit'),
    path('<slug:slug>/delete/', delete_bboard, name='delete'),
]
