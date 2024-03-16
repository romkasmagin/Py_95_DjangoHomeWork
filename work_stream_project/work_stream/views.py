from django.shortcuts import render, redirect, get_object_or_404
from work_stream.models import Project, Tag
from work_stream.forms import ProjectForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    return render(request, 'projects/projects.html', context)


def project(request, project_id):
   project = Project.objects.get(id=project_id)
   tags = project.tags.all()
   form = ReviewForm()
   if request.method == 'POST':
       form = ReviewForm(request.POST)
       review = form.save(commit=False)
       review.project = project
       review.owner = request.user.profile
       review.save()
       project.getVoteCount
       messages.success(request, 'Ваш отзыв был добавлен!')
       return redirect('project', project_slug=project.slug)
   return render(request, 'projects/single-project.html', {'project': project, 'form': form})


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


def update_project(request, project_id):
    project = Project.objects.get(id=project_id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'projects/delete.html', context)


def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    context = {
        'projects': projects
    }

    return render(request, 'projects/projects.html', context)
