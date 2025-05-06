from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Удаляем стандартную регистрацию модели User в админке,
# чтобы переопределить её с кастомной конфигурацией
admin.site.unregister(User)


# Повторно регистрируем модель User с кастомной настройкой отображения
@admin.register(User)
class CustomUserAdmin(UserAdmin):
     # Указываем, какие поля будут отображаться в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active') #'is_staff', Является ли пользователь админом
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name') # Настраиваем поля, по которым можно искать пользователей
    ordering = ('username',)# Указываем порядок сортировки по умолчанию (по логину)
