from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)


# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:

#         cвязь «один к одному» с встроенной моделью пользователей User;
#         рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

#     Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
# Он состоит из следующего:

#     суммарный рейтинг каждой статьи автора умножается на 3;
#     суммарный рейтинг всех комментариев автора;
#     суммарный рейтинг всех комментариев к статьям автора.

    def update_rating(self):
        posts_rating = self._get_rating_sum_posts()
        self.rating = posts_rating * 3 + self._get_rating_sum_comments() + self._get_rating_sum_comments_to_posts()
        print(f'user={self.user}, rating={self.rating}')
        self.save()

    def _get_rating_sum_posts(self):
        return self.__get_rating_sum(self._get_own_posts())

    def _get_rating_sum_comments(self):
        return self.__get_rating_sum(Comment.objects.filter(user=self.user))

    def _get_rating_sum_comments_to_posts(self):
        posts = self._get_own_posts()
        return self.__get_rating_sum(Comment.objects.filter(post__in=posts))

    def __get_rating_sum(self, subquery):
        return subquery.aggregate(Sum('rating')).get('rating__sum')

    def _get_own_posts(self):
        return Post.objects.filter(author=self)

# Модель Category
# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). Имеет единственное поле: название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:

#         связь «один ко многим» с моделью Author;
#         поле с выбором — «статья» или «новость»;
#         автоматически добавляемая дата и время создания;
#         связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
#         заголовок статьи/новости;
#         текст статьи/новости;
#         рейтинг статьи/новости.

class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2, choices=POST_TYPES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255, default="Без Названия")
    body = models.TextField()
    rating = models.IntegerField(default=0.0)

    def like(self):
        strategy_like(self)

    def dislike(self):
        strategy_dislike(self)

    # Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.

    def preview(self):
        return f'{self.body[:124]}...'

    def __str__(self):
        return f'id:{self.id}\ntype: {self.type}\nheader:{self.header}\nbody:{self.body}'

# Модель PostCategory
# Промежуточная модель для связи «многие ко многим»:
#
        # связь «один ко многим» с моделью Post;
        # связь «один ко многим» с моделью Category.

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:

#         связь «один ко многим» с моделью Post;
#         связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
#         текст комментария;
#         дата и время создания комментария;
#         рейтинг комментария.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        strategy_like(self)
    
    def dislike(self):
        strategy_dislike(self)

# Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.


def strategy_like(target):
    target.rating += 1
    target.save()

def strategy_dislike(target):
    target.rating -= 1
    target.save()