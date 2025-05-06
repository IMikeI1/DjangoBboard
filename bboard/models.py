from django.db import models
from slugify import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Модель объявления
class Bboard(models.Model):
    # Заголовок объявления
    title = models.CharField(max_length=200, verbose_name="Заголовок")

    # Описание объявления
    content = models.TextField(verbose_name="Описание")

    # Картинка (необязательная)
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Изображение")

    # Дата и время создания (устанавливается автоматически)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    # Уникальный slug для генерации URL (может быть пустым при создании)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    # Автор объявления (пользователь), null и blank разрешены для старых данных
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)

    # Дополнительные характеристики автомобиля:
    year = models.PositiveIntegerField(verbose_name="Год выпуска", blank=True, null=True)
    mileage = models.PositiveIntegerField(verbose_name="Пробег (км)", blank=True, null=True)
    condition = models.CharField(max_length=100, verbose_name="Состояние", blank=True)
    modification = models.CharField(max_length=100, verbose_name="Модификация", blank=True)
    engine_volume = models.CharField(max_length=50, verbose_name="Объём двигателя", blank=True)
    engine_type = models.CharField(max_length=50, verbose_name="Тип двигателя", blank=True)
    transmission = models.CharField(max_length=50, verbose_name="Коробка передач", blank=True)
    drive = models.CharField(max_length=50, verbose_name="Привод", blank=True)
    equipment = models.CharField(max_length=200, verbose_name="Комплектация", blank=True)
    body_type = models.CharField(max_length=50, verbose_name="Тип кузова", blank=True)
    color = models.CharField(max_length=50, verbose_name="Цвет", blank=True)
    steering_wheel = models.CharField(max_length=50, verbose_name="Руль", blank=True)
    price = models.PositiveIntegerField(verbose_name="Стоимость (руб.)", blank=True, null=True)
    price_arenda_car = models.PositiveIntegerField(verbose_name="Стоимость (руб/час.)", blank=True, null=True)

    # Метод сохранения модели, где автоматически создаётся уникальный slug
    def save(self, *args, **kwargs):
        # Если slug ещё не установлен, создаём его
        if not self.slug and self.title:  
            base_slug = slugify(self.title)  # Преобразуем заголовок в slug
            if not base_slug:  
                base_slug = 'announcement'  # Если slugify не дал результата
            slug = base_slug
            counter = 1
            
            # Проверяем, существует ли такой slug в базе, если да — добавляем номер
            while Bboard.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug  # Устанавливаем уникальный slug

        # Резервный вариант: если slug по-прежнему пустой
        if not self.slug:  
            self.slug = 'announcement-' + str(Bboard.objects.count() + 1)

        # Вызываем оригинальный метод сохранения родительского класса
        super().save(*args, **kwargs)

    # Метод, возвращающий абсолютный URL для объекта — используется в шаблонах и перенаправлениях
    def get_absolute_url(self):
        return reverse('bboard:detail', kwargs={'slug': self.slug})

    # Строковое представление объекта — будет отображаться в админке и консоли
    def __str__(self):
        return self.title
