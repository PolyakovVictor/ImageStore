import requests


def get_pins_data():
    response = requests.get('http://127.0.0.1:8080/Pin/')
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass
