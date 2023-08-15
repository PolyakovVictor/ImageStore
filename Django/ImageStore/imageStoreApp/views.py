from django.shortcuts import render
from .utils import get_pins_data, get_pins_by_id, get_tags_for_pin


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
