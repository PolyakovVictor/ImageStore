from django.shortcuts import render
from .utils import get_pins_data


def HomeView(request):
    pins_data = get_pins_data()
    context = {'pins': pins_data}
    print(context)
    return render(request, 'imageStore/home.html', context)
