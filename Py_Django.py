# region #* Установка django, импорт библиотек, назначение переменных ---------
"""
(последняя версия)
_ pip install django

Установка django (конкретная версия)
_ pip install django==3.0.0

# Создание проекта
_ django-admin startproject project_name

# Создание приложения django
_ py manage.py startapp name_app   # (на curserra рекомендовано core)

После создания приложения, его необходимо активировать в settings.py, в разделе
INSTALLED_APPS. Внутри папки приложения создан apps.py. В нем класс приложения.
Его и необходимо указать в разделе INSTALLED_APPS по форме:
'app_name.apps.app_name_config_class'
"""
import os
from django.conf.urls import url
from core import views
from django.http import HttpResponse
import datetime
from django.db import models
from django.urls import path
from core.models import Blog, Author, Entry
from django.db.models import Avg, Count, Max

key = 'somekey'
value = 'somevalue'
httponly = 'httponly'
BASE_DIR = "."
# endregion -------------------------------------------------------------------

# region #* Индексы, запросы. Логика определения ссылок -----------------------
"""Когда происходит запрос какого-то веб-сервиса, то запрос попадает в urls,
там находит необходимый обработчик запроса, которому передается управление. В
обработчике выполняется бизнес-логика, формируется ответ клиенту.
При старте приложения, django загружает модуль, который указан в root_urlconf,
в файле settings. Внутри него ищет urlpatterns. Затем проверяет по порядку
каждое регулярное выражение (regex), которое указано в urlpatterns. При
нахождении первого совпадения, вызывается url-обработчик (veiw), который
передает объект httprequest и параметр из regex. Если он просканил все url'ы и
не нашел совпадения, вызывает view обработчика ошибки.
Найденные аргументы - всегда строки. Именованные аргументы имеют приоритет.
Каждое регулярное выражение компилируется при первом обращении.
Структура HTML
https://www.coursera.org/learn/python-for-web/lecture/V6JT4/osnovy-html
"""
""" Для создания страниц - добавляется индекс в фале urls.py в папке проекта.
Роутинг - это сопоставление url'а с его обработчиком. Описан в файликах urls и
переменной urlpatterns. Urlpatterns представляет из себя массив из объектов
urls.Когда создается объект urls, там указывается регулярное выражение, которое
соответствует url'у и его обработчик.
urlpatterns = [
    path(r'articles/2003/', view,special_case_2003),
    url(r'....')
]
В современной версии Джанго вместо url используется синтаксис path. см. докум..
Это же касается регулярных выражений. Они упрощены, но пока не понятны.
"""
""" Include. С его помощью организовывается иерархическая структура. В
переменной urlpatterns указывается url, который в начале соответствует некому
префиксу, и далее указывается include, либо переменная, которая содержит список
из url'ов, либо файлик, в котором есть переменная urlpatterns.
extra_pattern = [
    url(r'articles/2003/$', view,special_case_2003),
    url(r'articles/2004/$', view,special_case_2004),
    url(r'articles/2005/$', view,special_case_2005),
]
urlpatterns = [
    url(r'^help/', include('apps.help.urls')),
    url(r'extra', include (extra_pattern))
]
Также этот метод используется для сокращения записи длинных повторяющихся
regex, а также в шаблонах при использовании namespace через механизм resolve.
"""
# endregion -------------------------------------------------------------------

# region #* View, параметры, создание -----------------------------------------
""" Для создания view - файл view.py в папке приложения. Структура обработчика
View. Каждый View принимает httpRequest в качестве своего первого параметра
(request). Возвращает всегда HttpResponse, содержащий сгенерированный ответ.
"""
""" HttpRequest - объект, в качестве атрибутов имеющий методы: GET, в котором
содержатся get параметры; POST, в котором содержится тело запроса; FILES, в
котором содержатся файлs, кпереданные от запроса; COOKIES, в котором указаны
cookie запросы; META, в котором указаны заголовки запроса. """


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


""" HttpResponse - объект формирующий тело ответа. Содержит атрибуты: content,
тело ответа. content_type — тип MIME, тип данных, которые мы будут возвращены.
status — это статус http ответа, например, ok(200), not found(404), bad request
и так далее. reason — указывается если необходимо как-то предопределить ответ
status reason в http, иначе он берется из статуса http ответа. И charset — это
собственная кодировка, с которой будут переданы данные клиенту.
HttpResponse это словарь, которому можно присваивать некие ключь/значение.
"""
response = HttpResponse()
response['Age'] = 120
del response['Age']
response.has_header('Age')  # проверка наличия заголовка
response.set_cookie(key, value, ..., httponly)  # установка кукис
response.delete_cookies(key, ..., value)  # удаление кукис
response.write('<p>Необходимо что то дописать</p>')

"""Декораторы применяются по принципам синтаксиса пайтон.
Станадртные декораторы:
@reuire_http_method(request_method_list)  # проверяет допустимость метода
@require_GET()  # разрешает обработку только гет запросов
@require_POST()  # пост запросов
"""
# endregion -------------------------------------------------------------------

# region #* Шаблонизация. Синтаксис шаблонов. Струкутра проекта
""" Шаблонизация — необходимый способ динамической генерации HTML для
формирования HTTP ответа. Наиболее распространенный подход основан на шаблонах.
Шаблон содержит статический части html, а также специальный синтаксис,
описывающий динамический контент. Джанго можно настраивать с использованием
одного или нескольких движков шаблонизации. Есть встроенный - DTL. Есть
альтернативные двжики - например Jinia2.
Настройка - settings.py
"""
TEMPLATES = [
    {
        # путь к движку шаблонизации
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  # список папкок в которых находятся все шаблоны
            os.path.join(BASE_DIR, 'templates'),  # добавление папки в проект
        ],
        'APP_DIRS': True,  # искать шаблоны внутри аппсов (приложений)
        'OPTIONS': {},  # специальные настройки
    }
]
""" Для того, чтобы не усложнять проект, в приложениях имеется своя папка
templates, где лежат шаблоны относящиеся непосредственно к приложению. В корне
проекта, также создается папка, где лежат базовые шаблоны. При таком
подходе APP_DIRS = True
В переменную TEMPLATES/DIRS как список добавляются нужные папки проекта
Внутри корневого templates создаем base.html (см пример)
Внутри папки приложения, свой templates/app_name/ И там index.html (см пример)
Глобальные стили и js (bootstrap, jquery ) подключаются в ./templates/base.html
"""
# _Шаблоны имеют механизм наследования. Через механизмы extand и include
""" Для extand - cоздается базовый шаблон, где каждый блок который надо
переопределить оборачивается в теги {% block ... %} {% endblock ... %}
Название блоков произвольное, но лучше одним словом, маленькими буквами
При этом если какой либо код в родительской странице обернуть такими блоками,
то в дочерних страницах можно переопределять этот код, заменяя его - оборачивая
такими же блоками. Пример см. в ./templates/base.html {% block nav %}

<!DOCTYPE html>
<html>
<head>
#** <title>{% block title %} {% endblock title %}</title>
</head>
<body>
    <div id="content">
#**     {% block content %} {% endblock content %}
    </div>
</body>
</html>

В дочерних шаблонах указываем из какого шаблона необходимо наследоваться через
механизм extand.
В дальнейшем при вызове дочерней страницы, базовые атрибуты html берутся из
базы, а прописанные в дочернем - от него самого.

{% extends "base.html" %}

{% block title %} .......
{% endblock title %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{entry.titles}}</h2>
    <p>{{entry.body}}</p>
{% endfor %}
{% endblock content %}
"""
""" При использовании include необходимый кусок кода просто вставляется через
тег include в место кода, где он указан.
При этом можно использовать дополнительные элементы. Как пример в даном проекте
в папке ./core/templates создан шаблон списка топиков блога - topic_list.html.
В нем определен список топиков, который затем вставлен в core/index.html через
механизм include. Тоже самое для category.html
+ созданы файлы topic_details.html - для открытого блога, и на его основе
создана view с таким же названием.

{% block content %}
{% for entry in blog_entries %}
    ......
#** {% include "entry.html" whith entry=entry %}
{% endfor %}
{% endblock content %}
"""

"""# _Синтаксис шаблонизаторов, для передачи переменных внутрь шаблона - через
двойные фигурные скобки {{}}.

My first name is {{first_name}}.
My last name is {{last_name}}.

# _К атрибутам объектов (в т.ч. словарей, списков и т.п.) обращение идет также
внутри двойных {{}}, а ключ, атрибут или индекс указывается через точку "."
{{my_dict.key}}
{{my_object.attribute}}
{{my_list.0}}

# _Условия и циклы заключаются в одинарные {} Дополнительно обрамляются % .. %
{% if number == 2 %}
    Число равно 2
{% elif number == 3 %}
    Число равно 3
{% else %}
    Число равно {{number}}
{% endif %
}
{% for o in some_list %}
    {{o}}
{% endfor %}
"""
"""# _Фильтры и тэги. Язык шаблонов поставляется с широким спектром встроенных
тегов и фильтров. Если требуется функциональность которой нет, надо дописывать
свои. Принято, дописанные фильтры/теги создавать в папке temlatetags внутри
папки приложения. Если теги или фильтры глобальные для всего проекта, то
temlatetags создается в папке проекта. Чтобы добавить свои фильтры и теги в
шаблон

{% load template_name%}
"""
""" Фильтры при создании обрамляются декоратором @registr.filter. """
@registr.filter
def filter(value, arg):
    return value.replace(arg, '')


""" Применяются к переменным через |. Атрибуты добавляются как ключи

{{somevariable|filter_name:"value"}}
"""
"""#** Для того чтобы зарегистрировать тег, нужно его объявить в файле
poll_extras и повесить на него декоратор @register.simpletag.
Inclusion теги создаются через декоратор @registr.inclusion_tag. Могут
применяться как с параметрами так и без них. Применяются когда нужно вернуть не
просто какое то значение/результат - а когда нужно вернуть верстку.
"""
@registr.inclusion_tag
def my_tag(a, b, *args):
    warning = args['warning']
    profile = args['profile']
    return ...


"""#** вызываются фильтры через {%...
{% my_tag 12, "abcd", book.title warning=message|lower profile=user.profile %}
"""
# endregion -------------------------------------------------------------------

# region #* Базы данных в Джанго (теория) -------------------------------------
"""# _Миграция — способ применения изменений, которые делаются в моделях, в
схему базы данных. Делается с помощью следующих команд.
makemigrations создает файл миграции. То есть вы добавили какое-то поле, он
определил, какое, и сгенерировал такой файлик, в котором описаны все действия,
которые нужно сделать с базой.
migrate —  применяет файл к базе.
sqlmigrate — отображает тот SQL, который будет применен во время миграции.
showmigrations — отобразит список всех миграций и их статус.

#** workflow:
добавили какое-то поле, сделали
#// python manage.py makemigrations
сгенерирован файл миграции. Затем
#// python manage.py migrate
Этот файл применяется к базе данных.
"""
""" в settings.py есть переменная DATABASES. Там указываются все базы данных, к
которым подключено приложение. Для того, чтобы указать дефолтную базу данных, в
дикте указывается ключик default и указываем параметры.
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': "user",
        'PASSWORD': "pasword",
        'HOST': "127.0.0.1",
        'PORT': "8080",  # если не указан, то дефолтный
        'OPTIONS': {'autocommit': True},
    }
}
"""ENGINE — это тот коннектор, который будет использоваться для подключения к
базе. NAME — это имя базы. USER — это имя пользователя. PASSWORD — это пароль.
HOST — это место где расположена база. PORT — на какой порт нужно стучаться.
OPTIONS, специфичный для каждой базы данных параметр.
"""
"""# _Все таблицы, которые есть в БД, описываются с помощью Python классов.
Выполнение запросов к БД производятся через вызов методов данного класса.
Каждая запись в таблице — это объект данного класса. Все модели описаны в фале
models.py
Связи между классами/таблицами базы данных организованы через связи между
классами, .ForeignKey, .ManyToManyField см. примеры в файле models.py"""


class Blog(models.Model):
    """Создание класса модели работы с базой (таблица).
    Создаются колонки name, tagline, + по умолчанию еще и classname_id
    """
    name = models.CharField(max_length=155)
    tagline = models.TextField()


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()


class Entry(models.Model):
    """ Создание таблицы, с присваиванием связей.
    атрибут blog - связь 1 к многим в объектам класса Blog
    атрибут authors - связь многие ко многим к объектам класса Author
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)  # связь 1 = &
    headline = models.CharField(max_length=255, blank=True, null=True,
                                default=0)
    views = models.IntegerField(default=0)
    authors = models.ManyToManyField(Author)  # связь & = &


""" Поля модели данных (документация). Каждое поле модели данных должно быть
экземпляром класса Field. Джанго использует типы классов полей для определения:
типа столбца - сообщает какие данные храним (INT, VAR ит.д); Виджета - то что
используется при отображении; требования к проверке.
#** Параметры полей:
null - если True, Джанго хранит пустые значения как nuul.
blank - если True, полю разрешено быть пустым.
db_index - если True, по этому полю будет создан индекс базы.
primary_key - если True, поле становится первичным ключом
unique - если True, то значения в столбце - уникальны
validator - список валидаторов для этого поля
"""
""" Создание, изменение, и сохранение объектов из базы осуществляется через
импорт классов из модели данных """

# создание объекта класса с переданными параметрами
b = Blog(name='first name', tagline='All the latest Beatles news')
b.save()  # запись значения в базу данных

b.name = 'another first name'  # изменение атрибута
b.save()  # запись нового значения в базу
b.delete()  # удаление объекта из базы

# ** для присваивания связи между объектами:
# получение объекта класса entry через метод get, присаивание id объекта (pk-1)
entry = Entry.object.get()

# получение объекта класса blog
cheese_blog = Blog.object.get(name="Cheder Talk")
entry.blog = cheese_blog  # присваивание связи между entry и blog 1 к многим
entry.save()

genry = Author(name="Genry")  # создание автора
jonny = Author(name="Jonny")  # создание автора
entry.authors.add(genry, jonny)  # присваивание связи авторов к заметке & = &
# endregion -------------------------------------------------------------------

# region #* ОРМ базы данных ---------------------------------------------------
"""#** Для извлечения данных из базы (фильтр) нужно создать QuerySet - набор
объектов из базы. QuerySet соответствует SQL-выражению, а фильтры, которые к
нему применены, это условия в WHERE. QuerySet можно получить с помощью
менеджеров модели. Каждая модель имеет, по крайней мере, один менеджер, и по
умолчанию он называется objects."""
all_entries = Entry.objects.all()  # создание QuerySet всех объектов Entry
print(all_entries.query)  # .query - посмотреть соответствие SQL запроса

# создание QuerySet с фильтром по значению headline
entries = Entry.objects.filter(headline='name')

# создание QuerySet не включая объекты по значению headline
entries = Entry.objects.exclude(headline='noname')

# ** Сложные фильтры
# через опускаемый оператор "И", все что перечислено в аргументах через ","
entries = Entry.objects.filter(headline='name', blog_id=1)

# фильтры "OR" (или). Через класс Q (дочерний к классу Models) и операторы.
entries = Entry.objects.filter(
    (models.Q(headline='name') | models.Q(headline='name2')
     & models.Q(blog_id=1))
)
# ** Цепочки фильтров. Делаются в несколко этапов:
entries = Entry.objects.filter(headline='name')
entries = entries.objects.exclude(blog_id=1)  # метод применяется уже к объекту

# ** Lookups. Поиск по полю. Это условие которое будет указано в WHERE SQL
# шаблон attributname__lookuptype=value
entries = Entry.objects.filter(headline__in=('name', 'noname'))
entries = Entry.objects.exclude(headline__notin='name')
"""Типы lookups (ILIKE означает нечувствительный к регистру):
contains и icontains - LIKE и ILIKE, "%<то что должно содержаться>%"
startwith и istartwith - LIKE и ILIKE "<то, что должно начинаться>%"
Endwith и iendwith - LIKE и ILIKE "%<должно содержаться в конце хедлайна>"
in - in в SQL
gt >, gte >=, lt <, lte <=
Range соответствует оператору between
IS NULL соответствует проверке на NULL в SQL.
"""
# ** Lookups with relationships. Фильтрация по связанной сущености
# делается через двойное подчеркивание __table_pole_name
entries = Entry.objects.filter(blog__name=("Beates Blog"))

# Обращение к обратным отношениям (reverse) используется имя класса low_registr
entries = Entry.objects.filter(blog__authors__name=("Lennon"))

# чтобы вывести только одну сущеность из множества испольуется .distinct()
entries = Entry.objects.filter(blog__authors__name=("Lennon")).distinct()

# метод SQL (обход ограничений.. Дебил учитель не может объяснить)
Blog.objects.filter(entry__isnull=False, entry__headline__isnull=True)

# ** Order by. Сортировка выборки
blogs = Blog.objects.all().order_by('name')  # сортировка по столбцу name
# для сортировки по нескольким полям, простое перечисление
blogs = Blog.objects.all().order_by('-name', 'tagline')  # -""в оратном порядке

# ** Limit & Offset - лимиты и смещения.
blogs = Blog.objects.all()[:5]  # получить первые пять значений
blogs = Blog.objects.all()[5:10]  # с 5-го по 9-й

"""# _QuerySet — ленивый. Можно сколько угодно раз вызывать фильтр exclude у
QuerySet, но Django выполнит запрос только тогда, когда будет вызвана операция
обращения к данным (evaluation).
Iteration. QuerySet итерируемый объект. Выполняет запрос при 1-м обращении
Slicing. Limit, Offset
len() - выполняет запрос и считает количество записей (для этого есть count)
List() принудительное выполнение путем вызова list() на QuerySet
bool(), тестирование в контексте bool
"""
# _.aggregate Агрегация, это когда нужно посчитать количество блогов всего.
blogs.objects.all.count = blogs.objects.all.aggregate  # одинаковые запросы
Blog.objects.all().count()  # посчитать сколько всего имеется блогов
# агрегационная функция и поле, по которому нужно агрегировать.
Blog.objects.all().aggregate(Count('pk'))  # сколько всего данных с полем "pk"

# посчитать разницу между максимальным кол-м просмотров и его сред. значсением
Entry.objects.aggregate(diff=Max('views', output_field=models.FloatField())
                        - Avg('views'))

# совмещение с фильтрами (только до агрегации)
Blog.objects.filter(name='name').aggregate(Count('pk'))

# _.annotation Анотация, для подсчета количества entry у каждого блога
blogs = Blog.objects.annotate(Count('entry'))
# в .annotate() можно вызывать фильтр как до так и после анотации
blogs = Blog.objects.annotate(Count('entry')).filter(entry_count__gt=0)
blogs = Blog.objects.filter(name='name').annotate(entry_count=Count('entry'))
# также можно сортировать антоции по order_by
Blog.objects.annotate(entry_count=Count('entry')).order_by('-entry_count')

""" Существуют альтернативные ОРМ (синтаксис общения с базой данных)
https://www.sqlalchemy.org/
http://docs.peewee-orm.com/en/latest/
"""
# endregion -------------------------------------------------------------------

# region #* CSS, JS -----------------------------------------------------------
"""
Все примеры в файлах проекта.

#** CSS и JS файлы хранятся в папках static. Либо в корне проекта (глобальные),
либо в корне папки приложения.
Для хранения статических элементов приложения - app_name/static/app_name/
Для хранения стилей приложения -  app_name/static/app_name/css/file_style.css
Подключаются в необходимых html страницах приложений, либо через наследование.

#** Bootstrap и Jquery устанавливаются в следующие структуры:
.../static/bootstrap/css/ или .../static/bootstrap/js/
.../static/jquery/
Могут в глобальный static проекта, а могут в static приложений.
Подключаются в глобальный base.html, после чего доступны во всем проекте через
наследование.

#** Шаблоны страниц (templates) хранятся в папках templates по такому же
принципу как и css/js Для облегчения доступа к templates внутри приложений,
создается струткура папок ./app_name/templates/app_name. Доступ к шаблону
приложения в этом случае по синтаксису "app_name/filename.html"
Подключаются через мехнизм ./app_name/views.py и урлов - ./project_name/urls.py
Кроме шаблонов страниц в templates хранятся блоки встраиваемого кода. Данные
блоки встраиваются в страницы через механизм наследования (в основом include)
"""
# endregion -------------------------------------------------------------------

# region #* Динамический контент (работа с базой данных) ----------------------
"""
# _Сначала необходимо создать базу. SQLight уже создана при создании проекта
Джанго и находится в корневой папке проекта. Можно перенести с ./src или ./bd
Если необходимо использовать базу mysql, то нужен коннектор. Для его установки
#** pip install mysqlclient
Подключение к базе данных - settings.py/DATABASE. ENGINE меняем на необходимый
для mysql - django.db.backends.mysql, для SQLight - стоит по дефолту. Настройки
в разделе Базы данных в Джанго (теория). Для SQLight установки по дефолту.
Для MySQL - редактируем NAME, USER, PASSWORD. HOST: 127.0.0.1, PORT:3306 дефолт
OPTIONS — зависит от базы данных. Словарь. Для кодировки {'charset': 'utf8mb4'}

# _После настройки, необходимо применить миграции:
#** python manage.py migrate
В этот момент создаются дефолтные таблицы auth и django, формы auth_tablename и
django_tablename, где первое — название приложения, а второе — название таблицы
Теперь можно подключаться к базе данных. Для mysql - mysql -u username -p

# _Создаем модели в ./core/models.py (пример:)
class(таблица) Category(models.Model):
    title(поле) = models.CharField(max_lenght=255)

class Topic (models.Model):
    title = models.CharField(max_lenght=255)
    body = models.TextField()
    categories = models.ManyToManyField(Category,related_name='topics')
Создаем миграцию
#** python manage.py makemigrations app_name
В ./core/migrations/ создался файл миграции.
Для применения этой миграции:
#** python manage.py migrate
На основе созданых моделей, в базе создались таблицы по шаблону:
app_name/model_class_name: По настоящему примеру - core_category, core_topic
и core_topic_categories (является связкой ManyToMany между Category и Topic).
Для заполнения содержимого топиков необходимо открыть shell:
#** python manage.py shell
В открывшейся консоли, импортируем модели:
#** from core.models import Topic, Category
и создаем два топика:
#** topic1 = Topic.objects.create(title='First Topic', body= 'body')
#** topic2 = Topic.objects.create(title='Second Topic', body='body2')
Cоздание трех категорий
#** category = Category.objects.create(title='Category 1')
#** category2 = Category.objects.create(title='Category 2')
#** category3 = Category.objects.create(title='Category 3')
Добавление Topic1 в три категории, а Topic2 в две категории. Для этого:
#** topic1.categories.add(category, category2, category3)
#** topic2.categories.add(category2, category3)
После заполнения содержимого, выходим изх консоли.
Написание обработчиков происходит в ./app_name/views.py
#** def index(request):
#**     topic = Topic.objects.all()... См файл views.py, комменатрии там.
Далее, в шаблоне ./core/templates/topic_list.html через циклы формируем шаблон
#** см пример в шаблоне, div class="topic-list"
Для шаблона категорий ./core/templates/category.html также используется цикл:
#** см пример в шаблоне, div class="category"
Чтобы сделать переход на topic также динамическим, изменяем
#** ./project_name/views.py/topic details
"""
# endregion -------------------------------------------------------------------

# region #* HTML, создание форм -----------------------------------------------
"""#** py manage.py startapp forms
создаем приложение forms. Появляется папка приложения с таким же названием.
settings.py/INSTALLED_APPS подключаем к проекту: 'forms.apps.FormsConfig'

"""
# endregion -------------------------------------------------------------------
