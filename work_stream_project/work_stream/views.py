from django.shortcuts import render
from work_stream.models import Project


def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    tags = project_obj.tags.all()
    context = {'project': project_obj}
    return render(request, 'projects/single-project.html', context)
