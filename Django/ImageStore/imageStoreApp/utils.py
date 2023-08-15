import requests


def get_pins_data():
    response = requests.get('http://127.0.0.1:8080/Pin/')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass


def get_pins_by_id(id):
    response = requests.get(f'http://127.0.0.1:8080/Pin/{id}')
    if response.status_code == 200:
        data = response.json()
        print(data, "1//////////////////////////////////////////////////")
        return data
    else:
        pass


def get_tags_for_pin(id):
    response = requests.get(f'http://127.0.0.1:8080/Pin/pin_tags/{id}')
    print("ENTER")
    if response.status_code == 200:
        data = response.json()
        print(data, "//////////////////////////////////////////////////")
        return data
    else:
        pass
