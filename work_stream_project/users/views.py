from django.shortcuts import render, get_object_or_404
from users.models import Profile, Skill


def profiles(request):
    profiles_obj = Profile.objects.all()
    context = {'profiles': profiles_obj}

    return render(request, 'users/profiles.html')


def user_profile(request, projects_slug):
    profile = Profile.objects.get(slug=projects_slug)
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