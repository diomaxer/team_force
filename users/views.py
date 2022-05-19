from django.shortcuts import render

from .models import User
from .forms import CreateForm


def all_users(request):
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, 'index.html', context)


def register(request):
    form = CreateForm()
    return render(request, 'register.html', {'form': form})

