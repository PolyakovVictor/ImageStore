import requests
import jwt
import json


def get_pins_data():
    response = requests.get('http://127.0.0.1:8080/pin/')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_image_by_id(id):
    response = requests.get(f'http://127.0.0.1:8080/image/{id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_pins_by_id(id):
    response = requests.get(f'http://127.0.0.1:8080/pin/{id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_tags_for_pin(id):
    response = requests.get(f'http://127.0.0.1:8080/pin/pin_tags/{id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_all_user_pins(user_id):
    response = requests.get(f'http://localhost:8080/pin/get_all_user_pins/{user_id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_all_user_boards(user_id):
    response = requests.get(f'http://localhost:8080/board/get_all_user_boards/{user_id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def pins_sort_by_tags(tags):
    names = [item["name"] for item in tags]
    data = json.dumps(names)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8080/pin/pin_sort_by_tags/', data=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def generate_jwt_token(user_id):
    payload = {'user_id': user_id}
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token


def get_favorite_pins(user):
    user_id = user.id
    response = requests.post(f'http://localhost:8080/pin/get_favorite_pin_for_user/{user_id}')
    if response.status_code == 200:
        raw_data = response.json()
        return raw_data
    else:
        pass


def check_on_favorite(user, pin_id):
    favorite_pins = get_favorite_pins(user)
    try:
        for favorite_pin in favorite_pins:
            if favorite_pin['pin_id'] == int(pin_id):
                return favorite_pin
            else:
                pass
        return 0
    except (TypeError):
        return 0


def add_pin_to_favorite(pin_id, user_id):
    pin_data = {
        "parameter": {
            "pin_id": int(pin_id),
            "user_id": user_id
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8080/pin/add_to_favorite_pin/', data=json.dumps(pin_data), headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('status code:', response.status_code)


def remove_pin_from_favorite(favorite_pin_id):
    response = requests.delete(f'http://localhost:8080/pin/remove_favorite_pin/{favorite_pin_id}')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('status code remove def:', response.status_code)


def create_board(user_id, title, description):
    payload = {
        "parameter": {
            "user_id": user_id,
            "title": title,
            "description": description
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8080/board/create/', data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('status code:', response.status_code)


def add_img_info_to_pin(pins_data):
    pins = []
    for pin in pins_data:
        image_id = pin['image_id']
        image_info = get_image_by_id(image_id)
        pin['image_info'] = image_info
        pins.append(pin)

    return pins


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


def create_pin(pin_data, user):
    try:
        response = requests.post('http://localhost:8080/pin/create', json=pin_data, headers={'Authorization': f'Bearer {user.id}'})
        return response
    except requests.exceptions.RequestException as e:
        print({"error": str(e)}, status=500)
