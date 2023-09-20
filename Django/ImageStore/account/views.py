from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, LoginForm


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('imageStoreApp:home')
        else:
            messages.error(request, "Incorrect username or password")
    return render(request, 'account/login.html', {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:login")
        else:
            messages.error(request, "Error, incorrect data. Please, try again.")
    else:
        form = RegistrationForm()
    return render(request, "account/registration.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('imageStoreApp:home')
