from .utils import get_pins_data, get_pins_by_id, get_tags_for_pin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PinForm
import requests, base64


def home_view(request):
    pins_data = get_pins_data()
    context = {'pins': pins_data}
    return render(request, 'imageStore/home.html', context)


def pin_detail_view(request, id):
    pin = get_pins_by_id(id=id)
    tags = get_tags_for_pin(id=id)
    context = {
        'pin': pin,
        'tags': tags,
    }
    return render(request, 'imageStore/pin_detail.html', context)


def create_pin_view(request):
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            tags = request.POST.get('tags')
            image_bytes = form.cleaned_data['image'].read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            pin_data = {
                "title": title,
                "image": image_base64,
                "description": description,
                "tags": tags
            }

            try:
                response = requests.post('http://localhost:8080/Pin/create', json=pin_data)

                if response.status_code == 200:
                    return redirect('imageStoreApp/home')
                else:
                    return JsonResponse({"error": "Failed to create pin"}, status=response.status_code)
            
            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = PinForm()

    return render(request, 'imageStore/create_pin.html')
