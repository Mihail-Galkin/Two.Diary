# [Two.Diary](https://two43.ddns.net/)
[![Группа в ВК](https://img.shields.io/badge/вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/public219719675)
[![Schedule bot](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Mihail-Galkin/kpml-schedule)
## Основная информация
Сайт, расширяющий возможности электронного [дневника](https://one.43edu.ru), представленного правительством Кировской области. 

Добавленные возможности:
1. Просмотр последних оценок
2. Просмотр урока в модальном окне
3. Просмотр последних уроков заданного типа
4. Переход к уроку при нажатии на оценку
5. Расчет балла при получении/исправлении оценки 

Подробнее можно почитать в [статье](https://vk.com/@-219719675-pochemu-stoit-ispolzovat-twodiary)

## Техническая информация
### Зависимости
Зависимости находятся в папке requirements

Установка выполняется командой:
```
pip install -r requirements/development.txt
```
или
```
pip install -r requirements/production.txt
```

### Переменные окружения
Для работы пиложения, необходимо установить переменные среды:
+ **FLASK_ENV** (development или production)
+ **SECRET_KEY**
+ **PASSWORD_KEY**
+ **DATABASE_URL**

### Структура проекта
+ **app** - главный пакет приложения
+ В **\_\_init\_\_.py** файле инициализируются расширения flask, добавляются маршрутизаторы
+ В **extensions.py** создаются переменные расширений flask
+ Маршрутизаторы - это подпакеты app

Подробнее о структуре можно узнать из **docstrings**

## Яндекс.Лицей
Материалы для защиты:
+ [Презентация](https://disk.yandex.ru/i/j0kRVWhw4-CsWw)
+ [ТЗ](https://disk.yandex.ru/d/Bx_FEYURkONFQw)
