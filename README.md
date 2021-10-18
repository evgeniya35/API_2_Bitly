# Работа с сервисом bit.ly

Программа работы с API сервиса сжатия(укорачивания) ссылок [https://bitly.com](https://bitly.com/a/sign_up).

## Окружение и установка

Python должен быть установлен.

## Установка зависимостей

Используйте pip для установки зависимостей:
```bash
pip install -r requirements.txt
```

## Запуск

- Скачайте код: [https://github.com/evgeniya35/bitly_lesson2.git](https://github.com/evgeniya35/bitly_lesson2.git), или клонируйте `git` репозиторий в локальную папку:
```
git clone https://github.com/evgeniya35/bitly_lesson2.git
```
- Зарегистрирутесь на сайте [https://bitly.com](https://bitly.com) и получите персональный токен. Токен поместите в файл `.env`:
```
BIT_TOKEN=ваш токен
```
- Запустите программу командой:
```bash
python main.py {url}
```

## Как работает

 Программа `main.py` запрашивает у пользователя адрес ссылки. Анализирует введенную ссылку. В зависимости от введенной ссылки, трансформирует ссылку в сокращённую `bit.ly` ссылку или выводит количество переходов по `bit.ly` ссылке.

## Особенности работы

`main.py` содержит функции:

* Функция `def is_bitlink(url)` - Проверяет адрес ссылки на содержание домена `bit.ly`. 
* Функция `is_bitlink_api(token, parsed)` - Проверяет через API `bit.ly` ссылку. 
* Функция `shorten_link(token, url)` - Трансформирует ссылку в сокращённую `bit.ly` ссылку.
* Функция `count_clicks(token, short_url)` Подсчитывает количество переходов по сокращённой `bit.ly` ссылке.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).