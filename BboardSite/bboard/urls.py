from django.urls import path
from .views import (
    index, about, user_info, add_addd, edit_addd,
 delete_addd, search_addd, filter_addd, user_addd, read_addd, contact
)

app_name = 'bboard'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('user-info/<int:user_id>/', user_info, name='user_info'),
    path('addd/add/', add_addd, name='add_addd'),
    # path('addd/<int:addd_id>/', detail_addd, name='addd_detail'),
    path('addd/edit/<slug:slug>/', edit_addd, name='addd_edit'),
    path('addd/delete/<int:addd_id>/', delete_addd, name='addd_delete'),
    path('user-info/<int:user_id>/', user_addd, name='user_addd'),
    path('addd/<slug:slug>/', read_addd, name='read_addd'),
    # path('addd/edit/<slug:slug>/', update_addd, name='update_addd'),
    path('search/', search_addd, name='search_addd'),
    path('filter/', filter_addd, name='filter_addd'),
]
