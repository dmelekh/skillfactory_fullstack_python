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
article1 = Post.objects.create(author=author1, type=Post.article, header='User1 article header', body='article1 line1\narticle1 line2\narticle1 line3')
article2 = Post.objects.create(author=author2, type=Post.article, header='User2 article header', body='article2 line1\narticle2 line2\narticle2 line3')
news1 = Post.objects.create(author=author1, header='User1 news header', body='yellow papers')
news2 = Post.objects.create(author=author2, header='User2 news header', body='green cards')
news2 = Post.objects.create(author=author1, header='User1 news header rovers', body='As of May 2021, there have been six successful robotically operated Mars rovers, the first five managed by the American NASA Jet Propulsion Laboratory: Sojourner (1997), Opportunity (2004), Spirit (2004), Curiosity (2012), and Perseverance (2021). The sixth is Zhurong (2021), managed by the China National Space Administration. ')

#         Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
article1.categories.add(cat_sci)
article1.categories.add(cat_econo)
article2.categories.add(cat_polit)
news1.categories.add(cat_sport)
news2.categories.add(cat_sport)

#         Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
from news.models import Comment
comment1 = Comment.objects.create(post=article1, user=author1.user, body='моя статья самая научная')
comment2 = Comment.objects.create(post=article1, user=author2.user, body='ты все списал у меня')
comment3 = Comment.objects.create(post=article2, user=author1.user, body='это статья про котиков?')
comment4 = Comment.objects.create(post=article2, user=author2.user, body='не всем думают о политике как о науке')
comment5 = Comment.objects.create(post=news1, user=author2.user, body='где-то я это уже видел')
comment6 = Comment.objects.create(post=news2, user=author1.user, body='давным-давно в очень далекой галлактике')

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
# from news.models import Author
for author in Author.objects.all(): author.update_rating()

#         Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_author = Author.objects.all().order_by('-rating')[0]
print(f'best_author.username={best_author.user.username}, best_author.rating={best_author.rating}')

#         Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
# from news.models import Post
articles = Post.objects.filter(type=Post.article)
best_article = articles.order_by('-rating')[0]
print('best article:')
print(f'date:{best_article.time_in.date().strftime("%Y.%m.%d")}, author:{best_article.author.user}, rating:{best_article.rating}')
print(f'header:{best_article.header}')
print(f'preview:\n{best_article.preview()}')

#         Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
#from news.models import Comment
best_article_comments = Comment.objects.filter(post=best_article)
for comment in best_article_comments: print(f'time:{comment.time_in}, user:{comment.user}, rating:{comment.rating}, text:{comment.body}')

