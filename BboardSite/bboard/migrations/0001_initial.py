# Generated by Django 5.2.3 on 2025-07-05 09:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Addds/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Дата создания')),
                ('brand', models.CharField(max_length=100, verbose_name='Марка')),
                ('model', models.CharField(max_length=100, verbose_name='Модель')),
                ('year', models.PositiveIntegerField(verbose_name='Год выпуска')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('slug', models.SlugField(editable=False, max_length=200, null=True, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Addds', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ['-created_at'],
            },
        ),
    ]
