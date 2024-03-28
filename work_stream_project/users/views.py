from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from users.models import Profile, Skill
from users.forms import (CustomUserCreationForm,
                         ProfileForm,
                         SkillForm,
                         MessageForm)


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого пользователя нет в системе')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Аккаунт успешно создан!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(
                request, 'Во время регистрации возникла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles_obj = Profile.objects.all()
    context = {'profiles': profiles_obj}

    return render(request, 'users/profiles.html', context)


def user_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    main_skills = profile.skills.all()[:2]
    extra_skills = profile.skills.all()[2:]
    context = {
        'profile': profile,
        'main_skills': main_skills,
        'extra_skills': extra_skills,
    }

    return render(request, 'users/user-profile.html', context)


def profiles_by_skill(request, skill_slug):
    skill = get_object_or_404(Skill, slug=skill_slug)
    profiles_obj = Profile.objects.filter(skills__in=[skill])
    context = {
        "profiles": profiles_obj
    }

    return render(request, "users/profiles.html", context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile

    skills = profile.skills.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill_slug = request.POST.get('slug')
            skill_description = request.POST.get('description')
            profile.skills.get_or_create(name=skill, slug=skill_slug,
                                         description=skill_description)
            messages.success(request, 'Навык добавлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, skill_id):
    profile = request.user.profile
    skill = profile.skills.get(id=skill_id)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Навык успешно обновлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, skill_slug):
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Навык успешно удален')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'message_requests': message_requests, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, username):
    recipient = Profile.objects.get(username=username)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', user_id=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
