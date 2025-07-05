from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Addd
from .forms import AdddForm, FilterForm
from django.http import HttpResponseNotFound

def trigger_404(request):
    return HttpResponseNotFound(render(request, 'blog/404.html'))

def trigger_403(request):
    return HttpResponseNotFound(render(request, 'blog/403.html'))

def trigger_500(request):
    return HttpResponseNotFound(render(request, 'blog/500.html'))





def index(request):
    addds = Addd.objects.all()
    paginator = Paginator(addds, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = addds.count()

    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
        'count_posts': count_addds
    }
    return render(request, 'bboard/index.html', context)

def about(request):
    return render(request, 'bboard/about.html', {'title': 'О сайте'})


@login_required
def user_info(request, pk):
    user_addds = Addd.objects.filter(author=pk)
    paginator = Paginator(user_addds, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = user_addds.count()

    context = {
        'title': 'Мои объявления',
        'page_obj': page_obj,
        'count_posts': count_addds,
    }
    return render(request, 'bboard/user_info.html', context)


@login_required
def add_addd(request):
    if request.method == 'GET':
        addd_form = AdddForm()
        context = {'form': addd_form, 'title': 'Добавить объявление'}
        return render(request, template_name='bboard/addd_add.html', context=context)

    if request.method == 'POST':
        addd_form = AdddForm(data=request.POST, files=request.FILES)
        if addd_form.is_valid():
            addd = addd_form.save(commit=False)
            addd.author = request.user  # <-- вот где правильно установить автора
            addd.save()
            return redirect('bboard:read_addd', slug=addd.slug) 
        else:
            context = {'form': addd_form, 'title': 'Добавить объявление'}
            return render(request, 'bboard/addd_add.html', context)
    # if request.method == 'GET':
    #     post_form = AdddForm(author=request.user)
    #     context = {'form': post_form, 'title': 'Добавить объявление'}
    #     return render(request, template_name='bboard/addd_add.html', context=context)
    # if request.method == 'POST':
    #     post_form = AdddForm(data = request.POST, files=request.FILES, author=request.user)
    #     if post_form.is_valid():
    #         # post = Post()
    #         # post.title = post_form.cleaned_data['title']
    #         # post.text = post_form.cleaned_data['text']
    #         # post.author = post_form.cleaned_data['author'] # request.user
    #         # post.image = post_form.cleaned_data['image']
    #         post_form.save()
    #         return index(request)



def read_addd(request, slug):
    addd = get_object_or_404(Addd, slug=slug)
    context = {'addd': addd, 'title': addd.title}
    return render(request, template_name='bboard/addd_detail.html', context=context)

@login_required
def update_addd(request, slug):
    addd = get_object_or_404(Addd, slug=slug)

    if request.method == 'POST':
        form = AdddForm(data=request.POST, files=request.FILES, instance=addd, initial={'author': addd.author})
        if form.is_valid():
            addd.title = form.cleaned_data['title']
            addd.content = form.cleaned_data['content']
            addd.author = form.cleaned_data['author']
            addd.image = form.cleaned_data['image']
            addd.save()
            return redirect('bboard:read_addd', slug=addd.slug)
    else:
        form = AdddForm(initial={
            'title': addd.title,
            'content': addd.content,
            'image': addd.image,
            'author': addd.author,
            'price': addd.price,
            'brand': addd.brand,
            'model': addd.model,
                        
        }, author=request.user)

    return render(request, template_name='bboard/addd_update.html', context={'form': form})




def user_addd(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Addd.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,       # для заголовка
        'posts': posts,     # список объявлений пользователя
    }
    return render(request, 'bboard/user_addd.html', context)






@login_required
def edit_addd(request, slug):
    addd = get_object_or_404(Addd, slug=slug)

    if request.method == 'POST':
        form = AdddForm(data=request.POST, files=request.FILES, author=request.user)
        if form.is_valid():
            addd.title = form.cleaned_data['title']
            addd.content = form.cleaned_data['content']
            addd.author = form.cleaned_data['author']
            addd.image = form.cleaned_data['image']
            addd.save()
            return detail_addd(request, addd.slug)
    else:
        form = AdddForm(initial={
            'title': addd.title,
            'content': addd.content,
            'image': addd.image,
        }, author=request.user)

    return render(request, 'bboard/addd_edit.html', context={'form': form})



@login_required
def delete_addd(request, addd_id):
    addd = get_object_or_404(Addd, pk=addd_id, user=request.user)
    if request.method == 'POST':
        addd.delete()
        return redirect('bboard:user_info', pk=request.user.pk)
    return render(request, 'bboard/addd_delete.html', {'title': 'Удаление объявления', 'addd': addd})


# Кастомные страницы ошибок

def page_not_found(request, exception):
    return render(request, template_name='bboard/404.html', context={'title': '404'})


def forbidden(request, exception):
    return render(request, template_name='bboard/403.html', context={'title': '403'})


def server_error(request):
    return render(request, template_name='bboard/500.html', context={'title': '500'})


# Поиск по объявлениям

def search_addd(request):
    query = request.GET.get('query')
    query_text = Q(title__icontains=query) | Q(content__icontains=query)
    results = Addd.objects.filter(query_text)

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = results.count()

    context = {
        'title': 'Результаты поиска',
        'page_obj': page_obj,
        'count_posts': count_addds
    }
    return render(request, template_name='bboard/index.html', context=context)




def filter_addd(request):
    author_id = request.GET.get('author')
    if not author_id:
        results = Addd.objects.all()
    else:
        author = get_object_or_404(User, pk=author_id)
        results = Addd.objects.filter(user=author)

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = results.count()
    filter_form = FilterForm()

    context = {
        'title': 'Фильтр объявлений',
        'page_obj': page_obj,
        'count_posts': count_addds,
        'post_text': 'Результаты фильтрации',
        'filter_form': filter_form
    }
    return render(request, template_name='bboard/index.html', context=context)
