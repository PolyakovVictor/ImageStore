from . import utils
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PinForm, BoardForm


def home_view(request):
    pins_data = utils.get_pins_data()
    pins = utils.add_img_info_to_pin(pins_data)
    context = {'pins': pins}
    return render(request, 'imageStore/home.html', context)


def pin_detail_view(request, id, image_id):
    user = request.user
    pin = utils.get_pins_by_id(id=id)
    tags = utils.get_tags_for_pin(id=id)
    image = utils.get_image_by_id(image_id)
    similar_pins_data = utils.pins_sort_by_tags(tags=tags)
    similar_pins = []

    for similar_pin in similar_pins_data:
        if similar_pin['id'] != pin['id']:
            image_id = similar_pin['image_id']
            image_info = utils.get_image_by_id(image_id)
            similar_pin['image_info'] = image_info
            similar_pins.append(similar_pin)
        else:
            pass

    favorite_check = utils.check_on_favorite(user, id)
    if favorite_check != 0:
        context = {
            'pin': pin,
            'tags': tags,
            'image': image,
            'similar_pins': similar_pins,
            'favorite_check': favorite_check['pin_id'],
            'user_id': user.id
        }
    else:
        context = {
            'pin': pin,
            'tags': tags,
            'image': image,
            'similar_pins': similar_pins,
            'favorite_check': 0,
            'user_id': user.id
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

            image_name = image.name
            image_data = image.read()
            image_id = utils.send_image_to_api(image_data, image_name)

            pin_data = {
                "title": title,
                "image_id": image_id,
                "description": description,
                "board_id": '1',
                "tags": tags,
            }

            response = utils.create_pin(pin_data, user)
            if response.status_code == 200:
                return redirect('imageStoreApp:home')
            else:
                return JsonResponse({"error": "Failed to create pin"}, status=response.status_code)
    else:
        form = PinForm()

    return render(request, 'imageStore/create_pin.html')


def favorite_view(request):
    user = request.user
    pins = []
    favorite_pins_id_raw = utils.get_favorite_pins(user)
    favorite_pins_id = [item['pin_id'] for item in favorite_pins_id_raw]
    for pin_id in favorite_pins_id:
        pins_data = utils.get_pins_by_id(pin_id)
        pins.append(pins_data)

    favorite_pins = utils.add_img_info_to_pin(pins)
    context = {
        'favorite_pins': favorite_pins,
    }

    return render(request, 'imageStore/favorite.html', context)


def user_page_view(request):
    pins_data = utils.get_all_user_pins(request.user.id)
    pins = utils.add_img_info_to_pin(pins_data)
    boards = utils.get_all_user_boards(request.user.id)
    print('boards: ', boards)
    context = {
        'pins': pins,
        'boards': boards
    }
    return render(request, 'imageStore/user_page.html', context=context)


def add_pin_to_favorite(request, pin_id, image_id):
    user = request.user
    favorite_check = utils.check_on_favorite(user, pin_id)
    if favorite_check != 0:
        utils.remove_pin_from_favorite(favorite_check['id'])
        return redirect('imageStoreApp:pin_detail', pin_id, image_id)
    else:
        utils.add_pin_to_favorite(pin_id, user.id)
        return redirect('imageStoreApp:pin_detail', pin_id, image_id)


def create_board_view(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board_data = form.cleaned_data
            utils.create_board(board_data['user_id'], board_data['title'], board_data['description'])
            return redirect('imageStoreApp:user_page')
    else:
        form = BoardForm()
    return render(request, 'imageStore/create_board.html')


def board_detail_view(request, board_id):
    return render(request, 'imageStore/board_detail.html')


def daily_view(request):

    return render(request, 'imageStore/daily.html')
