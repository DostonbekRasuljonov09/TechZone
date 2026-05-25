from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, AuthenticationForm, ProfileUpdateForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        phone = user.phone
        form = ProfileUpdateForm(data=request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.phone = phone
            user.save()
        else:
            context['form'] = form

    return render(request, 'user/profile.html', context=context)