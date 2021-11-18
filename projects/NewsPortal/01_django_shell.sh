#!/bin/bash

# Что вы должны сделать в консоли Django?
python3 manage.py shell

#         Создать двух пользователей (с помощью метода User.objects.create_user('username')).
from django.contrib.auth.models import User
user1 = User.objects.create_user('test_user_1')
user2 = User.objects.create_user('test_user_2')

#         Создать два объекта модели Author, связанные с пользователями.
from news.models import Author
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

#         Добавить 4 категории в модель Category.
from news.models import Category
cat_sci = Category.objects.create(name='Наука')
cat_sport = Category.objects.create(name='Спорт')
cat_polit = Category.objects.create(name='Политика')
cat_econo = Category.objects.create(name='Экономика')

#         Добавить 2 статьи и 1 новость.
from news.models import Post
article1 = Post.objects.create(author=author1, type='AR', body='text line 1\ntext line 2\ntext line 3')
article2 = Post.objects.create(author=author2, type='AR', body='text line 4\ntext line 5\ntext line 6')
news1 = Post.objects.create(author=author1, body='comment words')

#         Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
article1.categories.add(cat_sci)
article1.categories.add(cat_econo)
article2.categories.add(cat_polit)
news1.categories.add(cat_sport)

#         Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
from news.models import Comment
comment1 = Comment.objects.create(post=article1, user=author1, body='моя статья самая научная')
comment2 = Comment.objects.create(post=article1, user=author2, body='ты все списал у меня')
comment3 = Comment.objects.create(post=article2, user=author1, body='это статья про котиков?')
comment4 = Comment.objects.create(post=news1, user=author2, body='где-то я это уже видел')

#         Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
for i in range(5): article1.like()

article1.dislike()
for i in range(7): article2.like()

article2.dislike()
for i in range(3): news1.like()

news1.dislike()
for i in range(8): comment1.like()

comment1.dislike()
for i in range(10): comment2.like()

comment2.dislike()
for i in range(4): comment3.like()

comment3.dislike()
for i in range(6): comment4.like()

comment3.dislike()

#         Обновить рейтинги пользователей.
for author in Author.objects.all(): author.update_rating()

#         Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_author = Author.objects.all().order_by('-rating')[0]
print(f'best_author.username={best_author.user.username}, best_author.rating={best_author.rating}')

#         Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.

#         Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
