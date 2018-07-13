from django.shortcuts import render, redirect

# Create your views here.

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from .forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'accounts/index.html')


def user_register(request):
    redirect_url = request.POST.get('next', request.GET.get('next', '/'))
    if request.user.is_authenticated():
        return redirect(redirect_url)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_permissions.add(
                Permission.objects.get(codename='add_comment'))
            return redirect(redirect_url)
    form = RegisterForm(initial={'next': redirect_url})
    return render(request, 'accounts/register.html',
                  context={'form': form, 'next': redirect_url})


def user_login(request):
    redirect_url = request.POST.get('next', request.GET.get('next', '/'))
    if request.user.is_authenticated():
        return redirect(redirect_url)
    # if request.method == 'POST':
    #     form = LoginForm(request, request.POST)
    #     if form.is_valid():
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #         user = authenticate(username=username, password=password)
    #         if user is not None and user.is_superuser:
    #             login(request, user)
    #             return redirect(redirect_url)
    #     return render(request, 'accounts/login.html', context={'form': form, 'next': redirect_url})
    # form = LoginForm(initial={'next': redirect_url})
    return render(request, 'accounts/login.html',
                  context={'next': redirect_url})


@csrf_protect
def user_logout(request):
    redirect_url = request.POST.get('next', request.GET.get('next', '/'))
    if request.method == 'POST':
        logout(request)
    return redirect(redirect_url)
