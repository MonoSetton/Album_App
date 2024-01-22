from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdateUsername, UpdateEmail
from django.contrib.auth.models import User


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)


def update_username(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUsername(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UpdateUsername()

    return render(request, 'accounts/update_username.html', {'form': form})


def update_email(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateEmail(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UpdateEmail()

    return render(request, 'accounts/update_email.html', {'form': form})



