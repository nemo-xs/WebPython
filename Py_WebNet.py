# region #* импорт, global ----------------------------------------------------
import requests  # модуль работы с сетевыми запросами
import json  # модуль для работы с json объектами
import re  # библиотека re (регулярные выражения)
from bs4 import BeautifulSoup  # импорт beutifulsoup 4 (модуль)
# endregion -------------------------------------------------------------------

# region #* Теория сети -------------------------------------------------------
"""Интерфейс - набор примитивных операций, которые нижний уровень предоставляет
верхнему. Протокол - правила и соглашения для связи уровня n одногокомпьютера с
уровнем n другого компьютера.
Стандарты сетей. Модель взаимодействия открытых систем OSI и модель TCP/IP.
"""
"""#? Модель TCP/IP включает в себя четыре уровня:
прикладной, транспортный, сетевой и уровень сетевых интерфейсов.
#** Network access layer - Уровень сетевых интерфейсов.
Для TCP/IP любая подсеть, это средство транспортировки пакетов между двумя
соседними узлами. Его задачей является упаковка IP пакета в единицу данных
промежуточной сети и преобразование IP адресов в адреса технологии данной
промежуточной сети.
#** Network layer - Сетевой уровень.
Служит для образования единой транспортной системы, объединяющей несколько
сетей, причем эти сети могут использовать совершенно разные технологии передачи
данных. Протоколы сетевого уровня поддерживают интерфейсы с уровнем выше,
получая от него запросы на передачу данных по составной сети.
Примером протокола сетевого уровня является IP.
#** Transport layer - Транспортный уровень.
Примером проколов транспортного уровня является протокол TCP или UDP.
Обеспечивает передачу данных между процессами. Особенностью транспортного
уровня является управление надежностью. Уровень предоставляет приложениям или
верхним уровнем стека передачу данных с той степенью надежности, которая им
требуется.
Например, нужно передать очень большой файл. Этот файл будет передаваться по
сети небольшими кусочками. Необходимо обеспечить, чтобы все эти кусочки пришли
и еще в правильном порядке.
Для адресации на транспортном уровне используются порты. Каждое приложение на
хосте имеет свой порт. Номера портов и приложений не должны повторятся.
#** Application layer — Прикладной уровень.
Набор разнообразных протоколов, с помощью которых пользователи сети получают
доступ к разделяемым ресурсам. В модели считается, что если приложению нужны
какие-то функции представления информации, например, шифрование или управление
сеансом связи, то оно должно само их реализовывать.
Примерами протоколов прикладного уровня являются протоколы HTTP или FTP.
"""
"""#? OSI — это модель взаимодействия открытых систем. Open systems
interconnection, стандарт, принятый по стандартизации ISO. Обычно нумерация
начинается с уровня, который находится ближе всего к среде передачи.
Физический уровень, канальный, сетевой, транспортный, сеансовый, уровень
представления и прикладной уровень.
"""
# endregion -------------------------------------------------------------------

# region #* HTTP-протокол -----------------------------------------------------
"""HTTP работает поверх протокола TCP.
Для начала необходимо установить соединение с сервером, после этого клиент
формирует запрос и передает его на сервер, сервер как-то обрабатывает этот
запрос, подготавливает данные, формирует ответ и отправляет этот ответ клиенту.
Клиент его получает и закрывает HTTP соединение.
Сначала идет метод HTTP запроса, потом идет URL путь и после этого идет версия
HTTP протокола.

#** Методы HTTP запроса:
- GET запрос информации от сервера
- HTAD аналогичен get запросу, только мы говорим, выполни get запрос, но не
присылай нам тела этого запроса.
- POST отправка данные на сервер (публикация)
- PATCH для изменения отправленных данных. Отправили данные,они сохранилась
на сервере, после этого понадобилось изменить и patch-ем отправляем изменения.
- DELETE удаление данных
- PUT создание/замена рессурса

#** Заголовки HTTP запроса:
- host, это доменное имя или IP адрес узла, к которому обращается клиент.
- Referer это URL, откуда пришел клиент, например, если мы из google.com
переходим на docs.google.com, то в referer-е запрос docs.google.com будет
указывать только google.com.
- Accept это типы данных, которые могут обрабатываться клиентом.
- Accept-Charset это перечень поддерживаемых кодировок,
- Content-Type это тип данных которые содержат тело HTTP, запроса.
- Content-Length это число символов, которое содержит тело запроса.
- conection это директива, которая управляет TCP соединением. Если указать
conection типа live, то соединение не будет закрыто и будет использоваться для
дальнейших запросов
- user-agent - это информация о клиентах, google chromе, Сафарии и т.п.

#** MIME. Это Multipurpose Internet Mail Extension.
MIME используют для определения формата тип и подтип.
Собственно тип указывает класс данных, а подтип указывает формат, например, в
случае HTML, это тег/HTML, в случае картинки в формате PNG это img/png.

Структура HTTP ответа.
Состоит из строки состояния, после строки состояния идут заголовки HTTP ответа.
В совокупности называется заголовком ответа.
После этого идет пустая строка, после пустой строки идет тело ответа.
Строка состояния состоит из версий протокола, статуса HTTP ответа и расшифровки
этого ответа.

#** Коды ответов или статусы.
- 1хх это информационный класс сообщений. Говорит - сервер продолжает работу.
Например, мы работали по протоколу HTTP, а сервер нас переключил на работу по
протоколу веб сокета и для этого он отправляет статус 101 свичем протокола.
- 2хх Ответы означают успешную обработку запроса. Например 200, когда сервер
отдает страницу. Или 201, когда отправили серверу данные, он их принял,
сохранил и ответил 201 created.
- 3хх, это перенаправление запроса. Если ресурс переехал на другой адрес,сервер
ответит 301 move permanently [inaudible]. В случае, если переехал на время, 302
- 4хх, Ошибка клиента. Некорректный HTTP запрос, сервер ответит 400 BadRequest.
У клиента недостаточно прав для доступа к ресурсу, ответят 403. Обращение к
ресурсу, которого не существует, 404 и тд.
- 5хх Ошибки сервера. Если бизнес логика сервера некорректно отработала, 500. В
случае, если сервер приложений не отвечает, промежуточный сервер ответит 502.

#** Заголовки ответа. Это Server, это имя и номер версии сервера, который
обрабатывает HTTP запрос, например [inaudible] апач и так далее.
- Allow, это список методов, которые доступны для данного ресурса.
- Content-Type это тип данных, которые содержится в теле.
- Content-lengths это их длина.
- Last-Modifief это дата и время последнего изменения ресурса.
- Expires это дата, когда информация устареет.
- Location расположение ресурса. Например сервер прислал, 302 и говорит
переместиться на другой ресурс. Собственно оттуда браузер возьмет информацию и
перейдет на другой ресурс.
- Кэш-контроль эта директива, которая управляет кэшированием, если указать
кэш-контроль на у-кэш, то данные, которые приходят с сервера, никогда не будут
сохранены или закэшированы.

#** Как работает протокол HTTP.
GET/HTTP, то есть стартовая строка, хост, директива conection, кэш контроль,
user agent и типы данных, которые мы можем принимать.
В отывет получаем HTTP ответ со статусом 200, с данными и контент-тайпом HTML.
"""
# endregion -------------------------------------------------------------------
"""
# region #* библиотека requests -----------------------------------------------

#** Query string - для передачи пользовательских данных
Это не иерархическая часть url. Набор параметров в виде (ключь: значение).
В Query string передаются либо ASSCI либо кодированный юникод. Часто применют
для выборки неких объектов.

#** Request body - также для передачи пользовательских данных
Через него передаются структурированные данные. Вт.ч. данные форм включая файлы
также через него передают json, xml,

# передача get параметров (словарь).
payload = {'key1': 'value1', 'key2': 'value2'}

# для передачи заголовков - словарь. Ключ - имя заголвка, Значение - значение
headers = {'user-agent': 'my-app/0.0.1'}

# для передачи кукиз авторизации, или дургих
cookies = dict(cookies_are='working')

# _Выполнение get запроса. Дополнительно передаются get-параметры, заголовки и
# кукиc. При необходимости, запрет на редирект.
r = requests.get('http://httpbin.org/get', params=payload,
                 headers=headers, cookies=cookies, allow_redirects=False)

# _Выполнение post запроса с передачей post,put и patch данных и json данных.
# При передаче json данные передаются и в поле дата и в поле json. По такому же
# приницпу реализована передача файла (files=filse)
r = requests.post('http://httpbin.org/post',
                  data=json.dumps({'key': 'value'}), json={'key': 'value'})

r = requests.put('http://httpbin.org/put', data={'key': 'value'})

print(r.text)  # получение простого ответа от сервера
print(r.headers)  # получить заголовки http ответа
print(type(r.text), r.text)  # получение ответа с типом string
print(type(r.content), r.content)  # получение ответа в виде байт массива
print(type(r.json()), r.json())  # получение ответа в виде словаря json
print(r.status_code)  # получить статус ответа сервера

# сравнить полученный ответ с ответом с ответом из библиотеки requests
print(r.status_code == requests.codes.ok)
# bad_r.raise_for_status()  # для выбрасывания исключения

print(r.url)  # получить истинный url от сервера (в т.ч. с учетом редиректа)
print(r.history)  # получить history запроса, в т.ч. redirect

# _Session Objects - сессия
# После объявления сессии, все последующие запросы выполняются с теми же
# параметрами, что и предыдущие.
s = requests.Session()  # объявление сессии
# get запрос сессии, в которой установлены куки '123456789'
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('http://httpbin.org/cookies')  # куки добавляются в рамках сессии
print(s.cookies)  # получение используемых в сессии кукис
print(r.text)

s = requests.Session()  # объявление сессии
s.headers.update({'x-test1': 'true'})  # установка параметров сессии x-test1

# При передаче запроса, содержащего только заголовок x-test2, в отете получим
# заголовки содержащие как x-test2 так и x-test1 (из параметров сессии)
r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
print(r.text)

# region #? формирование запроса OpenWeatherMap ------------------------

# вместо 1-й строки можно формировать ссылку через параметры запроса
resp = requests.get(
    "http://api.openweathermap.org/data/2.5/weather",
    params={
        "q": "Moscow",
        "APPID": "7543b0d800ce423bab3b2f6ad38df30b",
        "mode": "json", "units": "metric"
    }
)
data = resp.json()
print(data['main']['temp'])
# endregion #?---------------------------------------

# endregion -------------------------------------------------------------------
"""
# region #* регулярные выражения, библиотека "re" -----------------------------
# https://habr.com/ru/post/349860/
# https://stepik.org/lesson/24470/step/2?unit=6776
# https://www.coursera.org/learn/python-for-web/lecture/3Oxp1/poisk-s-pomoshch-iu-rieghuliarnykh-vyrazhienii

# region # ?Получение курса Евро с сайта Центробанка --------------------------
# Извлечение данных из полученного массива (html, json, xml и т.п) происходит
# с помощью библиотеки re, и регулярных выражений.

# ** раскомментрировать блок --------------------------------------------------
# result = requests.get('http://cbr.ru')  # get запрос на сайт ЦБ
# html = result.text  # html код страницы лежит в атрибуте text класса requests
# coin = "Евро"  # Переменная валюта. Использование в шаблоне поиска и печати
# ** --------------------------------------------------------------------------

# _для поиска делаем маску, где r - регулярное выражение. Ищем слово Евро.
# r - указание, что это регулярное выражение
# (\D) - пропускает все что не является цифрами.
# (+) - указывает что тут не может быть цифр и может повториться несколько раз.
# () - группа. То что находится в (них), модуль запоминает
# (\d+,\d) - указание, что мы ищем цифры, запятую и еще цифры
# Все что находится в () будет возвращено в перовой группе объекта match

# _базовый запрос:
# mach = re.search(r'Евро\D+(\d+,\d+)\D+(\d+,\d+)', html)

# _подстановка методом str.format(...).То что в () подставляется на место {}
# mach = re.search(r'{}\D+(\d+,\d+)\D+(\d+,\d+)'.format(coin), html)

# ** раскомментировать блок --------------------------------------------------
# _подстановка методом f-string, которая допускает в {указывать переменные}
# mach = re.search(rf'{coin}\D+(\d+,\d+)\D+(\d+,\d+)', html)

# print("Курс", coin, "по данным ЦБ РФ составляет: ")
# print("Продажа - ", mach.group(1))  # данные в первой группе () объекта match
# print("Покупка - ", mach.group(2))  # данные второй группы () объекта match
# ** --------------------------------------------------------------------------
# endregion #? ------------------------------------------

# _Метасимволы в строках, экранируются от текста через '\' (без кавычек)
# _Метасимволы . ^ $ * + ? { } [ ] \ | ( )
"""Ключи: "| re.DOTALL" - включая перевод строки, re.IGNORECASE - игнорировать
регистр букв, re.ASCII - только символы латинского алфавита и цифры """

"""#_ '.' любой символ кроме переноса строки. Заменяет любой входящий символ.
то есть abcdef найдется по ab..ef (без скобок). Можно совмещать с *, +, итп.
чтобы '.' включала в себя перевод строки, #_ добавляется "| re.DOTALL"

#_  '^' - начало строки. '$' - конец строки. Если multyline, то всего текста

#_  '*', "+" - любое количество повторяющих тот что перед * символов, то есть
# abbbbbc = ab*c, при этом если "+" то кол-во символов должно быть > 0

# _ '+' или '*' по умолчанию являются "жадным" и ищут по самой длинной фразе.
'.*' - самое дорогое. Берет весь текст и выкидывает по 1-му символу. Форма
записи ab[ab]*d - будет искать самые длинные вхождения, а если наборот, надо
искать самые короткие вхождения, то вместе с * добавляем ? то есть запись
ab[ab]*?d - будет искать самое короткое вхождение. Надо использовать с ?

# _"?" - количество повторяющихся вхождение должно быть или 0 или 1.

# _Если нас интересует конкретное количество вхождений символа, то он
указывается в {} - ab{4}c = 4b, а если ab{2,4}c - то ищем от 2-х до 4-х b.
Синтаксис итератора. a{,5} = от 0 до 5. b{3,} от 3-х до бесконечности.
Таким образом '*' = {0,бесконечность}; '+' = {1,бесконечность}; '?' = {0,1}"""

# _Автономер:1 буква из используемых в номерах, 3 цифры, 2 буквы, 1 или 2 цифры
car_number = r"[АВЕКМНОРСТУХ}]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}"


"""# _Символьный класс - набор символов, из которого используется 1-н символ.

# _внутри [] указываются подходящие символы,или диапазон. Через '-' [a-zA-Z]
(как пример такой записи - все буквы английского алфавита). Если внутри []
стоит ^ это значит что указанный диапазон не подходит [^b-z] или [a-z^A-Z]
что означает, что подходят только маленькие буквы, а большие - нет."""

# _\d - цифры, = [0-9]. Если \D то не цифры, = [^0-9] = [^\d]

# _\s - пробельные символы [\t\n\r\f\v]. \S наоборот = [^\t\n\r\f\v] = [^\s]

# _\w - буквы + цифры + _ [a-zA-Z0-9_]. \W наоборот  = [^a-zA-Z0-9_] = [^\w]

# _\b - граница слова. Между \w и \W. {0} символов. \B позиция внутри слова

# _[] при сокращенной записи не используют "abc[a-zA-Z0-9_]de" = "abc\wde"

# _[] испольуется при совмещении "abc[a-zA-Z0-9_юра]de" = "abc[\wюра]de"


# _метасимволы можно группировать через (), как пример
pattern = r"(test)*"  # ищет любое вхождение фразы в скобках

pattern = r"(test|text)*"  # ищет или test или text, с любым кол-ом вхождений
# символ | (или) можно ставить и вне скобок, например r"abc|(test|text)*"
# c помощью скобок можно группировать как угодно r"((abc)|(test|text)*|(bcd))"
# с помощью ?: можно указывать, то что в () не является группой для вывода.
# (?:.|.) - то что внутри () это группа, но не для внешей группировки вывода

# перед закрытием скобки через \ стоит номер группы которая нам нужна, то есть
pattern = r"((abc)|(test|text)*|(bcd)\2)"  # вызовет вторую группу. группы
# считаются с первой открывающей скобки, 1-я группа - все выражение целиком итд

hellow2 = "Привет, Василий!"  # Создание строковой переменной
pattern = r"abcd, Василий!"  # создание паттерна (см выше)

pattern = r"Пр[ивював]ет[,.-] Василий[!.ура]"  # в [] указываются возможные
# варианты, то есть в средних [] будут проходить и ',' и '.' и '-' а в конечных
# [] и '!' и '.' и 'у' 'р' 'а' (или их сочетание)

re.search(pattern, hellow2, re.IGNORECASE)  # ищет вхождение строки в шаблон, а
# IGNORECASE говорит игнорировать заглавные буквы

re.match(pattern, hellow2)  # проверяет подходит ли строка под заданный шаблон

re.findall(pattern, hellow2)  # ищет все вхождения патерна в строку

re.sub(r'ве', "ва", hellow2)  # заменяет все вхождения шаблона 'ве' на "ва"

re.sub(r'(\w)\1', lambda r: r.group(0).upper(), hellow2)  # использование
# lambda в регулярных выражениях. В данном случае возвращает заглавные буквы.

reg = re.compile(pattern)  # компиляция регулярного выражения. Имеет смысл при
# множественном использовании. Затем, для использования, reg.method("source").
# Удобно применять в циклах reg.match(), дает True/False, либо при поиске по
# многим источникам reg.findall(), reg.search('source')

# region #? Примеры использования регулярных выражений ------------------------
# Найти все действительные числа, например: -100; 21.4; +5.3; -1.5; 0
res = re.findall(r"[-+]?\d+(?:\.\d+)?", hellow2)

# Проверить, что строка это серийный номер вида 00XXX-XXXXX-XXXXX-XXXXX, где X
# - шестнадцатиричная цифра
re.match(r"^00[\da-f]{3}(?:-[\da-f]{5}){3}$", hellow2, re.IGNORECASE)

# Проверить, что строка является корректным IPv4 адресом
re.match(r"^((25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(\.|$)){4}(?<!\.)$", hellow2)

# Проверить, что логин содержит от 8 до 16 латинских букв, цифр и _
re.match(r"^\w{8,16}$", hellow2)

# Проверить, что пароль состоит не менее чем из 8 символов без пробелов. Пароль
# должен содержать хотя бы одну: строчную букву, заглавную, цифру
re.match(r"^(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{8,}$", hellow2)

# Переформатировать код, убрав лишние пробелы между def, именем функции и (
# Например: def    myFunc   (x, y):  => def myFunc(x, y):
re.sub(r'def\s+(\w+)\s*\(', r'def \1(', hellow2)

# Заменить все "camel_case" на "сamelCase"
# Например: my_function_name, peer__2__peer  =>  myFunctionName, peer2Peer
re.sub(r'_+([a-zA-Z\d])', lambda x: x.group(1).upper(), hellow2.lower())
# endregion #?------------------------------------------------------

hellow2 = "Привет, Василий!"  # Создание строковой переменной

f'{hellow2}'  # _f-string, принимающая значение hellow2. Передает содержание
# переменной. на выходе "Привет, Василий!" https://python-scripts.com/f-strings

f'{hellow2=}'  # Строка передает название и значение переменной (новинка P 3.8)
# то есть на выходе: "hellow2 = 'Привет, Василий!'"

# имя = бибилиотека re, метод search, (маска разбирающая переменную и ее имя)
name = re.search(r', (.*)!', hellow2)

# имя = бибилиотека re, метод search, (маска разбирающая переменную и ее имя)
if name:  # когда просто # * if name: без всяких условий, сравнений или ==
    # подразумевается "если name == True (то есть оно просто существует)"
    print(name.group(1))  # печатать группу из полученной переменной name

if (name := re.search(r', (.*)!', hellow2)):
    print(name.group(1))
# Тоже самое что в верхнем блоке, но запись с использованием нового оператора
# присваивания ':=' (появился в Питоне 3.8)#//(PeP не обновился. потому ошибка)
# endregion -------------------------------------------------------------------

# region #* Beautiful Soup ----------------------------------------------------
"""Beautiful Soup это модуль для извлечения данных из HTML и XML, в том числе
из HTML и XML с плохой разметкой, в которой есть не закрытые теги, неправильные
атрибуты и так далее. LXML строит дерево синтаксического разбора, по которым
можно искать, манипулировать и получать различные данные из HTML и XML.
#_ pip install beautifulsoup4
Для работы в Beautiful Soup нужен parser. Beautiful Soup преобразует полученные
данные в дерево, но сам разбирать на низком уровне HTML и XML не умеет.
html parser - встроен в питон. Не умеет работать с XML.
LXML - parser лояльный к некачественной разметке, умеет работать с XML. BS его
использует самостоятельно, как свою часть. Отдельного import не требуется.
#_ pip install lxml
Полученный от parser результат, как строку - в объект Beautiful Soup и получаем
объект разложенный по тэгам, с методами soup.body.p['id']
https://www.coursera.org/learn/python-for-web/lecture/Xoihi/vviedieniie-v-beautiful-soup
"""
# soup. ... wrapper_tag. ... inner_tag.in_inner_finish_tag['index or key']
# soup. ... wrapper_tag('inner_tag')(search_index)['finish_condition']
# soup. ... wrapper_tag. ... method('search_condition')['index or key']

parser_text = """<!DOCTYPE html>
<html lang='en'>
<head> <title>page title </title> </head>
<body class='mybody' id='js-body'>
    <p class='text odd'>first <b>bold</b> paragraf</p>
    <p class = 'text even'>second <a href='https://mail.ru'>link </a></p>
    <p class = 'list odd'>third <a id='paragraf'> <b>bold link</b> </a></p>
</body>
</html>
"""
# имортируем источник (строим дерево тегов). 2-й агрумент - модуль lxml
soup = BeautifulSoup(parser_text, 'lxml')

soup  # вывод полученного как есть кода
soup.prettify()  # вывод отформатированного с отступами полученного кода

""" Вызов содержимого тегов происходит по иерархии. Родительский тег body,
затем в нем дочерний элемент p, в нем, дочерний элемент b и так далее..
При этом если не указывать родительские элементы, ищет первый указанный тэг в
теле документа. Это касается всех методов, можно указывать все родительские
теги, тогда ищет в них. Если не указано, то ищет первый найденный без учета
иерархии.
.name - имя найденного тега
.parent - вывод содержимого родительского тега
.find_parent(id='js-body') - поиск родителя по условию в ()
.find_parent('body')['id'] - поиск родителя (.) и вывод содержимого ключа [.]
.parents - генератор всех родительских тегов (через цикл for)
.contents - список всех вложенных тегов
.children - генератор вложенных тегов (через list, или через for)
.next - следующий за тегом элемент, внутри него же.. <p... first ... </p>
.next.next - второй по списку <p... f.. <b>bold</b> ... </p>
.next_sibling - элемент после закрытия тега <p>..</p> next_sibling
.find_next_sibling(class_='odd') - поиск следующего элемента по условию. Нижнее
    подчеркивание после class_ - потому что без _ резервное слово Python
.find(id='js-body')['class'] - найти первый по id и вывести по ключу 'class'
.find('b', text='bold') - первый аргумент - в каких тегах искать, второй - по
    каким параметрам искать
.find_all('p', 'list odd') - найти все p попадающие под условие. Список
.select('p.text.odd') - найти все p имеющие классы text и odd
.select('p:nth-of-type(3)') - вывести третий тэг p в документе
"""
soup.body.p.b.string  # 'bold' - родитель(body)/родитель(p)/(вывод)/метод
soup.p  # <p class=" ... </p> обращение к 1-му найденному тегу p
soup.p.name  # 'p' вывод имени найденного тега
soup.p.parent  # '<body class> ..... </body>' вывод родителя (целиком)
soup.p.b.find_parent(id='js-body').name  # 'body' поиск родителя по условию
soup.p.b.find_parent('body')['id']  # 'js-body' вывод по ключу как словарь
soup.p.contents  # ['first', '<b>..</b>', 'paragraf'] список дочерних тэгов
list(soup.p.children)  # ['first', '<b>..</b>', 'paragraf'] через генератор
soup.p.next  # 'first' вывод следующего за тегом p элемента, без учета закрытия
soup.p.next.next  # '<b>bold</b>' следующий, следующий..
soup.p.next_sibling  # '\n' следующий за тегом p элемент с учетом закрытия </p>
soup.p.next_sibling.next_sibling  # <p class = 'text even'> ... </p>
soup.p.find_next_sibling(class_='odd')  # <p class = 'list odd'>third ... </p>
soup.p.b  # '<b>bold</b>' 1-й найденный элемент p и внутри него 1-й элемент b
soup.p.b.string  # 'bold' вывод содержимого элемента. Далее методы string
soup.p.find('b')  # '<b>bold</b>' найти все элементы b внутри тэга p
soup.find('b', text='bold')  # найти все b в которых есть текст bold
soup.find(id='js-body')['class']  # ['mybody'] найти по id.. и вывести по ключу
soup.find_all('p', 'list odd')  # [p class = 'list odd'> ... </p>, ]
soup.select('p.odd.text')  # [[p class = 'text odd'> ... </p>, ]]
soup.select('p:nth-of-type(3)')  # [p class='list... </p>, ] 3-й p в документе
soup.select('a > b')  # [<b>bold link</b>] найти <b> который есть внтури <a>
[i.name for i in soup.find_all(name=re.compile('^b'))]  # совещение с re
[i for i in soup(['a', 'b'])]  # все <a> и <b> которые есть в документе
soup.body['id']  # 'js-body' - Строка, т.к. id в html всегда строка
soup.p['class']  # ['text', 'odd'] Список, т.к. class в html это всегда список
soup('p')[1]['class']  # ['text', 'even'] - через индекс p (отсчет с 0-ля)

"""Кроме вывода и фильтрации тегов, через библиотеку BS можно также менять
содержимое документа. Сначала присваиваем некую переменную к нужному тэегу, а
затем меняем ее параметры.."""
tag = soup.b  # присваиваем переменную нужному тегу
tag.name = 'i'  # меняем имя тега с b на i
tag['id'] = 'myid'  # присваиваем id тегу
tag.string = 'italic'  # меняем содержимое тега
print(soup.p)  # вывод измененной строки через родительский тэг
"""
# region #? Парсинг Wikipedia.org -------------------------------
resp = requests.get("https://wikipedia.org/")
html = resp.text

# _метод разбора с помощью биюлиотеки re -----------------
# ищем все, в открывающемся тег а, внутри которого пропускаем что угодно кроме
# закрытия тега. Затем ищем other..., пропускаем все кроме закрытия тега. Затем
# ищем блоки href? внутри него ищем все, что в '' и запоминаем ().
# На выходе имеем список сервисов википедии. Выражение не универсальное..

print(re.findall(r'<a[^>]*other-project-link[^>]*href="([^"]*)"', html))

# _метод разбора через BeautifulSoup ---------------------
soup = BeautifulSoup(html, 'lxml')  # импортируем источник(строим дерево тегов)
tags = soup('a', 'other-project-link')  # findall все теги а с классом other...

# полученные выше теги являются списком объектов bs-tag. Чтобы выделить из них
# ссылки, запускаем генератор, который ищет все href внтри списка, обращаясь к
# нему как к индексу словря
print([tag['href'] for tag in tags])  # метод цикла list comprihation

# можно написать более короткую запись совместив строки findall и listCompr...
[tag['href'] for tag in soup('a', 'other-project-link')]
# endregion #? -----------------------------------------
"""
"""
# region #? Парсинг mail.ru -------------------------------------
# https://www.coursera.org/learn/python-for-web/lecture/oiYcs/slozhnyi-poisk-i-izmienieniie-s-beautiful-soup

result = requests.get("https://news.mail.ru/")
html = result.text
soup = BeautifulSoup(html, 'lxml')

# Собираем список секций и всех новостей, которые в нее входят. Для этого, в
# исходном коде ищем секцию. Здесь она span с классом hdr__inner. Сразу делаем
# список. Поэтому все выражение в [].
# Выводим section.string (имя секции), для каждой section (секции ), которую мы
# находим soup.find_all во всех тегах span с классом hdr__inner. Получаем код
# [section.string for section in soup.find_all('span', 'hdr__inner')]

# Чтобы кроме названий секций вывести также и их содержимое, делаем кортедж из
# section.string, где первый элемент название секции а вторым - набор ссылок,
# которые в него входят. (section.string, [link.string]).

# Ссылка здесь, это span у которого есть класс link__text. Но, искать надо не
# все подряд, а для каждой секции.. Для этого надо найти общего родителя секции
# и всех ее ссылок. В данном случае, он является 4-м если считать от section.
# От найденной секции, ищем всех родителей section.find_parents(), берем 4-го
# из найденных [4]. И от него, ищем вниз все его дочерние span имеющие класс
# link__text. Получаем section.find_parents()[4].find_all('span','link__text')

# Для получения списка ссылок в секции, запускаем генератор списка:
# link.string for link in section_finder
# где перебираем все link.string для всех link в полученных ссылках.

print([
    (section.string,
     [link.string for link in
      section.find_parents()[4].find_all('span', 'link__text')])
    for section in soup.find_all('span', 'hdr__inner')])

# endregion #? -----------------------------------------
"""
# endregion -------------------------------------------------------------------

# region #* web API -----------------------------------------------------------
"""API - программный интерфейс приложения. Это интерфейс для взаимодействия
одних программ с другими. Когда мы говорим, об апи в применении к вебу, это
называется веб-апи. Как правило, это урл или набор урлов, на которые мы можем
делать http-запросы, передавая свои данные, и получать в ответ какие-то данные,
отформатированные, как правило, в JSON или XML.
Многие инфо сайты предоставляют свои данные в виде xml изначально.
Каждый RSS это тоже своего рода API, поскольку в ответ дает более понятные для
разбора данные.
Многие сайты, и сетевые сервисы типа Телеграмм, VK - дают полноценный удаленный
интерефейс управления данными, что является наиболее широким понятием API.
У каждого сервиса или сайта свой API, универсального нет. Есть документация.
#** REST - общая теория создания API.
Название/версия/коллекция данных/метод запроса /api/v1/users/:id(HTTPmethod):
/api/version2/users/(POST)
/api/version2/users/:id(GET)
"""
# endregion -------------------------------------------------------------------

# region #* СУБД --------------------------------------------------------------
"""Система управления базами данных, обеспечивает работу с большими объемами
данных. Обеспечивает управление данными на диске или в памяти, целостность,
резервирование, и, у нее есть какой-то язык для доступа и определения данных.
Типов баз данных бывает очень много, по разным параметрам.
Клиент-серверные - есть отдельно выделенный сервер, а приложение является
клиентом, оно обращается к серверу, сохраняет там данные, получает по протоколу
Встроенные - нет никакого выделенного сервера, система управления встраивается
в приложение и поставляется вместе с ним. Не требует установки.
Также есть, локальные и распределенные базы данных.
Локальные — это когда все файлы, все таблицы, все-все, что есть в этой базе
данных, хранится на одном компьютере.
А распределенные — это когда база данных работает на нескольких серверах.
Бывают также реляционные и нереляционные базы данных.
SQL - Реляционные базы данных — состоят из таблиц и отношений между ними.
NoSQL - нереляционные — хранилище «ключ-значение», там нет никаких связей между
таблицами. Redis, Tarantool - NoSQL базы данных.
"""
""" # _SQL - это набор таблиц, похожих на таблицы Excel. Имеет связи с другими
таблицами. Связи - это ключевой момент. Реляционные базы данных и происходят от
слова "relation" - связь.
Каждая таблица имеет набор строк и столбцов, содержит информацию об объектах
определенного типа. В одной таблице информация об одинаковых по типу объектах.
В каждой строке таблицы находятся данные одного объекта, это может быть пост,
комментарий, пользователь и так далее. А столбцы описывают свойства этого
объекта, например, логин, имя, пароль, если речь идет о пользователе.
Все строки одной таблицы имеют одинаковую структуру. Каждое поле, имеет строго
определенный тип данных: число, строка, дата итп. Все строки имеют один и тот
же набор полей, и каждое поле, имеет определенный тип данных. Структура базы
данных описывается схемой базы данных, которая включает в себя описание
содержания, структуры и ограничения целостности. Описывается эта структура на
языке СУБД, как правило, это SQL.
#** ACID. Atomicity — атомарность, Consistency — согласованность, Isolation —
изолированность и Durability — устойчивость или долговечность.
#** Транзакция — последовательность операций с базой данных, которая либо
выполнена либо целиком, либо полностью не выполнена. Либо все операции пройдут
успешно и деньги переведутся со счета A на счет B, либо вся транзакция будет
отменена, и состояние будет такое, как будто бы она никогда и не проводилась.
#** Индекс используется для повышения скорости поиска данных. Если по полю
построить индекс, то система управления базой данных создаст определенную
структуру, оптимизированную под поиск. Индекс может быть составным, по
нескольким колонкам. Индексов у таблицы может быть сколько угодно. Индекс
ускоряет поиск, но замедляет модификацию данных. Индекс может быть уникальным.
Он не только упорядочивает данные, но еще и делает уникальным поле, по которому
построен индекс.
https://www.coursera.org/learn/python-for-web/lecture/plz9L/rieliatsionnyie-bazy-dannykh
"""
""" # _NoSQL - нет никакой схемы данных, ничего заранее не определено, нет
никаких ограничений, отношений, но из-за этого нет и контроля целостности.
В NoSQL данные денормализованы, в записях могут храниться любые поля.
Вместо ACID, NoSQL рассматривается как набор свойств BASE: базовая доступность
(basic availability), гибкое состояние (soft state), согласованность в конечном
счете (eventual consistency). NoSQL жертвуют согласованностью данных ради
масштабируемости и увеличения доступности. Банки (важные операции) - всегда
SQL. Социальные сети (миллиарды операций ожновременно)- всегда NoSQL.
NoSQL бывают четырех типов: хранилища «ключ-значение», документориентированные,
bigtable-подобные и графовые базы данных.
#** хранилище вида «ключ-значение». MemcacheDB, Redix, Amazon DynamoDB и
Berkeley DB. Самый простой вид нереляционной базы данных. Просто словарь или
ассоциативный массив, который позволяет по уникальному ключу сохранить какое-то
значение. Значение может быть строкой, может быть разных типов: строки, числа,
даже какие-то структуры данных. Хорошо масштабируются. Нет заранее определенной
схемы базы данных. Нет связей между значениями.
Минусы вытекают из плюсов. Из-за того что они такие простые, невозможно делать
какие-то операции, кроме поиска по точному значению ключа.
#** Документоориентированные. MongoDB, CouchDB и Exist. Более сложная версия
хранилищ «ключ-значение». Данные (документы) представлены в виде дерева или
массива деревьев, то есть леса, и у них есть иерархия. Одна запись называется
документом. Есть корневой узел, внутри него - внутренние узлы и листовые узлы,
которые содержат данные. Каждый документ содержит произвольное количество
произвольных полей, записи разнородны. Есть индексы.Не являются заменой SQL. Но
позволяют делать выборки без полного перебора всех документов, быстрые выборки.
Хорошо подходят, когда требуется какое-то упорядоченное хранение информации, но
тем не менее нет множества связей между данными, и не нужна какая-то статистика
по этим данным. Не требует определения какой-то схемы, каждый документ может
состоять из любого количества любых уникальных полей.
#** Bigtable-подобные. HBase, Cassandra, Hypertable и SimpleDB. Есть общий
прародитель, это Google Bigtable. Хранят данные в виде разреженной матрицы.
Столбцы и строки этой матрицы используются в качестве ключей. Матрицы бывают
многомерными: не только столбцы и строки, но, может, еще какое-то третье
измерение, например, время —  получается трехмерная матрица. Разреженная
означает, что несмотря на большие размеры этой матрицы, большинство ее ячеек на
самом деле пустое, данных в ней относительно общих ее размеров не так много.
Имеют очень много общего с документоориентированными базами и применяются для
целей веб-индексирования или схожих задач, предполагающих огромные базы данных,
большое число серверов. Хорошо масштабируются, быстрые и способны работать с
действительно огромными базами данных, что и требуется при веб-индексировани.
#** Графовые базы данных. FlockDB, Giraph, OrientDB, Neo4j. Лучше всего
подходят для тех задач, в которых данные уже по своей структуре представляют
граф. Данные хранятся в виде узлов и связей между ними. Например, в соцсетях
пользователи могут быть вершинами графа, а дружеские отношения между ними —
ребрами этого графа. С помощью графовых баз данных, нетрудно построить списки
общих друзей, узнать через каких друзей два любых человека связаны.
Графовые базы данных гораздо быстрее, нагляднее, удобнее, чем реляционные базы
данных. Хотя все то же самое можно сделать и с помощью реляционных баз данных.
Графовые базы данных могут работать с очень большими графами (Facebook).
"""
# endregion -------------------------------------------------------------------
