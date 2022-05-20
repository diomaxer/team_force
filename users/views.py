from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext

from .models import User, Skills
from .forms import RegisterForm, LoginForm, UpdateSkills, UpdateUserSkills


def all_users(request):
    """Домашняя страница со всеми пользователями кроме админа"""
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, 'home.html', context)


def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login_view(request):
    """Авторизация"""
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            error = 'Почта или пароль введены не верно'
    else:
        form = LoginForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'login.html', context)


@login_required
def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('home')


@login_required()
def lk_view(request):
    """Личный кабинет"""
    return render(request, 'lk.html')


@login_required()
def add_skill_view(request):
    """Добавление и удаление навыков"""
    skill_ids = [skill.id for skill in User.objects.get(id=request.user.id).skills.all()]  # Данные для checkbox initial
    if request.method == 'POST':
        user_skills = UpdateUserSkills(request.POST)
        new_skills = UpdateSkills(request.POST)
        if user_skills.is_valid() and new_skills.is_valid():
            # Функция создания новых навыков и записи выбранных навыков пользлвателю
            user_skills.add_skills(request.user, user_skills.cleaned_data.get('skills'), new_skills.get_skills_query())
            return redirect('lk')
    else:
        user_skills = UpdateUserSkills(initial={"skills": skill_ids})
        new_skills = UpdateSkills()
    context = {
        'user_skills': user_skills,
        'new_skills': new_skills,
    }
    return render(request, 'add_skill.html', context=context)

