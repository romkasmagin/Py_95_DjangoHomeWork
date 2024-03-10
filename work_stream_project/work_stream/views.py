from django.shortcuts import render


def projects(request):
    projects_list = [{'id': 1,
                     'title': 'Онлайн кинотеатр',
                     'description': 'Кинотеатр с самой '
                                    'полной бибилиотекой фильмов.'},
                     {'id': 2,
                     'title': 'Платформа с ИТ-курсами',
                     'description': 'Курсы по фронтенду, бэкэнду и мобилке.'},]

    return render(request, 'projects/projects.html', {'projects':projects_list})


def project(request):
    return render(request, 'projects/single-project.html')
