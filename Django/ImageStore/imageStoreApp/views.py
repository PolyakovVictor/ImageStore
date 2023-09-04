from .utils import get_pins_data, get_pins_by_id, get_tags_for_pin
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CreateUserForm


def home_view(request):
    pins_data = get_pins_data()
    context = {'pins': pins_data}
    return render(request, 'imageStore/home.html', context)


def pin_detail(request, id):
    pin = get_pins_by_id(id=id)
    tags = get_tags_for_pin(id=id)
    context = {
        'pin': pin,
        'tags': tags,
    }
    return render(request, 'imageStore/pin_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('imageStoreApp:home')
    else:
        form = CreateUserForm()
    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('imageStoreApp:home')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('imageStoreApp:home')
