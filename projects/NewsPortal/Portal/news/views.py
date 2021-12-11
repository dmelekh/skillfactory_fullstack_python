from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from .filters import NewsFilter
from .models import Post

# class NewsList(ListView):
#     # model = Post
#     # указываем модель, объекты которой мы будем выводить
#     template_name = 'news_preview.html'
#     # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
#     context_object_name = 'news'
#     paginate_by = '2'  # TODO 211201 - change value to 10
#     # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
#     def get_queryset(self):
#         return Post.objects.filter(type=Post.news).order_by('-time_in')

class NewsList(View):
    def get(self, request):
        news_all = Post.objects.filter(type=Post.news).order_by('-time_in')
        p = Paginator(news_all, '2')  # TODO 211201 - change value to 10
        news = p.get_page(request.GET.get('page', 1))  # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        data = {'news': news}
        return render(request, 'news_preview.html', data)

class NewsDetail(DetailView):
    # model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'article.html'  # название шаблона будет product.html
    context_object_name = 'article'  # название объекта. в нём будет
    def get_queryset(self):
        return Post.objects.filter(type=Post.news)

class NewsSearch(ListView):
    # model = Post
    # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    # ordering = ['-time_in']
    paginate_by = 2  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        # добавим переменную текущей даты time_now
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        return context

    def get_queryset(self):
        return Post.objects.filter(type=Post.news).order_by('-time_in')
