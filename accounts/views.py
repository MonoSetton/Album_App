from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdateUsername, UpdateEmail, ChangePasswordForm
from django.contrib.auth import authenticate


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


def logout_view(request):
    logout(request)
    return redirect('/')


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword1']
            username = request.user.username
            password = form.cleaned_data['oldpassword']

            user = authenticate(username=username, password=password)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                return redirect('/')
            else:
                context = {'error': 'You have entered wrong old password', 'form': form}
                return render(request, 'accounts/change_password.html', context)
        else:
            context = {'error': 'You have entered old password', 'form': form}
            return render(request, 'accounts/change_password.html', context)
    else:
        form = ChangePasswordForm()
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='/login')
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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



