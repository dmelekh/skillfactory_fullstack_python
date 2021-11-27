import re

from django import template

register = template.Library()
# если мы не зарегистрируем наши фильтры, то Django никогда не узнает,
# где именно их искать и фильтры потеряются

CENSORED_WORDS_ROOTS = ['perseverance', 'curiosity', 'opportunity']
# for case insensitive replace
CENSORED_PATTERNS = [re.compile(root, re.IGNORECASE) for root in CENSORED_WORDS_ROOTS]

@register.filter(name='censor')
# регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
def censor(value):
    # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|multiply:arg
    if isinstance(value, str):
        # проверяем, что value — это точно строка
        censored = value
        for pattern in CENSORED_PATTERNS:
            censored = pattern.sub('**Censored**', censored)
        return censored
        # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    else:
        raise ValueError(f'{type(value)} can not be censored')
            # в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку
