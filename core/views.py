from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from core.models import Topic, Category  # импорт моделей
from django.db.models import Count
from django.http.response import Http404

# Create your views here.


def index(request):
    """ Создание view для работы с базой данных."""
    # дополнительно применяем анотацию, с подсчетом кол-ва категорий к топику
    topics = Topic.objects.all().annotate(Count('categories'))
    # получаем все категории, чтобы можно было их вывести
    categories = Category.objects.all()
    # передача полученных запросов в контекст
    return render(request, 'core/index.html', context={
        'topics': topics,
        'categories': categories,
    })


def index_first(request):
    """Индексная страница приложения.
    Чтобы было легче использовать, внутри папки templates приложения, создается
    подпапка с именем приложения, и, затем во view легко читать, какое view
    к какому приложению относится.
    """
    return render(request, 'core/index.html')


def my_view_full(request):  # полная запись для вызова шаблона
    # в этом месте прописывается бизнес логика
    t = loader.get_template('myapp/index.html')
    context = {'foo': "bar"}
    return HttpResponse(t.render(context, request))


def my_view_shotcut(request):  # запись с использованием shotcut (render)
    # в этом месте прописывается бизнес логика
    return render(request, 'my_app/index.html', {'foo': "bar"})


def my_view_shot_redirect(request):  # редирект через шоткат
    return redirect('some/url')


def topic_details_old(request):
    return render(request, "core/topic_details.html")


def topic_details(request):
    try:
        topic = Topic.body
    except Topic.DoesNotExist:
        raise Http404
    return render(request, "core/topic_details.html", context={'topic': topic})
