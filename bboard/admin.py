from django.contrib import admin
from .models import Bboard

# Регистрируем модель Bboard в административной панели с кастомной конфигурацией
@admin.register(Bboard)
class BboardAdmin(admin.ModelAdmin):
    # Указываем, какие поля отображаются в списке объявлений в админке
    list_display = ('title', 'user', 'created_at', 'year', 'mileage', 'condition', 'modification', 'engine_volume', 'engine_type', 'transmission', 'drive', 'equipment', 'body_type', 'color', 'steering_wheel', 'price', 'price_arenda_car')
    list_filter = ('created_at', 'user', 'year', 'condition', 'engine_type', 'transmission', 'drive', 'body_type', 'color', 'steering_wheel')
    search_fields = ('title', 'content', 'user__username') # Поля, по которым можно искать через строку поиска
    # Поля, которые будут только для чтения (нельзя изменить вручную)
    readonly_fields = ('created_at',)
