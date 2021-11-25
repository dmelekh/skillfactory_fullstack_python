from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from news.models import Post

class NewsList(ListView):
    # model = Post
    # указываем модель, объекты которой мы будем выводить
    template_name = 'news_preview.html'
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    def get_queryset(self):
        return Post.objects.filter(type=Post.news).order_by('-time_in')

class NewsDetail(DetailView):
    # model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'article.html'  # название шаблона будет product.html
    context_object_name = 'article'  # название объекта. в нём будет
    def get_queryset(self):
        return Post.objects.filter(type=Post.news)
