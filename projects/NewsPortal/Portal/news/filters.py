from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики

from .models import Post


# создаём фильтр
class NewsFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {
            'time_in': ['gt'],
            'header': ['icontains'],
            'author__user__username': ['icontains'],  # iexact icontains
            # 'type': [f'iexact={Post.news}']
        }
