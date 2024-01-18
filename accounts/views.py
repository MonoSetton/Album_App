from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
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
    return render(request, 'accounts/profile.html')


def update_profile(request, pk):
    account = User.objects.get(id=pk)
    context = {'account': account}
    return render(request, 'accounts/update_profile.html', context)