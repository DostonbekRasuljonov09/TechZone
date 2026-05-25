from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def register_view(request):
    error = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        username   = request.POST.get('username')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        if password1 != password2:
            error = "Parollar mos kelmadi."
        elif User.objects.filter(username=username).exists():
            error = "Bu username allaqachon band."
        else:
            user = User.objects.create_user(
                username=username, password=password1,
                first_name=first_name, last_name=last_name,
            )
            login(request, user)
            return redirect('index')
    return render(request, 'accounts/register.html', {'error': error})


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Username yoki parol noto'g'ri."
    return render(request, 'accounts/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def profile_view(request):
    success = None
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.save()
        success = "Ma'lumotlar muvaffaqiyatli saqlandi!"
    return render(request, 'accounts/profile.html', {'success': success})
