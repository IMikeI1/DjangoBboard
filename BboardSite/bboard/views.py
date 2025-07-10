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
    addds = Addd.objects.all().order_by('-created_at')
    count_addds = addds.count()
    per_page = 6
    paginator = Paginator(addds, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter_form = FilterForm()
    context = {"title": "Главная страница", "page_obj": page_obj, "count_addds": count_addds, "filter_form": filter_form}
    return render(request, template_name='bboard/index.html', context=context)

def about(request):
    count_addds = Addd.objects.count()
    context = {"title": "О сайте", "count_addds": count_addds}
    return render(request, template_name='bboard/about.html', context=context)


def contact(request):
    count_addds = Addd.objects.count()
    context = {"title": "О сайте", "count_addds": count_addds}
    return render(request, template_name='bboard/contact.html', context=context)

@login_required
def add_addd(request):
    if request.method == "GET":
        addd_form = AdddForm()
        context = {'title': 'Добавить объявление', 'form': addd_form}
        return render(request, template_name='bboard/addd_add.html', context=context)
    if request.method == "POST":
        addd_form = AdddForm(data=request.POST, files=request.FILES)
        if addd_form.is_valid():
            addd = addd_form.save(commit=False)
            addd.author = request.user
            addd.save()
            return redirect('bboard:index')
        context = {'title': 'Добавить объявление', 'form': addd_form}
        return render(request, template_name='bboard/addd_add.html', context=context)

def read_addd(request, slug):
    addd = get_object_or_404(Addd, slug=slug)
    context = {"title": "Информация об объявлении", "addd": addd}
    return render(request, template_name='bboard/addd_detail.html', context=context)

# @login_required
# def update_addd(request, pk):
#     addd = get_object_or_404(Addd, pk=pk)
#     if request.method == "POST":
#         addd_form = AdddForm(data=request.POST, files=request.FILES, instance=addd)
#         if addd_form.is_valid():
#             addd = addd_form.save(commit=False)
#             addd.author = request.user
#             addd.save()
#             return redirect('bboard:read_addd', pk=addd.id)
#     else:
#         addd_form = AdddForm(instance=addd)
#     return render(request, template_name="bboard/addd_edit.html", context={"form": addd_form})

@login_required
def edit_addd(request, slug):
    addd = get_object_or_404(Addd, slug=slug)
    if request.method == "POST":
        addd_form = AdddForm(data=request.POST, files=request.FILES, instance=addd)
        if addd_form.is_valid():
            addd = addd_form.save(commit=False)
            addd.author = request.user
            addd.save()
            return redirect('bboard:read_addd', slug=addd.slug)
    else:
        addd_form = AdddForm(instance=addd)
    return render(request, template_name="bboard/addd_edit.html", context={"form": addd_form})

@login_required
def delete_addd(request, addd_id):
    addd = get_object_or_404(Addd, pk=addd_id, author=request.user)
    context = {"addd": addd}
    if request.method == "POST":
        addd.delete()
        return redirect('bboard:index')
    return render(request, template_name='bboard/addd_delete.html', context=context)

def page_not_found(request, exception):
    return render(request, template_name="bboard/404.html", context={"title": "404"})

def forbidden(request, exception):
    return render(request, template_name="bboard/403.html", context={"title": "403"})

def server_error(request):
    return render(request, template_name="bboard/500.html", context={"title": "500"})

def user_addd(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    addd = Addd.objects.filter(author=user).select_related('author')
    context = {'user': user, 'addd': addd}
    return render(request, template_name='bboard/user_addd.html', context=context)

@login_required
def user_info(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    addds = Addd.objects.filter(author=user).select_related('author')
    context = {'user': user, 'addds': addds}
    return render(request, template_name='bboard/user_info.html', context=context)

def search_addd(request):
    query = request.GET.get('query')
    query_text = Q(title__icontains=query) | Q(content__icontains=query)
    results = Addd.objects.filter(query_text)
    per_page = 6
    paginator = Paginator(results, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = results.count()
    context = {"title": "Главная страница", "page_obj": page_obj, "count_addds": count_addds}
    return render(request, template_name='bboard/index.html', context=context)

def filter_addd(request):
    author_id = request.GET.get('author')
    if not author_id:
        results = Addd.objects.all()
    else:
        author = User.objects.get(pk=author_id)
        query_text = Q(author__exact=author)
        results = Addd.objects.filter(query_text)
    per_page = 6
    paginator = Paginator(results, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_addds = results.count()
    filter_form = FilterForm()
    context = {"title": "Главная страница", "page_obj": page_obj, "count_addds": count_addds, "filter_form": filter_form}
    return render(request, template_name='bboard/index.html', context=context)