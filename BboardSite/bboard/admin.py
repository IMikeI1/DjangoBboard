from django.contrib import admin
from .models import Addd  # предполагаем, что модель называется Addd

# @admin.register(Addd)
# class AdddAdmin(admin.ModelAdmin):
#     list_display = ('title', 'brand', 'model', 'year', 'author', 'created_at')  # настрой по своему усмотрению
#     list_filter = ('created_at', 'brand', 'year', 'model',)
#     search_fields = ('title', 'content', 'brand', 'model', 'year',)
#     ordering = ('-created_at',)

admin.site.register(Addd)


# Register your models here.
