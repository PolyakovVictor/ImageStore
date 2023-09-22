from .utils import get_pins_data, get_pins_by_id, get_tags_for_pin, get_image_by_id, pins_sort_by_tags
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PinForm
import requests


def home_view(request):
    pins_data = get_pins_data()
    updated_pins_data = []

    for pin in pins_data:
        image_id = pin['image_id']
        image_info = get_image_by_id(image_id)
        pin['image_info'] = image_info
        updated_pins_data.append(pin)
    context = {'pins': updated_pins_data}
    return render(request, 'imageStore/home.html', context)


def pin_detail_view(request, id, image_id):
    pin = get_pins_by_id(id=id)
    tags = get_tags_for_pin(id=id)
    image = get_image_by_id(image_id)
    similar_pins_data = pins_sort_by_tags(tags=tags)
    similar_pins = []
    for similar_pin in similar_pins_data:
        if similar_pin['id'] != pin['id']:
            image_id = similar_pin['image_id']
            image_info = get_image_by_id(image_id)
            similar_pin['image_info'] = image_info
            similar_pins.append(similar_pin)
        else:
            pass
    context = {
        'pin': pin,
        'tags': tags,
        'image': image,
        'similar_pins': similar_pins
    }
    return render(request, 'imageStore/pin_detail.html', context)


def create_pin_view(request):
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            title = request.POST.get('title')
            description = request.POST.get('description')
            tags = request.POST.get('tags')
            image = form.cleaned_data['image']

            def send_image_to_api(image, image_name):
                url = 'http://localhost:8080/image/upload'
                files = {'file': (image_name, image)}

                try:
                    response = requests.post(url, files=files)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.RequestException as e:
                    print(f"Error when sending a request: {e}")
                    return None

            image_name = image.name
            image_data = image.read()
            image_id = send_image_to_api(image_data, image_name)

            pin_data = {
                "title": title,
                "image_id": image_id,
                "description": description,
                "board_id": '1',
                "tags": tags,
            }

            try:
                response = requests.post('http://localhost:8080/pin/create', json=pin_data, headers={'Authorization': f'Bearer {user.id}'})

                if response.status_code == 200:
                    return redirect('imageStoreApp:home')
                else:
                    return JsonResponse({"error": "Failed to create pin"}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = PinForm()

    return render(request, 'imageStore/create_pin.html')


def favorite_view(request):
    return render(request, 'imageStore/favorite.html')


def user_page_view(request):
    return render(request, 'imageStore/user_page.html')
