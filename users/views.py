from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm


def about(request):
    return render(request, 'about.html') 

# Представление регистрации нового пользователя
def register(request):
    if request.method == 'POST': # Если форма отправлена
        form = UserCreationForm(request.POST) # Заполняем форму переданными данными
        if form.is_valid():# Проверяем корректность данных
            form.save() # Сохраняем
            return redirect('users:register_done')  # Перенаправляем на страницу успешной регистрации
    else: # Если форма не отправлена, то просто отображаем пустую форму
        form = UserCreationForm() 
    return render(request, 'registration/register.html', {'form': form}) # Отображаем страницу регистрации с формой

# Представление страницы успешной регистрации
def register_done(request):
    return render(request, 'registration/register_done.html')
# Представление профиля пользователя (только для авторизованных пользователей)
@login_required
def profile(request):
    # Отображаем шаблон с профилем текущего пользователя
    return render(request, 'users/profile.html')

# Представление редактирования профиля (только для авторизованных пользователей)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Передаём текущие данные пользователя в форму вместе с обновлёнными данными
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:  # Если форма не отправлена, просто отображаем её с текущими данными пользователя
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})



