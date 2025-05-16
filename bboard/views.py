from django.shortcuts import render
from .models import Bboard
from .forms import BboardForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from slugify import slugify
from django.db.utils import IntegrityError
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
# Функция-проверка: является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and user.is_staff


# Статическая страница "О сайте"
def about(request):
    return render(request, 'about.html')  # Просто отображаем шаблон


# Статическая страница "Контакты"
def contacts(request):
    context = {
        'email': 'retrocars@example.com',
        'phone': '+7 (999) 123-45-67',
        'address': 'г. Москва, ул. Автомобильная, д. 1'
    }
    return render(request, 'contacts.html', context)  # Передаём контакты в шаблон


# Поиск объявлений
def index(request):
    query = request.GET.get('query')
    bboards = Bboard.objects.all().order_by('-created_at')
    if query:
        bboards = bboards.filter(
            Q(title__icontains=query) | Q(user__username__icontains=query)
        )
    # Главная страница — список всех объявлений с пагинацией
    paginator = Paginator(bboards, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_count = bboards.count()
    # Формируем список объявлений с can_edit
    page_items = []
    user = request.user
    for item in page_obj:
        can_edit = user.is_authenticated and (user.is_staff or item.user == user)
        page_items.append({'item': item, 'can_edit': can_edit})
    return render(request, 'bboard/index.html', {
        'page_obj': page_obj,
        'page_items': page_items,
        'total_count': total_count,
    })


# Добавление нового объявления (только для авторизованных пользователей)
@login_required
def add_bboard(request):
    if request.method == 'POST':  # Обработка отправки формы
        form = BboardForm(request.POST, request.FILES)  # Заполняем форму с данными и файлами
        if form.is_valid():  # Проверка валидности
            try:
                form.save(user=request.user)  # Сохраняем с привязкой к текущему пользователю
                return redirect('bboard:index')  # Перенаправляем на главную страницу
            except IntegrityError:
                form.add_error(None, "Объявление с таким заголовком уже существует.")  # Обработка ошибки уникальности
    else:
        form = BboardForm()  # Пустая форма при GET-запросе
    return render(request, 'bboard/add.html', {'form': form})  # Отображаем шаблон с формой


# Просмотр одного объявления по slug (только авторизованные)
@login_required
def detail_bboard(request, slug):
    item = get_object_or_404(Bboard, slug=slug)  # Получаем объект или 404
    return render(request, 'bboard/detail.html', {'item': item})  # Показываем объявление


# Удаление объявления (только автор или админ)
@login_required
def delete_bboard(request, slug):
    item = get_object_or_404(Bboard, slug=slug)  # Получаем объявление по slug
    if not (request.user.is_staff or item.user == request.user):
        raise PermissionDenied  # Если не автор и не админ — ошибка доступа
    if request.method == 'POST':
        item.delete()  # Удаляем объявление
        return redirect('bboard:index')  # Возвращаемся на главную
    return render(request, 'bboard/delete_confirm.html', {'item': item})  # Показываем подтверждение удаления


# Обработка ошибки 404 — Страница не найдена
def page_not_found(request, exception):
    context = RequestContext(request)  # Создаём контекст
    response = render(request, '404.html', context=context.flatten())  # Отображаем шаблон ошибки
    response.status_code = 404
    return response


# Обработка ошибки 403 — Доступ запрещён
def forbidden(request, exception):
    return render(request, '403.html', status=403)


# Обработка ошибки 500 — Внутренняя ошибка сервера
def server_error(request):
    return render(request, '500.html', status=500)


@login_required
def edit_bboard(request, slug):
    item = get_object_or_404(Bboard, slug=slug)
    if not (request.user.is_staff or item.user == request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = BboardForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('bboard:index')
    else:
        form = BboardForm(instance=item)
    return render(request, 'bboard/edit.html', {'form': form, 'item': item})







